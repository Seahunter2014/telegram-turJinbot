from app.services.common import with_marker
from urllib.parse import quote_plus
import re

SERVICE_ID = "insurance"
BUTTON = "🛡 Оберег туриста"
OPEN_TEXT = "🛡 Открыть страховки"
STEPS = ["ins_q1"]
START_TEXT = """🧞 Слушаюсь и повинуюсь, мой господин.
Для какой страны нужен оберег?
Можно сразу указать срок поездки.
Например:
Италия 7 дней
Турция 10 дней"""
CLARIFY_TEXT = "Назовите страну.\nПри желании сразу добавьте срок поездки.\nНапример: Турция 10 дней"


def parse_input(text: str):
    m = re.search(r'(\d+)\s+(?:дней|день|дня|недель|неделю|недели)', text.lower())
    days = int(m.group(1)) if m else None
    country = text
    if m:
        country = re.sub(r'(\d+)\s+(?:дней|день|дня|недель|неделю|недели)', '', text, flags=re.I).strip(' ,.-')
    return {"country": country.strip().capitalize() or None, "days": days}


def is_valid(data: dict) -> bool:
    return bool(data.get("country"))


def build_url(data: dict) -> str:
    return with_marker(f"https://cherehapa.ru/?country={quote_plus(data.get('country') or '')}")


def summary(data: dict) -> str:
    line = data.get('country')
    if data.get('days'):
        line += f" · {data['days']} дней"
    return f"✨ Ваше желание исполнено, мой господин.\n🛡 {line}\nЯ открыл сервис страхования.\nЭти данные нужно будет ввести на сайте."
