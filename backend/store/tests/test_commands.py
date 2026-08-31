import os
import json
import tempfile
from io import StringIO
from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from store.models import Category, Product, Order, OrderItem, CartItem

User = get_user_model()

class ManagementCommandsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="commanduser",
            email="cmd@nexus.com",
            password="SecurePassword123!",
            name="Command User"
        )
        self.category = Category.objects.create(
            name="Smartphones",
            slug="smartphones",
            icon="Smartphone",
            description="Next-gen phones"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Nexus Quantum Phone",
            price=Decimal("999.00"),
            stock_qty=20,
            image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",
            description="Flagship smartphone"
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("999.00"),
            payment_status="paid",
            status="processing"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price_at_purchase=self.product.price,
            quantity=1
        )
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def test_sales_report_command_stdout(self):
        out = StringIO()
        call_command('sales_report', stdout=out)
        output = out.getvalue()
        self.assertIn("NEXUS TECH STORE SALES REPORT", output)
        self.assertIn("Total Orders:", output)
        self.assertIn("Total Revenue:", output)

    def test_sales_report_command_json(self):
        out = StringIO()
        call_command('sales_report', '--json', stdout=out)
        output = out.getvalue()
        data = json.loads(output)
        self.assertEqual(data['total_orders'], 1)
        self.assertEqual(data['paid_orders'], 1)
        self.assertEqual(data['total_units_sold'], 1)

    def test_check_integrity_command(self):
        out = StringIO()
        call_command('check_integrity', stdout=out)
        output = out.getvalue()
        self.assertIn("Integrity check completed", output)

    def test_prune_stale_carts_dry_run(self):
        out = StringIO()
        call_command('prune_stale_carts', '--dry-run', stdout=out)
        output = out.getvalue()
        self.assertIn("[DRY RUN]", output)

    def test_export_catalog_command(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            temp_path = tmp_file.name

        try:
            out = StringIO()
            call_command('export_catalog', f'--output={temp_path}', stdout=out)
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
                self.assertIn('categories', catalog)
                self.assertIn('products', catalog)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
