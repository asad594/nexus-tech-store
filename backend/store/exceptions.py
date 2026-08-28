"""
Custom Exception Handler for Django REST Framework
Ensures unhandled or validation exceptions follow a unified JSON error schema.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_api_exception_handler(exc, context):
    """
    Custom DRF exception handler returning structured error formats.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "success": False,
            "error_type": exc.__class__.__name__,
            "message": "Validation or execution error occurred.",
            "details": response.data
        }
        response.data = custom_data
    else:
        logger.error(f"Unhandled backend server exception: {str(exc)}", exc_info=context)

    return response
