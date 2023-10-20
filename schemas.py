from pydantic import BaseModel


class ShortenTheURLRequestBody(BaseModel):
    long_url: int
    group_guid: str
