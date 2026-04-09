from app.keyboards import MAIN_KEYBOARD, CANCEL_KEYBOARD, MODE_KEYBOARD, inline_keyboard
from app.storage import user_states, save_request, get_last_request, subscribe
from app.utils.telegram import send_message, answer_callback
from app.voice import is_voice_available
from app.integrations.alean_client import is_configured as alean_configured
from app.services import flights, vacation, hotels, insurance, car_rental, transfer, excursions

BUTTON_TO_SERVICE = {
    flights.BUTTON: flights,
    vacation.BUTTON: vacation,
    hotels.BUTTON: hotels,
    insurance.BUTTON: insurance,
    car_rental.BUTTON: car_rental,
    transfer.BUTTON: transfer,
    excursions.BUTTON: excursions,
}
SERVICE_BY_ID = {
    flights.SERVICE_ID: flights,
    vacation.SERVICE_ID: vacation,
    hotels.SERVICE_ID: hotels,
    insurance.SERVICE_ID: insurance,
    car_rental.SERVICE_ID: car_rental,
    transfer.SERVICE_ID: transfer,
    excursions.SERVICE_ID: excursions,
}
CHOOSE_MODE_SERVICES = {vacation.BUTTON: vacation, hotels.BUTTON: hotels}


def _build_result_keyboard(service_id: str, url: str, open_text: str):
    return inline_keyboard([
        [{"text": open_text, "url": url}],
        [{"text": "✏️ Изменить запрос", "callback_data": f"retry:{service_id}"}, {"text": "🧙 Старший маг", "callback_data": "contact_admin"}],
        [{"text": "🔔 Подписаться", "callback_data": "subscribe"}],
    ])


def _send_followup_menu(chat_id: int):
    send_message(chat_id, "_Чего изволите далее?_", reply_markup=MAIN_KEYBOARD, parse_mode="Markdown")


def _send_result(chat_id: int, module, data: dict, user_info: dict):
    url = module.build_url(data)
    text = module.summary(data)
    save_request(chat_id, {"service": module.SERVICE_ID, "data": data, "summary": text, "url": url, "user": user_info})
    send_message(chat_id, text, reply_markup=_build_result_keyboard(module.SERVICE_ID, url, module.OPEN_TEXT))
    _send_followup_menu(chat_id)


def _start_service(chat_id: int, user_info: dict, module):
    if module.STEPS == []:
        user_states.pop(chat_id, None)
        _send_result(chat_id, module, {}, user_info)
        return
    user_states[chat_id] = {"service": module.SERVICE_ID, "module": module, "step_index": 0, "data": {}, "user": user_info}
    send_message(chat_id, module.START_TEXT, reply_markup=CANCEL_KEYBOARD)


def _start_choose_mode(chat_id: int, user_info: dict, module):
    user_states[chat_id] = {"service": module.SERVICE_ID, "module": module, "mode": "choosing_mode", "user": user_info}
    send_message(chat_id, "Выберите формат поиска, мой господин.", reply_markup=MODE_KEYBOARD)


def _process_service_text(chat_id: int, user_info: dict, text: str, state: dict):
    module = state["module"]
    data = module.parse_input(text)
    if not module.is_valid(data):
        send_message(chat_id, getattr(module, "CLARIFY_TEXT", "Уточните запрос."), reply_markup=CANCEL_KEYBOARD)
        return
    user_states.pop(chat_id, None)
    _send_result(chat_id, module, data, user_info)


def _process_contact_admin(chat_id: int, text: str, user_info: dict):
    prev = get_last_request(chat_id)
    request_text = "🔔 Новая заявка TourJin\n\n"
    request_text += f"Пользователь: @{user_info.get('username') or '-'} / id={chat_id}\n"
    request_text += f"Имя: {user_info.get('first_name') or '-'}\n\n"
    request_text += f"Текст заявки:\n{text}\n"
    if prev:
        request_text += f"\nПоследний запрос бота:\n{prev.get('summary','-')}\n"
        request_text += f"\nСсылка:\n{prev.get('url','-')}"
    # здесь можно отправить админу, если ADMIN_TELEGRAM_ID задан
    user_states.pop(chat_id, None)
    send_message(chat_id, "🧙 Ваше желание передано старшему магу.\nОн свяжется с вами в ближайшее время.\n\n_Чего изволите далее?_", reply_markup=MAIN_KEYBOARD, parse_mode="Markdown")


