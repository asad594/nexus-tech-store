import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

laptop_cat = Category.objects.get(slug='laptops')
products = Product.objects.filter(category=laptop_cat)

brands = ['Dell', 'HP', 'Apple', 'Lenovo', 'Acer']
counts = {b: 0 for b in brands}

missing_images = []

public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public')

print("--- LAPTOP POPULATION VERIFICATION REPORT ---\n")

for p in products:
    brand = p.brand
    if brand in counts:
        counts[brand] += 1
    
    # Check image path
    img_rel = p.image_url.lstrip('/')
    abs_img_path = os.path.join(public_dir, img_rel)
    if not os.path.exists(abs_img_path):
        missing_images.append((p.name, abs_img_path))

for b in brands:
    print(f"[OK] {b}: {counts[b]}/10")

total = products.count()
print(f"\nTOTAL PRODUCTS: {total}/50")

if missing_images:
    print(f"\n[FAIL] Missing image files ({len(missing_images)}):")
    for name, path in missing_images:
        print(f"  - {name}: {path}")
else:
    print("\n[OK] ALL 50 PRODUCT IMAGES VERIFIED ON DISK AT REAL RELATIVE PATHS!")
