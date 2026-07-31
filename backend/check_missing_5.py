import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

for p in Product.objects.all():
    if p.image_url:
        disk_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', p.image_url.lstrip('/')))
        if not os.path.exists(disk_path):
            print(f"Missing: id={p.id} | name={p.name} | category={p.category.name} | url={p.image_url}")
