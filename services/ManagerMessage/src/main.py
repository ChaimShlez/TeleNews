from services.ManagerMessage.src.consumer_manager import ConsumerManager
from services.ManagerMessage.src.config import *
from utils.topics.topics import *

topics = [v for k, v in TOPICS.items()]
consumer = ConsumerManager(*topics, connection=CONNECTION, db_name=DB_NAME, collection=COLLECTION, url=URL, host=HOST, port=REDIS_PORT)


def main():
    consumer.consume_messages()


if __name__ == '__main__':
    main()
