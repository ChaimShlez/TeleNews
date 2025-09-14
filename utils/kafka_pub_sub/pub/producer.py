from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time

from utils.kafka_pub_sub.config import *
from utils.logger.logger import Logger

logger = Logger.get_logger()


class Producer:
    def __init__(self):
        logger.info('Producer start')
        logger.info('kafka_broker = {}'.format(KAFKA_BROKER))

        while True:
            try:
                logger.info("connecting to kafka")
                self.producer = KafkaProducer(
                    bootstrap_servers=[KAFKA_BROKER],
                    value_serializer=lambda x: json.dumps(x).encode('utf-8')
                )
                logger.info("Connected to Kafka!")
                break
            except NoBrokersAvailable:
                logger.info("Kafka broker not ready yet, waiting...")
                time.sleep(2)

    def publish_message(self, topic, message):
        logger.info(f"Sending to {topic}: {message}")
        self.producer.send(topic, message)
        logger.info("Message sent")
        self.producer.flush()
