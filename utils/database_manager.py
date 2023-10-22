from utils.singleton import SingletonMeta
import redis
import pymongo


class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self, redis_connection_string, redis_port, mongo_connection_string):
        self.redis_connection = redis.StrictRedis(
            host=redis_connection_string, port=redis_port, decode_responses=True)
        self.mongo_connection = pymongo.MongoClient(mongo_connection_string)

    def increment_counter(self, lock_key):
        # distributed lock
        with self.redis_connection.lock(lock_key):
            counter = self.redis_connection.incr("url_counter")
            return counter
