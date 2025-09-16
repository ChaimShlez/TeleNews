from utils.logger.logger import Logger
logger = Logger.get_logger()
from services.CheckerService.src.config import *
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from transformers import pipeline
from googletrans import Translator
import asyncio
import re

classifier = pipeline(
    "text-classification",
    model="unitary/unbiased-toxic-roberta",
    device=-1  # CPU
)

translator = Translator()


class Check_channel:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.client = TelegramClient("my_session", self.api_id, self.api_hash)

    async def check_channel(self, link: str) -> bool:
        try:
            await self.client.start()
            await self.client(JoinChannelRequest(link))

            messages = await self.client.get_messages(link, limit=20)
            texts = []
            for msg in messages:
                if msg.message:
                    texts.append(msg.message)
                if hasattr(msg, "media") and getattr(msg.media, "caption", None):
                    texts.append(msg.media.caption)

            if await self._contains_bad_content(texts, link):
                try:
                    await self.client(LeaveChannelRequest(link))
                except Exception as e:
                    logger.info(f"Error leaving channel {link}: {e}")
                return False

            return True

        except Exception as e:
            logger.info(f"Error checking channel {link}: {e}")
            return False

    async def _contains_bad_content(self, messages: list[str], link: str) -> bool:
        for msg in messages:
            try:
                text_en = translator.translate(msg, dest="en").text
            except Exception as e:
                logger.info(f"Translation error for channel {link}: {e}")
                continue

            for category, keywords in CATEGORIES.items():
                if any(re.search(rf"\b{kw}\b", text_en, re.IGNORECASE) for kw in keywords):
                    logger.info(f"Channel flagged in category '{category}': {link}")
                    return True

            results = classifier(text_en)
            for item in results:
                label = item["label"].lower()
                score = item["score"]
                if label == "nsfw" and score > 0.5:
                    logger.info(f"Channel flagged by model as NSFW: {link}")
                    return True

        return False

