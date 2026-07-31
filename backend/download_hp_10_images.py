import os
import requests
import re
import urllib.parse
from PIL import Image
import io
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'laptops')
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

HP_TARGETS = [
    ("HP Spectre x360 14", "hp-spectre-x360-14.webp", "HP Spectre x360 14 2-in-1 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:notebookcheck.net"),
    ("HP Spectre x360 16", "hp-spectre-x360-16.webp", "HP Spectre x360 16 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:notebookcheck.net"),
    ("HP ENVY x360 14", "hp-envy-x360-14.webp", "HP ENVY x360 14 2-in-1 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP ENVY 16", "hp-envy-16.webp", "HP ENVY 16 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP Pavilion 15", "hp-pavilion-15.webp", "HP Pavilion 15 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP Pavilion Plus 14", "hp-pavilion-plus-14.webp", "HP Pavilion Plus 14 OLED laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP Victus 15", "hp-victus-15.webp", "HP Victus 15 gaming laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP OMEN 16", "hp-omen-16.webp", "HP OMEN 16 gaming laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP EliteBook 840 G11", "hp-elitebook-840-g11.webp", "HP EliteBook 840 G11 business laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("HP ProBook 450 G10", "hp-probook-450-g10.webp", "HP ProBook 450 G10 notebook isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
]

def fetch_hp_studio_photo(query):
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
                    if w >= 400 and h >= 300 and 0.8 <= (w / h) <= 2.2:
                        return u, img
            except Exception:
                continue
    except Exception as e:
        print(f"Error fetching: {e}")
    return None, None

print("=== FETCHING FRESH PRODUCT PHOTOGRAPHY FOR ALL 10 HP MODELS ===\n")

success_count = 0
for idx, (name, filename, query) in enumerate(HP_TARGETS, 1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/10] Processing {name}...")

    src_url, img = fetch_hp_studio_photo(query)
    if not img:
        src_url, img = fetch_hp_studio_photo(f"{name} laptop front view transparent png white background")

    if img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
            img = bg
        else:
            img = img.convert('RGB')

        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        img.save(file_path, 'WEBP', quality=95)

        rel_path = f"/images/products/laptops/{filename}"
        Product.objects.filter(name=name).update(image_url=rel_path)

        success_count += 1
        print(f"  [OK] Saved {filename} ({img.size[0]}x{img.size[1]} px, {os.path.getsize(file_path)//1024} KB)")
        print(f"       URL: {src_url[:80]}...\n")
    else:
        print(f"  [FAIL] Failed for {name}\n")

print(f"=== FINISHED! {success_count}/10 HP PRODUCT PHOTOS DOWNLOADED & APPLIED ===")
