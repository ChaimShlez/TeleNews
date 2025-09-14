from transelator.src.translator import HebrewTranslator
from utils.kafka.kafka_configuration import *


class Manager:
    def __init__(self):
        self.translator = HebrewTranslator()
        self.producer = produce_message()

    def main(self):
        topic = 'text-telegram'
        consumer = consume_messages(topic)
        for message in consumer:
            event = message.value
            translated_text = self.translator.translate_with_fallback(event['text'])
            self.producer(event['id'], translated_text)

    def producer(self, doc_id, text):
        topic = 'translated_text'
        event = {'id': doc_id, 'text': text}
        send_event(self.producer, topic, event)



