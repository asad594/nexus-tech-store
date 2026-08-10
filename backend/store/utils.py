"""
Utility functions for store backend calculations and response standardizations.
"""
from decimal import Decimal

def format_currency(amount: float | Decimal) -> str:
    """Format numeric value into USD currency string."""
    return f"${Decimal(amount):,.2f}"

def calculate_tax_and_total(subtotal: Decimal, tax_rate: Decimal = Decimal('0.08')) -> dict:
    """Calculate tax amount and total given subtotal and optional tax rate."""
    tax = round(subtotal * tax_rate, 2)
    total = subtotal + tax
    return {
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }
