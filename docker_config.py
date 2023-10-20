from sqids import Sqids
import redis
import socket
import logging.config
from constants import LOGGING_CONFIG


class DockerConfig:
    REDIS_CONNECTION_STRING = "localhost"
    REDIS_PORT = "6379"
    # take from env
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    counter = 0  # take from zookeeper or sql or redis or mongodb
    sqids = Sqids(alphabet=allowed_chars)
    redis_connector = redis.Redis(
        host=REDIS_CONNECTION_STRING, port=REDIS_PORT, decode_responses=True)
    log_level = "DEBUG"  # take from Env var
    resource_attributes = {
        "service.name": "SHORTURL",
        "service.instance.id": socket.gethostname()
    }
    logging.config.dictConfig(LOGGING_CONFIG)
