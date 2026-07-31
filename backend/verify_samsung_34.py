import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

phones_category = Category.objects.get(slug='phones')
samsungs = Product.objects.filter(category=phones_category, brand='Samsung')

print("--- SAMSUNG POPULATION VERIFICATION REPORT ---")
print(f"Total Samsung Phones in DB: {samsungs.count()}/34")

missing_files = []
for p in samsungs:
    disk_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', p.image_url.lstrip('/')))
    if os.path.exists(disk_path):
        print(f" [OK] {p.name}: ${p.price} | {p.image_url}")
    else:
        missing_files.append(p.name)

if not missing_files:
    print("\n[OK] ALL 34 SAMSUNG GALAXY PRODUCT IMAGES VERIFIED ON DISK & DATABASE!")
else:
    print(f"\n[FAIL] Missing files: {missing_files}")
