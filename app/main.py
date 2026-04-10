import requests
from fastapi import FastAPI, Request

from app.config import BOT_TOKEN, webhook_url
from app.handlers import handle_text, handle_callback

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
    resp = requests.get(f"{API_BASE}/setWebhook", params={"url": url})
    return resp.json()


@app.post("/webhook")
async def webhook(req: Request):
    update = await req.json()

    # MESSAGE
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = (msg.get("text") or "").strip()

        handle_text(chat_id, user_id, text)

    # CALLBACK
    if "callback_query" in update:
        cb = update["callback_query"]
        chat_id = cb["message"]["chat"]["id"]
        user_id = cb["from"]["id"]
        data = cb["data"]
        callback_id = cb["id"]

        handle_callback(chat_id, user_id, data, callback_id)

    return {"ok": True}
