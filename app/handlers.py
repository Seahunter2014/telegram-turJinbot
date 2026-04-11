from app.keyboards import main_menu
from app.utils.telegram import send_message, answer_callback
from app.storage import get_user_flow, clear_state, get_last_service, subscribe
from app.config import MAIN_MENU_TEXT, SERVICE_IN_PROGRESS_TEXT

from app.services.flights import start_flights, handle_flights
from app.services.vacation import start_vacation, handle_vacation_choice, handle_vacation
from app.services.hotels import start_hotels, handle_hotels_choice, handle_hotels
from app.services.insurance import start_insurance, handle_insurance
from app.services.car_rental import start_car, handle_car
from app.services.transfer import start_transfer
from app.services.excursions import start_excursions, handle_excursions


def start(chat_id: int):
    send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_menu())


def handle_text(chat_id: int, user_id: int, text: str):
    state, service, data = get_user_flow(user_id)

    if text == "❌ Отмена":
        clear_state(user_id)
        send_message(chat_id, "🧞 Слушаюсь, мой господин.", reply_markup=main_menu())
        return

    if state == "flights_input":
        handle_flights(chat_id, user_id, text)
        return

    if state == "vacation_choice":
        handle_vacation_choice(chat_id, user_id, text)
        return

    if state == "vacation_input":
        handle_vacation(chat_id, user_id, text)
        return

    if state == "hotels_choice":
        handle_hotels_choice(chat_id, user_id, text)
        return

    if state == "hotels_input":
        handle_hotels(chat_id, user_id, text)
        return

    if state == "insurance_input":
        handle_insurance(chat_id, user_id, text)
        return

    if state == "car_input":
        handle_car(chat_id, user_id, text)
        return

    if state == "excursions_input":
        handle_excursions(chat_id, user_id, text)
        return

    if text == "/start":
        start(chat_id)
        return

    if text == "🧞 Ковер самолет":
        start_flights(chat_id, user_id)
        return

    if text == "🌴 Отпуск под ключ":
        start_vacation(chat_id, user_id)
        return

    if text == "🏰 Снять дворец":
        start_hotels(chat_id, user_id)
        return

    if text == "🛡 Оберег туриста":
        start_insurance(chat_id, user_id)
        return

    if text == "🚗 Аренда авто":
        start_car(chat_id, user_id)
        return

    if text == "🚖 Эх, прокачу":
        start_transfer(chat_id, user_id)
        return

    if text == "🎭 Хлеба и зрелищ":
        start_excursions(chat_id, user_id)
        return

    if service == "flights":
        handle_flights(chat_id, user_id, text)
        return

    if service == "vacation":
        handle_vacation(chat_id, user_id, text)
        return

    if service == "hotels":
        handle_hotels(chat_id, user_id, text)
        return

    if service == "insurance":
        handle_insurance(chat_id, user_id, text)
        return

    if service == "car":
        handle_car(chat_id, user_id, text)
        return

    if service == "excursions":
        handle_excursions(chat_id, user_id, text)
        return

    send_message(chat_id, SERVICE_IN_PROGRESS_TEXT, reply_markup=main_menu())


def handle_callback(chat_id: int, user_id: int, data: str, callback_id: str):
    answer_callback(callback_id)

    if data.startswith("retry_"):
        service = data.split("_", 1)[1]

        if service == "flights":
            start_flights(chat_id, user_id)
            return
        if service == "vacation":
            start_vacation(chat_id, user_id)
            return
        if service == "hotels":
            start_hotels(chat_id, user_id)
            return
        if service == "insurance":
            start_insurance(chat_id, user_id)
            return
        if service == "car":
            start_car(chat_id, user_id)
            return
        if service == "transfer":
            start_transfer(chat_id, user_id)
            return
        if service == "excursions":
            start_excursions(chat_id, user_id)
            return

    if data == "subscribe":
        subscribe(user_id)
        send_message(
            chat_id,
            "Готово.\n"
            "Подписка включена :\n"
            "• карта цен авиарейсов\n"
            "• горящие туры\n"
            "• лучшие предложения дня",
            reply_markup=main_menu(),
        )
        return

    if data == "contact_admin":
        send_message(
            chat_id,
            "🧙 Передам старшему магу.\n"
            "Укажите:\n"
            "— Имя\n"
            "— Контакт\n"
            "— Даты\n"
            "— Пожелания",
            reply_markup=main_menu(),
        )
        return
