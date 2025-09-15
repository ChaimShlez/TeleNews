import os
import io
from telethon import TelegramClient, events
from services.DataLoaders.TelegramLoader.config import *
from utils.kafka_pub_sub.pub.producer import Producer
from utils.logger.logger import Logger
from utils.redis.redis_service import RedisService
from services.DataLoaders.TelegramLoader.admin import Admin

logger = Logger.get_logger()


class TelegramHandler:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        logger.info("Initializing Telegram client")
        self.client = TelegramClient("my_session", self.api_id, self.api_hash)
        self.producer = Producer()
        self.redis_service = RedisService(REDIS_HOST, int(os.getenv("REDIS_PORT")))
        self.blacklist = set()

        self.admin = Admin(self.client)

    async def handle_message(self, event):
        sender = await event.get_chat()
        chat_title = getattr(sender, "title", str(sender.id))
        msg_id = event.message.id

        # סינון לפי Blacklist
        if getattr(sender, "username", None) in self.blacklist or getattr(sender, "id", None) in self.blacklist:
            logger.info(f"Skipping blacklisted channel: {chat_title}")
            return

        msg = event.message


        if msg.text:
            payload = {
                "chat": chat_title,
                "id": msg_id,
                "text": msg.text
            }
            self.producer.publish_message(TOPIC, payload)

        elif msg.photo or msg.video or msg.audio or msg.document:
            media_type = None
            if msg.photo:
                media_type = "photo"
            elif msg.video:
                media_type = "video"
            elif msg.audio:
                media_type = "audio"
            elif msg.document:
                media_type = "document"

            buffer = io.BytesIO()
            await msg.download_media(file=buffer)
            file_bytes = buffer.getvalue()

            metadata = {
                "chat": chat_title,
                "media_type": media_type,
            }

            self.redis_service.save_media_with_metadata(
                media_id=msg_id,
                media_data=file_bytes,
                metadata=metadata
            )

    def run(self):
        logger.info('Listening to messages from all subscribed channels')

        @self.client.on(events.NewMessage)
        async def wrapper(event):
            await self.handle_message(event)

        self.client.start()
        self.client.run_until_disconnected()
