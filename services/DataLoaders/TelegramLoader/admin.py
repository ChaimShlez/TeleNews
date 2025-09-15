from tabnanny import check

from utils.mongodb.mongodb_service import MongoDBService
from services.DataLoaders.TelegramLoader.config import *
from utils.logger.logger import Logger

# logger = Logger.get_logger()


class Admin:
    def __init__(self):
        self.mongodb = MongoDBService(CONNECTION_STRING,DB_NAME)
        self.channels = [channel for channel in CHANNELS["link"]]
    def admin_channels(self,channels=CHANNELS):
        if isinstance(list,channels):
            for channel in channels:
                self.mongodb.insert_one(ADMIN_COLLECTION,{"channel":channel})
        else:
            self.mongodb.insert_one(ADMIN_COLLECTION, {"channel": channels})

        self.channels.add(channels)
        # logger.info("default channel added")
    def check_channels(self,channel: str):

        admin_channels = set()
        blacklist_channels = set()
        check_channels = set()
        admin_mongo = self.mongodb.find(ADMIN_COLLECTION,query=None,fields=["channel"])
        if admin_mongo:
            for channel,name in admin_mongo.items():
                admin_channels.add(name)

        blacklist_mongo = self.mongodb.find(BLACKLIST_COLLECTION, query=None, fields=["channel"])
        if blacklist_mongo:
            for channel, name in blacklist_mongo.items():
                blacklist_channels.add(name)

        check_mongo = self.mongodb.find(CHECK_COLLECTION, query=None, fields=["link"])
        if check_mongo:
            for channel, name in check_mongo.items():
                check_channels.add(name)


        check_channels = check_channels - admin_channels - blacklist_channels

        for channel in check_channels:
            """
            תכניס פה את הלוגיקה של הסקור
            


            # logger.info("validating the channel contents")
            #if score:
                # logger.info("channel passed the validation")
                self.admin_channels(channel)
            else:
                # logger.info("channel passed to blacklist content is not proper")
                self.blacklist_channel(channel)
            """

    def blacklist_channels(self,channel:str):

        pass

        """
        # logger.info("saving bad channel in mongodb in the blacklist")
        self.mongodb.insert_one(BLACKLIST_COLLECTION,{"channel":channel})
        
        """
    def get_channels(self) -> set:
        return self.channels

