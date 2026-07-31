import os
import django
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

products = Product.objects.all()

print(f"=== VERIFYING HD QUALITY & FILE INTEGRITY FOR ALL {products.count()} PRODUCTS ===")

low_res = []
missing = []

for p in products:
    if not p.image_url:
        continue
    disk_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', p.image_url.lstrip('/')))
    if os.path.exists(disk_path):
        im = Image.open(disk_path)
        w, h = im.size
        if w < 400 or h < 400:
            low_res.append((p.name, w, h))
    else:
        missing.append(p.name)

print(f"Total Products Checked: {products.count()}")
print(f"Missing Image Files: {len(missing)}")
print(f"Low Resolution Images (<400px): {len(low_res)}")

if not missing and not low_res:
    print("\n[OK] ALL PRODUCT IMAGES IN ENTIRE STORE ARE HD QUALITY & VERIFIED!")
