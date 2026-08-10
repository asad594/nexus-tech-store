from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from store.models import Category, Product

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Smartphones",
            slug="smartphones",
            icon="Smartphone"
        )
        self.product = Product.objects.create(
            name="Nexus Phone 15",
            category=self.category,
            price=999.00,
            description="Flagship smartphone",
            stock_qty=20,
            image_url="https://example.com/phone.jpg",
            brand="Nexus"
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
