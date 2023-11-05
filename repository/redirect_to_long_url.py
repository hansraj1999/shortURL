from config import config
from fastapi import HTTPException

class Handler:
    def __init__(self, url_hash) -> None:
        self.url_hash = url_hash
    
    def handle(self) -> str:
        doc = config.backend.fetch_long_url(self.url_hash)
        if not doc:
            raise HTTPException(status_code=404, detail={
                            "message": "URL not found", "details": []})
        return doc["actual_url"]