import requests
from app.config import BOT_TOKEN

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


def send_message(chat_id: int, text: str, reply_markup=None, parse_mode="Markdown"):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        requests.post(f"{API_BASE}/sendMessage", json=payload, timeout=30)
    except Exception:
        pass


def send_inline(chat_id: int, text: str, reply_markup):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": reply_markup,
        "parse_mode": "Markdown",
    }

    try:
        requests.post(f"{API_BASE}/sendMessage", json=payload, timeout=30)
    except Exception:
        pass


def answer_callback(callback_id: str):
    try:
        requests.post(
            f"{API_BASE}/answerCallbackQuery",
            json={"callback_query_id": callback_id},
            timeout=30,
        )
    except Exception:
        pass


def send_typing(chat_id: int):
    try:
        requests.post(
            f"{API_BASE}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=30,
        )
    except Exception:
        pass
