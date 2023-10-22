from pydantic import BaseModel, Field


class ShortenTheURLRequestBody(BaseModel):
    long_url: str
    group_guid: str


class XUserData(BaseModel):
    user_id: int
    role: str
    user_name: str


class UserData(BaseModel):
    x_user_data: XUserData = Field(alias="x-user-data")
