from typing import Dict
import ujson
from validators.custom_exceptions import UnAuthorized
from pydantic import ValidationError
from schemas import UserData
import logging

logger = logging.getLogger(__name__)


def validate_headers(headers: str) -> Dict[str, str]:
    try:
        headers_dict = ujson.loads(headers)
        UserData(**headers_dict)
    except ValidationError as e:
        logger.exception(e)
        raise UnAuthorized("UnAuthorized", e.errors(
            include_url=False, include_input=False))
    return headers_dict
