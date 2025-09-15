import os
from dotenv import load_dotenv


load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

TOKEN = os.getenv('TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))
TOPIC = os.getenv("TOPIC","text-telegram")
REDIS_HOST = os.getenv("REDIS_HOST","redis")

CHANNELS = [{"link":"https://t.me/amitsegal","country":"Israel"},
            {"link":"https://t.me/cnn_world_news","country":"USA"},
            {"link":"https://t.me/TommyRobinsonNews","country":"England"},
            {"link":"https://t.me/rian_ru","country":"Russia"},
            {"link":"https://t.me/indianexpress","country":"India"},
            {"link":"https://t.me/voachinese","country":"China"}]


CONNECTION_STRING = os.getenv("CONNECTION_STRING" ,"mongodb://TeleNews:TeleNews@mongo:27017/TeleNews?authSource=admin")
DB_NAME = "TeleNews"

ADMIN_COLLECTION = "admin_channels"
CHECK_COLLECTION = "check_channels"
BLACKLIST_COLLECTION = "blacklist_channels"