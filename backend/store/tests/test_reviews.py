from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command
from store.models import Category, Product, Review

User = get_user_model()

class ProductReviewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='reviewer1',
            email='reviewer1@nexus.com',
            password='TestPassword123!',
            name='Reviewer One'
        )
        self.user2 = User.objects.create_user(
            username='reviewer2',
            email='reviewer2@nexus.com',
            password='TestPassword123!',
            name='Reviewer Two'
        )
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            name='Nexus VR Headset',
            category=self.category,
            price=Decimal('599.99'),
            stock_qty=25,
            image_url='https://example.com/vr.jpg'
        )

    def test_review_creation_updates_product_rating(self):
        Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5,
            comment='Outstanding futuristic build!'
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.num_reviews, 1)
        self.assertEqual(float(self.product.rating), 5.0)

        Review.objects.create(
            product=self.product,
            user=self.user2,
            rating=3,
            comment='Good but battery could be longer.'
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.num_reviews, 2)
        self.assertEqual(float(self.product.rating), 4.0)

    def test_review_deletion_updates_product_rating(self):
        r1 = Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5,
            comment='First review'
        )
        r2 = Review.objects.create(
            product=self.product,
            user=self.user2,
            rating=3,
            comment='Second review'
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.num_reviews, 2)

        # Delete review and verify recalculation
        r2.delete()
        self.product.refresh_from_db()
        self.assertEqual(self.product.num_reviews, 1)
        self.assertEqual(float(self.product.rating), 5.0)

    def test_sync_ratings_command(self):
        Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=4,
            comment='Great headset'
        )
        call_command('sync_ratings', f'--product-id={self.product.id}')
        self.product.refresh_from_db()
        self.assertEqual(self.product.num_reviews, 1)
        self.assertEqual(float(self.product.rating), 4.0)

