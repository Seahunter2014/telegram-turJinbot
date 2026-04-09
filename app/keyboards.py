def reply_keyboard(rows):
    return {"keyboard": [[{"text": t} for t in row] for row in rows], "resize_keyboard": True}


def inline_keyboard(rows):
    return {"inline_keyboard": rows}


MAIN_KEYBOARD = reply_keyboard([
    ["🧞 Ковер самолет", "🌴 Отпуск под ключ"],
    ["🏰 Снять дворец", "🛡 Оберег туриста"],
    ["🚗 Аренда авто", "🚖 Эх, прокачу"],
    ["🎭 Хлеба и зрелищ"],
])

CANCEL_KEYBOARD = reply_keyboard([["❌ Отмена"]])

MODE_KEYBOARD = reply_keyboard([["⚡ Быстрый поиск", "🧭 Детальный подбор"], ["❌ Отмена"]])
