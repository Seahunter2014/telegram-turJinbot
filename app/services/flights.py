from urllib.parse import quote_plus

import requests

from app.utils.telegram import send_message, send_inline, send_typing
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import (
    TRAVELPAYOUTS_MARKER,
    TRAVELPAYOUTS_API_TOKEN,
    NEXT_ACTION_TEXT,
    WEBHOOK_BASE_URL,
)
from app.services.common import (
    normalize_text,
    find_dates_ru,
    iso_to_ddmm,
    CITY_TO_IATA,
    title_city,
    parse_passengers,
)

API_URL = "https://api.travelpayouts.com/v2/prices/latest"


def start_flights(chat_id: int, user_id: int):
    set_user_flow(user_id, "flights_input", "flights")
    send_message(
        chat_id,
        "🧞 Слушаюсь и повинуюсь, мой господин.\n"
        "Куда летим?\n\n"
        "Например:\n"
        "Москва Стамбул 15 июня в одну сторону 2 взрослых\n"
        "Москва Стамбул 15 июня туда 22 июня обратно 2 взрослых\n\n"
        "Если есть дети:\n"
        "0–2 года — младенец\n"
        "2–11 лет — ребёнок\n\n"
        "Текстом или голосом — как вашей душе угодно.",
    )


def get_price(origin: str, destination: str):
    if not TRAVELPAYOUTS_API_TOKEN:
        return None

    try:
        r = requests.get(
            API_URL,
            params={
                "origin": origin,
                "destination": destination,
                "currency": "rub",
                "limit": 1,
            },
            headers={"X-Access-Token": TRAVELPAYOUTS_API_TOKEN},
            timeout=10,
        )
        data = r.json().get("data", [])
        if not data:
            return None
        return data[0].get("price")
    except Exception:
        return None
