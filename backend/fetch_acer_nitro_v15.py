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
filename = "acer-nitro-v-15.webp"
file_path = os.path.join(DEST_DIR, filename)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

query = "Acer Nitro V 15 ANV15-51 gaming laptop product photo white background"
search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"

r = requests.get(search_url, headers=HEADERS, timeout=8)
murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text) or re.findall(r'"murl":"(https?://[^"]+)"', r.text)

saved = False
for u in murls[:20]:
    u_lower = u.lower()
    if any(bad in u_lower for bad in ['logo', 'banner', 'icon', 'cookielaw', 'wallpaper', 'vector', 'illustration', 'stock', 'unsplash', 'pexels', 'pixabay', 'shutterstock', 'avatar', 'horoscope', 'sign']):
        continue
    if not any(ext in u_lower for ext in ['.jpg', '.jpeg', '.png', '.webp']):
        continue

    try:
        resp = requests.get(u, headers=HEADERS, timeout=6)
        if resp.status_code == 200 and len(resp.content) > 15000:
            img = Image.open(io.BytesIO(resp.content))
            w, h = img.size
            if w >= 350 and h >= 300:
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                    img = bg
                else:
                    img = img.convert('RGB')

                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                img.save(file_path, 'WEBP', quality=92)

                rel_url = f"/images/products/laptops/{filename}"
                Product.objects.filter(name="Acer Nitro V 15").update(image_url=rel_url)
                print(f"[OK] Saved Acer Nitro V 15 photo ({w}x{h})")
                saved = True
                break
    except Exception as e:
        continue

if not saved:
    print("[WARN] Failed to download Acer Nitro V 15")
