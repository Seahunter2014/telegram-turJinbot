from app.services.common import with_marker

SERVICE_ID = "hotels"
BUTTON = "🏰 Снять дворец"
OPEN_TEXT = "🏨 Смотреть жильё"
STEPS = ["ht_q1"]
START_TEXT = """🧞 Слушаюсь и повинуюсь, мой господин.
В каком городе ищем жильё?
Например:
Милан
Дубай
Стамбул
Даты и гостей вы выберете внутри сервиса."""
CLARIFY_TEXT = "Назовите город, в котором ищем жильё."
COUNTRY_BY_CITY = {"стамбул":"turkey","анталья":"turkey","дубай":"uae","милан":"italy","рим":"italy","бангкок":"thailand","пхукет":"thailand"}


def parse_input(text: str):
    return {"city": text.strip().capitalize() or None}


def is_valid(data: dict) -> bool:
    return bool(data.get("city"))


def build_url(data: dict) -> str:
    city = data.get("city") or ""
    slug = COUNTRY_BY_CITY.get(city.lower())
    if slug:
        return with_marker(f"https://hotels.travelata.ru/{slug}")
    from urllib.parse import quote_plus
    return with_marker(f"https://hotels.travelata.ru/?query={quote_plus(city)}")


def summary(data: dict) -> str:
    city = data.get("city")
    if COUNTRY_BY_CITY.get((city or '').lower()):
        return f"✨ Ваше желание исполнено, мой господин.\n🏨 {city}\nОткрою подборку жилья по направлению.\nТочный город, даты и гостей выберите на странице."
    return f"✨ Ваше желание исполнено, мой господин.\n🏨 {city}\nОткрою страницу поиска отелей.\nВведите город ещё раз прямо на сайте — там более гибкий поиск."
