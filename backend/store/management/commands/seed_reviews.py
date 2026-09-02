"""
Management command to seed realistic customer reviews for catalog products.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Product, Review

User = get_user_model()

SAMPLE_REVIEWS = [
    {
        "rating": 5,
        "comment": "Exceeded all my expectations! Ultra responsive, crisp display, and incredible battery life."
    },
    {
        "rating": 5,
        "comment": "Top-tier flagship craftsmanship. The futuristic aesthetics and build quality are unmatched."
    },
    {
        "rating": 4,
        "comment": "Great performance for everyday professional workload. Fast shipping and premium packaging."
    },
    {
        "rating": 5,
        "comment": "Best hardware investment I made this year. High performance and seamless setup."
    }
]

class Command(BaseCommand):
    help = 'Seed realistic sample reviews for store products to enrich customer feedback demonstrations.'

    def handle(self, *args, **options):
        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.WARNING("No products found in the catalog. Please run seed_data first."))
            return

        users = User.objects.filter(is_superuser=False)
        if not users.exists():
            # Create a test customer if none exists
            user, _ = User.objects.get_or_create(
                username='review_customer',
                defaults={
                    'email': 'customer@nexustech.io',
                    'name': 'Alex Mercer'
                }
            )
            users = [user]

        created_count = 0
        for product in products:
            for idx, user in enumerate(users[:len(SAMPLE_REVIEWS)]):
                sample = SAMPLE_REVIEWS[idx % len(SAMPLE_REVIEWS)]
                review, created = Review.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'rating': sample['rating'],
                        'comment': sample['comment']
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {created_count} new product review(s) across {products.count()} products."
            )
        )
