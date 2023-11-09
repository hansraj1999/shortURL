from utils.singleton import SingletonMeta
import redis
import pymongo
from constants import DATABASE_NAME
from schemas import InsertUrl
import logging

logger = logging.getLogger(__name__)


class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self, redis_connection_string, redis_port, mongo_connection_string, mongo_port):
        self.redis_connection = redis.StrictRedis(
            host=redis_connection_string, port=redis_port, decode_responses=True)
        self.mongo_connection = pymongo.MongoClient(
            mongo_connection_string, mongo_port)[DATABASE_NAME]

    def increment_counter(self, lock_key):
        # distributed lock
        with self.redis_connection.lock(lock_key):
            counter = self.redis_connection.incr("url_counter")
            return counter

    def insert_into_mongo(self, data: InsertUrl):
        logger.info("insert_into_mongo: %s", data)
        data = InsertUrl(**data).__dict__
        self.mongo_connection["urls"].insert_one(data)

    def fetch_long_url(self, url_hash: str):
        url_hash = str(url_hash)
        logger.info(f"fetch_long_url: {url_hash}")
        return self.mongo_connection["urls"].find_one({
            "url_hash": url_hash
        })

    def add_url_in_cache(self, key, value):
        self.redis_connection.set(key, value)
        logger.info(f"Added url in cache: {key}")

    def get_url_from_cache(self, key):
        long_url = self.redis_connection.get(key)
        return long_url
