from utils.mongodb.mongodb_service import MongoDBService
from services.DataLoaders.TelegramLoader.config import *
from utils.logger.logger import Logger

# logger = Logger.get_logger()


class Admin:
    def __init__(self):
        self.mongodb = MongoDBService(CONNECTION_STRING,DB_NAME)
    def admin_channels(self):
        self.mongodb.insert_one(ADMIN_COLLECTION,{"channels":CHANNELS})
        # logger.info("default channel added")
    def check_channels(self,channel: str):
        pass
        """
        
        check channels are !!
        
        logger.info("validating the channel contents")
        #if score:
            logger.info("channel passed the validation")
            self.mongodb.insert_one(CHECK_COLLECTION,{"channel":channel})
        else:
            logger.info("channel passed to blacklist content is not proper") 
            self.blacklist_channel(channel)
        """





    def blacklist_channels(self,channel:str):

        pass

        """
        logger.info("saving bad channel in mongodb in the blacklist")
        self.mongodb.insert_one(BLACKLIST_COLLECTION,{"channel":channel})
        
        """