def handle_callback(callback_query: dict):
    data = callback_query.get("data", "")
    chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
    user = callback_query.get("from", {})
    answer_callback(callback_query.get("id"))
    if data.startswith("retry:"):
        service_id = data.split(":", 1)[1]
        module = SERVICE_BY_ID[service_id]
        if module.BUTTON in CHOOSE_MODE_SERVICES:
            _start_choose_mode(chat_id, user, module)
        else:
            _start_service(chat_id, user, module)
        return
    if data == "subscribe":
        subscribe(chat_id)
        send_message(chat_id, "✨ Готово. Я буду присылать вам новые достойные варианты.\n_Чего изволите далее?_", reply_markup=MAIN_KEYBOARD, parse_mode="Markdown")
        return
    if data == "contact_admin":
        user_states[chat_id] = {"service": "contact_admin", "mode": "collect_request", "user": user}
        send_message(chat_id, "🧙 Передам ваше желание старшему магу.\n\nПожалуйста, укажите как можно подробнее:\n\n— Имя\n— Контакт (Telegram / телефон)\n— Услуга или несколько услуг\n— Город вылета / направление\n— Даты поездки\n— Состав туристов (взрослые / дети / младенцы)\n— Любые пожелания\n\nЧем подробнее вы опишете желание, тем точнее оно будет исполнено.", reply_markup=CANCEL_KEYBOARD)
        return


def handle_update(update: dict):
    if update.get("callback_query"):
        handle_callback(update["callback_query"])
        return

    message = update.get("message") or {}
    chat = message.get("chat") or {}
    user = message.get("from") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if message.get("voice"):
        if not is_voice_available():
            send_message(chat_id, "🧞 Сервис на доработке.", reply_markup=MAIN_KEYBOARD)
            return

    if text == "/start":
        user_states.pop(chat_id, None)
        send_message(chat_id, "🧞 Слушаюсь и повинуюсь, мой господин.\n_Чего изволите?_", reply_markup=MAIN_KEYBOARD, parse_mode="Markdown")
        return

    if text == "❌ Отмена":
        user_states.pop(chat_id, None)
        send_message(chat_id, "Слушаюсь, мой господин. Возвращаемся в главное меню.\n_Чего изволите?_", reply_markup=MAIN_KEYBOARD, parse_mode="Markdown")
        return

    state = user_states.get(chat_id)
    if state:
        if state.get("service") == "contact_admin" and state.get("mode") == "collect_request":
            _process_contact_admin(chat_id, text, user)
            return
        if state.get("mode") == "choosing_mode":
            module = state["module"]
            if text == "⚡ Быстрый поиск":
                _start_service(chat_id, user, module)
                return
            if text == "🧭 Детальный подбор":
                user_states.pop(chat_id, None)
                if not alean_configured():
                    send_message(chat_id, "🧭 Детальный подбор сейчас на доработке.", reply_markup=MAIN_KEYBOARD)
                else:
                    send_message(chat_id, "🧭 Детальный подбор сейчас на доработке.", reply_markup=MAIN_KEYBOARD)
                return
            send_message(chat_id, "Выберите формат поиска, мой господин.", reply_markup=MODE_KEYBOARD)
            return
        _process_service_text(chat_id, user, text, state)
        return

    if text in CHOOSE_MODE_SERVICES:
        _start_choose_mode(chat_id, user, CHOOSE_MODE_SERVICES[text])
        return
    if text in BUTTON_TO_SERVICE:
        _start_service(chat_id, user, BUTTON_TO_SERVICE[text])
        return

    send_message(chat_id, "🧞 Слушаюсь и повинуюсь, мой господин.\nВоспользуйтесь кнопками ниже.", reply_markup=MAIN_KEYBOARD)
