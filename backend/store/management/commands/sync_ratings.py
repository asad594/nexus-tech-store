"""
Management command to recalculate and synchronize product review ratings and counts.
"""
from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Recalculates and synchronizes average rating and review counts across products.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--product-id',
            type=int,
            dest='product_id',
            help='Optional specific Product ID to sync rating for.',
        )

    def handle(self, *args, **options):
        product_id = options.get('product_id')

        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                product.update_rating()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Synced rating for Product #{product.id} '{product.name}': {product.rating}★ ({product.num_reviews} reviews)"
                    )
                )
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Product #{product_id} not found."))
            return

        products = Product.objects.all()
        synced_count = 0
        for p in products:
            p.update_rating()
            synced_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully synced rating aggregations for {synced_count} product(s)."
            )
        )
