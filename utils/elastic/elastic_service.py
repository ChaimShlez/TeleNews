import time
from elasticsearch import Elasticsearch
from utils.elastic.config import ES_HOST


class ElasticConn:

    def __init__(self):
        self.es: Elasticsearch = Elasticsearch(f'http://{ES_HOST}:9200')
        self.__availability_check()

    def get_es(self) -> Elasticsearch:
        return self.es

    def __availability_check(self):
        while True:
            try:
                if self.es.ping():
                    return "Elasticsearch is ready"

            except ConnectionError:
                pass
            time.sleep(2)
