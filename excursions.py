from app.services.common import with_marker, slugify_ru

SERVICE_ID = "car"
BUTTON = "🚗 Аренда авто"
OPEN_TEXT = "🚗 Смотреть авто"
STEPS = ["car_q1"]
START_TEXT = """🧞 Слушаюсь и повинуюсь, мой господин.
В каком городе нужна машина?
Например:
Анталья
Тбилиси
Дубай
Даты и детали вы выберете внутри сервиса."""
CLARIFY_TEXT = "Назовите город аренды."
CITY_SLUGS = {"анталья":"antalya","тбилиси":"tbilisi","дубай":"dubai","стамбул":"istanbul"}


def parse_input(text: str):
    city = text.strip().capitalize() or None
    return {"city": city, "city_slug": CITY_SLUGS.get((city or '').lower(), slugify_ru(city or ''))}


def is_valid(data: dict) -> bool:
    return bool(data.get("city"))


def build_url(data: dict) -> str:
    return with_marker(f"https://localrent.com/cars/{data.get('city_slug')}")


def summary(data: dict) -> str:
    return f"✨ Ваше желание исполнено, мой господин.\n🚗 {data.get('city')}\nГород учтён в ссылке.\nДаты и тип автомобиля выберите на месте."
