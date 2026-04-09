from app.services.common import with_marker

SERVICE_ID = "transfer"
BUTTON = "🚖 Эх, прокачу"
OPEN_TEXT = "🚖 Открыть трансфер"
STEPS = []


def parse_input(text: str):
    return {}


def is_valid(data: dict) -> bool:
    return True


def build_url(data: dict) -> str:
    return with_marker("https://kiwitaxi.com/")


def summary(data: dict) -> str:
    return "✨ Ваше желание исполнено, мой господин.\n🚖 Трансфер открыт.\nМаршрут и время выберите на странице."
