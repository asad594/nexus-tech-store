from decimal import Decimal
from django.test import TestCase
from store.utils import format_currency, calculate_tax_and_total

class StoreUtilsTestCase(TestCase):
    def test_format_currency(self):
        self.assertEqual(format_currency(1234.5), "$1,234.50")
        self.assertEqual(format_currency(0), "$0.00")

    def test_calculate_tax_and_total(self):
        result = calculate_tax_and_total(Decimal('100.00'))
        self.assertEqual(result['subtotal'], Decimal('100.00'))
        self.assertEqual(result['tax'], Decimal('8.00'))
        self.assertEqual(result['total'], Decimal('108.00'))
