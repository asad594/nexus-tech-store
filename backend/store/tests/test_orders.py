from django.test import TestCase
from decimal import Decimal
from store.models import Category, Product, Order, OrderItem, User

class OrderProcessingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='buyer1',
            email='buyer1@nexus.com',
            password='SecurePassword123!'
        )
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.product = Product.objects.create(
            name='Nexus Earbuds Pro',
            category=self.category,
            price=Decimal('199.99'),
            stock_qty=50,
            image_url='https://example.com/earbuds.jpg'
        )

    def test_order_and_item_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('399.98'),
            shipping_address='100 Tech Blvd',
            city='San Francisco',
            postal_code='94105',
            payment_status='paid'
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name_snapshot=self.product.name,
            quantity=2,
            price_at_purchase=self.product.price
        )

        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price_at_purchase, Decimal('199.99'))
        self.assertEqual(order.status, 'pending')
