from app.keyboards import main_menu
from app.utils.telegram import send_message, answer_callback
from app.storage import (
    get_user_flow,
    clear_state,
    subscribe_user,
    unsubscribe_user,
    is_subscribed,
)
from app.config import MAIN_MENU_TEXT, SERVICE_IN_PROGRESS_TEXT

# сервисы
from app.services.flights import start_flights, handle_flights
from app.services.vacation import start_vacation, handle_vacation_choice, handle_vacation
from app.services.hotels import start_hotels, handle_hotels_choice, handle_hotels
from app.services.insurance import start_insurance, handle_insurance
from app.services.car_rental import start_car, handle_car
from app.services.transfer import start_transfer
from app.services.excursions import start_excursions, handle_excursions


def _news_inline_keyboard() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🔔 Подписаться на новости", "callback_data": "subscribe"},
                {"text": "🔕 Отписаться", "callback_data": "unsubscribe"},
            ]
        ]
    }


def _news_status_text(user_id: int) -> str:
    if is_subscribed(user_id):
        status = "включена"
    else:
        status = "выключена"

    return (
        f"🔔 Подписка на рассылку: *{status}*\n\n"
        "Буду присылать:\n"
        "• вторник 10:15 — карта цен Aviasales\n"
        "• четверг 19:15 — горящие туры\n"
        "• суббота 11:15 — лучшие предложения дня Trip.com"
    )


def start(chat_id: int, user_id: int) -> None:
    send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_menu())
    send_message(
        chat_id,
        _news_status_text(user_id),
        reply_markup=_news_inline_keyboard(),
    )


def handle_text(chat_id: int, user_id: int, text: str) -> None:
    state, service, data = get_user_flow(user_id)

    # ====== COMMANDS ======
    if text == "/start":
        start(chat_id, user_id)
        return

    if text == "/news_on":
        subscribe_user(user_id)
        send_message(
            chat_id,
            "🔔 Подписка включена.\n"
            "Буду присылать карту цен, горящие туры и лучшие предложения дня.",
            reply_markup=main_menu(),
        )
        return

    if text == "/news_off":
        unsubscribe_user(user_id)
        send_message(
            chat_id,
            "🔕 Подписка отключена.",
            reply_markup=main_menu(),
        )
        return

    if text == "/news_status":
        send_message(
            chat_id,
            _news_status_text(user_id),
            reply_markup=_news_inline_keyboard(),
        )
        return

    # ====== CANCEL ======
    if text == "❌ Отмена":
        clear_state(user_id)
        send_message(chat_id, "🧞 Слушаюсь, мой господин.", reply_markup=main_menu())
        return

    # ====== STATES ======
    if state == "flights_input":
        handle_flights(chat_id, user_id, text)
        return

    if state == "vacation_choice":
        handle_vacation_choice(chat_id, user_id, text)
        return

    if state == "vacation_input":
        handle_vacation(chat_id, user_id, text)
        return

    if state == "hotels_choice":
        handle_hotels_choice(chat_id, user_id, text)
        return

    if state == "hotels_input":
        handle_hotels(chat_id, user_id, text)
        return

    if state == "insurance_input":
        handle_insurance(chat_id, user_id, text)
        return

    if state == "car_input":
        handle_car(chat_id, user_id, text)
        return

    if state == "excursions_input":
        handle_excursions(chat_id, user_id, text)
        return

    # ====== ENTRY BUTTONS ======
    if text == "🧞 Ковер самолет":
        start_flights(chat_id, user_id)
        return

    if text == "🌴 Отпуск под ключ":
        start_vacation(chat_id, user_id)
        return

    if text == "🏰 Снять дворец":
        start_hotels(chat_id, user_id)
        return

    if text == "🛡 Оберег туриста":
        start_insurance(chat_id, user_id)
        return

    if text == "🚗 Аренда авто":
        start_car(chat_id, user_id)
        return

    if text == "🚖 Эх, прокачу":
        start_transfer(chat_id, user_id)
        return

    if text == "🎭 Хлеба и зрелищ":
        start_excursions(chat_id, user_id)
        return

    # ====== FIX: если state слетел, но service сохранился ======
    if service == "flights":
        handle_flights(chat_id, user_id, text)
        return

    if service == "vacation":
        handle_vacation(chat_id, user_id, text)
        return

    if service == "hotels":
        handle_hotels(chat_id, user_id, text)
        return

    if service == "insurance":
        handle_insurance(chat_id, user_id, text)
        return

    if service == "car":
        handle_car(chat_id, user_id, text)
        return

    if service == "excursions":
        handle_excursions(chat_id, user_id, text)
        return

    # ====== FALLBACK ======
    send_message(chat_id, SERVICE_IN_PROGRESS_TEXT, reply_markup=main_menu())


def handle_callback(chat_id: int, user_id: int, data: str, callback_id: str) -> None:
    answer_callback(callback_id)

    if data.startswith("retry_"):
        service = data.split("_", 1)[1]

        if service == "flights":
            start_flights(chat_id, user_id)
            return
        if service == "vacation":
            start_vacation(chat_id, user_id)
            return
        if service == "hotels":
            start_hotels(chat_id, user_id)
            return
        if service == "insurance":
            start_insurance(chat_id, user_id)
            return
        if service == "car":
            start_car(chat_id, user_id)
            return
        if service == "transfer":
            start_transfer(chat_id, user_id)
            return
        if service == "excursions":
            start_excursions(chat_id, user_id)
            return

    if data == "subscribe":
        subscribe_user(user_id)
        send_message(
            chat_id,
            "🔔 Готово.\n"
            "Подписка включена на все 3 рассылки:\n"
            "• карта цен Aviasales\n"
            "• горящие туры\n"
            "• лучшие предложения дня Trip.com",
            reply_markup=main_menu(),
        )
        return

    if data == "unsubscribe":
        unsubscribe_user(user_id)
        send_message(
            chat_id,
            "🔕 Подписка отключена.",
            reply_markup=main_menu(),
        )
        return

    if data == "contact_admin":
        send_message(
            chat_id,
            "🧙 Передам старшему магу.\n"
            "Укажите:\n"
            "— Имя\n"
            "— Контакт\n"
            "— Даты\n"
            "— Пожелания",
            reply_markup=main_menu(),
        )
        return
