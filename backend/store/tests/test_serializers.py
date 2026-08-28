from django.test import TestCase
from store.serializers import RegisterSerializer, CategorySerializer, ProductSerializer
from store.models import Category, Product

class SerializerValidationTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Audio",
            slug="audio",
            icon="Headphones",
            description="Spatial audio headphones"
        )

    def test_category_serializer_valid_data(self):
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data
        self.assertEqual(data["name"], "Audio")
        self.assertEqual(data["slug"], "audio")

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
