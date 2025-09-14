from services.DataLoaders.TelegramLoader.fetch_data import TelegramHandler
from utils.logger.logger import Logger

logger = Logger.get_logger()



telegram_handler = TelegramHandler()
logger.info("fetching data and sanding it to kafka")
telegram_handler.run()
