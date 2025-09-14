import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

TOKEN = os.getenv('TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))

CHANNELS = ["https://t.me/amitsegal","https://t.me/cnn_world_news",
            "https://t.me/TommyRobinsonNews","https://t.me/rian_ru",
            "https://t.me/indianexpress","https://t.me/voachinese",
            "https://t.me/Tasnimnews","https://t.me/tikvahethiopia",
            "https://t.me/TheBigBadShadow","https://t.me/INSIDER_UK_NEWS",
            "https://t.me/Sport_HUB_football","https://t.me/sportsdirect_eng"]