from django.test import TestCase
from store.models import Category, Product, User

class StoreModelsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Laptops",
            slug="laptops",
            icon="Laptop",
            description="High performance laptops"
        )
        self.product = Product.objects.create(
            name="Nexus Pro 16",
            category=self.category,
            price=1999.99,
            description="Quantum core laptop",
            stock_qty=15,
            image_url="https://example.com/laptop.jpg",
            brand="Nexus",
            is_featured=True
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Laptops")
        self.assertEqual(self.category.slug, "laptops")

    def test_product_creation(self):
        self.assertEqual(str(self.product), "Nexus Pro 16")
        self.assertEqual(self.product.price, 1999.99)
        self.assertTrue(self.product.is_featured)
