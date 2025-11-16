from repository.encode import encode_url
from repository.qr_code_generator import generate_qr_code
import logging
from config import config
from constants import LOCK_KEY
import datetime

logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, long_url: str, group_guid, user_data, qr_code: bool = False) -> None:
        self.long_url = long_url
        self.group_guid = group_guid
        self.user_data = user_data
        self.qr_code = qr_code

    def normalize_url(self):
        """Normalize the URL by ensuring it has a protocol and trimming whitespace."""
        self.long_url = self.long_url.strip()
        if not self.long_url.startswith("http://") and not self.long_url.startswith("https://"):
            self.long_url = "http://" + self.long_url

    def handle(self) -> dict:
        """
        Handle URL shortening.
        Always creates a new short URL to enable per-user tracking and analytics.
        
        Returns:
            dict with 'short_url' and optionally 'qr_code' (base64 encoded)
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
        
        # Build response
        response = {"short_url": url_hash}
        
        # Generate QR code if requested
        if self.qr_code:
            try:
                # Build full short URL
                full_short_url = f"{config.BASE_URL}/{url_hash}"
                qr_code_base64 = generate_qr_code(full_short_url)
                response["qr_code"] = qr_code_base64
                logger.info(f"Generated QR code for short URL: {url_hash}")
            except Exception as e:
                logger.error(f"Failed to generate QR code: {str(e)}")
                # Don't fail the request if QR code generation fails
                response["qr_code"] = None
        
        return response
