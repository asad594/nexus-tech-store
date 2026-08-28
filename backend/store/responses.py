"""
Standardized API Response Wrappers
Ensures consistent JSON serialization envelope for API consumers.
"""
from rest_framework.response import Response
from rest_framework import status

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK, meta=None):
    """
    Format standard successful JSON API response.
    """
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    if meta is not None:
        payload["meta"] = meta
    return Response(payload, status=status_code)

def error_response(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Format standard error JSON API response.
    """
    payload = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {}
    }
    return Response(payload, status=status_code)

def paginated_response(results, count, page, page_size, total_pages, message="Success"):
    """
    Format standardized paginated payload.
    """
    return success_response(
        data=results,
        message=message,
        meta={
            "count": count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        }
    )
