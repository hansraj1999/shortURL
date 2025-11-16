"""
Migration script to create database indexes.

This script can be run independently to create/update indexes in MongoDB.
Usage: python migerations/create_indexes.py
"""
import sys
import os
import logging

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from models.url_model import INDEXES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_indexes():
    """Create all indexes defined in the URL model."""
    collection = config.backend.mongo_connection["urls"]
    
    logger.info("Starting index creation...")
    
    for index_def in INDEXES:
        try:
            index_name = index_def["name"]
            keys = index_def["keys"]
            unique = index_def.get("unique", False)
            description = index_def.get("description", "")
            
            # Check if index already exists
            existing_indexes = list(collection.list_indexes())
            index_exists = any(idx.get("name") == index_name for idx in existing_indexes)
            
            if not index_exists:
                collection.create_index(
                    keys,
                    unique=unique,
                    name=index_name,
                    background=True  # Create index in background to avoid blocking
                )
                logger.info(f"✓ Created index: {index_name} - {description}")
            else:
                logger.info(f"⊘ Index {index_name} already exists, skipping...")
                
        except Exception as e:
            logger.error(f"✗ Error creating index {index_def.get('name', 'unknown')}: {str(e)}")
    
    logger.info("Index creation process completed!")
    
    # Display all indexes
    logger.info("\nCurrent indexes on 'urls' collection:")
    indexes = list(collection.list_indexes())
    for idx in indexes:
        logger.info(f"  - {idx.get('name', 'unnamed')}: {idx.get('key', {})}")


if __name__ == "__main__":
    try:
        create_indexes()
    except Exception as e:
        logger.error(f"Failed to create indexes: {str(e)}")
        sys.exit(1)

