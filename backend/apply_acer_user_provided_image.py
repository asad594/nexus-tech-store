import os
from PIL import Image
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

SRC_IMG = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495098270.png"
DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'laptops')
os.makedirs(DEST_DIR, exist_ok=True)

ACER_FILENAMES = [
    ("Acer Aspire 3", "acer-aspire-3.webp"),
    ("Acer Aspire 5", "acer-aspire-5.webp"),
    ("Acer Aspire 7", "acer-aspire-7.webp"),
    ("Acer Swift Go 14", "acer-swift-go-14.webp"),
    ("Acer Swift X 14", "acer-swift-x-14.webp"),
    ("Acer Swift Edge 16", "acer-swift-edge-16.webp"),
    ("Acer Nitro V 15", "acer-nitro-v-15.webp"),
    ("Acer Nitro 16", "acer-nitro-16.webp"),
    ("Acer Predator Helios Neo 16", "acer-predator-helios-neo-16.webp"),
    ("Acer Predator Helios 18", "acer-predator-helios-18.webp"),
]

print("=== APPLYING USER PROVIDED ACER LAPTOP IMAGE TO ALL 10 ACER MODELS ===\n")

img = Image.open(SRC_IMG)
if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
    bg = Image.new('RGB', img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    img = bg
else:
    img = img.convert('RGB')

for idx, (name, filename) in enumerate(ACER_FILENAMES, 1):
    file_path = os.path.join(DEST_DIR, filename)
    img.save(file_path, 'WEBP', quality=95)
    
    rel_path = f"/images/products/laptops/{filename}"
    Product.objects.filter(name=name).update(image_url=rel_path)
    
    print(f"[{idx}/10] [OK] Applied image to {name} -> {filename} ({os.path.getsize(file_path)//1024} KB)")

print("\n=== FINISHED! ALL 10 ACER LAPTOPS UPDATED WITH USER'S IMAGE ===")
