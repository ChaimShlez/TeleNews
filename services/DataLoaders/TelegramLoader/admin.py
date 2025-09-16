from utils.mongodb.mongodb_service import MongoDBService
from services.DataLoaders.TelegramLoader.config import *
from utils.logger.logger import Logger
from telethon.tl.functions.channels import JoinChannelRequest
import httpx
import asyncio

logger = Logger.get_logger()


class Admin:
    def __init__(self, telegram_client):
        self.client = telegram_client
        self.mongodb = MongoDBService(CONNECTION_STRING, DB_NAME)
        self.channels = set()

    async def init_default_channels(self):

        for channel in CHANNELS:
            link = channel.get("link", channel)
            country = channel.get("country", "unknown")
            try:
                await self.client(JoinChannelRequest(link))
                logger.info(f"Subscribed to default channel: {link}")
                self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": link, "country": country})
                self.channels.add(link)
            except Exception as e:
                logger.error(f"Failed to subscribe to default channel {link}: {e}")

    def blacklist_channels(self, channel: str, country: str = "unknown"):

        logger.info(f"Adding bad channel to Blacklist: {channel}")
        self.mongodb.insert_one(BLACKLIST_COLLECTION, {"channel": channel, "country": country})

    async def approve_and_subscribe_channel(self, link, country="unknown"):

        admin_channels = set(doc["channel"] for doc in self.mongodb.find(ADMIN_COLLECTION, fields=["channel"]) or [])
        blacklist_channels = set(doc["channel"] for doc in self.mongodb.find(BLACKLIST_COLLECTION, fields=["channel"]) or [])

        if link in admin_channels or link in blacklist_channels:
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(CHECKER_URL,
                                             json={"link": link, "country": country})
                result = response.json()
            except Exception as e:

                logger.error(f"Failed to send channel to checker: {e}")
                return

        if result.get("approved"):

            try:
                await self.client(JoinChannelRequest(link))
                logger.info(f"Subscribed to new approved channel: {link}")
                self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": link, "country": country})
                self.channels.add(link)
            except Exception as e:
                logger.error(f"Failed to subscribe to {link}: {e}")
        else:
            self.blacklist_channels(link, country)

    def check_new_channels(self):

        check_mongo = self.mongodb.find(CHECK_COLLECTION, query=None, fields=["link", "country"]) or []
        for doc in check_mongo:
            link = doc["link"]
            country = doc.get("country", "unknown")
            import asyncio
            asyncio.create_task(self.approve_and_subscribe_channel(link, country))
