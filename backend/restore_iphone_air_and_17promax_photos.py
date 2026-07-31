import os
from PIL import Image, ImageChops
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

air_src = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504754251.png"
promax_src = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504853120.png"

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')

def process_and_save(src_path, filename, model_name):
    img = Image.open(src_path)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = bg
    else:
        img = img.convert('RGB')
    
    # Trim white borders tightly if present
    bg_white = Image.new('RGB', img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg_white)
    bbox = diff.getbbox()
    if bbox:
        l, u, r, d = bbox
        img = img.crop((max(0, l-3), max(0, u-3), min(img.width, r+3), min(img.height, d+3)))

    file_path = os.path.join(DEST_DIR, filename)
    img.save(file_path, 'WEBP', quality=95)
    
    rel_path = f"/images/products/phones/{filename}"
    Product.objects.filter(name=model_name).update(image_url=rel_path)
    print(f"[OK] Restored high-res photo for {model_name} -> {filename} ({img.size[0]}x{img.size[1]} px)")

process_and_save(air_src, "iphone-air.webp", "iPhone Air")
process_and_save(promax_src, "iphone-17-pro-max.webp", "iPhone 17 Pro Max")

print("\n=== HIGH-RES PHOTOS RESTORED FOR IPHONE AIR & IPHONE 17 PRO MAX ===")
