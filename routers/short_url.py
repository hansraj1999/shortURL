from fastapi import APIRouter, HTTPException
from repository.shorten_url import Handler
from schemas import ShortenUrlResponse, ShortenTheURLRequestBody
import logging
from fastapi import Header
from validators.auth import validate_headers
from validators.custom_exceptions import UnAuthorized
import traceback
from pydantic import ValidationError

logger = logging.getLogger(__name__)
router = APIRouter(tags=["short-url"], prefix="/v1")


@router.post("/shorten", response_model=ShortenUrlResponse)
async def shorten_url_endpoint(
    request: ShortenTheURLRequestBody, headers: str = Header(...)
):
    try:
        # {"x-user-data": { "user_id": 1, "role": "admin", "user_name": "admin" }}
        logger.info(request)
        headers = validate_headers(headers)
        user_data = headers["x-user-data"]
        handler = Handler(
            request.long_url, 
            request.group_guid, 
            user_data,
            qr_code=request.qr_code or False
        )
        result = handler.handle()
        return result

    except UnAuthorized as e:
        logger.exception(e)
        raise HTTPException(
            status_code=401, detail={"message": e.message, "details": e.details}
        )
    except ValidationError as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Validation Error",
                "details": e.errors(include_url=False, include_input=False),
            },
        )
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail={"message": str(e), "details": []})
