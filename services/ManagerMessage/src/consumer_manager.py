from services.ManagerMessage.src.message_sender import MessageSender
from utils.kafka_pub_sub.sub.consumer import Consumer
from utils.kafka_pub_sub.pub.producer import Producer
from utils.mongodb.mongodb_service import MongoDBService
from utils.redis.redis_service import RedisService
from config import *

class ConsumerManager:

    def __init__(self, *topics_sub, connection, db_name: str, collection: str, url: str):
        self.events = Consumer(*topics_sub).consumer
        self.producer = Producer()
        self.mongo_service = MongoDBService(connection, db_name)
        self.collection = collection
        self.sender = MessageSender(url)
        self.redis_service = RedisService(host=HOST, port=REDIS_PORT)



    def __get_users_id_from_mongo(self, topic: str, collection: str)-> list[dict]:
        query = {"topics": topic}
        fields = ["user_id"]
        results = self.mongo_service.find(collection, query=query, fields=fields, exclude_id=True)
        return results



    def consume_messages(self):
        print("starting to consume")
        for message in self.events:
            users_id: list[dict] = self.__get_users_id_from_mongo(message.topic, self.collection)
            media_data = self.redis_service.get_media_with_metadata(message.value['id'],message.value['metadata']['chat'])
            response = self.sender.send_message(message.value, users_id,media_data)
            print(response)

