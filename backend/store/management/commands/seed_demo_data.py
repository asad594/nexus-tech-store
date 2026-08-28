"""
Quick Demo Data Seeder Management Command
Populates a lightweight sandbox dataset for rapid local testing and development.
"""
from django.core.management.base import BaseCommand
from store.models import Category, Product, User

class Command(BaseCommand):
    help = 'Seeds lightweight demo data for quick testing and sandbox environments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding demo hardware catalog..."))

        cat, _ = Category.objects.get_or_create(
            slug='demo-laptops',
            defaults={
                'name': 'Demo Laptops',
                'icon': 'Laptop',
                'description': 'Demo category for automated testing'
            }
        )

        p1, _ = Product.objects.get_or_create(
            name='Nexus Book Stealth 14',
            category=cat,
            defaults={
                'price': 1499.00,
                'description': 'Ultra-thin titanium chassis laptop with OLED HDR display.',
                'specs': {'Processor': 'M4 Max', 'RAM': '32GB', 'Storage': '1TB SSD'},
                'stock_qty': 20,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8',
                'is_featured': True
            }
        )

        p2, _ = Product.objects.get_or_create(
            name='Nexus Horizon Phone 1',
            category=cat,
            defaults={
                'price': 999.00,
                'description': 'Edge-to-edge curved holographic display flagship phone.',
                'specs': {'Display': '6.8 inch 144Hz', 'Camera': '200MP', 'Battery': '5500mAh'},
                'stock_qty': 45,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02560',
                'is_featured': True
            }
        )

        self.stdout.write(self.style.SUCCESS(f"Demo data seeded successfully! Created/verified 1 category and 2 products."))
