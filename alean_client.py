import re
from app.services.common import with_marker, slugify_ru

SERVICE_ID = "excursions"
BUTTON = "🎭 Хлеба и зрелищ"
OPEN_TEXT = "🎭 Смотреть экскурсии"
STEPS = ["ex_q1"]
START_TEXT = """🧞 Слушаюсь и повинуюсь, мой господин.
В каком городе и на какую дату ищем зрелища?
Например:
Стамбул 15 июня
Рим 1 июля"""
CLARIFY_TEXT = "Назовите город и дату. Например: Стамбул 15 июня"
MONTHS = {"января": "01", "февраля": "02", "марта": "03", "апреля": "04", "мая": "05", "июня": "06", "июля": "07", "августа": "08", "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"}
SLUGS = {"стамбул":"istanbul","рим":"rome","милан":"milan","дубай":"dubai"}


def parse_input(text: str):
    m = re.search(r'(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)', text.lower())
    date = None
    if m:
        date = f"2026-{MONTHS[m.group(2)]}-{int(m.group(1)):02d}"
    city = re.sub(r'\d{1,2}\s+(?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)', '', text, flags=re.I).strip(' ,.-').capitalize()
    return {"city": city or None, "date": date, "city_slug": SLUGS.get(city.lower() if city else '', slugify_ru(city or ''))}


def is_valid(data: dict) -> bool:
    return bool(data.get("city"))


def build_url(data: dict) -> str:
    slug = data.get('city_slug')
    url = f"https://tripster.ru/city/{slug}/experiences/"
    if data.get('date'):
        url += f"?date={data['date']}"
    return with_marker(url)


def summary(data: dict) -> str:
    tail = f" · {data['date']}" if data.get('date') else ''
    return f"✨ Ваше желание исполнено, мой господин.\n🎭 {data.get('city')}{tail}\nОткрою зрелища по городу.\nДетали уточните на странице."
