from utils.singleton import SingletonMeta
import redis
import pymongo
from constants import DATABASE_NAME
from schemas import InsertUrl
import logging
import datetime
from typing import Optional
from pymongo.server_api import ServerApi
from models.url_model import INDEXES

logger = logging.getLogger(__name__)


class DatabaseManager(metaclass=SingletonMeta):
    def __init__(
        self,
        redis_host,
        redis_port,
        redis_username,
        redis_password,
        mongo_connection_string,
    ):
        self.redis_connection = redis.StrictRedis(
            host=redis_host,
            port=int(redis_port),
            decode_responses=True,
            username=redis_username,
            password=redis_password,
        )
        logger.info(f"MongoDB connection string: {mongo_connection_string}")
        self.mongo_connection = pymongo.MongoClient(
            mongo_connection_string, server_api=ServerApi("1")
        )[DATABASE_NAME]
        # Create indexes on initialization
        self.create_indexes()

    def increment_counter(self, lock_key):
        """
        Atomically increment the URL counter.
        Redis INCR is already atomic, so no lock is needed.
        The lock_key parameter is kept for backward compatibility but not used.
        """
        # Redis INCR is atomic, so no lock needed
        counter = self.redis_connection.incr("url_counter")
        return counter

    def insert_into_mongo(self, data: InsertUrl):
        logger.info("insert_into_mongo: %s", data)
        data = InsertUrl(**data).__dict__
        self.mongo_connection["urls"].insert_one(data)

    def fetch_long_url(self, url_hash: str):
        url_hash = str(url_hash)
        logger.info(f"fetch_long_url: {url_hash}")
        result = self.mongo_connection["urls"].find_one({"url_hash": url_hash})
        logger.info(f"fetch_long_url mongo result: {result}")
        if result:
            self.add_url_in_cache(url_hash, result["actual_url"], ttl=3600)
        return result

    def add_url_in_cache(self, key, value, ttl=3600):
        self.redis_connection.set(key, value)
        self.redis_connection.expire(key, ttl)
        logger.info(f"Added url in cache: {key}")

    def get_url_from_cache(self, key):
        long_url = self.redis_connection.get(key)
        return long_url

    def increment_redirect_count(self, url_hash: str):
        """Increment the redirect count and update last_redirected_at timestamp."""
        url_hash = str(url_hash)
        now = str(datetime.datetime.now())
        self.mongo_connection["urls"].update_one(
            {"url_hash": url_hash},
            {
                "$inc": {"hits": 1},
                "$set": {"last_redirected_at": now, "updated_at": now}
            }
        )
        logger.info(f"Incremented redirect count for {url_hash}")

    def get_total_urls_count(self, filter_by_user_id: Optional[int] = None, filter_by_user_name: Optional[str] = None):
        """Get total count of shortened URLs."""
        query = {}
        if filter_by_user_id:
            query["user_id"] = filter_by_user_id
        if filter_by_user_name:
            query["user_name"] = filter_by_user_name
        return self.mongo_connection["urls"].count_documents(query)

    def get_total_redirects_count(self, filter_by_user_id: Optional[int] = None, filter_by_user_name: Optional[str] = None):
        """Get total count of all redirects (sum of all hits)."""
        query = {}
        if filter_by_user_id:
            query["user_id"] = filter_by_user_id
        if filter_by_user_name:
            query["user_name"] = filter_by_user_name
        
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": "$hits"}}}
        ]
        result = list(self.mongo_connection["urls"].aggregate(pipeline))
        return result[0]["total"] if result else 0

    def get_analytics_data(
        self,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        filter_by_user_id: Optional[int] = None,
        filter_by_user_name: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ):
        """
        Get analytics data with sorting and filtering.
        sort_by options: 'hits', 'created_at', 'last_redirected_at'
        sort_order: 'asc' or 'desc'
        """
        query = {}
        if filter_by_user_id:
            query["user_id"] = filter_by_user_id
        if filter_by_user_name:
            query["user_name"] = filter_by_user_name

        # Map sort_by to MongoDB field names
        sort_mapping = {
            "hits": "hits",
            "redirect_count": "hits",
            "created_at": "created_at",
            "latest_shortened": "created_at",
            "last_redirected_at": "last_redirected_at",
            "latest_redirected": "last_redirected_at"
        }
        
        sort_field = sort_mapping.get(sort_by, "created_at")
        sort_direction = -1 if sort_order == "desc" else 1
        
        cursor = self.mongo_connection["urls"].find(query).sort(sort_field, sort_direction).skip(skip).limit(limit)
        
        results = []
        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        
        return results

    def create_indexes(self):
        """Create all necessary indexes for the urls collection."""
        collection = self.mongo_connection["urls"]
        
        for index_def in INDEXES:
            try:
                index_name = index_def["name"]
                keys = index_def["keys"]
                unique = index_def.get("unique", False)
                
                # Check if index already exists
                existing_indexes = collection.list_indexes()
                index_exists = any(idx.get("name") == index_name for idx in existing_indexes)
                
                if not index_exists:
                    collection.create_index(
                        keys,
                        unique=unique,
                        name=index_name,
                        background=True  # Create index in background to avoid blocking
                    )
                    logger.info(f"Created index: {index_name} on {keys}")
                else:
                    logger.debug(f"Index {index_name} already exists")
            except Exception as e:
                logger.error(f"Error creating index {index_def.get('name', 'unknown')}: {str(e)}")
        
        logger.info("Index creation process completed")

    def get_index_info(self):
        """Get information about all indexes on the urls collection."""
        collection = self.mongo_connection["urls"]
        indexes = list(collection.list_indexes())
        return indexes