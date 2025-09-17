from services.Translator.src.translator import HebrewTranslator
from utils.kafka_pub_sub.sub.consumer import Consumer
from utils.kafka_pub_sub.pub.producer import Producer
from utils.logger.logger import Logger

logger = Logger().get_logger()

class Manager:
    def __init__(self, topic_pub, topic_sub):
        logger.info('init translator manager')
        self.translator = HebrewTranslator()
        self.producer = Producer()
        self.events = Consumer(topic_sub).consumer
        self.topic_pub = topic_pub

    def consume_and_publish_translated_text(self):
        for message in self.events:
            document = message.value
            doc_id = document['id']
            text = document['text']
            chat=document['chat']
            text = f"{chat}: \n{text}"
            logger.info(f"message:{document}")
            translated_text = self.translator.translate_with_fallback(text)['translated_text']
            self.publisher(doc_id, translated_text,chat)

    def publisher(self, doc_id, text,chat):
        message = {'id': doc_id, 'text': text,"chat":chat}
        self.producer.publish_message(topic=self.topic_pub, message=message)





