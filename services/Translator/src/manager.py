from services.Translator.src.translator import HebrewTranslator
from utils.kafka.kafka_configuration import *


class Manager:
    def __init__(self):
        self.translator = HebrewTranslator()
        self.producer = produce_message()

    def main(self):
        topic = 'text-telegram'
        consumer = consume_messages(topic)
        for message in consumer:
            document = message.value
            doc_id = document['id']
            text = document['text']
            translated_text = self.translator.translate_with_fallback(text)
            self.producer(doc_id, translated_text)

    def producer(self, doc_id, text):
        topic = 'translated_text'
        event = {'id': doc_id, 'text': text}
        send_event(produce=self.producer, topic=topic, event=event)

if __name__ == '__main__':
    manager = Manager()
    manager.main()


