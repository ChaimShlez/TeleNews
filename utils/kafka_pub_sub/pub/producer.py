from kafka import KafkaProducer,errors
from kafka.errors import NoBrokersAvailable
import json
import time
import os
from utils.logger.logger import Logger

logger = Logger.get_logger()


class Producer:
    def __init__(self):
        logger.info('Producer start')
        logger.info('kafka_broker = {}'.format(os.environ['KAFKA_BROKER']))
        kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")

        while True:
            try:
                logger.info("connecting to kafka")
                self.producer = KafkaProducer(
                    bootstrap_servers=[kafka_broker],
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
