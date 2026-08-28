from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from store.models import Category, Product

class ProductsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat1 = Category.objects.create(name='Laptops', slug='laptops')
        self.cat2 = Category.objects.create(name='Smartphones', slug='smartphones')

        self.p1 = Product.objects.create(
            name='Nexus Book Pro',
            category=self.cat1,
            price=Decimal('1899.99'),
            stock_qty=10,
            image_url='https://example.com/p1.jpg',
            is_featured=True
        )
        self.p2 = Product.objects.create(
            name='Nexus Ultra Phone',
            category=self.cat2,
            price=Decimal('999.00'),
            stock_qty=20,
            image_url='https://example.com/p2.jpg',
            is_featured=False
        )

    def test_list_all_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handling paginated or list response
        results = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(results), 2)

    def test_filter_products_by_category(self):
        url = reverse('product-list')
        response = self.client.get(url, {'category': 'laptops'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Nexus Book Pro')
