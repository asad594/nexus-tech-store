from django.test import TestCase
from django.db import IntegrityError
from decimal import Decimal
from store.models import Category, Product, Wishlist, User

class WishlistModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='wishlistuser',
            email='wishlist@nexus.com',
            password='Password123!'
        )
        self.category = Category.objects.create(name='Accessories', slug='accessories')
        self.product = Product.objects.create(
            name='Nexus MagSafe Charger',
            category=self.category,
            price=Decimal('49.99'),
            stock_qty=100,
            image_url='https://example.com/charger.jpg'
        )

    def test_add_to_wishlist(self):
        item = Wishlist.objects.create(user=self.user, product=self.product)
        self.assertEqual(self.user.wishlist.count(), 1)
        self.assertEqual(item.product.name, 'Nexus MagSafe Charger')

    def test_duplicate_wishlist_prevention(self):
        Wishlist.objects.create(user=self.user, product=self.product)
        with self.assertRaises(IntegrityError):
            Wishlist.objects.create(user=self.user, product=self.product)
