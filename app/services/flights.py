from app.utils.telegram import send_message, send_inline, send_typing
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, NEXT_ACTION_TEXT
from app.services.common import (
    normalize_text,
    find_dates_ru,
    iso_to_ddmm,
    CITY_TO_IATA,
    title_city,
    parse_passengers,
)


def start_flights(chat_id: int, user_id: int):
    set_user_flow(user_id, "flights_input", "flights")

    send_message(
        chat_id,
        "🧞 Слушаюсь и повинуюсь, мой господин.\n"
        "Куда летим?\n\n"
        "Например:\n"
        "Москва Стамбул 15 июня туда 22 июня обратно 2 взрослых\n\n"
        "Если есть дети:\n"
        "0–2 года — младенец\n"
        "2–11 лет — ребёнок\n\n"
        "Текстом или голосом — как вашей душе угодно.",
    )


def handle_flights(chat_id: int, user_id: int, text: str):
    send_typing(chat_id)

    t = normalize_text(text)

    dates = find_dates_ru(t)
    if not dates:
        send_message(
            chat_id,
            "Уточню ещё немного, мой господин.\n"
            "Мне нужны маршрут и дата.\n"
            "Например: Москва Стамбул 15 июня",
        )
        return

    cities = []
    for city in CITY_TO_IATA.keys():
        if city in t:
            cities.append(city)

    if len(cities) < 2:
        send_message(
            chat_id,
            "Уточню ещё немного, мой господин.\n"
            "Мне нужны города вылета и прилёта.",
        )
        return

    from_city = cities[0]
    to_city = cities[1]

    origin = CITY_TO_IATA.get(from_city)
    destination = CITY_TO_IATA.get(to_city)

    if not origin or not destination:
        send_message(chat_id, "Не удалось определить города.")
        return

    depart = dates[0]
    return_date = dates[1] if len(dates) > 1 else None

    ddmm_depart = iso_to_ddmm(depart)
    ddmm_return = iso_to_ddmm(return_date) if return_date else ""

    adults, children, infants = parse_passengers(t)

    url = (
        f"https://www.aviasales.ru/search/"
        f"{origin}{ddmm_depart}{destination}{ddmm_return}"
        f"?adults={adults}&children={children}&infants={infants}"
        f"&marker={TRAVELPAYOUTS_MARKER}"
    )

    summary = (
        f"✈️ {title_city(from_city)} → {title_city(to_city)}\n"
        f"📅 {depart}"
    )

    send_inline(
        chat_id,
        "✨ Ваше желание исполнено, мой господин.\n"
        f"{summary}\n"
        f"👥 взрослых: {adults}\n"
        "Маршрут, даты и пассажиры учтены в ссылке.\n\n"
        "💰 Цены уточняются при переходе.",
        result_inline(url, "flights"),
    )

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "flights", text, summary, url)
    clear_state(user_id)
