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

ACER_TARGETS = [
    ("Acer Aspire 3", "acer-aspire-3.webp", "Acer Aspire 3 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Aspire 5", "acer-aspire-5.webp", "Acer Aspire 5 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Aspire 7", "acer-aspire-7.webp", "Acer Aspire 7 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Swift Go 14", "acer-swift-go-14.webp", "Acer Swift Go 14 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Swift X 14", "acer-swift-x-14.webp", "Acer Swift X 14 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Swift Edge 16", "acer-swift-edge-16.webp", "Acer Swift Edge 16 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Nitro V 15", "acer-nitro-v-15.webp", "Acer Nitro V 15 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Nitro 16", "acer-nitro-16.webp", "Acer Nitro 16 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Predator Helios Neo 16", "acer-predator-helios-neo-16.webp", "Acer Predator Helios Neo 16 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
    ("Acer Predator Helios 18", "acer-predator-helios-18.webp", "Acer Predator Helios 18 laptop front isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:laptopmedia.com"),
]

ALLOWED_DOMAINS = ['bbystatic.com', 'bhphotovideo.com', 'laptopmedia.com', 'acer.com', 'notebookcheck.net', 'mos.cms.futurecdn.net', '1worldsync.com', 'ssl-images-amazon.com', 'media-amazon.com']

def fetch_clean_acer_photo(query):
    search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None, None
        murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text) or re.findall(r'"murl":"(https?://[^"]+)"', r.text)

        for u in murls[:40]:
            u_lower = u.lower()
            if not any(dom in u_lower for dom in ALLOWED_DOMAINS):
                continue
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

print("=== FETCHING 10 CLEAN ACER STUDIO LAPTOP PHOTOS FROM RETAIL CDNS ===\n")

success_count = 0
for idx, (name, filename, query) in enumerate(ACER_TARGETS, 1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/10] Processing {name}...")

    src_url, img = fetch_clean_acer_photo(query)
    if not img:
        src_url, img = fetch_clean_acer_photo(f"{name} laptop front isolated white background")

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

print(f"=== FINISHED! {success_count}/10 ACER PRODUCT PHOTOS DOWNLOADED & APPLIED ===")
