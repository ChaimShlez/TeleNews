from services.Classifier.src.consumer_manager import ConsumerManager
from services.Classifier.src.config import *

consumer = ConsumerManager(TOPIC_SUB)


def main():
    consumer.consume_messages()


if __name__ == '__main__':
    main()
