"""
Custom API throttling classes for Nexus Tech Store.
Provides scoped rate-limiting for sensitive endpoints like auth, order creation, and checkout.
"""
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstRateThrottle(AnonRateThrottle):
    """Throttle for controlling rapid request bursts from anonymous visitors."""
    scope = 'burst'
    rate = '60/minute'

class SustainedRateThrottle(AnonRateThrottle):
    """Throttle for sustained daily request limits from anonymous visitors."""
    scope = 'sustained'
    rate = '1000/day'

class AuthRateThrottle(AnonRateThrottle):
    """Strict throttle for login and registration endpoints to prevent brute force attacks."""
    scope = 'auth'
    rate = '10/minute'

class OrderCreationThrottle(UserRateThrottle):
    """Throttle to prevent rapid-fire duplicate order placements from authenticated users."""
    scope = 'order_creation'
    rate = '5/minute'

class ReviewSubmissionThrottle(UserRateThrottle):
    """Throttle to limit product review creation frequency."""
    scope = 'review_submission'
    rate = '10/hour'
