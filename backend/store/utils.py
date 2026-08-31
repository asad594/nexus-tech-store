"""
Utility functions for store backend calculations and response standardizations.
"""
import re
import uuid
from decimal import Decimal, ROUND_HALF_UP

def format_currency(amount: float | Decimal) -> str:
    """Format numeric value into USD currency string."""
    return f"${Decimal(str(amount)):,.2f}"

def calculate_tax_and_total(subtotal: Decimal, tax_rate: Decimal = Decimal('0.08')) -> dict:
    """Calculate tax amount and total given subtotal and optional tax rate."""
    tax = round(subtotal * tax_rate, 2)
    total = subtotal + tax
    return {
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }

def validate_sku_format(sku: str) -> bool:
    """Validate that SKU follows standard alphanumeric hyphenated format (e.g., NX-PRO-001)."""
    if not isinstance(sku, str) or not sku.strip():
        return False
    return bool(re.match(r'^[A-Z0-9]{2,10}(-[A-Z0-9]{2,10})+$', sku.strip().upper()))

def calculate_discount_percentage(original_price: Decimal | float, sale_price: Decimal | float) -> int:
    """Calculate percentage discount between original price and sale price."""
    orig = Decimal(str(original_price))
    sale = Decimal(str(sale_price))
    if orig <= 0 or sale >= orig:
        return 0
    discount = ((orig - sale) / orig) * 100
    return int(discount.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def apply_discount(price: Decimal | float, percentage: int | float) -> Decimal:
    """Apply discount percentage to base price and return discounted amount."""
    base = Decimal(str(price))
    if percentage <= 0:
        return base
    if percentage >= 100:
        return Decimal('0.00')
    discount_factor = Decimal(str(percentage)) / Decimal('100')
    discounted = base * (Decimal('1') - discount_factor)
    return discounted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def generate_order_reference(prefix: str = "NX") -> str:
    """Generate a clean unique order tracking code."""
    unique_suffix = uuid.uuid4().hex[:8].upper()
    return f"{prefix}-{unique_suffix}"

