import re
from app.services.common import with_marker

SERVICE_ID = "flights"
BUTTON = "🧞 Ковер самолет"
OPEN_TEXT = "✈️ Открыть варианты"
STEPS = ["fl_q1"]

START_TEXT = """🧞 Слушаюсь и повинуюсь, мой господин.
Куда летим?

Например:
Москва Стамбул 15 июня в одну сторону 2 взрослых
Москва Стамбул 15 июня туда 22 июня обратно 2 взрослых

Если есть дети:
0–2 года — младенец
2–11 лет — ребёнок

Текстом или голосом — как вашей душе угодно."""

CLARIFY_TEXT = "Уточню ещё немного, мой господин.\nМне нужны маршрут и дата.\nНапример: Москва Стамбул 15 июня"

MONTHS = {"января": "01", "февраля": "02", "марта": "03", "апреля": "04", "мая": "05", "июня": "06", "июля": "07", "августа": "08", "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"}
IATA = {"москва":"MOW","санкт-петербург":"LED","петербург":"LED","стамбул":"IST","анталья":"AYT","дубай":"DXB","сочи":"AER","ереван":"EVN","тбилиси":"TBS","рим":"ROM","милан":"MIL","бангкок":"BKK","пхукет":"HKT","париж":"PAR","барселона":"BCN","казань":"KZN"}


def _find_dates(text: str):
    found = []
    for day, month in re.findall(r'(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)', text.lower()):
        found.append(f"2026-{MONTHS[month]}-{int(day):02d}")
    return found


def _ddmm(date_iso: str | None):
    if not date_iso:
        return None
    _, m, d = date_iso.split('-')
    return f"{d}{m}"


def parse_input(text: str):
    raw = text.strip()
    low = raw.lower()
    adults = int(re.search(r'(\d+)\s+взросл', low).group(1)) if re.search(r'(\d+)\s+взросл', low) else 1
    ch = re.search(r'(\d+)\s+(?:ребенок|ребёнок|детей|дети|ребенка|ребёнка)', low)
    inf = re.search(r'(\d+)\s+(?:младенец|младенца|младенцев)', low)
    children = int(ch.group(1)) if ch else 0
    infants = int(inf.group(1)) if inf else 0
    dates = _find_dates(low)
    depart_date = dates[0] if dates else None
    return_date = dates[1] if len(dates) > 1 else None
    cleaned = re.sub(r'\d+\s+взросл\w+', '', raw, flags=re.I)
    cleaned = re.sub(r'\d+\s+(?:ребенок|ребёнок|детей|дети|ребенка|ребёнка)', '', cleaned, flags=re.I)
    cleaned = re.sub(r'\d+\s+(?:младенец|младенца|младенцев)', '', cleaned, flags=re.I)
    cleaned = re.sub(r'\d{1,2}\s+(?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)', '', cleaned, flags=re.I)
    cleaned = re.sub(r'в одну сторону|туда|обратно|туда-обратно', '', cleaned, flags=re.I)
    parts = [p for p in re.split(r'[\s,-]+', cleaned.strip()) if p]
    from_city = parts[0].capitalize() if len(parts) >= 1 else None
    to_city = parts[1].capitalize() if len(parts) >= 2 else None
    return {"from_city": from_city, "to_city": to_city, "depart_date": depart_date, "return_date": return_date, "adults": adults, "children": children, "infants": infants}


def is_valid(data: dict) -> bool:
    return bool(data.get("from_city") and data.get("to_city") and data.get("depart_date"))


def build_url(data: dict) -> str:
    origin = IATA.get((data.get("from_city") or '').lower(), (data.get("from_city") or 'AAA')[:3].upper())
    dest = IATA.get((data.get("to_city") or '').lower(), (data.get("to_city") or 'BBB')[:3].upper())
    path = f"{origin}{_ddmm(data.get('depart_date'))}{dest}"
    if data.get("return_date"):
        path += _ddmm(data.get("return_date"))
    params = {}
    if data.get("adults", 1) > 1:
        params["adults"] = data["adults"]
    if data.get("children", 0) > 0:
        params["children"] = data["children"]
    if data.get("infants", 0) > 0:
        params["infants"] = data["infants"]
    base = f"https://www.aviasales.ru/search/{path}"
    if params:
        from urllib.parse import urlencode
        base = f"{base}?{urlencode(params)}"
    return with_marker(base)


def summary(data: dict) -> str:
    origin = IATA.get((data.get("from_city") or '').lower(), (data.get("from_city") or 'AAA')[:3].upper())
    dest = IATA.get((data.get("to_city") or '').lower(), (data.get("to_city") or 'BBB')[:3].upper())
    lines = [
        "✨ Ваше желание исполнено, мой господин.",
        f"✈️ {data.get('from_city')} ({origin}) → {data.get('to_city')} ({dest})",
        f"📅 {data.get('depart_date')}",
        f"👥 взрослых: {data.get('adults', 1)}",
    ]
    if data.get('children'):
        lines.append(f"👦 детей: {data.get('children')}")
    if data.get('infants'):
        lines.append(f"👶 младенцев: {data.get('infants')}")
    lines += [
        "Маршрут, даты и пассажиры учтены в ссылке.",
        "",
        f"✈️ Найдены билеты {data.get('from_city')} → {data.get('to_city')}",
        "1. Лучшая цена месяца",
        "💰 Цены приблизительные, уточняются при переходе.",
    ]
    return "\n".join(lines)
