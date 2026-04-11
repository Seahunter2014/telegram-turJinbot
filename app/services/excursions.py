from urllib.parse import quote_plus

from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import NEXT_ACTION_TEXT, WEBHOOK_BASE_URL
from app.services.common import find_dates_ru, normalize_text


TRIPSTER_BASE_URL = "https://experience.tripster.ru"

# Только точечная правка: нормальные city slug для Tripster.
# Добавляй сюда города по мере необходимости.
TRIPSTER_CITY_SLUGS = {
    "рим": "Rome",
    "rome": "Rome",
    "стамбул": "Istanbul",
    "istanbul": "Istanbul",
    "дубай": "Dubai",
    "dubai": "Dubai",
    "милан": "Milan",
    "milan": "Milan",
    "тбилиси": "Tbilisi",
    "tbilisi": "Tbilisi",
    "анталья": "Antalya",
    "antalya": "Antalya",
    "париж": "Paris",
    "paris": "Paris",
    "барселона": "Barcelona",
    "barcelona": "Barcelona",
    "вена": "Vienna",
    "vienna": "Vienna",
    "прага": "Prague",
    "prague": "Prague",
    "берлин": "Berlin",
    "berlin": "Berlin",
    "мадрид": "Madrid",
    "madrid": "Madrid",
    "ереван": "Yerevan",
    "yerevan": "Yerevan",
}


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


def _extract_city(raw_text: str) -> str:
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


def _normalize_city_key(city: str) -> str:
    return city.strip().lower()


def _build_tripster_target(city: str) -> str:
    city_key = _normalize_city_key(city)
    slug = TRIPSTER_CITY_SLUGS.get(city_key)

    # Если город известен — ведём на валидную страницу города.
    if slug:
        return f"{TRIPSTER_BASE_URL}/experience/{slug}/"

    # Осторожный fallback: общая страница экскурсий.
    # Не отправляем на битый search URL.
    return f"{TRIPSTER_BASE_URL}/"


def _build_masked_excursion_url(city: str, target_url: str) -> str:
    item_id = city.strip().lower().replace(" ", "-")
    target = quote_plus(target_url)
    return f"{WEBHOOK_BASE_URL}/go/excursion/{item_id}?target={target}"


def handle_excursions(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)
    if not t:
        send_message(chat_id, "Назовите город, мой господин.")
        return

    city = _extract_city(text)
    if not city:
        send_message(chat_id, "Назовите город, мой господин.")
        return

    dates = find_dates_ru(t)
    date_text = dates[0] if dates else None

    target_url = _build_tripster_target(city)
    url = _build_masked_excursion_url(city, target_url)

    if date_text:
        result_text = (
            "✨ Ваше желание исполнено, мой господин.\n"
            f"🎭 {city}\n"
            f"📅 {date_text}\n\n"
            "Подобрал впечатления по городу.\n"
            "Если сайт не применит дату автоматически, её можно быстро выбрать на странице."
        )
    else:
        result_text = (
            "✨ Ваше желание исполнено, мой господин.\n"
            f"🎭 {city}\n\n"
            "Подобрал впечатления по городу."
        )

    send_inline(
        chat_id,
        result_text,
        result_inline(url, "excursions"),
    )
    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(
        user_id,
        "excursions",
        text,
        f"🎭 {city}" + (f" · {date_text}" if date_text else ""),
        url,
    )
    clear_state(user_id)
