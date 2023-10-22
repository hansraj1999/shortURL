from fastapi import APIRouter, HTTPException
from repository import shorten_url
import schemas
import logging
from fastapi import Header
from validators.auth import validate_headers
from validators.custom_exceptions import UnAuthorized
import traceback


logger = logging.getLogger(__name__)
router = APIRouter(tags=['short-url'], prefix='/v1')


@router.post('/shorten')
async def shorten_url_endpoint(request: schemas.ShortenTheURLRequestBody, headers: str = Header(...)):
    try:
        headers = validate_headers(headers)
        user_data = headers["x-user-data"]
        handler = shorten_url.Handler(
            request.long_url, request.group_guid, user_data)
        short_url = handler.handle()
        return {"short_url": short_url}

    except UnAuthorized as e:
        logger.exception(e)
        raise HTTPException(status_code=401, detail={
                            "message": e.message, "details": e.details})

    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail=str(e))
