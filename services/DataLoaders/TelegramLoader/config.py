import os
from dotenv import load_dotenv


load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
CHECKER_URL=os.getenv("CHECKER_URL","http://localhost:8001/check")

TOKEN = os.getenv('TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))
TOPIC = os.getenv("TOPIC","text-telegram")
REDIS_HOST = os.getenv("REDIS_HOST","redis")

CHANNELS = [{"link":"https://t.me/amitsegal","country":"Israel"},
            {"link":"https://t.me/cnn_world_news","country":"USA"},
            {"link":"https://t.me/TommyRobinsonNews","country":"England"},
            {"link":"https://t.me/rian_ru","country":"Russia"},
            {"link":"https://t.me/indianexpress","country":"India"},
            {"link":"https://t.me/voachinese","country":"China"},
            {"link":"https://t.me/France24_fr","country":"France"},
            {"link":"https://t.me/A3Noticias","country":"Spain"},
            {"link":"httpa://t.me/sapiens3","country":"Italy"},
            {"link":"https://t.me/theriotimes","country":"Brazil"},
            {"link":"https://t.me/sepahcybery","country":"Iran"},
            {"link":"https://t.me/solcugazete","country":"Turkey"},
            {"link":"https://t.me/LaColombiaOscuraa","country":"Spain"},
            {"link":"https://t.me/MILITSIYA_UZB","country":"Uzbekistan"},
            {"link":"https://t.me/oa_channel","country":"Cambodia"},
            {"link":"https://t.me/markuskrall_abb","country":"Germany"}]


CONNECTION_STRING = os.getenv("CONNECTION_STRING" ,"mongodb://TeleNews:TeleNews@mongo:27017/TeleNews?authSource=admin")
DB_NAME = "TeleNews"

ADMIN_COLLECTION = "admin_channels"
CHECK_COLLECTION = "check_channels"
BLACKLIST_COLLECTION = "blacklist_channels"