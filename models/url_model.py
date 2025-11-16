"""
Database schema/model for URL documents in MongoDB.

This module defines the structure and indexes for URL documents.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class URLDocument(BaseModel):
    """
    MongoDB document schema for shortened URLs.
    
    Fields:
    - _id: MongoDB ObjectId (auto-generated)
    - url_hash: Unique hash for the shortened URL (indexed)
    - actual_url: The original long URL
    - user_id: ID of the user who created the URL (indexed)
    - user_name: Name of the user who created the URL (indexed)
    - user_role: Role of the user
    - group_guid: Group identifier for the URL
    - created_at: Timestamp when URL was created (indexed)
    - updated_at: Timestamp when URL was last updated
    - last_redirected_at: Timestamp when URL was last redirected (indexed)
    - hits: Number of times the URL was redirected (indexed)
    - has_custom_domain: Whether URL has a custom domain
    - custom_domain: Custom domain if applicable
    """
    url_hash: str = Field(..., description="Unique hash for the shortened URL")
    actual_url: str = Field(..., description="The original long URL")
    user_id: int = Field(..., description="ID of the user who created the URL")
    user_name: str = Field(..., description="Name of the user who created the URL")
    user_role: str = Field(..., description="Role of the user")
    group_guid: str = Field(..., description="Group identifier for the URL")
    created_at: str = Field(..., description="Timestamp when URL was created")
    updated_at: str = Field(..., description="Timestamp when URL was last updated")
    last_redirected_at: Optional[str] = Field(None, description="Timestamp when URL was last redirected")
    hits: int = Field(0, description="Number of times the URL was redirected")
    has_custom_domain: bool = Field(False, description="Whether URL has a custom domain")
    custom_domain: Optional[str] = Field(None, description="Custom domain if applicable")


# Index definitions for MongoDB
INDEXES = [
    # Single field indexes
    {
        "name": "url_hash_idx",
        "keys": [("url_hash", 1)],
        "unique": True,
        "description": "Unique index on url_hash for fast lookups"
    },
    {
        "name": "user_id_idx",
        "keys": [("user_id", 1)],
        "unique": False,
        "description": "Index on user_id for filtering by user"
    },
    {
        "name": "user_name_idx",
        "keys": [("user_name", 1)],
        "unique": False,
        "description": "Index on user_name for filtering by user name"
    },
    {
        "name": "created_at_idx",
        "keys": [("created_at", -1)],
        "unique": False,
        "description": "Index on created_at for sorting by latest shortened"
    },
    {
        "name": "last_redirected_at_idx",
        "keys": [("last_redirected_at", -1)],
        "unique": False,
        "description": "Index on last_redirected_at for sorting by latest redirected"
    },
    {
        "name": "hits_idx",
        "keys": [("hits", -1)],
        "unique": False,
        "description": "Index on hits for sorting by redirect count"
    },
    
    # Compound indexes for common query patterns
    {
        "name": "user_id_hits_idx",
        "keys": [("user_id", 1), ("hits", -1)],
        "unique": False,
        "description": "Compound index for filtering by user_id and sorting by hits"
    },
    {
        "name": "user_name_hits_idx",
        "keys": [("user_name", 1), ("hits", -1)],
        "unique": False,
        "description": "Compound index for filtering by user_name and sorting by hits"
    },
    {
        "name": "user_id_created_at_idx",
        "keys": [("user_id", 1), ("created_at", -1)],
        "unique": False,
        "description": "Compound index for filtering by user_id and sorting by created_at"
    },
    {
        "name": "user_name_created_at_idx",
        "keys": [("user_name", 1), ("created_at", -1)],
        "unique": False,
        "description": "Compound index for filtering by user_name and sorting by created_at"
    },
    {
        "name": "user_id_last_redirected_at_idx",
        "keys": [("user_id", 1), ("last_redirected_at", -1)],
        "unique": False,
        "description": "Compound index for filtering by user_id and sorting by last_redirected_at"
    },
    {
        "name": "user_name_last_redirected_at_idx",
        "keys": [("user_name", 1), ("last_redirected_at", -1)],
        "unique": False,
        "description": "Compound index for filtering by user_name and sorting by last_redirected_at"
    },
]

