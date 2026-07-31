import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

phones_cat = Category.objects.get(slug='phones')
phones = Product.objects.filter(category=phones_cat)

print(f"Total phones in database: {phones.count()}")
for p in phones:
    print(f"- id={p.id}: {p.name} | brand={p.brand} | price=${p.price} | img={p.image_url}")
