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
        logger.info("Admin service initialized with persistent session support")

    def load_channels_from_mongo(self):

        try:
            approved_docs = self.mongodb.find(ADMIN_COLLECTION, fields=["channel"]) or []
            self.channels.clear()
            for doc in approved_docs:
                self.channels.add(doc["channel"])
            logger.info(f"Loaded {len(self.channels)} approved channels from MongoDB")
            return self.channels
        except Exception as e:
            logger.error(f"Failed to load channels from MongoDB: {e}")
            return set()

    async def init_default_channels(self):

        logger.info("Initializing default channels...")

        existing_channels = set(doc["channel"] for doc in self.mongodb.find(ADMIN_COLLECTION, fields=["channel"]) or [])

        for channel in CHANNELS:
            link = channel.get("link", channel)
            country = channel.get("country", "unknown")

            if link not in existing_channels:
                try:
                    self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": link, "country": country})
                    logger.info(f"Added default channel to MongoDB: {link}")
                except Exception as e:
                    logger.error(f"Failed to add channel {link} to MongoDB: {e}")

            try:
                await self.client(JoinChannelRequest(link))
                logger.info(f"Subscribed to default channel: {link}")
            except Exception as e:
                logger.error(f"Failed to subscribe to default channel {link}: {e}")

        self.load_channels_from_mongo()

    def add_channel_to_mongo(self, link: str, country: str = "unknown"):

        try:
            self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": link, "country": country})
            self.channels.add(link)
            logger.info(f"Channel added to MongoDB and internal list: {link}")
        except Exception as e:
            logger.error(f"Failed to add channel {link} to MongoDB: {e}")

    def blacklist_channels(self, channel: str, country: str = "unknown"):

        try:
            self.mongodb.insert_one(BLACKLIST_COLLECTION, {"channel": channel, "country": country})
            logger.info(f"Channel added to blacklist: {channel}")
        except Exception as e:
            logger.error(f"Failed to blacklist channel {channel}: {e}")

    async def approve_and_subscribe_channel(self, link: str, country: str = "unknown"):

        admin_channels = set(doc["channel"] for doc in self.mongodb.find(ADMIN_COLLECTION, fields=["channel"]) or [])
        blacklist_channels = set(
            doc["channel"] for doc in self.mongodb.find(BLACKLIST_COLLECTION, fields=["channel"]) or [])

        if link in admin_channels or link in blacklist_channels:
            logger.info(f"Channel {link} already processed (approved or blacklisted)")
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(CHECKER_URL, json={"link": link, "country": country})
                result = response.json()
        except Exception as e:
            logger.error(f"Failed to send channel to checker: {e}")
            return

        if result.get("approved")or True:
            try:

                await self.client(JoinChannelRequest(link))
                logger.info(f"Subscribed to new approved channel: {link}")

                self.add_channel_to_mongo(link, country)

            except Exception as e:
                logger.error(f"Failed to subscribe to {link}: {e}")
        else:
            logger.info(f"Channel {link} was not approved by checker")
            self.blacklist_channels(link, country)

    async def check_new_channels(self):

        try:
            check_docs = self.mongodb.find(CHECK_COLLECTION, query=None, fields=["link", "country"]) or []

            for doc in check_docs:
                link = doc["link"]
                country = doc.get("country", "unknown")
                await self.approve_and_subscribe_channel(link, country)

        except Exception as e:
            logger.error(f"Failed to check new channels: {e}")

    def get_approved_usernames(self):

        self.load_channels_from_mongo()

        approved_usernames = set()
        for link in self.channels:
            if link.startswith("https://t.me/"):
                username = link.split("/")[-1]
                approved_usernames.add(username)
            else:
                approved_usernames.add(link)

        return approved_usernames