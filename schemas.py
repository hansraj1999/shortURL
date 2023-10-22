from pydantic import BaseModel


class ShortenTheURLRequestBody(BaseModel):
    long_url: str
    group_guid: str
