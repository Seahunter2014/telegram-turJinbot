import requests
from fastapi import FastAPI, Request, HTTPException, Query

from app.config import BOT_TOKEN, webhook_url, BROADCAST_SECRET
from app.handlers import handle_text, handle_callback
from app.services.broadcasts import run_broadcast

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


@app.get("/broadcast/run")
async def broadcast_run(
    secret: str = Query(...),
    kind: str = Query(..., description="flight_map | hot_tours | trip_best"),
):
    if not BROADCAST_SECRET or secret != BROADCAST_SECRET:
        raise HTTPException(status_code=403, detail="forbidden")

    if kind not in {"flight_map", "hot_tours", "trip_best"}:
        raise HTTPException(status_code=400, detail="unknown broadcast kind")

    result = run_broadcast(kind)
    return result


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
