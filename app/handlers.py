from aiogram import Router, types
from aiogram.types import Message
from app.keyboards import get_main_keyboard

router = Router()


@router.message()
async def handle_message(message: Message):
    text = message.text

    if text == "🧞 Ковер самолет":
        await message.answer(
            "🧞 Слушаюсь и повинуюсь, мой господин.\n"
            "Куда летим?\n\n"
            "Например:\n"
            "Москва Стамбул 15 июня\n"
            "Москва Стамбул 15 июня туда 22 июня обратно 2 взрослых\n\n"
            "Текстом или голосом — как вашей душе угодно.",
            reply_markup=get_main_keyboard()
        )

    elif text == "🌴 Отпуск под ключ":
        await message.answer("🌴 Сервис в доработке.", reply_markup=get_main_keyboard())

    elif text == "🏰 Снять дворец":
        await message.answer("🏰 Сервис в доработке.", reply_markup=get_main_keyboard())

    elif text == "🛡 Оберег туриста":
        await message.answer("🛡 Сервис в доработке.", reply_markup=get_main_keyboard())

    elif text == "🚗 Аренда авто":
        await message.answer("🚗 Сервис в доработке.", reply_markup=get_main_keyboard())

    elif text == "🚖 Эх, прокачу":
        await message.answer("🚖 Сервис в доработке.", reply_markup=get_main_keyboard())

    elif text == "🎭 Хлеба и зрелищ":
        await message.answer("🎭 Сервис в доработке.", reply_markup=get_main_keyboard())

    else:
        await message.answer("🧞 Чего изволите?", reply_markup=get_main_keyboard())
