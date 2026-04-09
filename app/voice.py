from app.config import OPENAI_API_KEY


def is_voice_available() -> bool:
    return bool(OPENAI_API_KEY)
