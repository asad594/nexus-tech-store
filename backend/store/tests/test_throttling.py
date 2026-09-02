from django.test import TestCase
from store.throttling import (
    BurstRateThrottle,
    SustainedRateThrottle,
    AuthRateThrottle,
    OrderCreationThrottle,
    ReviewSubmissionThrottle,
)

class ThrottlingConfigurationTestCase(TestCase):
    def test_burst_rate_throttle_scope(self):
        throttle = BurstRateThrottle()
        self.assertEqual(throttle.scope, 'burst')
        self.assertEqual(throttle.rate, '60/minute')

    def test_sustained_rate_throttle_scope(self):
        throttle = SustainedRateThrottle()
        self.assertEqual(throttle.scope, 'sustained')
        self.assertEqual(throttle.rate, '1000/day')

    def test_auth_rate_throttle_scope(self):
        throttle = AuthRateThrottle()
        self.assertEqual(throttle.scope, 'auth')
        self.assertEqual(throttle.rate, '10/minute')

    def test_order_creation_throttle_scope(self):
        throttle = OrderCreationThrottle()
        self.assertEqual(throttle.scope, 'order_creation')
        self.assertEqual(throttle.rate, '5/minute')

    def test_review_submission_throttle_scope(self):
        throttle = ReviewSubmissionThrottle()
        self.assertEqual(throttle.scope, 'review_submission')
        self.assertEqual(throttle.rate, '10/hour')
