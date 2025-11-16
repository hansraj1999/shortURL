from fastapi import APIRouter, HTTPException, Query, Header
from config import config
from schemas import AnalyticsResponse, AnalyticsQueryParams
from validators.auth import validate_headers
from validators.custom_exceptions import UnAuthorized
import logging
import traceback

logger = logging.getLogger(__name__)
router = APIRouter(tags=["analytics"], prefix="/v1")


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    sort_by: str = Query(default="created_at", description="Sort by: hits, redirect_count, created_at, latest_shortened, last_redirected_at, latest_redirected"),
    sort_order: str = Query(default="desc", description="Sort order: asc or desc"),
    filter_by_user_id: int = Query(default=None, description="Filter by user ID"),
    filter_by_user_name: str = Query(default=None, description="Filter by user name"),
    limit: int = Query(default=100, ge=1, le=1000, description="Number of results to return"),
    skip: int = Query(default=0, ge=0, description="Number of results to skip"),
    headers: str = Header(...)
):
    """
    Get analytics data for shortened URLs.
    
    Features:
    - Total count of URLs shortened
    - Total count of redirects
    - Sorting options:
      * hits/redirect_count: Sort by number of redirects
      * created_at/latest_shortened: Sort by creation date
      * last_redirected_at/latest_redirected: Sort by last redirect time
    - Filtering by created_by (user_id or user_name)
    - Pagination support (limit and skip)
    """
    try:
        # Validate headers
        headers_data = validate_headers(headers)
        user_data = headers_data.get("x-user-data", {})
        
        # Get analytics data
        urls = config.backend.get_analytics_data(
            sort_by=sort_by,
            sort_order=sort_order,
            filter_by_user_id=filter_by_user_id,
            filter_by_user_name=filter_by_user_name,
            limit=limit,
            skip=skip
        )
        
        # Get total counts
        total_urls = config.backend.get_total_urls_count(
            filter_by_user_id=filter_by_user_id,
            filter_by_user_name=filter_by_user_name
        )
        
        total_redirects = config.backend.get_total_redirects_count(
            filter_by_user_id=filter_by_user_id,
            filter_by_user_name=filter_by_user_name
        )
        
        return {
            "total_urls": total_urls,
            "total_redirects": total_redirects,
            "urls": urls
        }
        
    except UnAuthorized as e:
        logger.exception(e)
        raise HTTPException(
            status_code=401, detail={"message": e.message, "details": e.details}
        )
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=500, detail={"message": str(e), "details": []})

