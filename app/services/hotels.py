from urllib.parse import quote_plus

from app.utils.telegram import send_message, send_inline
from app.keyboards import choice_menu, main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import (
    TRAVELPAYOUTS_MARKER,
    NEXT_ACTION_TEXT,
    ALEAN_IN_PROGRESS_TEXT,
    WEBHOOK_BASE_URL,
)
from app.services.common import (
    normalize_text,
    HOTELS_CITY_TO_COUNTRY,
    translit_slug,
    title_city,
)


def start_hotels(chat_id: int, user_id: int):
    set_user_flow(user_id, "hotels_choice", "hotels")
    send_message(
        chat_id,
        "Выберите формат поиска, мой господин.",
        reply_markup=choice_menu(),
    )


def handle_hotels_choice(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    if "быстрый" in t:
        set_user_flow(user_id, "hotels_input", "hotels")
        send_message(
            chat_id,
            "🧞 Слушаюсь и повинуюсь, мой господин.\n"
            "В каком городе ищем жильё?\n\n"
            "Например:\n"
            "Милан\n"
            "Дубай\n"
            "Стамбул\n\n"
            "Даты и гостей выберете на сайте.",
        )
    elif "детальный" in t:
        send_message(chat_id, ALEAN_IN_PROGRESS_TEXT, reply_markup=main_menu())
        clear_state(user_id)
    elif "отмена" in t:
        clear_state(user_id)
        send_message(chat_id, "Слушаюсь, возвращаемся.", reply_markup=main_menu())


def _build_hotel_target(city: str) -> tuple[str, str]:
    city_title = title_city(city)
    country_slug = HOTELS_CITY_TO_COUNTRY.get(city)

    if country_slug:
        target_url = f"https://hotels.travelata.ru/{country_slug}?marker={TRAVELPAYOUTS_MARKER}"
        text_result = (
            "✨ Ваше желание исполнено, мой господин.\n"
            f"🏰 {city_title}\n"
            "Открою подборку жилья по направлению.\n"
            "Точный город и даты выберите на странице."
        )
        return target_url, text_result

    query = translit_slug(city)
    target_url = f"https://hotels.travelata.ru/search?query={query}&marker={TRAVELPAYOUTS_MARKER}"
    text_result = (
        "✨ Ваше желание исполнено, мой господин.\n"
        f"🏰 {city_title}\n"
        "Открою поиск отелей.\n"
        "Введите город ещё раз на сайте — там гибкий поиск."
    )
    return target_url, text_result


def _build_masked_url(city: str, target_url: str) -> str:
    item_id = translit_slug(city) or city.lower()
    target = quote_plus(target_url)
    return f"{WEBHOOK_BASE_URL}/go/hotel/{item_id}?target={target}"


def handle_hotels(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)
    city = t.split()[0] if t else ""

    if not city:
        send_message(chat_id, "Назовите город, мой господин.")
        return

    city_title = title_city(city)
    target_url, text_result = _build_hotel_target(city)
    url = _build_masked_url(city, target_url)

    send_inline(chat_id, text_result, result_inline(url, "hotels"))
    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "hotels", text, f"🏰 {city_title}", url)
    clear_state(user_id)
