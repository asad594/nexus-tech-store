import os
from PIL import Image
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
    
    file_path = os.path.join(DEST_DIR, filename)
    img.save(file_path, 'WEBP', quality=95)
    
    rel_path = f"/images/products/phones/{filename}"
    Product.objects.filter(name=model_name).update(image_url=rel_path)
    print(f"[OK] Updated {model_name} image with high-res photo -> {filename} ({img.size[0]}x{img.size[1]} px, {os.path.getsize(file_path)//1024} KB)")

process_and_save(air_src, "iphone-air.webp", "iPhone Air")
process_and_save(promax_src, "iphone-17-pro-max.webp", "iPhone 17 Pro Max")

print("\n=== HIGH RESOLUTION PRODUCT IMAGES UPDATED IN DB AND DISK! ===")
