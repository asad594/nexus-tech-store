from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='authuser',
            email='authuser@nexus.com',
            password='TestPassword123!',
            name='Auth User'
        )

    def test_user_registration_success(self):
        url = reverse('register')
        payload = {
            'username': 'newcustomer',
            'email': 'customer@nexus.com',
            'password': 'SecurePassword123!',
            'name': 'New Customer'
        }
        response = self.client.post(url, payload, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        payload = {
            'username': 'authuser',
            'password': 'TestPassword123!'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
