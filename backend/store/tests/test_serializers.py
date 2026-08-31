from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from store.serializers import (
    RegisterSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    OrderItemSerializer,
)
from store.models import Category, Product, Review, Order, OrderItem

User = get_user_model()


class SerializerValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@nexusstore.com",
            password="SecurePassword2026!",
            name="Test User"
        )
        self.category = Category.objects.create(
            name="Audio",
            slug="audio",
            icon="Headphones",
            description="Spatial audio headphones"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Quantum Headphones Pro",
            price=Decimal("299.99"),
            stock_qty=15,
            image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
            description="High fidelity audio headphones"
        )

    def test_category_serializer_valid_data(self):
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data
        self.assertEqual(data["name"], "Audio")
        self.assertEqual(data["slug"], "audio")

    def test_product_serializer_fields(self):
        serializer = ProductSerializer(instance=self.product)
        data = serializer.data
        self.assertEqual(data["name"], "Quantum Headphones Pro")
        self.assertEqual(float(data["price"]), 299.99)
        self.assertEqual(data["stock_qty"], 15)

    def test_register_serializer_validation(self):
        valid_payload = {
            "username": "testdeveloper",
            "email": "dev@nexusstore.com",
            "password": "SecurePassword2026!",
            "name": "Test Developer"
        }
        serializer = RegisterSerializer(data=valid_payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_register_serializer_missing_required_fields(self):
        invalid_payload = {
            "email": "dev@nexusstore.com"
        }
        serializer = RegisterSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_order_item_serializer_representation(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("299.99"),
            shipping_address="123 Future Way",
            city="Tech City",
            postal_code="94016",
            country="USA"
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price_at_purchase=self.product.price,
            quantity=1
        )
        serializer = OrderItemSerializer(instance=order_item)
        self.assertEqual(serializer.data["product_name_snapshot"], "Quantum Headphones Pro")
        self.assertEqual(serializer.data["quantity"], 1)
        self.assertEqual(float(serializer.data["price_at_purchase"]), 299.99)



