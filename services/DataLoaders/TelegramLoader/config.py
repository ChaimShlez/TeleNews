import os
from dotenv import load_dotenv


load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

TOKEN = os.getenv('TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))
TOPIC = os.getenv("TOPIC","text-telegram")
REDIS_HOST = os.getenv("REDIS_HOST","redis")

CHANNELS = ["https://t.me/amitsegal","https://t.me/cnn_world_news",
            "https://t.me/TommyRobinsonNews","https://t.me/rian_ru",
            "https://t.me/indianexpress","https://t.me/voachinese",
            "https://t.me/Tasnimnews","https://t.me/tikvahethiopia",
            "https://t.me/TheBigBadShadow","https://t.me/INSIDER_UK_NEWS",
            "https://t.me/Sport_HUB_football","https://t.me/sportsdirect_eng"]


CONNECTION_STRING = os.getenv("CONNECTION_STRING" ,"mongodb://TeleNews:TeleNews@mongo:27017/TeleNews?authSource=admin")
DB_NAME = "TeleNews"

ADMIN_COLLECTION = "admin_channels"
CHECK_COLLECTION = "check_channels"
BLACKLIST_COLLECTION = "blacklist_channels"