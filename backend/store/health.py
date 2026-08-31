"""
Health and System Diagnostics Module
Provides health check and system diagnostic status for monitoring tools.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import time

START_TIME = time.time()

@api_view(['GET'])
@permission_classes([AllowAny])
def system_diagnostics(request):
    """
    Detailed system health and database connectivity diagnostics including query latency.
    """
    db_status = "connected"
    db_latency_ms = 0.0
    try:
        t0 = time.perf_counter()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    except Exception as e:
        db_status = f"error: {str(e)}"

    uptime_seconds = int(time.time() - START_TIME)

    return Response({
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "database_latency_ms": db_latency_ms,
        "uptime_seconds": uptime_seconds,
        "timestamp": time.time(),
        "service": "nexus-tech-store-backend",
        "version": "1.3.0"
    }, status=status.HTTP_200_OK if db_status == "connected" else status.HTTP_503_SERVICE_UNAVAILABLE)

