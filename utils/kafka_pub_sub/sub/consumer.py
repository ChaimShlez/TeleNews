from kafka import KafkaConsumer
import json
import os

from utils.kafka_pub_sub.config import KAFKA_BROKER, GROUP_ID
from utils.logger.logger import Logger

logger = Logger.get_logger()


class Consumer:
    def __init__(self, topic):
        logger.info('Consumer init')
        logger.info("kafka_broker_topic: {}".format(topic))
        logger.info("kafka consumer connected")
        self.consumer = KafkaConsumer(
            topic,
            group_id=GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='earliest'
        )
