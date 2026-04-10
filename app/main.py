import requests
from fastapi import FastAPI, Request

from app.config import BOT_TOKEN, webhook_url
import app.handlers as handlers

app = FastAPI()

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


@app.get("/")
async def root():
    return {"message": "TourJin bot is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/set-webhook")
async def set_webhook():
    url = webhook_url()
    resp = requests.get(f"{API_BASE}/setWebhook", params={"url": url}, timeout=30)
    return resp.json()


@app.post("/webhook")
async def webhook(req: Request):
    update = await req.json()

    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = (msg.get("text") or "").strip()

        if hasattr(handlers, "handle_text"):
            handlers.handle_text(chat_id, user_id, text)
        elif hasattr(handlers, "handle_message"):
            handlers.handle_message(chat_id, user_id, text)
        elif hasattr(handlers, "process_text"):
            handlers.process_text(chat_id, user_id, text)

    if "callback_query" in update:
        cb = update["callback_query"]
        chat_id = cb["message"]["chat"]["id"]
        user_id = cb["from"]["id"]
        data = cb["data"]
        callback_id = cb["id"]

        if hasattr(handlers, "handle_callback"):
            handlers.handle_callback(chat_id, user_id, data, callback_id)
        elif hasattr(handlers, "process_callback"):
            handlers.process_callback(chat_id, user_id, data, callback_id)

    return {"ok": True}
