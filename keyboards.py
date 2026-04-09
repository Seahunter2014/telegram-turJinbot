import requests
from app.config import BOT_TOKEN

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


def send_message(chat_id: int, text: str, reply_markup: dict | None = None, parse_mode: str | None = None):
    if not API_BASE:
        return {"ok": False, "error": "BOT_TOKEN is not set"}
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup is not None:
        payload["reply_markup"] = reply_markup
    if parse_mode:
        payload["parse_mode"] = parse_mode
    r = requests.post(f"{API_BASE}/sendMessage", json=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "text": r.text, "status_code": r.status_code}


def answer_callback(callback_query_id: str, text: str | None = None):
    if not API_BASE:
        return {"ok": False}
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
    requests.post(f"{API_BASE}/answerCallbackQuery", json=payload, timeout=30)


def set_webhook(url: str):
    r = requests.get(f"{API_BASE}/setWebhook", params={"url": url}, timeout=30)
    return r.json()
