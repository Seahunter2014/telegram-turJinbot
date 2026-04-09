from fastapi import FastAPI, Request
from app.config import BOT_TOKEN, WEBHOOK_BASE_URL, WEBHOOK_PATH
from app.handlers import handle_update
from app.utils.telegram import set_webhook

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TourJin bot is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/set-webhook")
async def route_set_webhook():
    if not BOT_TOKEN:
        return {"ok": False, "error": "BOT_TOKEN is not set"}
    if not WEBHOOK_BASE_URL:
        return {"ok": False, "error": "WEBHOOK_BASE_URL is not set"}
    return set_webhook(f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}")


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    handle_update(update)
    return {"ok": True}
