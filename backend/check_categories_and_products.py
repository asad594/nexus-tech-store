import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

print("=== CATEGORIES ===")
for c in Category.objects.all():
    print(f"- {c.id}: {c.name} (slug={c.slug})")

print("\n=== SAMPLES OF PRODUCTS ===")
for p in Product.objects.all()[:10]:
    print(f"- {p.id}: {p.name} | category={p.category.name} | image_url={p.image_url}")
