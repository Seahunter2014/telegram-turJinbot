from urllib.parse import quote


def main_menu():
    return {
        "keyboard": [
            [{"text": "🧞 Ковер самолет"}, {"text": "🌴 Отпуск под ключ"}],
            [{"text": "🏰 Снять дворец"}, {"text": "🛡 Оберег туриста"}],
            [{"text": "🚗 Аренда авто"}, {"text": "🚖 Эх, прокачу"}],
            [{"text": "🎭 Хлеба и зрелищ"}],
        ],
        "resize_keyboard": True
    }


def cancel_keyboard():
    return {
        "keyboard": [
            [{"text": "❌ Отмена"}]
        ],
        "resize_keyboard": True
    }


def choice_menu():
    return {
        "keyboard": [
            [{"text": "⚡ Быстрый поиск"}, {"text": "🧭 Детальный подбор"}],
            [{"text": "❌ Отмена"}]
        ],
        "resize_keyboard": True
    }


def result_inline(url: str, service: str):
    return {
        "inline_keyboard": [
            [{"text": "🔗 Открыть", "url": url}],
            [
                {"text": "✏️ Изменить запрос", "callback_data": f"retry_{service}"},
                {"text": "🧙 Старший маг", "callback_data": "contact_admin"},
            ],
            [{"text": "🔔 Подписаться", "callback_data": "subscribe"}]
        ]
    }
