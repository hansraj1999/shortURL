from fastapi import APIRouter
from repository import shorten_url
import schemas
import time
import logging


logger = logging.getLogger(__name__)
router = APIRouter(tags=['short-url'], prefix='/v1')


@router.post('/shorten')
async def get_long_url(request: schemas.ShortenTheURLRequestBody):
    start_time = time.time()
    logger.info(f"request: {request}")
    handler = shorten_url.Handler(request.long_url, request.group_guid)
    logger.info(f"latency: {time.time() - start_time}")
    return {"short_url": handler.handle()}
