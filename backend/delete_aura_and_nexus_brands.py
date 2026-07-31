import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product, Category

print("=== DELETING AURA AND NEXUS PRODUCTS AND BRANDS ===")

# Delete products with brand AURA, NEXUS, Aura, Nexus
deleted_products, _ = Product.objects.filter(brand__in=['AURA', 'NEXUS', 'Aura', 'Nexus']).delete()
print(f"[OK] Deleted {deleted_products} products with brand AURA / NEXUS.")

# Check remaining categories
for c in Category.objects.all():
    count = c.products.count()
    print(f"Category '{c.name}' now has {count} products.")
    if count == 0:
        c.delete()
        print(f"  -> Deleted empty category '{c.name}'")

print("\n=== FINISHED! AURA & NEXUS BRAND FILTERS & PRODUCTS REMOVED FROM STORE ===")
