from pydantic import BaseModel, Field
from typing import Optional


class ShortenTheURLRequestBody(BaseModel):
    long_url: str
    group_guid: str = Optional # dk why is this is needed
    qr_code: bool = Optional # for future
    custom_domain: str = Optional # for future


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

class ShortUrlHash(BaseModel):
    url_hash: str