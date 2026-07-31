import requests
import re
import urllib.parse
from PIL import Image
import io
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def get_clean_product_photo(query):
    search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            return None
        murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text)
        if not murls:
            murls = re.findall(r'"murl":"(https?://[^"]+)"', r.text)
            
        for u in murls[:15]:
            u_lower = u.lower()
            # Ignore bad domains, logos, banners
            if any(bad in u_lower for bad in ['logo', 'banner', 'icon', 'cookielaw', 'wallpaper', 'vector', 'illustration', 'stock', 'unsplash', 'pexels', 'pixabay', 'shutterstock', 'avatar', 'horoscope', 'sign']):
                continue
            
            # Must be a photo extension
            if not any(ext in u_lower for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                continue

            try:
                resp = requests.get(u, headers=HEADERS, timeout=6)
                if resp.status_code == 200 and len(resp.content) > 15000:
                    img = Image.open(io.BytesIO(resp.content))
                    w, h = img.size
                    if w >= 400 and h >= 300 and 0.8 <= (w / h) <= 2.2:
                        return u, img
            except Exception:
                continue
    except Exception as e:
        print(f"Error for query {query}: {e}")
    return None, None

test_models = [
    "Dell Inspiron 16 Plus 7640 laptop white background product photo",
    "Dell Precision 3590 workstation laptop product photo white background",
    "Apple MacBook Pro 14 M4 space black official laptop product photo",
    "HP OMEN 16 gaming laptop product photo white background",
    "Lenovo Legion Pro 5i laptop product photo white background",
    "Acer Predator Helios Neo 16 laptop product photo white background"
]

for q in test_models:
    url, img = get_clean_product_photo(q)
    if url:
        print(f"[OK] {q[:30]}... -> {img.size} from {url[:60]}...")
    else:
        print(f"[FAIL] {q[:30]}...")
