import requests


class MessageSender:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def fit_message(message: str, users: list[dict]) -> list[tuple[str, str]]:
        data = [('message', message)]
        for user in users:
            data.append(('users_id', str(user["user_id"])))
        return data



