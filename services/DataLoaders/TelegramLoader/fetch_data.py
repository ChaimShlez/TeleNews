from telethon import TelegramClient, events
from services.DataLoaders.TelegramLoader.config import *
from utils.kafka_pub_sub.pub.producer import Producer
import io
from utils.logger.logger import Logger
from utils.redis.redis_service import RedisService
from services.DataLoaders.TelegramLoader.admin import Admin

logger = Logger.get_logger()


class TelegramHandler:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        logger.info("initialize telegram client")
        self.client = TelegramClient("my_session", self.api_id, self.api_hash)
        self.producer = Producer()
        self.redis_service = RedisService(REDIS_HOST, int(os.getenv("REDIS_PORT")))

    async def handle_message(self, event):
        logger.info("catching message")
        sender = await event.get_chat()
        msg = event.message
        chat_title = sender.title
        msg_id = msg.id

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
            path = await msg.download_media(file=io.BytesIO())
            with open(path, "rb") as f:
                file_bytes = f.read()

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
        logger.info('listening forever to new messages')
        @self.client.on(events.NewMessage(chats=Admin().get_channels()))
        async def wrapper(event):
            await self.handle_message(event)

        self.client.start()
        self.client.run_until_disconnected()


if __name__ == "__main__":
    bot = TelegramHandler()
    bot.run()
