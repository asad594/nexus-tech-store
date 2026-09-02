"""
Store Domain Constants & Enumerations
Provides centralized definitions for user roles, order lifecycles, and catalog defaults.
"""

# User Roles
ROLE_CUSTOMER = 'customer'
ROLE_ADMIN = 'admin'
USER_ROLES = (
    (ROLE_CUSTOMER, 'Customer'),
    (ROLE_ADMIN, 'Admin'),
)

# Order Statuses
ORDER_STATUS_PENDING = 'pending'
ORDER_STATUS_PROCESSING = 'processing'
ORDER_STATUS_SHIPPED = 'shipped'
ORDER_STATUS_DELIVERED = 'delivered'
ORDER_STATUS_CANCELLED = 'cancelled'

ORDER_STATUSES = (
    (ORDER_STATUS_PENDING, 'Pending'),
    (ORDER_STATUS_PROCESSING, 'Processing'),
    (ORDER_STATUS_SHIPPED, 'Shipped'),
    (ORDER_STATUS_DELIVERED, 'Delivered'),
    (ORDER_STATUS_CANCELLED, 'Cancelled'),
)

# Payment Methods
PAYMENT_METHOD_CARD = 'credit_card'
PAYMENT_METHOD_PAYPAL = 'paypal'
PAYMENT_METHOD_CRYPTO = 'crypto'
PAYMENT_METHOD_COD = 'cash_on_delivery'

PAYMENT_METHODS = (
    (PAYMENT_METHOD_CARD, 'Credit / Debit Card'),
    (PAYMENT_METHOD_PAYPAL, 'PayPal'),
    (PAYMENT_METHOD_CRYPTO, 'Cryptocurrency'),
    (PAYMENT_METHOD_COD, 'Cash On Delivery'),
)

# Pagination & Catalog Constraints
DEFAULT_PAGE_SIZE = 12
MAX_PAGE_SIZE = 100
MIN_REVIEW_RATING = 1
MAX_REVIEW_RATING = 5
LOW_STOCK_THRESHOLD = 5

# Financial & Tax Constraints
STANDARD_TAX_RATE = 0.08
FREE_SHIPPING_THRESHOLD = 100.00
STANDARD_SHIPPING_FEE = 15.00

# Supported Store Currencies
SUPPORTED_CURRENCIES = {
    'USD': {'symbol': '$', 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'name': 'Euro'},
    'GBP': {'symbol': '£', 'name': 'British Pound'},
    'JPY': {'symbol': '¥', 'name': 'Japanese Yen'},
    'CAD': {'symbol': 'CA$', 'name': 'Canadian Dollar'},
}

# Valid Order Status State Machine Transitions
ORDER_STATUS_TRANSITIONS = {
    ORDER_STATUS_PENDING: [ORDER_STATUS_PROCESSING, ORDER_STATUS_CANCELLED],
    ORDER_STATUS_PROCESSING: [ORDER_STATUS_SHIPPED, ORDER_STATUS_CANCELLED],
    ORDER_STATUS_SHIPPED: [ORDER_STATUS_DELIVERED],
    ORDER_STATUS_DELIVERED: [],
    ORDER_STATUS_CANCELLED: [],
}

# Standard Shipping Destinations
ALLOWED_SHIPPING_COUNTRIES = (
    'United States',
    'Canada',
    'United Kingdom',
    'Germany',
    'France',
    'Japan',
    'Australia',
)

