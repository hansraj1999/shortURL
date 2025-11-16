from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ShortenTheURLRequestBody(BaseModel):
    long_url: str
    group_guid: str = Optional  # dk why is this is needed
    qr_code: bool = Optional  # for future
    custom_domain: str = Optional  # for future


class XUserData(BaseModel):
    user_id: int
    role: str
    user_name: str


class UserData(BaseModel):
    x_user_data: XUserData = Field(alias="x-user-data")


class ShortenUrlResponse(BaseModel):
    short_url: str


class InsertUrl(BaseModel):
    group_guid: str
    user_name: str
    user_id: int
    url_hash: str
    actual_url: str
    created_at: str
    updated_at: str
    has_custom_domain: bool = False
    custom_domain: Optional[str] = None
    hits: int = 0
    last_redirected_at: Optional[str] = None


class ShortUrlHash(BaseModel):
    url_hash: str


class RedirectModel(BaseModel):
    url: str
    status_code: int = 303


class AnalyticsResponse(BaseModel):
    total_urls: int
    total_redirects: int
    urls: List[Dict[str, Any]]


class AnalyticsQueryParams(BaseModel):
    sort_by: Optional[str] = "created_at"  # Options: hits, redirect_count, created_at, latest_shortened, last_redirected_at, latest_redirected
    sort_order: Optional[str] = "desc"  # Options: asc, desc
    filter_by_user_id: Optional[int] = None
    filter_by_user_name: Optional[str] = None
    filter_by_url_hash: Optional[str] = None  # Search by full short URL (hash)
    limit: Optional[int] = 100
    skip: Optional[int] = 0
