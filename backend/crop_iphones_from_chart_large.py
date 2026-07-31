import os
from PIL import Image, ImageChops
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
os.makedirs(DEST_DIR, exist_ok=True)

path1 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785506096465.png" # 174 x 133
path2 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785506104183.png" # 618 x 385

im1 = Image.open(path1)
im2 = Image.open(path2)

def process_and_save_crop(crop_img, filename, model_name):
    # Convert to RGB
    if crop_img.mode in ('RGBA', 'LA') or (crop_img.mode == 'P' and 'transparency' in crop_img.info):
        bg = Image.new('RGB', crop_img.size, (255, 255, 255))
        bg.paste(crop_img, mask=crop_img.split()[3] if crop_img.mode == 'RGBA' else None)
        crop_img = bg
    else:
        crop_img = crop_img.convert('RGB')

    # Find bounding box of non-background content
    # The background of these images is slightly off-white (paper texture) ~ (235, 235, 235)
    # We create a tight crop around the phone body
    bg_ref = Image.new('RGB', crop_img.size, (240, 238, 236))
    diff = ImageChops.difference(crop_img, bg_ref)
    bbox = diff.getbbox()

    if bbox:
        l, u, r, d = bbox
        crop_img = crop_img.crop((l, u, r, d))

    # Resize up to 450px height for ultra-sharp card display
    w, h = crop_img.size
    aspect = w / h if h > 0 else 1.0
    target_h = 450
    target_w = int(target_h * aspect)

    resized = crop_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Put onto clean white canvas with minimal 8px padding
    canvas_w = target_w + 16
    canvas_h = target_h + 16
    canvas = Image.new('RGB', (canvas_w, canvas_h), (255, 255, 255))
    canvas.paste(resized, (8, 8))

    file_path = os.path.join(DEST_DIR, filename)
    canvas.save(file_path, 'WEBP', quality=95)

    rel_path = f"/images/products/phones/{filename}"
    Product.objects.filter(name=model_name).update(image_url=rel_path)
    print(f"[OK] Saved large iPhone crop {model_name} -> {filename} ({canvas_w}x{canvas_h} px)")

# Chart 1: 3 phones side by side
# Width = 174, Height = 133. Phone bodies are at top y: 5 to 88
c1_crops = [
    ("iPhone X", "iphone-x.webp", (5, 5, 58, 88)),
    ("iPhone XS", "iphone-xs.webp", (62, 5, 118, 88)),
    ("iPhone XS Max", "iphone-xs-max.webp", (122, 5, 170, 88)),
]

for name, filename, box in c1_crops:
    crop_img = im1.crop(box)
    process_and_save_crop(crop_img, filename, name)

# Chart 2: 618 x 385
# Row 1: y from 8 to 94 (XR, 11, 11 Pro, 11 Pro Max, SE 2, 12 Mini, 12, 12 Pro, 12 Pro Max, 13 Mini) - 10 items
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

dx1 = 618 / 10
for i, (name, filename) in enumerate(r1_names):
    x1 = int(i * dx1) + 2
    x2 = int((i + 1) * dx1) - 2
    crop_img = im2.crop((x1, 8, x2, 94))
    process_and_save_crop(crop_img, filename, name)

# Row 2: y from 125 to 212 (13, 13 Pro, 13 Pro Max, SE 3, 14, 14 Plus, 14 Pro, 14 Pro Max, 15, 15 Plus) - 10 items
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

dx2 = 618 / 10
for i, (name, filename) in enumerate(r2_names):
    x1 = int(i * dx2) + 2
    x2 = int((i + 1) * dx2) - 2
    crop_img = im2.crop((x1, 125, x2, 212))
    process_and_save_crop(crop_img, filename, name)

# Row 3: y from 242 to 335 (15 Pro, 15 Pro Max, 16, 16 Plus, 16 Pro, 16 Pro Max, 16e, 17, 17 Pro, 17 Pro Max, Air) - 11 items
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

dx3 = 618 / 11
for i, (name, filename) in enumerate(r3_names):
    x1 = int(i * dx3) + 2
    x2 = int((i + 1) * dx3) - 2
    crop_img = im2.crop((x1, 242, x2, 335))
    process_and_save_crop(crop_img, filename, name)

print("\n=== ALL 34 IPHONES CROPPED FROM USER CHARTS & UPSCALED TO LARGE DISPLAY SIZE ===")
