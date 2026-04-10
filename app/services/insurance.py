from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, NEXT_ACTION_TEXT
from app.services.common import normalize_text, title_city


def start_insurance(chat_id: int, user_id: int):
    set_user_flow(user_id, "insurance_input", "insurance")

    send_message(
        chat_id,
        "🧞 Слушаюсь и повинуюсь, мой господин.\n"
        "Для какой страны нужен оберег?\n"
        "Можно сразу указать срок поездки.\n\n"
        "Например:\n"
        "Италия 7 дней\n"
        "Турция 10 дней",
    )


def handle_insurance(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    if not t:
        send_message(chat_id, "Назовите страну, мой господин.")
        return

    parts = t.split()
    country = parts[0]

    country_title = title_city(country)

    url = f"https://cherehapa.ru/?country={country_title}&marker={TRAVELPAYOUTS_MARKER}"

    result_text = (
        "✨ Ваше желание исполнено, мой господин.\n"
        f"🛡 {country_title}\n"
        "Я открыл сервис страхования.\n"
        "Данные нужно будет ввести на сайте."
    )

    send_inline(chat_id, result_text, result_inline(url, "insurance"))

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "insurance", text, f"🛡 {country_title}", url)
    clear_state(user_id)
