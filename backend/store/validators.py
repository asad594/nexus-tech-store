"""
Custom field and model validation utilities for Nexus Tech Store catalog and orders.
"""
import re
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_positive_price(value):
    """Ensure price value is strictly positive and non-zero."""
    try:
        dec_val = Decimal(str(value))
        if dec_val <= 0:
            raise ValidationError(
                _("Price must be a positive number greater than zero."),
                code='invalid_price'
            )
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(
            _("Invalid price numerical format."),
            code='invalid_price_format'
        )


def validate_stock_bounds(value):
    """Ensure inventory stock quantity is non-negative and within allowable maximums."""
    if not isinstance(value, int) or value < 0:
        raise ValidationError(
            _("Stock quantity cannot be negative."),
            code='invalid_stock_negative'
        )
    if value > 100000:
        raise ValidationError(
            _("Stock quantity exceeds maximum allowable limit (100,000)."),
            code='invalid_stock_overflow'
        )

def validate_hex_color_code(value):
    """Validate 3 or 6 digit hex color code (e.g., #00F0FF or #FFF)."""
    if not isinstance(value, str) or not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
        raise ValidationError(
            _("Invalid hex color format. Must be a valid hex color code like #00F0FF."),
            code='invalid_hex_color'
        )

def validate_rating_bounds(value):
    """Ensure rating value is between 1.0 and 5.0."""
    try:
        val = float(value)
        if val < 1.0 or val > 5.0:
            raise ValidationError(
                _("Rating must be between 1.0 and 5.0."),
                code='invalid_rating_range'
            )
    except (ValueError, TypeError):
        raise ValidationError(
            _("Invalid rating value."),
            code='invalid_rating_type'
        )
