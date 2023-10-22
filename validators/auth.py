from typing import Dict
import ujson
from validators.custom_exceptions import UnAuthorized

def validate_headers(headers: str) -> Dict[str, str]:
    headers_dict = ujson.loads(headers)
    user_data = headers_dict.get("x-user-data", {})
    if not user_data or "user_id" not in user_data or "role" not in user_data:
        raise UnAuthorized("Authentication required")
    return headers_dict