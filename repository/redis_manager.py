from constants import LOCK_KEY
from config import config


def increment_counter():
    # distributed lock
    with config.redis_connector.lock(LOCK_KEY):
        counter = config.redis_connector.incr("url_counter")
        return counter
