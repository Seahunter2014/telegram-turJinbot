from typing import Any


_user_states: dict[int, dict[str, Any]] = {}
_subscribers: set[int] = set()


def get_state(user_id: int) -> dict[str, Any] | None:
    return _user_states.get(user_id)


def set_state(user_id: int, state: dict[str, Any]) -> None:
    _user_states[user_id] = state


def clear_state(user_id: int) -> None:
    _user_states.pop(user_id, None)


def set_user_flow(user_id: int, state_name: str, service: str | None = None, data: dict[str, Any] | None = None) -> None:
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


def subscribe(user_id: int) -> None:
    _subscribers.add(user_id)


def is_subscribed(user_id: int) -> bool:
    return user_id in _subscribers
