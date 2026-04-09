user_states = {}
last_requests = {}
subscribed_users = set()


def save_request(chat_id: int, payload: dict):
    last_requests[chat_id] = payload


def get_last_request(chat_id: int):
    return last_requests.get(chat_id)


def subscribe(chat_id: int):
    subscribed_users.add(chat_id)
