import os


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


BOT_TOKEN = _get_env("BOT_TOKEN")
WEBHOOK_BASE_URL = _get_env("WEBHOOK_BASE_URL").rstrip("/")
WEBHOOK_PATH = _get_env("WEBHOOK_PATH", "/webhook")

ADMIN_TELEGRAM_ID = _get_env("ADMIN_TELEGRAM_ID")
TRAVELPAYOUTS_MARKER = _get_env("TRAVELPAYOUTS_MARKER", "98526")
TRAVELPAYOUTS_API_TOKEN = _get_env("TRAVELPAYOUTS_API_TOKEN") or _get_env("AVIASALES_API_TOKEN")

OPENAI_API_KEY = _get_env("OPENAI_API_KEY")

ALEAN_BASE_URL = _get_env("ALEAN_BASE_URL")
ALEAN_AGENT_LOGIN = _get_env("ALEAN_AGENT_LOGIN")
ALEAN_AGENT_PASSWORD = _get_env("ALEAN_AGENT_PASSWORD")

APP_NAME = "TourJin"


MAIN_MENU_TEXT = "🧞 Слушаюсь и повинуюсь, мой господин.\nЧего изволите?"
NEXT_ACTION_TEXT = "_Чего изволите далее?_"
SERVICE_IN_PROGRESS_TEXT = "🧞 Сервис на доработке."
ALEAN_IN_PROGRESS_TEXT = "🧭 Детальный подбор сейчас на доработке."


def admin_chat_id() -> int | None:
    if not ADMIN_TELEGRAM_ID:
        return None
    try:
        return int(ADMIN_TELEGRAM_ID)
    except ValueError:
        return None


def webhook_url() -> str:
    if not WEBHOOK_BASE_URL:
        return ""
    return f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"
