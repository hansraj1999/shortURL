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

    def normalize_url(self):
        """Normalize the URL by ensuring it has a protocol and trimming whitespace."""
        self.long_url = self.long_url.strip()
        if not self.long_url.startswith("http://") and not self.long_url.startswith("https://"):
            self.long_url = "http://" + self.long_url

    def handle(self) -> str:
        """
        Handle URL shortening.
        Always creates a new short URL to enable per-user tracking and analytics.
        """
        # Normalize the URL first
        self.normalize_url()
        
        # Always create a new short URL (no deduplication)
        # This allows tracking who created each URL and their individual hit counts
        counter = config.backend.increment_counter(LOCK_KEY)
        logger.info(f"Creating new short URL, counter: {counter}")
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
        logger.info(f"Created new short URL: {url_hash} for {self.long_url} by user {self.user_data['user_name']}")
        return url_hash
