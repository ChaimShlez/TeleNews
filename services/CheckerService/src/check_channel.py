
import os
import io
import asyncio
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
        logger.info("Initializing Telegram client with persistent session")

        session_dir = "/app/services/DataLoaders/TelegramLoader/sessions"
        os.makedirs(session_dir, exist_ok=True)

        session_path = os.path.join(session_dir, "telegram_session")
        self.client = TelegramClient(session_path, self.api_id, self.api_hash)


        self.producer = Producer()
        self.redis_service = RedisService(REDIS_HOST, int(os.getenv("REDIS_PORT", 6379)))

        # Admin service
        self.admin = Admin(self.client)
        self.approved_usernames = set()

    async def refresh_approved_channels(self):

        logger.info("Refreshing approved channels from MongoDB...")
        self.approved_usernames = self.admin.get_approved_usernames()
        logger.info(f"Approved channels refreshed: {len(self.approved_usernames)} channels")

        if logger.isEnabledFor(10):  # DEBUG level
            logger.debug(f"Approved usernames: {self.approved_usernames}")

    async def init_system(self):

        logger.info("Initializing system...")

        await self.client.start()
        logger.info("Telegram client connected")

        await self.admin.init_default_channels()

        await self.refresh_approved_channels()

        logger.info("System initialization completed")

    async def handle_message(self, event):

        try:
            sender = await event.get_chat()
            chat_title = getattr(sender, "title", str(sender.id))
            chat_username = getattr(sender, "username", None)
            msg_id = event.message.id

            if not chat_username or chat_username not in self.approved_usernames:
                logger.debug(f"Skipping non-approved channel: {chat_title} (@{chat_username})")
                return

            msg = event.message

            if msg.text:
                await self._handle_text_message(msg, chat_title, msg_id)

            elif msg.photo or msg.video or msg.audio or msg.document:
                await self._handle_media_message(msg, chat_title, msg_id)

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def _handle_text_message(self, msg, chat_title, msg_id):

        payload = {
            "chat": chat_title,
            "id": msg_id,
            "text": msg.text
        }

        logger.info(f"Publishing text message from '{chat_title}' (ID: {msg_id})")
        self.producer.publish_message(TOPIC, payload)

    async def _handle_media_message(self, msg, chat_title, msg_id):

        media_type = None
        if msg.photo:
            media_type = "photo"
        elif msg.video:
            media_type = "video"
        elif msg.audio:
            media_type = "audio"
        elif msg.document:
            media_type = "document"

        try:

            buffer = io.BytesIO()
            await msg.download_media(file=buffer)
            file_bytes = buffer.getvalue()

            logger.info(f"Saving {media_type} from '{chat_title}' (ID: {msg_id}) to Redis")
            self.redis_service.save_media_with_metadata(
                media_id=msg_id,
                title_id=chat_title,
                media_type=media_type,
                media_data=file_bytes
            )
        except Exception as e:
            logger.error(f"Error handling media message: {e}")

    async def periodic_channel_refresh(self):

        while True:
            try:
                await asyncio.sleep(300)
                await self.refresh_approved_channels()

                await self.admin.check_new_channels()

            except Exception as e:
                logger.error(f"Error in periodic refresh: {e}")

    def run(self):


        async def main():
            try:

                await self.init_system()

                @self.client.on(events.NewMessage)
                async def message_handler(event):
                    await self.handle_message(event)

                asyncio.create_task(self.periodic_channel_refresh())

                logger.info("Client started, listening to messages...")

                await self.client.run_until_disconnected()

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                raise

        asyncio.run(main())
