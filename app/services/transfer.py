from urllib.parse import quote_plus

from app.utils.telegram import send_message, send_inline
from app.keyboards import main_menu, result_inline
from app.storage import clear_state, save_result
from app.config import TRAVELPAYOUTS_MARKER, NEXT_ACTION_TEXT, WEBHOOK_BASE_URL


def _build_target() -> str:
    return f"https://kiwitaxi.com/?marker={TRAVELPAYOUTS_MARKER}"


def _build_masked_url(target_url: str) -> str:
    target = quote_plus(target_url)
    return f"{WEBHOOK_BASE_URL}/go/transfer/main?target={target}"


def start_transfer(chat_id: int, user_id: int):
    target_url = _build_target()
    url = _build_masked_url(target_url)

    result_text = (
        "✨ Ваше желание исполнено, мой господин.\n"
        "🚖 Трансфер открыт.\n"
        "Маршрут и время выберите на странице."
    )

    send_inline(chat_id, result_text, result_inline(url, "transfer"))
    send_message(chat_id, NEXT_ACTION_TEXT, reply_markup=main_menu())

    save_result(user_id, "transfer", "", "🚖 Трансфер", url)
    clear_state(user_id)
