import os
import requests
import re
import urllib.parse
from PIL import Image
import io
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
os.makedirs(DEST_DIR, exist_ok=True)

phones_category, _ = Category.objects.get_or_create(slug='phones', defaults={'name': 'Phones'})

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

IPHONE_MODELS = [
    # Chart 1
    ("iPhone X", "iphone-x.webp", 599, "64GB, Super Retina OLED 5.8\", A11 Bionic, Dual 12MP Camera", "Apple iPhone X space gray isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone XS", "iphone-xs.webp", 649, "64GB, Super Retina OLED 5.8\", A12 Bionic, Dual 12MP Camera", "Apple iPhone XS silver isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone XS Max", "iphone-xs-max.webp", 699, "64GB, Super Retina OLED 6.5\", A12 Bionic, Dual 12MP Camera", "Apple iPhone XS Max gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),

    # Chart 2 - Row 1
    ("iPhone XR", "iphone-xr.webp", 499, "64GB, Liquid Retina LCD 6.1\", A12 Bionic, 12MP Camera", "Apple iPhone XR blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 11", "iphone-11.webp", 549, "64GB, Liquid Retina LCD 6.1\", A13 Bionic, Dual 12MP Camera", "Apple iPhone 11 purple isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 11 Pro", "iphone-11-pro.webp", 699, "64GB, Super Retina XDR OLED 5.8\", A13 Bionic, Triple 12MP", "Apple iPhone 11 Pro midnight green isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 11 Pro Max", "iphone-11-pro-max.webp", 749, "64GB, Super Retina XDR OLED 6.5\", A13 Bionic, Triple 12MP", "Apple iPhone 11 Pro Max gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone SE (2nd Gen)", "iphone-se-2.webp", 399, "64GB, Retina HD 4.7\", A13 Bionic, 12MP Camera", "Apple iPhone SE 2020 red isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12 Mini", "iphone-12-mini.webp", 599, "64GB, Super Retina XDR OLED 5.4\", A14 Bionic, Dual 12MP", "Apple iPhone 12 Mini green isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12", "iphone-12.webp", 649, "128GB, Super Retina XDR OLED 6.1\", A14 Bionic, Dual 12MP", "Apple iPhone 12 blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12 Pro", "iphone-12-pro.webp", 799, "128GB, Super Retina XDR OLED 6.1\", A14 Bionic, Triple 12MP + LiDAR", "Apple iPhone 12 Pro gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12 Pro Max", "iphone-12-pro-max.webp", 899, "128GB, Super Retina XDR OLED 6.7\", A14 Bionic, Triple 12MP + LiDAR", "Apple iPhone 12 Pro Max pacific blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13 Mini", "iphone-13-mini.webp", 699, "128GB, Super Retina XDR OLED 5.4\", A15 Bionic, Dual 12MP", "Apple iPhone 13 Mini pink isolated white background site:bhphotovideo.com OR site:bestbuy.com"),

    # Chart 2 - Row 2
    ("iPhone 13", "iphone-13.webp", 749, "128GB, Super Retina XDR OLED 6.1\", A15 Bionic, Dual 12MP", "Apple iPhone 13 midnight isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13 Pro", "iphone-13-pro.webp", 899, "128GB, ProMotion 120Hz OLED 6.1\", A15 Bionic, Triple 12MP", "Apple iPhone 13 Pro sierra blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13 Pro Max", "iphone-13-pro-max.webp", 999, "128GB, ProMotion 120Hz OLED 6.7\", A15 Bionic, Triple 12MP", "Apple iPhone 13 Pro Max gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone SE (3rd Gen)", "iphone-se-3.webp", 429, "64GB, Retina HD 4.7\", A15 Bionic, 5G, 12MP Camera", "Apple iPhone SE 2022 midnight isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14", "iphone-14.webp", 799, "128GB, Super Retina XDR OLED 6.1\", A15 Bionic, Dual 12MP", "Apple iPhone 14 yellow isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14 Plus", "iphone-14-plus.webp", 899, "128GB, Super Retina XDR OLED 6.7\", A15 Bionic, Dual 12MP", "Apple iPhone 14 Plus blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14 Pro", "iphone-14-pro.webp", 999, "128GB, Dynamic Island 120Hz OLED 6.1\", A16 Bionic, 48MP Triple Camera", "Apple iPhone 14 Pro gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14 Pro Max", "iphone-14-pro-max.webp", 1099, "128GB, Dynamic Island 120Hz OLED 6.7\", A16 Bionic, 48MP Triple Camera", "Apple iPhone 14 Pro Max deep purple isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15", "iphone-15.webp", 799, "128GB, Dynamic Island 6.1\", USB-C, A16 Bionic, 48MP Dual Camera", "Apple iPhone 15 yellow isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15 Plus", "iphone-15-plus.webp", 899, "128GB, Dynamic Island 6.7\", USB-C, A16 Bionic, 48MP Dual Camera", "Apple iPhone 15 Plus pink isolated white background site:bhphotovideo.com OR site:bestbuy.com"),

    # Chart 2 - Row 3
    ("iPhone 15 Pro", "iphone-15-pro.webp", 999, "128GB, Titanium 6.1\", A17 Pro, 48MP Triple Camera, Action Button", "Apple iPhone 15 Pro natural titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15 Pro Max", "iphone-15-pro-max.webp", 1199, "256GB, Titanium 6.7\", A17 Pro, 5x Telephoto 48MP, Action Button", "Apple iPhone 15 Pro Max blue titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16", "iphone-16.webp", 829, "128GB, Dynamic Island 6.1\", A18 Chip, Camera Control, 48MP Dual", "Apple iPhone 16 pink isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16 Plus", "iphone-16-plus.webp", 929, "128GB, Dynamic Island 6.7\", A18 Chip, Camera Control, 48MP Dual", "Apple iPhone 16 Plus teal isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16 Pro", "iphone-16-pro.webp", 999, "128GB, Titanium 6.3\", A18 Pro, 48MP Fusion Triple Camera, 4K 120fps", "Apple iPhone 16 Pro desert titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16 Pro Max", "iphone-16-pro-max.webp", 1199, "256GB, Titanium 6.9\", A18 Pro, 48MP Fusion Triple Camera, 5x Telephoto", "Apple iPhone 16 Pro Max natural titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16e", "iphone-16e.webp", 599, "128GB, OLED 6.1\", A18 Chip, Apple Intelligence, Single 48MP Camera", "Apple iPhone 16e white isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 17", "iphone-17.webp", 849, "128GB, 120Hz ProMotion OLED 6.3\", A19 Chip, 48MP Dual Camera", "Apple iPhone 17 lavender isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 17 Pro", "iphone-17-pro.webp", 1049, "256GB, Aluminum Unibody 6.3\", A19 Pro, Triple 48MP Camera System", "Apple iPhone 17 Pro dark blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 17 Pro Max", "iphone-17-pro-max.webp", 1249, "256GB, Aluminum Unibody 6.9\", A19 Pro, Triple 48MP Camera System", "Apple iPhone 17 Pro Max orange isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone Air", "iphone-air.webp", 999, "256GB, Ultra-Thin Design 5mm, 120Hz OLED 6.6\", A19 Chip, 48MP Camera", "Apple iPhone Air ultra thin silver isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
]

def fetch_iphone_photo(query):
    search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None, None
        murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text) or re.findall(r'"murl":"(https?://[^"]+)"', r.text)

        for u in murls[:30]:
            u_lower = u.lower()
            if any(bad in u_lower for bad in ['logo', 'banner', 'icon', 'cookielaw', 'wallpaper', 'vector', 'illustration', 'stock', 'freepik', 'shutterstock', 'avatar', 'horoscope', 'sign', 'hand', 'desk', 'person', 'man', 'woman']):
                continue
            if not any(ext in u_lower for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                continue

            try:
                resp = requests.get(u, headers=HEADERS, timeout=8)
                if resp.status_code == 200 and len(resp.content) > 15000:
                    img = Image.open(io.BytesIO(resp.content))
                    w, h = img.size
                    if w >= 300 and h >= 300 and 0.4 <= (w / h) <= 2.2:
                        return u, img
            except Exception:
                continue
    except Exception as e:
        print(f"Error fetching: {e}")
    return None, None

print(f"=== POPULATING ALL {len(IPHONE_MODELS)} IPHONE MODELS IN STORE ===\n")

success_count = 0
for idx, (name, filename, price, specs_str, query) in enumerate(IPHONE_MODELS, 1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/{len(IPHONE_MODELS)}] Processing {name} (${price})...")

    src_url, img = fetch_iphone_photo(query)
    if not img:
        src_url, img = fetch_iphone_photo(f"Apple {name} back view white background isolated")

    if img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
            img = bg
        else:
            img = img.convert('RGB')

        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        img.save(file_path, 'WEBP', quality=95)

        rel_path = f"/images/products/phones/{filename}"
        
        # Create or update Product record in DB
        prod, created = Product.objects.update_or_create(
            name=name,
            defaults={
                'category': phones_category,
                'brand': 'Apple',
                'price': price,
                'stock_qty': 25,
                'image_url': rel_path,
                'specs': {
                    'screen': specs_str.split(', ')[1] if len(specs_str.split(', ')) > 1 else 'Retina Display',
                    'processor': specs_str.split(', ')[2] if len(specs_str.split(', ')) > 2 else 'Apple Bionic',
                    'storage': specs_str.split(', ')[0],
                    'camera': specs_str.split(', ')[3] if len(specs_str.split(', ')) > 3 else 'Advanced Camera System'
                }
            }
        )

        success_count += 1
        print(f"  [OK] {'Created' if created else 'Updated'} {name} -> {filename} ({img.size[0]}x{img.size[1]} px, {os.path.getsize(file_path)//1024} KB)")
        print(f"       URL: {src_url[:80]}...\n")
    else:
        print(f"  [FAIL] Failed for {name}\n")

print(f"=== FINISHED! {success_count}/{len(IPHONE_MODELS)} IPHONE MODELS ADDED & APPLIED TO STORE ===")
