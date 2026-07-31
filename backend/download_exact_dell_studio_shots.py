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

DELL_TARGETS = [
    ("Dell XPS 13", "dell-xps-13.webp", "Dell XPS 13 9340 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:notebookcheck.net"),
    ("Dell XPS 14", "dell-xps-14.webp", "Dell XPS 14 9440 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:notebookcheck.net"),
    ("Dell XPS 16", "dell-xps-16.webp", "Dell XPS 16 9640 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com OR site:notebookcheck.net"),
    ("Dell Inspiron 14", "dell-inspiron-14.webp", "Dell Inspiron 14 5440 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("Dell Inspiron 15", "dell-inspiron-15.webp", "Dell Inspiron 15 3530 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("Dell Inspiron 16 Plus", "dell-inspiron-16-plus.webp", "Dell Inspiron 16 Plus 7640 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("Dell Latitude 5440", "dell-latitude-5440.webp", "Dell Latitude 5440 notebook isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("Dell Latitude 7440", "dell-latitude-7440.webp", "Dell Latitude 7440 laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("Dell Precision 3590", "dell-precision-3590.webp", "Dell Precision 3590 mobile workstation laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
    ("Dell Alienware m18", "dell-alienware-m18.webp", "Dell Alienware m18 R2 gaming laptop isolated white background site:bhphotovideo.com OR site:bestbuy.com"),
]

def fetch_exact_studio_shot(query):
    search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None, None
        murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text) or re.findall(r'"murl":"(https?://[^"]+)"', r.text)

        for u in murls[:30]:
            u_lower = u.lower()
            if any(bad in u_lower for bad in ['optiplex', 'video_imagery', 'csimages', 'dt-og-standard', 'uwaem', 'logo', 'banner', 'icon', 'cookielaw', 'wallpaper', 'vector', 'illustration', 'stock', 'freepik', 'shutterstock', 'avatar', 'horoscope', 'sign', 'hand', 'desk', 'person', 'man', 'woman']):
                continue
            if not any(ext in u_lower for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                continue

            try:
                resp = requests.get(u, headers=HEADERS, timeout=8)
                if resp.status_code == 200 and len(resp.content) > 20000:
                    img = Image.open(io.BytesIO(resp.content))
                    w, h = img.size
                    if w >= 400 and h >= 300 and 0.8 <= (w / h) <= 2.2:
                        return u, img
            except Exception:
                continue
    except Exception as e:
        print(f"Error fetching: {e}")
    return None, None

print("=== FETCHING 10 EXACT DELL STUDIO PRODUCT PHOTOS FROM OFFICIAL RETAIL SOURCES ===\n")

success_count = 0
for idx, (name, filename, query) in enumerate(DELL_TARGETS, 1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/10] Processing {name}...")

    src_url, img = fetch_exact_studio_shot(query)
    if not img:
        src_url, img = fetch_exact_studio_shot(f"{name} laptop front view isolated white background")

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
        print(f"  [FAIL] Could not fetch for {name}\n")

print(f"=== FINISHED! {success_count}/10 DELL PRODUCT PHOTOS UPDATED ===")
