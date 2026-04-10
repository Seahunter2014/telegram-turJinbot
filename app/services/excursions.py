from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, NEXT_ACTION_TEXT
from app.services.common import (
    normalize_text,
    EXCURSIONS_CITY_SLUGS,
    translit_slug,
    title_city,
    find_dates_ru,
)


def start_excursions(chat_id: int, user_id: int):
    set_user_flow(user_id, "excursions_input", "excursions")

    send_message(
        chat_id,
        "🧞 Слушаюсь и повинуюсь, мой господин.\n"
        "В каком городе ищем впечатления?\n\n"
        "Можно сразу указать дату.\n\n"
        "Например:\n"
        "Стамбул 15 июня\n"
        "Рим\n",
    )


def handle_excursions(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    if not t:
        send_message(chat_id, "Назовите город, мой господин.")
        return

    dates = find_dates_ru(t)
    date = dates[0] if dates else None

    city = t.split()[0]
    city_title = title_city(city)

    slug = EXCURSIONS_CITY_SLUGS.get(city) or translit_slug(city)

    if slug:
        url = f"https://tripster.ru/city/{slug}/experiences/?marker={TRAVELPAYOUTS_MARKER}"
        if date:
            url += f"&date={date}"
    else:
        url = f"https://tripster.ru/search/?q={city_title}&marker={TRAVELPAYOUTS_MARKER}"

    result_text = (
        "✨ Ваше желание исполнено, мой господин.\n"
        f"🎭 {city_title}\n"
        "Подобрал впечатления.\n"
        "Дата и детали уточняются на сайте."
    )

    send_inline(chat_id, result_text, result_inline(url, "excursions"))

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "excursions", text, f"🎭 {city_title}", url)
    clear_state(user_id)
