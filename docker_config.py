import redis
import logging.config
from constants import LOGGING_CONFIG
import os
from utils.database_manager import DatabaseManager
import string


class DockerConfig:
    REDIS_HOST = os.getenv("REDIS_HOST", "bithash_redis")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_USERNAME = os.getenv("REDIS_USERNAME", "default")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "default")
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    BASE62_ALPHABET = string.digits + string.ascii_letters
    BASE = 62

    MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "bithash_mongo")
    MONGO_CONNECTION_PORT = os.getenv("MONGO_CONNECTION_PORT", 27017)
    BASE_URL = os.getenv("BASE_URL", "https://shorturl.hansraj.me")  # Base URL for short URLs (must include protocol)
    logging.config.dictConfig(LOGGING_CONFIG)

    backend = DatabaseManager(
        REDIS_HOST,
        REDIS_PORT,
        REDIS_USERNAME,
        REDIS_PASSWORD,
        MONGO_CONNECTION_STRING,
    )
