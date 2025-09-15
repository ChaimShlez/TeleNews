import os

TOKEN_BOT = os.getenv("TOKEN_BOT" ,"8245597686:AAHyegxSPqLeEkajpvelrNYK7eQ4iLd_zRg")

CONNECTION_STRING = os.getenv("CONNECTION_STRING" ,"mongodb://TeleNews:TeleNews@mongo:27017/TeleNews?authSource=admin")
DB_NAME = "TeleNews"

COLLECTION_NAME = "users_preferences"

CHANNEL_COLLECTION_NAME = os.getenv("CHANNEL_COLLECTION_NAME" , "check_channels")