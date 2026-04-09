from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TourJin bot is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")


@app.get("/set-webhook")
async def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    webhook_url = f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"

    response = requests.get(url, params={"url": webhook_url})
    return response.json()
