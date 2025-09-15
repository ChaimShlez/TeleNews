from services.ManagerMessage.src.consumer_manager import ConsumerManager
# from services.ManagerMessage.src.config import *

consumer = ConsumerManager()


def main():
    consumer.consume_messages()


if __name__ == '__main__':
    main()