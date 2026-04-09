import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "").rstrip("/")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


def tg_send_message(chat_id: int, text: str) -> dict:
    if not BOT_TOKEN:
        return {"ok": False, "error": "BOT_TOKEN is not set"}

    url = f"{API_BASE}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    response = requests.post(url, json=payload, timeout=30)
    try:
        return response.json()
    except Exception:
        return {"ok": False, "status_code": response.status_code, "text": response.text}


@app.get("/")
async def root():
    return {"message": "TourJin bot is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/set-webhook")
async def set_webhook():
    if not BOT_TOKEN:
        return {"ok": False, "error": "BOT_TOKEN is not set"}

    if not WEBHOOK_BASE_URL:
        return {"ok": False, "error": "WEBHOOK_BASE_URL is not set"}

    webhook_url = f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"
    url = f"{API_BASE}/setWebhook"
    response = requests.get(url, params={"url": webhook_url}, timeout=30)
    return response.json()


@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()

    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if chat_id:
        if text == "/start":
            tg_send_message(
                chat_id,
                "🧞 Слушаюсь и повинуюсь, мой господин.\n"
                "TourJin пробуждён.\n\n"
                "Пока базовый режим активен.\n"
                "Напишите любой текст — я отвечу."
            )
        else:
            tg_send_message(
                chat_id,
                "🧞 Сервис на доработке.\n"
                f"Вы написали: {text if text else '[без текста]'}"
            )

    return {"ok": True}
