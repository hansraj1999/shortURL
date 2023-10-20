from repository.encode import encode_url
from repository.redis_manager import increment_counter
import logging

logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, long_url, group_guid) -> None:
        self.long_url = long_url
        self.group_guid = group_guid

    def handle(self):
        counter = increment_counter()
        print("counter_handle", counter)
        return encode_url(counter)
