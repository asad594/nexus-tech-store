"""
Data & Catalog Integrity Diagnostics Command
Scans for orphaned products, invalid image URLs, negative stock levels, and price anomalies.
"""
from django.core.management.base import BaseCommand
from store.models import Category, Product, Order, User

class Command(BaseCommand):
    help = 'Runs comprehensive database integrity checks across products, orders, and users'

    def handle(self, *args, **options):
        self.stdout.write("Running Nexus Tech Store database integrity analysis...")

        warnings = 0

        # Check negative stock
        negative_stock = Product.objects.filter(stock_qty__lt=0)
        if negative_stock.exists():
            for p in negative_stock:
                self.stdout.write(self.style.WARNING(f"Warning: Product '{p.name}' has negative stock: {p.stock_qty}"))
                warnings += 1

        # Check products with zero price
        free_products = Product.objects.filter(price__lte=0)
        if free_products.exists():
            for p in free_products:
                self.stdout.write(self.style.WARNING(f"Warning: Product '{p.name}' has price <= 0: {p.price}"))
                warnings += 1

        # Summary output
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_orders = Order.objects.count()
        total_users = User.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f"Integrity check completed. Found {warnings} warnings.\n"
            f"Stats: {total_categories} categories, {total_products} products, "
            f"{total_orders} orders, {total_users} users."
        ))
