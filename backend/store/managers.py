"""
Custom QuerySets and Model Managers for Nexus Tech Store.
Provides chainable query helpers for filtering inventory, orders, and products.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta

class ProductQuerySet(models.QuerySet):
    """Custom queryset providing domain-specific product queries."""

    def in_stock(self):
        """Filter products with available stock quantity."""
        return self.filter(stock_qty__gt=0)

    def out_of_stock(self):
        """Filter products that are out of stock."""
        return self.filter(stock_qty__lte=0)

    def featured(self):
        """Filter featured showcase products."""
        return self.filter(is_featured=True)

    def new_arrivals(self):
        """Filter products marked as newly arrived."""
        return self.filter(is_new=True)

    def top_rated(self, min_rating=4.5):
        """Filter products with minimum average rating."""
        return self.filter(rating__gte=min_rating)

    def by_brand(self, brand_name):
        """Filter products matching specified brand."""
        return self.filter(brand__iexact=brand_name)


class OrderQuerySet(models.QuerySet):
    """Custom queryset providing domain-specific order filtering."""

    def paid(self):
        """Filter orders with successful payment."""
        return self.filter(payment_status='paid')

    def unpaid(self):
        """Filter orders awaiting payment."""
        return self.filter(payment_status='unpaid')

    def pending_shipment(self):
        """Filter orders in pending or processing status."""
        return self.filter(status__in=['pending', 'processing'])

    def completed(self):
        """Filter delivered/fulfilled orders."""
        return self.filter(status='delivered')

    def recent(self, days=30):
        """Filter orders placed within the last N days."""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
