from utils.singleton import SingletonMeta
import redis
import pymongo
from constants import DATABASE_NAME
from schemas import InsertUrl


class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self, redis_connection_string, redis_port, mongo_connection_string, mongo_port):
        self.redis_connection = redis.StrictRedis(
            host=redis_connection_string, port=redis_port, decode_responses=True)
        self.mongo_connection = pymongo.MongoClient(mongo_connection_string, mongo_port)[DATABASE_NAME]

    def increment_counter(self, lock_key):
        # distributed lock
        with self.redis_connection.lock(lock_key):
            counter = self.redis_connection.incr("url_counter")
            return counter

    def insert_into_mongo(self, data: InsertUrl):
        print(data)
        InsertUrl(**data)
        self.mongo_connection["urls"].insert_one(data)