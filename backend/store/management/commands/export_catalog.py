"""
Catalog JSON Data Exporter Command
Dumps store categories and product catalogs to structured JSON files for backups or migrations.
"""
import json
import os
from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Exports the current category and product catalog to a JSON snapshot'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='catalog_export.json',
            help='Output file path for exported JSON catalog data'
        )

    def handle(self, *args, **options):
        output_path = options['output']
        self.stdout.write(f"Exporting hardware catalog to {output_path}...")

        categories = []
        for cat in Category.objects.all():
            categories.append({
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'icon': cat.icon,
                'description': cat.description,
            })

        products = []
        for prod in Product.objects.select_related('category').all():
            products.append({
                'id': prod.id,
                'name': prod.name,
                'category_slug': prod.category.slug if prod.category else None,
                'price': str(prod.price),
                'stock_qty': prod.stock_qty,
                'description': prod.description,
                'specs': prod.specs,
                'image_url': prod.image_url,
                'is_featured': prod.is_featured,
                'rating': str(prod.rating),
                'num_reviews': prod.num_reviews,
            })

        export_data = {
            'categories_count': len(categories),
            'products_count': len(products),
            'categories': categories,
            'products': products,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"Successfully exported {len(categories)} categories and {len(products)} products to {output_path}"
        ))
