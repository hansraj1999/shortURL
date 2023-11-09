from repository.encode import encode_url
import logging
from config import config
from constants import LOCK_KEY
import datetime

logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, long_url: str, group_guid, user_data) -> None:
        self.long_url = long_url
        self.group_guid = group_guid
        self.user_data = user_data

    def check_url_and_update_url(self):
        if self.long_url.startswith("http://") or self.long_url.startswith("https://"):
            return
        self.long_url = "http://" + self.long_url

    def handle(self) -> str:
        """handle."""
        counter = config.backend.increment_counter(LOCK_KEY)
        self.check_url_and_update_url()
        logger.info(f"counter: {counter}")
        url_hash = encode_url(counter)
        config.backend.insert_into_mongo(
            {
                "actual_url": self.long_url,
                "url_hash": url_hash,
                "user_name": self.user_data["user_name"],
                "user_id": self.user_data["user_id"],
                "created_at": str(datetime.datetime.now()),
                "updated_at": str(datetime.datetime.now()),
                "user_role": self.user_data["role"],
                "group_guid": self.group_guid,
            }
        )
        config.backend.add_url_in_cache(url_hash, self.long_url)
        return url_hash
