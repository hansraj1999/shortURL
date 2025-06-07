from config import config
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, url_hash) -> None:
        self.url_hash = url_hash

    def handle(self) -> str:
        try:
            actual_url = config.backend.get_url_from_cache(self.url_hash)
            if actual_url:
                logger.info("found in cache")
                return actual_url
            else:
                logger.info("not found on cache fetching from disk")
                doc = config.backend.fetch_long_url(self.url_hash)
                if not doc:
                    raise HTTPException(
                        status_code=404,
                        detail={"message": "URL not found", "details": []},
                    )
                return doc["actual_url"]
        except Exception as e:
            logger.exception(e)
            raise HTTPException(
                status_code=500, detail={"message": str(e), "details": []}
            )
