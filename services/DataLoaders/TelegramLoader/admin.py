from utils.mongodb.mongodb_service import MongoDBService
from services.DataLoaders.TelegramLoader.config import *
from utils.logger.logger import Logger
from telethon.tl.functions.channels import JoinChannelRequest

logger = Logger.get_logger()


class Admin:
    def __init__(self, telegram_client):
        self.client = telegram_client  # TelegramClient עבור מנוי לערוצים
        self.mongodb = MongoDBService(CONNECTION_STRING, DB_NAME)
        self.channels = set()  # שמירה פנימית של הערוצים

    def admin_channels(self, channels=CHANNELS):
        """ מוסיף ערוצים כברירת מחדל או חדשים למונגו ולסט פנימי """
        if isinstance(channels, list):
            for channel in channels:
                # שמירה במונגו
                self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": channel.get("link", channel), "country": channel.get("country", "unknown")})
                # שמירה בסט פנימי
                self.channels.add(channel.get("link", channel))
        else:
            self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": channels, "country": "unknown"})
            self.channels.add(channels)

        logger.info(f"Admin channel(s) added: {self.channels}")

    def blacklist_channels(self, channel: str, country: str = "unknown"):
        """ מוסיף ערוץ ל־Blacklist """
        logger.info(f"Adding bad channel to Blacklist: {channel}")
        self.mongodb.insert_one(BLACKLIST_COLLECTION, {"channel": channel, "country": country})

    async def approve_and_subscribe_channel(self, link, country="unknown"):
        """ בודק ומצטרף לערוץ חדש במידה והוא ראוי """
        admin_channels = set(doc["channel"] for doc in self.mongodb.find(ADMIN_COLLECTION, fields=["channel"]) or [])
        blacklist_channels = set(doc["channel"] for doc in self.mongodb.find(BLACKLIST_COLLECTION, fields=["channel"]) or [])

        if link in admin_channels or link in blacklist_channels:
            return  # כבר קיים או שחור

        # כאן אפשר להכניס לוגיקה של בדיקה אם הערוץ ראוי
        score = True  # בדוגמה כל ערוץ עובר
        if score:
            try:
                await self.client(JoinChannelRequest(link))
                logger.info(f"Subscribed to new approved channel: {link}")
                self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": link, "country": country})
                self.channels.add(link)  # גם בסט פנימי
            except Exception as e:
                logger.error(f"Failed to subscribe to {link}: {e}")
        else:
            self.blacklist_channels(link, country)

    def check_new_channels(self):
        """
        מחזיר רשימת ערוצים חדשים מה-CHECK_COLLECTION.
        כל ערוץ עובר approval אוטומטית עם מנוי אם score OK.
        """
        check_mongo = self.mongodb.find(CHECK_COLLECTION, query=None, fields=["link", "country"]) or []
        for doc in check_mongo:
            link = doc["link"]
            country = doc.get("country", "unknown")
            import asyncio
            asyncio.create_task(self.approve_and_subscribe_channel(link, country))
