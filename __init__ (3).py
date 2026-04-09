from app.config import ALEAN_BASE_URL, ALEAN_AGENT_LOGIN, ALEAN_AGENT_PASSWORD


def is_configured() -> bool:
    return bool(ALEAN_BASE_URL and ALEAN_AGENT_LOGIN and ALEAN_AGENT_PASSWORD)
