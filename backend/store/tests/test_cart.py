from django.test import TestCase
from decimal import Decimal
from store.models import Category, Product, CartItem, User

class CartModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cartshopper',
            email='shopper@nexus.com',
            password='Password123!'
        )
        self.category = Category.objects.create(name='Displays', slug='displays')
        self.product = Product.objects.create(
            name='Nexus 8K Ultra Display',
            category=self.category,
            price=Decimal('1299.00'),
            stock_qty=15,
            image_url='https://example.com/display.jpg'
        )

    def test_cart_item_creation_and_quantity(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        self.assertEqual(self.user.cart_items.count(), 1)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.product.price, Decimal('1299.00'))
