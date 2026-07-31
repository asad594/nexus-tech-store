import os
import requests
import re
import urllib.parse
from PIL import Image, ImageChops
import io
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')
os.makedirs(DEST_DIR, exist_ok=True)

phones_category = Category.objects.get(slug='phones')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

IPHONES = [
    ("iPhone X", "iphone-x.webp", "iPhone X 64GB space gray isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone XS", "iphone-xs.webp", "iPhone XS 64GB silver isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone XS Max", "iphone-xs-max.webp", "iPhone XS Max gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone XR", "iphone-xr.webp", "iPhone XR blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 11", "iphone-11.webp", "iPhone 11 purple isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 11 Pro", "iphone-11-pro.webp", "iPhone 11 Pro midnight green isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 11 Pro Max", "iphone-11-pro-max.webp", "iPhone 11 Pro Max gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone SE (2nd Gen)", "iphone-se-2.webp", "iPhone SE 2020 red isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12 Mini", "iphone-12-mini.webp", "iPhone 12 Mini green isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12", "iphone-12.webp", "iPhone 12 blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12 Pro", "iphone-12-pro.webp", "iPhone 12 Pro gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 12 Pro Max", "iphone-12-pro-max.webp", "iPhone 12 Pro Max pacific blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13 Mini", "iphone-13-mini.webp", "iPhone 13 Mini pink isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13", "iphone-13.webp", "iPhone 13 midnight isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13 Pro", "iphone-13-pro.webp", "iPhone 13 Pro sierra blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 13 Pro Max", "iphone-13-pro-max.webp", "iPhone 13 Pro Max gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone SE (3rd Gen)", "iphone-se-3.webp", "iPhone SE 2022 midnight isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14", "iphone-14.webp", "iPhone 14 yellow isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14 Plus", "iphone-14-plus.webp", "iPhone 14 Plus blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14 Pro", "iphone-14-pro.webp", "iPhone 14 Pro gold isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 14 Pro Max", "iphone-14-pro-max.webp", "iPhone 14 Pro Max deep purple isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15", "iphone-15.webp", "iPhone 15 yellow isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15 Plus", "iphone-15-plus.webp", "iPhone 15 Plus pink isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15 Pro", "iphone-15-pro.webp", "iPhone 15 Pro natural titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 15 Pro Max", "iphone-15-pro-max.webp", "iPhone 15 Pro Max blue titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16", "iphone-16.webp", "iPhone 16 pink isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16 Plus", "iphone-16-plus.webp", "iPhone 16 Plus teal isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16 Pro", "iphone-16-pro.webp", "iPhone 16 Pro desert titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16 Pro Max", "iphone-16-pro-max.webp", "iPhone 16 Pro Max natural titanium isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 16e", "iphone-16e.webp", "iPhone 16e white isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 17", "iphone-17.webp", "iPhone 17 lavender isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("iPhone 17 Pro", "iphone-17-pro.webp", "iPhone 17 Pro dark blue isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
]

ALLOWED_DOMAINS = ['bbystatic.com', 'bhphotovideo.com', 'laptopmedia.com', 'notebookcheck.net', 'mos.cms.futurecdn.net', '1worldsync.com', 'ssl-images-amazon.com', 'media-amazon.com', 'apple.com']

def fetch_iphone_retail_photo(query):
    search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None, None
        murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text) or re.findall(r'"murl":"(https?://[^"]+)"', r.text)

        for u in murls[:30]:
            u_lower = u.lower()
            if not any(dom in u_lower for dom in ALLOWED_DOMAINS):
                continue
            if any(bad in u_lower for bad in ['logo', 'banner', 'icon', 'cookielaw', 'wallpaper', 'vector', 'illustration', 'stock', 'freepik', 'shutterstock', 'avatar', 'horoscope', 'sign', 'hand', 'desk', 'person', 'man', 'woman', 'ripe-apple', 'fruit', 'pixabay']):
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

print("=== FETCHING FULL HIGH-RES RETAIL PHOTOS FOR ALL IPHONES ===\n")

success_count = 0
for idx, (name, filename, query) in enumerate(IPHONES, 1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/{len(IPHONES)}] Processing {name}...")

    src_url, img = fetch_iphone_retail_photo(query)
    if not img:
        src_url, img = fetch_iphone_retail_photo(f"{name} isolated white background site:bbystatic.com OR site:bhphotovideo.com")

    if img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
            img = bg
        else:
            img = img.convert('RGB')

        # Trim white margins tightly
        bg_white = Image.new('RGB', img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg_white)
        bbox = diff.getbbox()
        if bbox:
            l, u_b, r, d_b = bbox
            img = img.crop((max(0, l-2), max(0, u_b-2), min(img.width, r+2), min(img.height, d_b+2)))

        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        img.save(file_path, 'WEBP', quality=95)

        rel_path = f"/images/products/phones/{filename}"
        Product.objects.filter(name=name).update(image_url=rel_path)

        success_count += 1
        print(f"  [OK] Saved {name} -> {filename} ({img.size[0]}x{img.size[1]} px, {os.path.getsize(file_path)//1024} KB)")
        print(f"       URL: {src_url[:80]}...\n")

print(f"=== FINISHED! {success_count}/{len(IPHONES)} HIGH-RES IPHONE STANDALONE PHOTOS UPDATED ===")
