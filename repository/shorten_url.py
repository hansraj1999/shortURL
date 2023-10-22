from repository.encode import encode_url
import logging
from config import config
from constants import LOCK_KEY


logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, long_url, group_guid) -> None:
        self.long_url = long_url
        self.group_guid = group_guid

    def handle(self) -> str:
        """handle."""
        counter = config.backend.increment_counter(LOCK_KEY)
        logger.info(f"counter: {counter}")
        return encode_url(counter)
