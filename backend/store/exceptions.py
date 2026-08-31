"""
Custom Exception Handler and Domain Exceptions for Django REST Framework.
Ensures unhandled or validation exceptions follow a unified JSON error schema.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

logger = logging.getLogger(__name__)

class NexusAPIException(APIException):
    """Base exception for domain-specific store errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An error occurred while processing your request."
    default_code = "bad_request"

class InsufficientStockException(NexusAPIException):
    """Raised when an order or cart addition exceeds available inventory stock."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Requested quantity exceeds available stock."
    default_code = "insufficient_stock"

class ResourceConflictException(NexusAPIException):
    """Raised when an action conflicts with existing state (e.g. duplicate item)."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource conflict detected."
    default_code = "conflict"

class PaymentProcessingException(NexusAPIException):
    """Raised when a payment gateway transaction cannot be completed."""
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = "Payment transaction failed or was rejected."
    default_code = "payment_required"


def custom_api_exception_handler(exc, context):
    """
    Custom DRF exception handler returning structured error formats.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "success": False,
            "error_type": exc.__class__.__name__,
            "error_code": getattr(exc, 'default_code', 'error'),
            "message": str(exc.detail) if hasattr(exc, 'detail') and isinstance(exc.detail, str) else "Validation or execution error occurred.",
            "details": response.data
        }
        response.data = custom_data
    else:
        logger.error(f"Unhandled backend server exception: {str(exc)}", exc_info=context)

    return response

