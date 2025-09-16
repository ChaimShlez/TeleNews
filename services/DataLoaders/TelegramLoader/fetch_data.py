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
        self.redis_service = RedisService(REDIS_HOST, int(os.getenv("REDIS_PORT", 6379)))

        # Admin service
        self.admin = Admin(self.client)
        self.approved_usernames = set()

    async def init_approved_channels(self):
        await self.admin.init_default_channels()
        self.approved_usernames.clear()
        for link in self.admin.channels:
            if link.startswith("https://t.me/"):
                username = link.split("/")[-1]
                self.approved_usernames.add(username)
            else:
                self.approved_usernames.add(link)
        logger.info(f"Approved channels loaded: {self.approved_usernames}")

    async def handle_message(self, event):
        sender = await event.get_chat()
        chat_title = getattr(sender, "title", str(sender.id))
        chat_username = getattr(sender, "username", None)
        msg_id = event.message.id

        if not chat_username or chat_username not in self.approved_usernames:
            logger.info(f"Skipping non-approved channel: {chat_title}")
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

            self.redis_service.save_media_with_metadata(
                media_id=msg_id,
                title_id=chat_title,
                media_type=media_type,
                media_data=file_bytes
            )

    def run(self):
        logger.info("Listening to messages from all subscribed channels")

        @self.client.on(events.NewMessage)
        async def wrapper(event):
            await self.handle_message(event)

        import asyncio
        asyncio.get_event_loop().run_until_complete(self.init_approved_channels())

        self.client.start()
        self.client.run_until_disconnected()
