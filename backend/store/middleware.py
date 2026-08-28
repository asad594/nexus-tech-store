"""
Performance & Response Header Middleware
Attaches execution processing time metrics and diagnostic headers to HTTP responses.
"""
import time
import logging

logger = logging.getLogger(__name__)

class ResponseTimeMiddleware:
    """
    Middleware that measures request latency and appends
    an 'X-Process-Time-ms' header to responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()

        response = self.get_response(request)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response['X-Process-Time-ms'] = str(duration_ms)

        if duration_ms > 500:
            logger.warning(f"Slow request detected: {request.method} {request.path} took {duration_ms}ms")

        return response
