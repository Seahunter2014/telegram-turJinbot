from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import set_user_flow, clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, NEXT_ACTION_TEXT
from app.services.common import normalize_text, translit_slug, title_city, CAR_CITY_SLUGS


def start_car(chat_id: int, user_id: int):
    set_user_flow(user_id, "car_input", "car")

    send_message(
        chat_id,
        "🧞 Слушаюсь и повинуюсь, мой господин.\n"
        "В каком городе нужна машина?\n\n"
        "Например:\n"
        "Анталья\n"
        "Тбилиси\n"
        "Дубай\n\n"
        "Даты выберете на сайте.",
    )


def handle_car(chat_id: int, user_id: int, text: str):
    t = normalize_text(text)

    if not t:
        send_message(chat_id, "Назовите город аренды.")
        return

    city = t.split()[0]
    city_title = title_city(city)

    slug = CAR_CITY_SLUGS.get(city) or translit_slug(city)

    url = f"https://localrent.com/cars/{slug}?marker={TRAVELPAYOUTS_MARKER}"

    result_text = (
        "✨ Ваше желание исполнено, мой господин.\n"
        f"🚗 {city_title}\n"
        "Город учтён в ссылке.\n"
        "Даты и авто выберите на месте."
    )

    send_inline(chat_id, result_text, result_inline(url, "car"))

    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "car", text, f"🚗 {city_title}", url)
    clear_state(user_id)
