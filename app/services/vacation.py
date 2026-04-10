from app.utils.telegram import send_message, send_inline
from app.keyboards import choice_menu, main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, NEXT_ACTION_TEXT, ALEAN_IN_PROGRESS_TEXT
from app.services.common import (
    normalize_text,
    VACATION_COUNTRY_SLUGS,
    VACATION_MONTH_SLUGS,
)


def start_vacation(chat_id: int, user_id: int):
    set_user_flow(user_id, "vacation_choice", "vacation")

    send_message(
        chat_id,
        "Выберите формат поиска, мой господин.",
        reply_markup=choice_menu(),
    )


def handle_vacation_choice(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    if "быстрый" in t:
        set_user_flow(user_id, "vacation_input", "vacation")

        send_message(
            chat_id,
            "🧞 Слушаюсь и повинуюсь, мой господин.\n"
            "Куда и когда?\n\n"
            "Например:\n"
            "Турция август\n"
            "Египет февраль",
        )

    elif "детальный" in t:
        send_message(chat_id, ALEAN_IN_PROGRESS_TEXT, reply_markup=main_menu())
        clear_state(user_id)

    elif "отмена" in t:
        clear_state(user_id)
        send_message(chat_id, "Слушаюсь, возвращаемся.", reply_markup=main_menu())


def handle_vacation(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    country = None
    month = None

    for key in VACATION_COUNTRY_SLUGS:
        if key in t:
            country = key
            break

    for key in VACATION_MONTH_SLUGS:
        if key in t:
            month = key
            break

    if not country:
        send_message(
            chat_id,
            "Уточните направление, мой господин.\nНапример: Турция август",
        )
        return

    country_slug = VACATION_COUNTRY_SLUGS.get(country)

    if month:
        month_slug = VACATION_MONTH_SLUGS.get(month)
        url = f"https://www.travelata.ru/{country_slug}/{month_slug}?marker={TRAVELPAYOUTS_MARKER}"
    else:
        url = f"https://www.travelata.ru/{country_slug}?marker={TRAVELPAYOUTS_MARKER}"

    summary = f"🌴 {country.capitalize()}" + (f" · {month}" if month else "")

    send_inline(
        chat_id,
        "✨ Ваше желание исполнено, мой господин.\n"
        f"{summary}\n"
        "Подобрал туры по направлению и сезону.\n"
        "Город вылета и детали — внутри сервиса.",
        result_inline(url, "vacation"),
    )

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "vacation", text, summary, url)
    clear_state(user_id)
