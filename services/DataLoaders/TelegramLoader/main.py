from services.DataLoaders.TelegramLoader.fetch_data import TelegramHandler
from services.DataLoaders.TelegramLoader.admin import Admin
from utils.logger.logger import Logger
import asyncio

logger = Logger.get_logger()

try:

    telegram_handler = TelegramHandler()
    logger.info("Initializing default channels...")


    admin = Admin(telegram_handler.client)


    asyncio.run(admin.init_default_channels())

    logger.info("Fetching data and sending it to Kafka")
    telegram_handler.run()

except Exception as e:
    logger.error(e)
