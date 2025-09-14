import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

TOKEN = os.getenv('TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))

CHANNELS = ["https://t.me/amitsegal","https://t.me/cnn_world_news"]