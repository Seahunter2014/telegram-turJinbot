from urllib.parse import quote_plus

from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import NEXT_ACTION_TEXT, WEBHOOK_BASE_URL


def start_excursions(chat_id: int, user_id: int):
    set_user_flow(user_id, "excursions_input", "excursions")
    send_message(
        chat_id,
        "🧞 Слушаюсь и повинуюсь, мой господин.\n"
        "В каком городе ищем впечатления?\n\n"
        "Можно сразу указать дату.\n\n"
        "Например:\n"
        "Стамбул 15 июня\n"
        "Рим",
    )


def _normalize_city(raw_text: str) -> str:
    text = (raw_text or "").strip()
    if not text:
        return ""

    parts = text.split()
    city_parts = []

    for part in parts:
        token = part.strip(",. ")
        lowered = token.lower()

        if lowered.isdigit():
            break

        if lowered in {
            "января", "февраля", "марта", "апреля", "мая", "июня",
            "июля", "августа", "сентября", "октября", "ноября", "декабря",
            "сегодня", "завтра", "послезавтра",
        }:
            break

        city_parts.append(token)

    return " ".join(city_parts).strip()


def _tripster_search_url(city: str) -> str:
    query = quote_plus(city)
    return f"https://experience.tripster.ru/search/?query={query}"


def _masked_excursion_url(city: str) -> str:
    item_id = city.lower().replace(" ", "-")
    target = quote_plus(_tripster_search_url(city))
    return f"{WEBHOOK_BASE_URL}/go/excursion/{item_id}?target={target}"


def handle_excursions(chat_id: int, user_id: int, text: str):
    city = _normalize_city(text)

    if not city:
        send_message(chat_id, "Назовите город, мой господин.")
        return

    url = _masked_excursion_url(city)

    send_inline(
        chat_id,
        "✨ Ваше желание исполнено, мой господин.\n"
        f"🎭 {city}\n\n"
        "Подобрал впечатления.\n"
        "Дата и детали уточняются на сайте.",
        result_inline(url, "excursions"),
    )

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(
        user_id,
        "excursions",
        text,
        f"🎭 {city}",
        url,
    )
    clear_state(user_id)
