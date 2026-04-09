import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "").rstrip("/")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
ADMIN_TELEGRAM_ID = os.getenv("ADMIN_TELEGRAM_ID", "").strip()
TRAVELPAYOUTS_MARKER = os.getenv("TRAVELPAYOUTS_MARKER", "98526").strip()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

ALEAN_BASE_URL = os.getenv("ALEAN_BASE_URL", "").strip()
ALEAN_AGENT_LOGIN = os.getenv("ALEAN_AGENT_LOGIN", "").strip()
ALEAN_AGENT_PASSWORD = os.getenv("ALEAN_AGENT_PASSWORD", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
