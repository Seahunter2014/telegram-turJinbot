import re
from datetime import datetime


MONTHS_RU = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
    "январь": "01",
    "февраль": "02",
    "март": "03",
    "апрель": "04",
    "май": "05",
    "июнь": "06",
    "июль": "07",
    "август": "08",
    "сентябрь": "09",
    "октябрь": "10",
    "ноябрь": "11",
    "декабрь": "12",
}

MONTH_DISPLAY = {
    "01": "январь",
    "02": "февраль",
    "03": "март",
    "04": "апрель",
    "05": "май",
    "06": "июнь",
    "07": "июль",
    "08": "август",
    "09": "сентябрь",
    "10": "октябрь",
    "11": "ноябрь",
    "12": "декабрь",
}


CITY_TO_IATA = {
    "москва": "MOW",
    "санкт-петербург": "LED",
    "петербург": "LED",
    "стамбул": "IST",
    "анталья": "AYT",
    "дубай": "DXB",
    "сочи": "AER",
    "тбилиси": "TBS",
    "ереван": "EVN",
    "рим": "ROM",
    "милан": "MIL",
    "париж": "PAR",
    "барселона": "BCN",
    "бангкок": "BKK",
    "пхукет": "HKT",
    "казань": "KZN",
}


VACATION_COUNTRY_SLUGS = {
    "турция": "turkey",
    "египет": "egypt",
    "оаэ": "uae",
    "тайланд": "thailand",
    "таиланд": "thailand",
    "греция": "greece",
    "кипр": "cyprus",
    "италия": "italy",
    "испания": "spain",
}

VACATION_MONTH_SLUGS = {
    "январь": "january",
    "февраль": "february",
    "март": "march",
    "апрель": "april",
    "май": "may",
    "июнь": "june",
    "июль": "july",
    "август": "august",
    "сентябрь": "september",
    "октябрь": "october",
    "ноябрь": "november",
    "декабрь": "december",
}

HOTELS_CITY_TO_COUNTRY = {
    "стамбул": "turkey",
    "анталья": "turkey",
    "дубай": "uae",
    "милан": "italy",
    "рим": "italy",
    "бангкок": "thailand",
    "пхукет": "thailand",
}

CAR_CITY_SLUGS = {
    "анталья": "antalya",
    "тбилиси": "tbilisi",
    "дубай": "dubai",
    "стамбул": "istanbul",
    "сочи": "sochi",
    "ереван": "yerevan",
}

EXCURSIONS_CITY_SLUGS = {
    "стамбул": "istanbul",
    "рим": "rome",
    "милан": "milan",
    "париж": "paris",
    "барселона": "barcelona",
    "тбилиси": "tbilisi",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def title_city(text: str) -> str:
    return " ".join(part.capitalize() for part in normalize_text(text).split())


def date_to_iso(day: str, month_word: str, year: int | None = None) -> str:
    year = year or datetime.now().year
    month = MONTHS_RU.get(month_word.lower())
    if not month:
        return ""
    return f"{year}-{month}-{int(day):02d}"


def find_dates_ru(text: str) -> list[str]:
    pattern = re.compile(r"(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря|январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)", re.IGNORECASE)
    results = []
    for day, month_word in pattern.findall(text):
        iso = date_to_iso(day, month_word)
        if iso:
            results.append(iso)
    return results


def iso_to_ddmm(iso_date: str) -> str:
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d%m")


def translit_slug(text: str) -> str:
    mapping = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
        " ": "-", "-": "-"
    }
    text = normalize_text(text)
    return "".join(mapping.get(ch, ch) for ch in text)


def parse_passengers(text: str) -> tuple[int, int, int]:
    t = normalize_text(text).replace("ё", "е")
    adults = 1
    children = 0
    infants = 0

    m = re.search(r"(\d+)\s+взросл", t)
    if m:
        adults = int(m.group(1))

    m = re.search(r"(\d+)\s+(?:ребенок|ребенка|детей|дети)", t)
    if m:
        children = int(m.group(1))

    m = re.search(r"(\d+)\s+(?:младенец|младенца|младенцев)", t)
    if m:
        infants = int(m.group(1))

    return adults, children, infants
