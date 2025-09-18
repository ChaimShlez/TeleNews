from services.ManagerMessage.src.message_sender import MessageSender
from utils.kafka_pub_sub.sub.consumer import Consumer
from utils.kafka_pub_sub.pub.producer import Producer
from utils.logger.logger import Logger
from utils.mongodb.mongodb_service import MongoDBService
from utils.redis.redis_service import RedisService

logger = Logger.get_logger()

class ConsumerManager:

    def __init__(self, *topics_sub, connection, db_name: str, collection: str, url: str, host, port):
        self.events = Consumer(*topics_sub).consumer
        self.producer = Producer()
        self.mongo_service = MongoDBService(connection, db_name)
        self.collection = collection
        self.sender = MessageSender(url)
        self.redis_service = RedisService(host=host, port=port)

    def __get_users_id_from_mongo(self, topic: str, collection: str) -> list[dict]:
        query = {"topics": topic}
        fields = ["user_id"]
        results = self.mongo_service.find(collection, query=query, fields=fields, exclude_id=True)
        return results

    def consume_messages(self):
        logger.info("starting to consume")
        for message in self.events:
            users_id: list[dict] = self.__get_users_id_from_mongo(message.topic, self.collection)
            logger.info(f"Consuming message: id={message.value['id']}, chat={message.value['chat']}")

            file_data = self.redis_service.get_media_with_metadata(
                message.value['id'],
                message.value['chat']
            )

            if file_data:
                logger.info("Got file from Redis")
                # מחלץ גם את שם הקובץ אם שמרת אותו במטא-דאטה
                file_bytes = file_data.get("content")
                file_name = file_data.get("filename", f"{message.value['id']}.bin")
                response = self.sender.send_message(message.value, users_id, file_bytes, file_name)
            else:
                response = self.sender.send_message(message.value, users_id)

            logger.info(f"Response from sender: {response}")
