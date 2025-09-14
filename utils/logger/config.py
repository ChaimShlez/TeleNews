import os

ELASTICSEARCH_HOSTS = os.getenv("ELASTICSEARCH_HOSTS","http://elasticsearch:9200")
NAME = "teleNews"
INDEX = os.getenv("LOGS")