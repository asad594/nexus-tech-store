from decimal import Decimal
from django.test import TestCase
from store.utils import (
    format_currency,
    calculate_tax_and_total,
    validate_sku_format,
    calculate_discount_percentage,
    apply_discount,
    generate_order_reference,
)

class StoreUtilsTestCase(TestCase):
    def test_format_currency(self):
        self.assertEqual(format_currency(1234.5), "$1,234.50")
        self.assertEqual(format_currency(0), "$0.00")

    def test_calculate_tax_and_total(self):
        result = calculate_tax_and_total(Decimal('100.00'))
        self.assertEqual(result['subtotal'], Decimal('100.00'))
        self.assertEqual(result['tax'], Decimal('8.00'))
        self.assertEqual(result['total'], Decimal('108.00'))

    def test_validate_sku_format(self):
        self.assertTrue(validate_sku_format("NX-PRO-001"))
        self.assertTrue(validate_sku_format("GPU-RTX-5090"))
        self.assertFalse(validate_sku_format("invalid_sku"))
        self.assertFalse(validate_sku_format(""))
        self.assertFalse(validate_sku_format(None))

    def test_calculate_discount_percentage(self):
        self.assertEqual(calculate_discount_percentage(100, 80), 20)
        self.assertEqual(calculate_discount_percentage(200, 150), 25)
        self.assertEqual(calculate_discount_percentage(100, 120), 0)
        self.assertEqual(calculate_discount_percentage(0, 50), 0)

    def test_apply_discount(self):
        self.assertEqual(apply_discount(Decimal('100.00'), 20), Decimal('80.00'))
        self.assertEqual(apply_discount(Decimal('50.00'), 0), Decimal('50.00'))
        self.assertEqual(apply_discount(Decimal('50.00'), 100), Decimal('0.00'))

    def test_generate_order_reference(self):
        ref = generate_order_reference("NX")
        self.assertTrue(ref.startswith("NX-"))
        self.assertEqual(len(ref), 11)  # NX- + 8 chars

