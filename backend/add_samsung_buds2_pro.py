import os, time
from PIL import Image, ImageChops, ImageEnhance
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

brain_dir = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397"
files = [os.path.join(brain_dir, f) for f in os.listdir(brain_dir) if f.startswith('media__')]
files.sort(key=lambda f: os.path.getmtime(f), reverse=True)

latest_file = files[0]
print(f"Latest uploaded file (Samsung Galaxy Buds 2 Pro): {latest_file}")

dest_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'airpods'))
os.makedirs(dest_dir, exist_ok=True)

filename = "samsung-galaxy-buds2-pro.webp"
file_path = os.path.join(dest_dir, filename)

if os.path.exists(latest_file):
    img = Image.open(latest_file)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = bg
    else:
        img = img.convert('RGB')

    bg_white = Image.new('RGB', img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg_white)
    bbox = diff.getbbox()
    if bbox:
        l, u, r, d = bbox
        img = img.crop((max(0, l-5), max(0, u-5), min(img.width, r+5), min(img.height, d+5)))

    w, h = img.size
    target_h = 800
    target_w = int(target_h * (w / h))
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)

    img.save(file_path, 'WEBP', quality=95)
    print(f"[OK] Saved Samsung Galaxy Buds 2 Pro image to {file_path} ({img.size[0]}x{img.size[1]} px)")

# Category
cat, _ = Category.objects.get_or_create(slug="airpods", defaults={'name': "AirPods"})

rel_path = f"/images/products/airpods/{filename}"

product, created = Product.objects.get_or_create(
    name="Samsung Galaxy Buds 2 Pro",
    defaults={
        'category': cat,
        'brand': 'Samsung',
        'price': 149.00,
        'description': 'Original Samsung Galaxy Buds 2 Pro with 24-bit Hi-Fi Audio by AKG, Intelligent Active Noise Cancellation, 360 Audio, and IPX7 Water Resistance.',
        'image_url': rel_path,
        'rating': 4.8,
        'num_reviews': 110,
        'is_featured': True,
        'is_new': True,
        'stock_qty': 60,
        'specs': {
            "Sound": "24-bit Hi-Fi Sound Tuned by AKG",
            "ANC": "Intelligent Active Noise Cancellation",
            "Battery": "Up to 29 Hours Total Listening Time",
            "Water Resistance": "IPX7 Water & Sweat Resistant"
        }
    }
)

if not created:
    product.category = cat
    product.brand = 'Samsung'
    product.image_url = rel_path
    product.price = 149.00
    product.description = 'Original Samsung Galaxy Buds 2 Pro with 24-bit Hi-Fi Audio by AKG, Intelligent Active Noise Cancellation, 360 Audio, and IPX7 Water Resistance.'
    product.specs = {
        "Sound": "24-bit Hi-Fi Sound Tuned by AKG",
        "ANC": "Intelligent Active Noise Cancellation",
        "Battery": "Up to 29 Hours Total Listening Time",
        "Water Resistance": "IPX7 Water & Sweat Resistant"
    }
    product.save()

print(f"[OK] Product '{product.name}' (ID={product.id}) created under Category 'AirPods' with Brand 'Samsung'.")
