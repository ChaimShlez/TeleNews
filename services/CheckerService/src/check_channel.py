from utils.logger.logger import Logger
logger = Logger.get_logger()
from services.CheckerService.src.config import *
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from transformers import pipeline
from googletrans import Translator

classifier = pipeline(
    "text-classification",
    model="unitary/unbiased-toxic-roberta",
    device=-1
)

translator = Translator()
TARGET_LABELS = ["sexual"]




class Check_channel:
    def __init__(self):

        self.api_id = API_ID
        self.api_hash = API_HASH
        logger.info("Initializing Telegram client")
        self.client = TelegramClient("my_session", self.api_id, self.api_hash)



    async def check_channel(self, link: str) -> bool:

        try:
            await self.client(JoinChannelRequest(link))
            logger.info(f"Successfully joined channel: {link}")

            messages = await self.client.get_messages(link, limit=5)
            texts = [msg.message  for msg in messages if msg.message]

            if self._contains_bad_content(texts):
                logger.info(f"Channel {link} contains inappropriate content")
                try:
                    await self.client(LeaveChannelRequest(link))
                    logger.info(f"Left channel {link} due to inappropriate content")
                except Exception as e:
                    logger.error(f"Failed to leave channel {link}: {e}")
                return False

            logger.info(f"Channel {link} passed content check")
            return True

        except Exception as e:
            logger.error(f"Failed to join or check channel {link}: {e}")
            return False

    def _contains_bad_content(self, messages: list[str]) -> bool:
        for msg in messages:
            text_en = translator.translate(msg, dest="en").text

            results = classifier(text_en)
            for item in results:
                label = item["label"].lower()
                score = item["score"]
                if any(target in label for target in TARGET_LABELS) and score > 0.5:
                    logger.info(f"Text flagged: {label} ({score})")
                    return True
        return False

