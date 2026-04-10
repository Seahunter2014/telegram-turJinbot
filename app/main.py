import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "").rstrip("/")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


def send_message(chat_id: int, text: str):
    if not BOT_TOKEN:
        return
    requests.post(
        f"{API_BASE}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
        },
        timeout=30,
    )


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
    response = requests.get(
        f"{API_BASE}/setWebhook",
        params={"url": webhook_url},
        timeout=30,
    )
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
            send_message(
                chat_id,
                "🧞 Слушаюсь и повинуюсь, мой господин.\n"
                "Чего изволите?",
            )
        elif text == "🧞 Ковер самолет":
            send_message(
                chat_id,
                "🧞 Слушаюсь и повинуюсь, мой господин.\n"
                "Куда летим?\n\n"
                "Например:\n"
                "Москва Стамбул 15 июня в одну сторону 2 взрослых\n"
                "Москва Стамбул 15 июня туда 22 июня обратно 2 взрослых\n\n"
                "Если есть дети:\n"
                "0–2 года — младенец\n"
                "2–11 лет — ребёнок\n\n"
                "Текстом или голосом — как вашей душе угодно."
            )
        elif text == "🌴 Отпуск под ключ":
            send_message(chat_id, "🌴 Сервис на доработке.")
        elif text == "🏰 Снять дворец":
            send_message(chat_id, "🏰 Сервис на доработке.")
        elif text == "🛡 Оберег туриста":
            send_message(chat_id, "🛡 Сервис на доработке.")
        elif text == "🚗 Аренда авто":
            send_message(chat_id, "🚗 Сервис на доработке.")
        elif text == "🚖 Эх, прокачу":
            send_message(chat_id, "🚖 Сервис на доработке.")
        elif text == "🎭 Хлеба и зрелищ":
            send_message(chat_id, "🎭 Сервис на доработке.")
        else:
            send_message(chat_id, f"🧞 Сервис на доработке.\nВы написали: {text or '[без текста]'}")

    return {"ok": True}
