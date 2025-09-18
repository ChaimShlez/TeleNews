import requests
from utils.logger.logger import Logger

logger = Logger.get_logger()

class MessageSender:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def fit_message(message: dict, users: list[dict]) -> dict:
        combined_text = f"[{message.get('chat', '')}] {message.get('text', '')}"
        return {
            "message": combined_text,
            "users_id": ",".join(str(user["user_id"]) for user in users)
        }

    def send_message(self, message: dict, users: list[dict], file_bytes=None, file_name=None) -> dict:
        try:
            data = MessageSender.fit_message(message, users)
            files = None
            if file_bytes:
                files = {"file": (file_name or "file.bin", file_bytes)}

            logger.info(f"Sending to {self.url}, data={data}, file={'yes' if files else 'no'}")
            resp = requests.post(self.url, data=data, files=files)
            resp.raise_for_status()
            return resp.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return {"error": "Request failed", "details": str(e)}
