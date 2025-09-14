from utils.kafka.kafka_consumer import Consumer
from utils.kafka.kafka_producer import Producer
from services.Classifier.src.text_classifier import TextClassifier


class ConsumerManager:

    def __init__(self, *topics_sub):
        self.classifier = TextClassifier()
        self.events = Consumer(*topics_sub).consumer
        self.producer = Producer()

    def __classifier(self, text: str):
        return self.classifier.classify_text(text)


    def consume_messages(self):
        print("starting to consume")
        for messages in self.events:
            res = self.__classifier(messages.value['text'])
            # Sending massage to kafka by topic
            self.producer.send_event(res['category'], messages.value)
