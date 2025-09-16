from utils.kafka_pub_sub.sub.consumer import Consumer
from utils.kafka_pub_sub.pub.producer import Producer
from services.Classifier.src.text_classifier import TextClassifier
from utils.logger.logger import Logger

logger = Logger.get_logger()


class ConsumerManager:

    def __init__(self, *topics_sub):
        self.classifier = TextClassifier()
        self.events = Consumer(*topics_sub).consumer
        self.producer = Producer()

    def __classifier(self, text: str):
        return self.classifier.classify_text(text)


    def consume_messages(self):
        logger.info("starting to consume")
        for messages in self.events:
            res = self.__classifier(messages.value['text'])
            # Sending massage to kafka by topic
            self.producer.publish_message(res['category'], messages.value)
