from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from store.validators import (
    validate_positive_price,
    validate_stock_bounds,
    validate_hex_color_code,
    validate_rating_bounds,
)

class ValidatorsTestCase(TestCase):
    def test_validate_positive_price_valid(self):
        try:
            validate_positive_price(Decimal('19.99'))
            validate_positive_price(100)
            validate_positive_price("49.50")
        except ValidationError:
            self.fail("validate_positive_price raised ValidationError unexpectedly!")

    def test_validate_positive_price_invalid(self):
        with self.assertRaises(ValidationError):
            validate_positive_price(Decimal('-10.00'))
        with self.assertRaises(ValidationError):
            validate_positive_price(0)
        with self.assertRaises(ValidationError):
            validate_positive_price("not_a_number")

    def test_validate_stock_bounds_valid(self):
        try:
            validate_stock_bounds(0)
            validate_stock_bounds(500)
            validate_stock_bounds(100000)
        except ValidationError:
            self.fail("validate_stock_bounds raised ValidationError unexpectedly!")

    def test_validate_stock_bounds_invalid(self):
        with self.assertRaises(ValidationError):
            validate_stock_bounds(-1)
        with self.assertRaises(ValidationError):
            validate_stock_bounds(100001)

    def test_validate_hex_color_code_valid(self):
        try:
            validate_hex_color_code("#00F0FF")
            validate_hex_color_code("#FFF")
            validate_hex_color_code("#123456")
        except ValidationError:
            self.fail("validate_hex_color_code raised ValidationError unexpectedly!")

    def test_validate_hex_color_code_invalid(self):
        with self.assertRaises(ValidationError):
            validate_hex_color_code("00F0FF")
        with self.assertRaises(ValidationError):
            validate_hex_color_code("#GGGGGG")
        with self.assertRaises(ValidationError):
            validate_hex_color_code("#12")

    def test_validate_rating_bounds_valid(self):
        try:
            validate_rating_bounds(1.0)
            validate_rating_bounds(3.5)
            validate_rating_bounds(5.0)
        except ValidationError:
            self.fail("validate_rating_bounds raised ValidationError unexpectedly!")

    def test_validate_rating_bounds_invalid(self):
        with self.assertRaises(ValidationError):
            validate_rating_bounds(0.9)
        with self.assertRaises(ValidationError):
            validate_rating_bounds(5.1)
        with self.assertRaises(ValidationError):
            validate_rating_bounds("invalid")
