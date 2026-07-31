import os
from PIL import Image, ImageChops, ImageEnhance
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

src_path = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785512016142.png"
DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
filename = "galaxy-s26-ultra.webp"

# 1. Process and save the high-res image for Samsung Galaxy S26 Ultra
if os.path.exists(src_path):
    img = Image.open(src_path)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = bg
    else:
        img = img.convert('RGB')

    # Trim white borders tightly
    bg_white = Image.new('RGB', img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg_white)
    bbox = diff.getbbox()
    if bbox:
        l, u, r, d = bbox
        img = img.crop((max(0, l-3), max(0, u-3), min(img.width, r+3), min(img.height, d+3)))

    # Resize up to HD 800px
    w, h = img.size
    target_h = 800
    target_w = int(target_h * (w / h))
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)

    file_path = os.path.join(DEST_DIR, filename)
    img.save(file_path, 'WEBP', quality=95)

    rel_path = f"/images/products/phones/{filename}"
    Product.objects.filter(name="Samsung Galaxy S26 Ultra").update(image_url=rel_path)
    print(f"[OK] Updated Samsung Galaxy S26 Ultra photo -> {filename} ({img.size[0]}x{img.size[1]} px)")

# 2. Delete Samsung Galaxy S26+ card from DB
deleted_count, _ = Product.objects.filter(name="Samsung Galaxy S26+").delete()
print(f"[OK] Deleted Samsung Galaxy S26+ card from store database ({deleted_count} product deleted).")

print("\n=== S26 ULTRA PHOTO UPDATED & S26+ CARD REMOVED FROM STORE ===")
