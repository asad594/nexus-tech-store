import os
from PIL import Image
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

phones_category, _ = Category.objects.get_or_create(slug='phones', defaults={'name': 'Phones'})

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
os.makedirs(DEST_DIR, exist_ok=True)

path1 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504494258.png" # 403 x 153 (6 phones)
path2 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504494280.png" # 703 x 297 (20 phones, 2 rows of 10)
path3 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504494290.png" # 402 x 207 (3 phones)
path4 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504494293.png" # 264 x 214 (2 phones)
path5 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504494300.png" # 423 x 231 (3 phones)

im1 = Image.open(path1)
im2 = Image.open(path2)
im3 = Image.open(path3)
im4 = Image.open(path4)
im5 = Image.open(path5)

def save_and_create_product(crop_img, filename, model_name, price, specs_str):
    w, h = crop_img.size
    max_dim = max(w, h) + 20
    padded = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))
    padded.paste(crop_img, ((max_dim - w) // 2, (max_dim - h) // 2))
    
    file_path = os.path.join(DEST_DIR, filename)
    padded.save(file_path, 'WEBP', quality=95)
    
    rel_path = f"/images/products/phones/{filename}"
    
    prod, created = Product.objects.update_or_create(
        name=model_name,
        defaults={
            'category': phones_category,
            'brand': 'Samsung',
            'price': price,
            'stock_qty': 25,
            'image_url': rel_path,
            'specs': {
                'screen': specs_str.split(', ')[1] if len(specs_str.split(', ')) > 1 else 'AMOLED Display',
                'processor': specs_str.split(', ')[2] if len(specs_str.split(', ')) > 2 else 'Exynos / Snapdragon',
                'storage': specs_str.split(', ')[0],
                'camera': specs_str.split(', ')[3] if len(specs_str.split(', ')) > 3 else 'Triple Camera System'
            }
        }
    )
    print(f"[OK] {'Created' if created else 'Updated'} {model_name} -> {filename} ({w}x{h} px)")

# --- Image 1: S20, S20+, S20 Ultra, S20 FE, S21, S21+ ---
img1_items = [
    ("Samsung Galaxy S20", "galaxy-s20.webp", 499, "128GB, Dynamic AMOLED 6.2\", Exynos 990 / Snapdragon 865, Triple 12MP+64MP"),
    ("Samsung Galaxy S20+", "galaxy-s20-plus.webp", 549, "128GB, Dynamic AMOLED 6.7\", Exynos 990 / Snapdragon 865, Quad Camera"),
    ("Samsung Galaxy S20 Ultra", "galaxy-s20-ultra.webp", 699, "128GB, Dynamic AMOLED 6.9\", Snapdragon 865, 108MP 100x Space Zoom"),
    ("Samsung Galaxy S20 FE", "galaxy-s20-fe.webp", 429, "128GB, Super AMOLED 6.5\", Snapdragon 865, Triple 12MP Camera"),
    ("Samsung Galaxy S21", "galaxy-s21.webp", 599, "128GB, Dynamic AMOLED 2X 6.2\", Exynos 2100 / Snapdragon 888, Triple 64MP"),
    ("Samsung Galaxy S21+", "galaxy-s21-plus.webp", 699, "128GB, Dynamic AMOLED 2X 6.7\", Exynos 2100 / Snapdragon 888, Triple 64MP"),
]

dx1 = 403 / 6
for i, (name, filename, price, specs) in enumerate(img1_items):
    x1 = int(i * dx1) + 2
    x2 = int((i + 1) * dx1) - 2
    crop_img = im1.crop((x1, 32, x2, 148))
    save_and_create_product(crop_img, filename, name, price, specs)

# --- Image 2 Row 1: S21 Ultra, S21 FE, S22, S22+, S22 Ultra, S23, S23+, S23 Ultra, S23 FE, S24 ---
img2_r1 = [
    ("Samsung Galaxy S21 Ultra", "galaxy-s21-ultra.webp", 799, "128GB, Dynamic AMOLED 2X 6.8\", Snapdragon 888, 108MP Quad Camera"),
    ("Samsung Galaxy S21 FE", "galaxy-s21-fe.webp", 479, "128GB, Dynamic AMOLED 2X 6.4\", Snapdragon 888, Triple 12MP Camera"),
    ("Samsung Galaxy S22", "galaxy-s22.webp", 649, "128GB, Dynamic AMOLED 2X 6.1\", Snapdragon 8 Gen 1, 50MP Triple Camera"),
    ("Samsung Galaxy S22+", "galaxy-s22-plus.webp", 749, "128GB, Dynamic AMOLED 2X 6.6\", Snapdragon 8 Gen 1, 50MP Triple Camera"),
    ("Samsung Galaxy S22 Ultra", "galaxy-s22-ultra.webp", 899, "128GB, Dynamic AMOLED 2X 6.8\", S-Pen Built-in, 108MP Quad Camera"),
    ("Samsung Galaxy S23", "galaxy-s23.webp", 699, "128GB, Dynamic AMOLED 2X 6.1\", Snapdragon 8 Gen 2, 50MP Triple Camera"),
    ("Samsung Galaxy S23+", "galaxy-s23-plus.webp", 849, "256GB, Dynamic AMOLED 2X 6.6\", Snapdragon 8 Gen 2, 50MP Triple Camera"),
    ("Samsung Galaxy S23 Ultra", "galaxy-s23-ultra.webp", 999, "256GB, Dynamic AMOLED 2X 6.8\", Snapdragon 8 Gen 2, 200MP Quad Camera"),
    ("Samsung Galaxy S23 FE", "galaxy-s23-fe.webp", 549, "128GB, Dynamic AMOLED 2X 6.4\", Exynos 2200, 50MP Triple Camera"),
    ("Samsung Galaxy S24", "galaxy-s24.webp", 799, "128GB, Dynamic AMOLED 2X 6.2\", Exynos 2400 / Snapdragon 8 Gen 3, Galaxy AI"),
]

dx2 = 703 / 10
for i, (name, filename, price, specs) in enumerate(img2_r1):
    x1 = int(i * dx2) + 2
    x2 = int((i + 1) * dx2) - 2
    crop_img = im2.crop((x1, 25, x2, 130))
    save_and_create_product(crop_img, filename, name, price, specs)

# --- Image 2 Row 2: S24+, S24 Ultra, S24 FE, S25, S25+, S25 Edge, S25 Ultra, S26, S26+, S26 Ultra ---
img2_r2 = [
    ("Samsung Galaxy S24+", "galaxy-s24-plus.webp", 999, "256GB, Dynamic AMOLED 2X 6.7\", Exynos 2400 / Snapdragon 8 Gen 3, Galaxy AI"),
    ("Samsung Galaxy S24 Ultra", "galaxy-s24-ultra.webp", 1299, "256GB, Titanium Frame 6.8\", Snapdragon 8 Gen 3, 200MP Quad Camera"),
    ("Samsung Galaxy S24 FE", "galaxy-s24-fe.webp", 649, "128GB, Dynamic AMOLED 2X 6.7\", Exynos 2400e, Galaxy AI, 50MP Triple"),
    ("Samsung Galaxy S25", "galaxy-s25.webp", 849, "128GB, Dynamic AMOLED 2X 6.2\", Snapdragon 8 Elite, Galaxy AI"),
    ("Samsung Galaxy S25+", "galaxy-s25-plus.webp", 1049, "256GB, Dynamic AMOLED 2X 6.7\", Snapdragon 8 Elite, Galaxy AI"),
    ("Samsung Galaxy S25 Edge", "galaxy-s25-edge.webp", 1099, "256GB, Curved Edge Display 6.7\", Snapdragon 8 Elite, Dual 50MP Camera"),
    ("Samsung Galaxy S25 Ultra", "galaxy-s25-ultra.webp", 1349, "256GB, Titanium 6.9\", Snapdragon 8 Elite, 200MP Quad Camera"),
    ("Samsung Galaxy S26", "galaxy-s26.webp", 899, "128GB, Dynamic AMOLED 3X 6.3\", Snapdragon 8 Gen 4, Next-Gen AI"),
    ("Samsung Galaxy S26+", "galaxy-s26-plus.webp", 1099, "256GB, Dynamic AMOLED 3X 6.8\", Snapdragon 8 Gen 4, Next-Gen AI"),
    ("Samsung Galaxy S26 Ultra", "galaxy-s26-ultra.webp", 1399, "256GB, Titanium 6.9\", Snapdragon 8 Gen 4, 200MP Quad + Periscope Zoom"),
]

for i, (name, filename, price, specs) in enumerate(img2_r2):
    x1 = int(i * dx2) + 2
    x2 = int((i + 1) * dx2) - 2
    crop_img = im2.crop((x1, 150, x2, 285))
    save_and_create_product(crop_img, filename, name, price, specs)

# --- Image 3: Galaxy A25, Galaxy A15 5G, Galaxy A15 ---
img3_items = [
    ("Samsung Galaxy A25", "galaxy-a25.webp", 299, "128GB, Super AMOLED 120Hz 6.5\", Exynos 1280, 50MP OIS Camera"),
    ("Samsung Galaxy A15 5G", "galaxy-a15-5g.webp", 199, "128GB, Super AMOLED 90Hz 6.5\", Dimensity 6100+, 50MP Triple Camera"),
    ("Samsung Galaxy A15", "galaxy-a15.webp", 169, "128GB, Super AMOLED 90Hz 6.5\", Helio G99, 50MP Triple Camera"),
]

dx3 = 402 / 3
for i, (name, filename, price, specs) in enumerate(img3_items):
    x1 = int(i * dx3) + 5
    x2 = int((i + 1) * dx3) - 5
    crop_img = im3.crop((x1, 15, x2, 175))
    save_and_create_product(crop_img, filename, name, price, specs)

# --- Image 4: Galaxy A05s, Galaxy A05 ---
img4_items = [
    ("Samsung Galaxy A05s", "galaxy-a05s.webp", 139, "64GB, PLS LCD 90Hz 6.7\", Snapdragon 680, 50MP Triple Camera"),
    ("Samsung Galaxy A05", "galaxy-a05.webp", 119, "64GB, PLS LCD 6.7\", MediaTek Helio G85, 50MP Dual Camera"),
]

dx4 = 264 / 2
for i, (name, filename, price, specs) in enumerate(img4_items):
    x1 = int(i * dx4) + 5
    x2 = int((i + 1) * dx4) - 5
    crop_img = im4.crop((x1, 15, x2, 175))
    save_and_create_product(crop_img, filename, name, price, specs)

# --- Image 5: Galaxy F34, Galaxy Z Fold5, Galaxy Z Flip5 ---
img5_items = [
    ("Samsung Galaxy F34", "galaxy-f34.webp", 249, "128GB, Super AMOLED 120Hz 6.5\", Exynos 1280, 50MP OIS Camera"),
    ("Samsung Galaxy Z Fold5", "galaxy-z-fold5.webp", 1499, "256GB, Foldable Dynamic AMOLED 2X 7.6\", Snapdragon 8 Gen 2, S-Pen Support"),
    ("Samsung Galaxy Z Flip5", "galaxy-z-flip5.webp", 899, "256GB, Foldable Dynamic AMOLED 2X 6.7\", Flex Window Cover, Snapdragon 8 Gen 2"),
]

dx5 = 423 / 3
for i, (name, filename, price, specs) in enumerate(img5_items):
    x1 = int(i * dx5) + 5
    x2 = int((i + 1) * dx5) - 5
    crop_img = im5.crop((x1, 15, x2, 190))
    save_and_create_product(crop_img, filename, name, price, specs)

print("\n=== ALL 34 SAMSUNG GALAXY MODELS CROPPED & ADDED TO STORE ===")
