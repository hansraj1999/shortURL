from fastapi import APIRouter, HTTPException
from repository import shorten_url
import schemas
import time
import logging
from fastapi import Header
from validators.auth import validate_headers
from validators.custom_exceptions import UnAuthorized
import traceback


logger = logging.getLogger(__name__)
router = APIRouter(tags=['short-url'], prefix='/v1')


@router.post('/shorten')
async def get_long_url(request: schemas.ShortenTheURLRequestBody, headers: str = Header(...)):
    try:
        start_time = time.time()
        logger.info(f"request: {request}, headers: {headers}")
        headers = validate_headers(headers)
        user_data = headers["x-user-data"]

        handler = shorten_url.Handler(request.long_url, request.group_guid, user_data)
        logger.info(f"latency: {time.time() - start_time}")
        return {"short_url": handler.handle()}
    except UnAuthorized as e:
        traceback.print_exc()
        logger.exception(e)
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail=str(e))
