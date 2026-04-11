import requests
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse

from app.config import BOT_TOKEN, webhook_url, BROADCAST_SECRET
import app.handlers as handlers
from app.services.broadcasts import run_broadcast

app = FastAPI()

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


@app.get("/")
async def root():
    return {"message": "TourJin bot is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/set-webhook")
async def set_webhook():
    url = webhook_url()
    if not url:
        raise HTTPException(status_code=500, detail="WEBHOOK_BASE_URL is empty")

    resp = requests.get(
        f"{API_BASE}/setWebhook",
        params={"url": url},
        timeout=30,
    )
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
    return JSONResponse(content=result)


def _redirect_to_target(target: str | None, service: str, item_id: str):
    """
    Универсальный редирект на целевой URL.
    Пока минимально и безопасно:
    - если target не передан -> 400
    - если target передан -> redirect 302
    """
    if not target:
        raise HTTPException(
            status_code=400,
            detail=f"missing target for service={service}, id={item_id}",
        )

    return RedirectResponse(url=target, status_code=302)


@app.get("/go/flight/{item_id}")
async def go_flight(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "flight", item_id)


@app.get("/go/car/{item_id}")
async def go_car(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "car", item_id)


@app.get("/go/hotel/{item_id}")
async def go_hotel(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "hotel", item_id)


@app.get("/go/tour/{item_id}")
async def go_tour(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "tour", item_id)


@app.get("/go/insurance/{item_id}")
async def go_insurance(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "insurance", item_id)


@app.get("/go/transfer/{item_id}")
async def go_transfer(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "transfer", item_id)


@app.get("/go/excursion/{item_id}")
async def go_excursion(item_id: str, target: str | None = Query(default=None)):
    return _redirect_to_target(target, "excursion", item_id)


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
