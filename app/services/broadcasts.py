import time
from typing import Any

import requests

from app.config import (
    BOT_TOKEN,
    AVIASALES_MAP_URL,
    TRAVELATA_HOT_URL,
    TRIPCOM_DEALS_URL,
)
from app.storage import get_subscribed_user_ids, mark_user_blocked

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""


def _build_broadcast(kind: str) -> tuple[str, str, str]:
    if kind == "flight_map":
        text = (
            "✈️ Карта цен на вылеты из ближайшего аэропорта\n\n"
            "Смотрим, куда сейчас можно улететь особенно выгодно."
        )
        button_text = "🔥 Смотреть карту цен"
        url = AVIASALES_MAP_URL
        return text, button_text, url

    if kind == "hot_tours":
        text = (
            "🌴 Горящие туры\n\n"
            "Собрал для вас быстрый вход в актуальные предложения на сейчас."
        )
        button_text = "🔥 Смотреть туры"
        url = TRAVELATA_HOT_URL
        return text, button_text, url

    if kind == "trip_best":
        text = (
            "🏨 Лучшие предложения дня\n\n"
            "Свежая подборка выгодных вариантов на сегодня."
        )
        button_text = "🔥 Смотреть предложения"
        url = TRIPCOM_DEALS_URL
        return text, button_text, url

    raise ValueError(f"Unknown broadcast kind: {kind}")


def _send_broadcast_message(chat_id: int, text: str, button_text: str, url: str) -> str:
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": button_text, "url": url}],
                [{"text": "🔕 Отписаться", "callback_data": "unsubscribe"}],
            ]
        },
    }

    try:
        response = requests.post(
            f"{API_BASE}/sendMessage",
            json=payload,
            timeout=30,
        )
    except Exception:
        return "failed"

    try:
        data: dict[str, Any] = response.json()
    except Exception:
        data = {}

    if response.status_code == 200 and data.get("ok") is True:
        return "sent"

    error_code = data.get("error_code", response.status_code)
    description = str(data.get("description", "")).lower()

    if error_code == 403 or "bot was blocked by the user" in description:
        return "blocked"

    return "failed"


def run_broadcast(kind: str) -> dict[str, Any]:
    text, button_text, url = _build_broadcast(kind)
    user_ids = get_subscribed_user_ids()

    sent = 0
    blocked = 0
    failed = 0

    for user_id in user_ids:
        result = _send_broadcast_message(
            chat_id=user_id,
            text=text,
            button_text=button_text,
            url=url,
        )

        if result == "sent":
            sent += 1
        elif result == "blocked":
            blocked += 1
            mark_user_blocked(user_id)
        else:
            failed += 1

        time.sleep(0.05)

    return {
        "ok": True,
        "kind": kind,
        "total": len(user_ids),
        "sent": sent,
        "blocked": blocked,
        "failed": failed,
    }
