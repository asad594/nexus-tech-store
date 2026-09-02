"""
Catalog and Order Query Filtering Utilities for Nexus Tech Store.
Provides standardized request query parsing and filtering for viewsets.
"""
from decimal import Decimal
from django.db.models import Q

def parse_price_range(min_price_str=None, max_price_str=None):
    """Parses and validates optional min and max price filter bounds."""
    min_price = None
    max_price = None

    if min_price_str is not None:
        try:
            val = Decimal(str(min_price_str))
            if val >= 0:
                min_price = val
        except (ValueError, TypeError):
            pass

    if max_price_str is not None:
        try:
            val = Decimal(str(max_price_str))
            if val >= 0:
                max_price = val
        except (ValueError, TypeError):
            pass

    return min_price, max_price

def filter_products_by_params(queryset, params):
    """
    Applies common query parameter filters to a Product queryset.
    Supports: category, brand, min_price, max_price, in_stock, is_featured, is_new, search.
    """
    category = params.get('category')
    if category:
        queryset = queryset.filter(
            Q(category__slug__iexact=category) | Q(category__name__iexact=category)
        )

    brand = params.get('brand')
    if brand:
        queryset = queryset.filter(brand__iexact=brand)

    min_p, max_p = parse_price_range(params.get('min_price'), params.get('max_price'))
    if min_p is not None:
        queryset = queryset.filter(price__gte=min_p)
    if max_p is not None:
        queryset = queryset.filter(price__lte=max_p)

    in_stock = params.get('in_stock')
    if in_stock is not None:
        if str(in_stock).lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(stock_qty__gt=0)
        elif str(in_stock).lower() in ['false', '0', 'no']:
            queryset = queryset.filter(stock_qty=0)

    if params.get('is_featured') in ['true', '1']:
        queryset = queryset.filter(is_featured=True)

    if params.get('is_new') in ['true', '1']:
        queryset = queryset.filter(is_new=True)

    search_query = params.get('search') or params.get('q')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    return queryset
