from urllib.parse import quote_plus

from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import NEXT_ACTION_TEXT
from app.services.common import (
    normalize_text,
    title_city,
    find_dates_ru,
)

TRIPSTER_BASE = "https://experience.tripster.ru"


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


def _extract_city(text: str) -> str:
    parts = text.split()
    if not parts:
        return ""
    return parts[0]


def _build_tripster_url(city_title: str) -> str:
    # Безопасно ведём на поиск по городу, чтобы не получать битые city-slug ссылки.
    query = quote_plus(city_title)
    return f"{TRIPSTER_BASE}/search/?query={query}"


def handle_excursions(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    if not t:
        send_message(chat_id, "Назовите город, мой господин.")
        return

    dates = find_dates_ru(t)
    date = dates[0] if dates else None

    city = _extract_city(t)
    city_title = title_city(city)
    url = _build_tripster_url(city_title)

    if date:
        result_text = (
            "✨ Ваше желание исполнено, мой господин.\n"
            f"🎭 {city_title}\n"
            f"📅 {date}\n"
            "Подобрал впечатления.\n"
            "Дата и детали уточняются на сайте."
        )
    else:
        result_text = (
            "✨ Ваше желание исполнено, мой господин.\n"
            f"🎭 {city_title}\n"
            "Подобрал впечатления.\n"
            "Дата и детали уточняются на сайте."
        )

    send_inline(chat_id, result_text, result_inline(url, "excursions"))
    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(
        user_id,
        "excursions",
        text,
        f"🎭 {city_title}",
        url,
    )
    clear_state(user_id)
