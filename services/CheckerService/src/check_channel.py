from utils.logger.logger import Logger
logger = Logger.get_logger()

from services.CheckerService.src.config import *
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from googletrans import Translator
import re


translator = Translator()


class Check_channel:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.client = TelegramClient("my_session", self.api_id, self.api_hash)

    async def check_channel(self, link: str) -> bool:
        try:
            async with self.client:  # <-- כאן החיבור ייסגר אוטומטית בסיום
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
                        pass
                        # logger.info(f"Error leaving channel {link}: {e}")
                    return False

                return True

        except Exception as e:
            # logger.info(f"Error checking channel {link}: {e}")
            return False



import asyncio

if __name__ == '__main__':
    print("dwlefrnvj")
    ch = Check_channel()
    result = asyncio.run(ch.check_channel("amitsegal"))
    print(result)

