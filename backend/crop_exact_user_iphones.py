import os
from PIL import Image
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
os.makedirs(DEST_DIR, exist_ok=True)

path1 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495191289.png"
path2 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495193880.png"

im1 = Image.open(path1) # 174 x 133 (X, XS, XS Max)
im2 = Image.open(path2) # 618 x 385 (Row 1: 10 phones, Row 2: 10 phones, Row 3: 11 phones)

def save_cropped_phone(crop_img, filename, model_name):
    # Add white padding around crop
    w, h = crop_img.size
    max_dim = max(w, h) + 20
    padded = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))
    padded.paste(crop_img, ((max_dim - w) // 2, (max_dim - h) // 2))
    
    file_path = os.path.join(DEST_DIR, filename)
    padded.save(file_path, 'WEBP', quality=95)
    
    rel_path = f"/images/products/phones/{filename}"
    Product.objects.filter(name=model_name).update(image_url=rel_path)
    print(f"[OK] Cropped & saved {model_name} -> {filename} ({w}x{h} px)")

# Chart 1: 3 phones side by side
# Width = 174, Height = 133. Phones are roughly top 10 to 90px
chart1_crops = [
    ("iPhone X", "iphone-x.webp", (5, 10, 58, 90)),
    ("iPhone XS", "iphone-xs.webp", (62, 10, 118, 90)),
    ("iPhone XS Max", "iphone-xs-max.webp", (122, 5, 170, 90)),
]

for name, filename, box in chart1_crops:
    crop_img = im1.crop(box)
    save_cropped_phone(crop_img, filename, name)

# Chart 2: 618 x 385
# Row 1: y from ~15 to ~105 (XR, 11, 11 Pro, 11 Pro Max, SE 2, 12 Mini, 12, 12 Pro, 12 Pro Max, 13 Mini) - 10 items
r1_names = [
    ("iPhone XR", "iphone-xr.webp"),
    ("iPhone 11", "iphone-11.webp"),
    ("iPhone 11 Pro", "iphone-11-pro.webp"),
    ("iPhone 11 Pro Max", "iphone-11-pro-max.webp"),
    ("iPhone SE (2nd Gen)", "iphone-se-2.webp"),
    ("iPhone 12 Mini", "iphone-12-mini.webp"),
    ("iPhone 12", "iphone-12.webp"),
    ("iPhone 12 Pro", "iphone-12-pro.webp"),
    ("iPhone 12 Pro Max", "iphone-12-pro-max.webp"),
    ("iPhone 13 Mini", "iphone-13-mini.webp"),
]

# Row 2: y from ~130 to ~225 (13, 13 Pro, 13 Pro Max, SE 3, 14, 14 Plus, 14 Pro, 14 Pro Max, 15, 15 Plus) - 10 items
r2_names = [
    ("iPhone 13", "iphone-13.webp"),
    ("iPhone 13 Pro", "iphone-13-pro.webp"),
    ("iPhone 13 Pro Max", "iphone-13-pro-max.webp"),
    ("iPhone SE (3rd Gen)", "iphone-se-3.webp"),
    ("iPhone 14", "iphone-14.webp"),
    ("iPhone 14 Plus", "iphone-14-plus.webp"),
    ("iPhone 14 Pro", "iphone-14-pro.webp"),
    ("iPhone 14 Pro Max", "iphone-14-pro-max.webp"),
    ("iPhone 15", "iphone-15.webp"),
    ("iPhone 15 Plus", "iphone-15-plus.webp"),
]

# Row 3: y from ~250 to ~345 (15 Pro, 15 Pro Max, 16, 16 Plus, 16 Pro, 16 Pro Max, 16e, 17, 17 Pro, 17 Pro Max, Air) - 11 items
r3_names = [
    ("iPhone 15 Pro", "iphone-15-pro.webp"),
    ("iPhone 15 Pro Max", "iphone-15-pro-max.webp"),
    ("iPhone 16", "iphone-16.webp"),
    ("iPhone 16 Plus", "iphone-16-plus.webp"),
    ("iPhone 16 Pro", "iphone-16-pro.webp"),
    ("iPhone 16 Pro Max", "iphone-16-pro-max.webp"),
    ("iPhone 16e", "iphone-16e.webp"),
    ("iPhone 17", "iphone-17.webp"),
    ("iPhone 17 Pro", "iphone-17-pro.webp"),
    ("iPhone 17 Pro Max", "iphone-17-pro-max.webp"),
    ("iPhone Air", "iphone-air.webp"),
]

# Crop Row 1 (10 items across 618 width -> dx ~ 61)
dx1 = 618 / 10
for i, (name, filename) in enumerate(r1_names):
    x1 = int(i * dx1) + 2
    x2 = int((i + 1) * dx1) - 2
    y1, y2 = 12, 105
    crop_img = im2.crop((x1, y1, x2, y2))
    save_cropped_phone(crop_img, filename, name)

# Crop Row 2 (10 items across 618 width -> dx ~ 61)
dx2 = 618 / 10
for i, (name, filename) in enumerate(r2_names):
    x1 = int(i * dx2) + 2
    x2 = int((i + 1) * dx2) - 2
    y1, y2 = 130, 225
    crop_img = im2.crop((x1, y1, x2, y2))
    save_cropped_phone(crop_img, filename, name)

# Crop Row 3 (11 items across 618 width -> dx ~ 56)
dx3 = 618 / 11
for i, (name, filename) in enumerate(r3_names):
    x1 = int(i * dx3) + 2
    x2 = int((i + 1) * dx3) - 2
    y1, y2 = 250, 345
    crop_img = im2.crop((x1, y1, x2, y2))
    save_cropped_phone(crop_img, filename, name)

print("\n=== ALL 34 IPHONES CROPPED FROM USER'S TEMPLATES & SAVED TO DISK & DB ===")
