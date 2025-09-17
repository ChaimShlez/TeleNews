import requests

from utils.logger.logger import Logger

logger = Logger.get_logger()


class MessageSender:
    def __init__(self, url: str):
        self.url = url


    @staticmethod
    def fit_message(message: dict, users: list[dict]) -> list[tuple[str, str]]:

        combined_text = f"[{message.get('chat', '')}] {message.get('text', '')}"
        data = [
            ('message', combined_text)
        ]
        for user in users:
            data.append(('users_id', str(user["user_id"])))
        return data



    def send_message(self, message: dict, users: list[dict], files=None) -> dict:
        try:
            data = MessageSender.fit_message(message, users)
            logger.info(data)
            resp = requests.post(self.url, data=data, files=files)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return {"error": "Request failed", "details": str(e)}
        except ValueError as e:
            logger.error(f"JSON decode error: {e}")
            return {"error": "Invalid JSON response", "details": str(e)}

