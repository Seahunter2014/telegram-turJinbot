from app.services.common import with_marker, slugify_ru

SERVICE_ID = "vacation"
BUTTON = "🌴 Отпуск под ключ"
OPEN_TEXT = "🌴 Смотреть туры"
STEPS = ["vc_q1"]
START_TEXT = """🧞 Слушаюсь и повинуюсь, мой господин.
Куда и когда?
Например:
Турция август
Египет февраль
море и солнце, июль
Направление и месяц — этого достаточно.
Остальное удобно уточнить уже внутри сервиса."""
CLARIFY_TEXT = "Уточните направление, мой господин. Например: Турция август"
COUNTRIES = {"турция":"turkey","египет":"egypt","оаэ":"uae","тайланд":"thailand","таиланд":"thailand","греция":"greece","кипр":"cyprus","италия":"italy","испания":"spain"}
MONTHS = {"январь":"january","февраль":"february","март":"march","апрель":"april","май":"may","июнь":"june","июль":"july","август":"august","сентябрь":"september","октябрь":"october","ноябрь":"november","декабрь":"december"}


def parse_input(text: str):
    low = text.lower().strip()
    month_name = next((m for m in MONTHS if m in low), None)
    direction = text
    if month_name:
        direction = low.replace(month_name, '').strip(' ,.-').capitalize()
    else:
        direction = text.strip().capitalize()
    return {"direction": direction or None, "month_name": month_name}


def is_valid(data: dict) -> bool:
    return bool(data.get("direction"))


def build_url(data: dict) -> str:
    country_slug = COUNTRIES.get((data.get("direction") or '').lower(), slugify_ru(data.get("direction") or ''))
    month_slug = MONTHS.get((data.get("month_name") or '').lower())
    url = f"https://www.travelata.ru/{country_slug}"
    if month_slug:
        url += f"/{month_slug}"
    return with_marker(url)


def summary(data: dict) -> str:
    title = data.get("direction") or "Направление"
    if data.get("month_name"):
        title += f" · {data['month_name']}"
    return f"✨ Ваше желание исполнено, мой господин.\n🌴 {title}\nПодобрал туры по направлению и сезону.\nГород вылета, состав путешественников и прочие детали — внутри сервиса."
