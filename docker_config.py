from sqids import Sqids
import redis
import logging.config
from constants import LOGGING_CONFIG
import os
from utils.database_manager import DatabaseManager


class DockerConfig:
    REDIS_CONNECTION_STRING =  os.getenv("REDIS_CONNECTION_STRING", "bithash_redis")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    sqids = Sqids(alphabet=allowed_chars)
    MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "bithash_mongo")
    MONGO_CONNECTION_PORT = os.getenv("MONGO_CONNECTION_PORT", 27017)
    logging.config.dictConfig(LOGGING_CONFIG)

    backend = DatabaseManager(REDIS_CONNECTION_STRING, REDIS_PORT, MONGO_CONNECTION_STRING, MONGO_CONNECTION_PORT)
