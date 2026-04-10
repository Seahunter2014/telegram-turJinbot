from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_user_states: dict[int, dict[str, Any]] = {}

_lock = threading.Lock()
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SUBSCRIBERS_FILE.exists():
        SUBSCRIBERS_FILE.write_text("{}", encoding="utf-8")


def _read_subscribers() -> dict[str, dict[str, Any]]:
    _ensure_storage()
    try:
        raw = SUBSCRIBERS_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return {}
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        return {}


def _write_subscribers(data: dict[str, dict[str, Any]]) -> None:
    _ensure_storage()
    temp_file = SUBSCRIBERS_FILE.with_suffix(".tmp")
    temp_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_file.replace(SUBSCRIBERS_FILE)


def get_state(user_id: int) -> dict[str, Any] | None:
    return _user_states.get(user_id)


def set_state(user_id: int, state: dict[str, Any]) -> None:
    _user_states[user_id] = state


def clear_state(user_id: int) -> None:
    _user_states.pop(user_id, None)


def set_user_flow(
    user_id: int,
    state_name: str,
    service: str | None = None,
    data: dict[str, Any] | None = None,
) -> None:
    current = _user_states.get(user_id, {})
    current["state"] = state_name
    if service is not None:
        current["service"] = service
    if data is not None:
        current["data"] = data
    else:
        current.setdefault("data", {})
    _user_states[user_id] = current


def get_user_flow(user_id: int) -> tuple[str | None, str | None, dict[str, Any]]:
    current = _user_states.get(user_id, {})
    return current.get("state"), current.get("service"), current.get("data", {})


def save_result(user_id: int, service: str, query: str, summary: str, url: str) -> None:
    current = _user_states.get(user_id, {})
    current["last_service"] = service
    current["last_query"] = query
    current["last_summary"] = summary
    current["last_url"] = url
    current.setdefault("data", {})
    _user_states[user_id] = current


def get_last_service(user_id: int) -> str | None:
    current = _user_states.get(user_id, {})
    return current.get("last_service")


def get_last_query(user_id: int) -> str | None:
    current = _user_states.get(user_id, {})
    return current.get("last_query")


def get_last_summary(user_id: int) -> str | None:
    current = _user_states.get(user_id, {})
    return current.get("last_summary")


def get_last_url(user_id: int) -> str | None:
    current = _user_states.get(user_id, {})
    return current.get("last_url")


def subscribe_user(user_id: int) -> None:
    with _lock:
        data = _read_subscribers()
        key = str(user_id)
        item = data.get(key, {})
        item["telegram_user_id"] = user_id
        item["is_subscribed"] = True
        item["is_blocked"] = False
        item["subscribed_at"] = item.get("subscribed_at") or datetime.now(timezone.utc).isoformat()
        item["updated_at"] = datetime.now(timezone.utc).isoformat()
        data[key] = item
        _write_subscribers(data)


def unsubscribe_user(user_id: int) -> None:
    with _lock:
        data = _read_subscribers()
        key = str(user_id)
        item = data.get(key, {})
        item["telegram_user_id"] = user_id
        item["is_subscribed"] = False
        item["unsubscribed_at"] = datetime.now(timezone.utc).isoformat()
        item["updated_at"] = datetime.now(timezone.utc).isoformat()
        data[key] = item
        _write_subscribers(data)


def is_subscribed(user_id: int) -> bool:
    with _lock:
        data = _read_subscribers()
        item = data.get(str(user_id), {})
        return bool(item.get("is_subscribed", False)) and not bool(item.get("is_blocked", False))


def get_subscribed_user_ids() -> list[int]:
    with _lock:
        data = _read_subscribers()
        result: list[int] = []
        for key, item in data.items():
            if item.get("is_subscribed") and not item.get("is_blocked"):
                try:
                    result.append(int(key))
                except ValueError:
                    continue
        return result


def mark_user_blocked(user_id: int) -> None:
    with _lock:
        data = _read_subscribers()
        key = str(user_id)
        item = data.get(key, {})
        item["telegram_user_id"] = user_id
        item["is_blocked"] = True
        item["is_subscribed"] = False
        item["blocked_at"] = datetime.now(timezone.utc).isoformat()
        item["updated_at"] = datetime.now(timezone.utc).isoformat()
        data[key] = item
        _write_subscribers(data)


# Совместимость с уже существующим callback_data="subscribe"
def subscribe(user_id: int) -> None:
    subscribe_user(user_id)
