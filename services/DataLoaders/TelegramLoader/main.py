from services.DataLoaders.TelegramLoader.fetch_data import TelegramHandler
from utils.logger.logger import Logger

logger = Logger.get_logger()


try:
    telegram_handler = TelegramHandler()
    logger.info("fetching data and sanding it to kafka")
    telegram_handler.run()
except Exception as e:
    logger.error(e)
