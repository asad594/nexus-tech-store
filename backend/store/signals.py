"""
Store Signals & Lifecycle Event Observers
Handles inventory auditing, stock change notifications, and system event logging.
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def product_stock_monitor(sender, instance, created, **kwargs):
    """
    Log low stock warning when product inventory dips below safety threshold.
    """
    if created:
        logger.info(f"New product created: {instance.name} (Initial stock: {instance.stock_qty})")
    else:
        if instance.stock_qty <= 5:
            logger.warning(
                f"LOW STOCK ALERT: Product '{instance.name}' (ID: {instance.id}) "
                f"has only {instance.stock_qty} units remaining."
            )
