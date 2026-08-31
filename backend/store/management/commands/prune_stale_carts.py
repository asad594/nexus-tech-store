"""
Management command to prune inactive/stale shopping cart items older than N days.
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from store.models import CartItem

class Command(BaseCommand):
    help = 'Prune old, abandoned shopping cart items to maintain clean database hygiene.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Age threshold in days for stale cart items (default: 30 days).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            help='Simulate deletion without committing changes to database.',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        cutoff_date = timezone.now() - timedelta(days=days)

        stale_items = CartItem.objects.filter(updated_at__lt=cutoff_date)
        count = stale_items.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"[DRY RUN] Found {count} stale cart items older than {days} days (cutoff: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}). None deleted."
                )
            )
            return

        deleted_count, _ = stale_items.delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {deleted_count} stale cart item(s) older than {days} days."
            )
        )
