import requests

from app.utils.telegram import send_message, send_inline, send_typing
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, TRAVELPAYOUTS_API_TOKEN, NEXT_ACTION_TEXT
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


def _is_one_way(text: str) -> bool:
    one_way_markers = [
        "в одну сторону",
        "в один конец",
        "one way",
        "one-way",
        "без обратного",
        "только туда",
    ]
    return any(marker in text for marker in one_way_markers)


def _extract_cities(text: str):
    cities = [city for city in CITY_TO_IATA if city in text]
    if len(cities) < 2:
        return None, None
    return cities[0], cities[1]


def handle_flights(chat_id: int, user_id: int, text: str):
    send_typing(chat_id)

    t = normalize_text(text)
    dates = find_dates_ru(t)

    if not dates:
        send_message(chat_id, "Укажите дату, мой господин.")
        return

    from_city, to_city = _extract_cities(t)
    if not from_city or not to_city:
        send_message(chat_id, "Нужны город вылета и прилёта.")
        return

    origin = CITY_TO_IATA[from_city]
    destination = CITY_TO_IATA[to_city]

    depart = dates[0]
    one_way = _is_one_way(t)

    if one_way:
        return_date = None
    else:
        return_date = dates[1] if len(dates) > 1 else None

    ddmm_depart = iso_to_ddmm(depart)
    ddmm_return = iso_to_ddmm(return_date) if return_date else ""

    adults, children, infants = parse_passengers(t)

    path = f"{origin}{ddmm_depart}{destination}"
    if ddmm_return:
        path += ddmm_return

    url = (
        f"https://www.aviasales.ru/search/{path}"
        f"?adults={adults}&children={children}&infants={infants}"
        f"&marker={TRAVELPAYOUTS_MARKER}"
    )

    price = get_price(origin, destination)
    price_text = f"от {price} ₽" if price else "Цены уточняются при переходе"

    if return_date:
        route_line = (
            f"✈️ {title_city(from_city)} → {title_city(to_city)}\n"
            f"📅 {depart} — {return_date}\n"
            f"👤 взрослых: {adults}"
        )
    else:
        route_line = (
            f"✈️ {title_city(from_city)} → {title_city(to_city)}\n"
            f"📅 {depart}\n"
            f"🛫 в одну сторону\n"
            f"👤 взрослых: {adults}"
        )

    if children:
        route_line += f"\n🧒 детей: {children}"
    if infants:
        route_line += f"\n👶 младенцев: {infants}"

    send_inline(
        chat_id,
        "✨ Ваше желание исполнено, мой господин.\n"
        f"{route_line}\n\n"
        f"{price_text}",
        result_inline(url, "flights"),
    )

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())
    save_result(
        user_id,
        "flights",
        text,
        f"✈️ {title_city(from_city)} → {title_city(to_city)}",
        url,
    )
    clear_state(user_id)
