import os
from PIL import Image, ImageChops, ImageEnhance
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

src_path = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785513445113.png"
DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
filename = "galaxy-s21-ultra.webp"

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

    # Resize up to HD 800px height
    w, h = img.size
    target_h = 800
    target_w = int(target_h * (w / h))
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)

    file_path = os.path.join(DEST_DIR, filename)
    img.save(file_path, 'WEBP', quality=95)

    rel_path = f"/images/products/phones/{filename}"
    Product.objects.filter(name="Samsung Galaxy S21 Ultra").update(image_url=rel_path)
    print(f"[OK] Updated Samsung Galaxy S21 Ultra photo -> {filename} ({img.size[0]}x{img.size[1]} px)")

print("\n=== S21 ULTRA PRODUCT PHOTO UPDATED IN STORE DATABASE & DISK ===")
