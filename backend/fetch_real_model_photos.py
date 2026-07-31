import os
import requests
import json
from PIL import Image, ImageOps
import io
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'laptops')
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, image/webp, image/apng, image/*, */*; q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

LAPTOP_MODELS = [
    # DELL (10)
    ("Dell XPS 13", "dell-xps-13.webp"),
    ("Dell XPS 14", "dell-xps-14.webp"),
    ("Dell XPS 16", "dell-xps-16.webp"),
    ("Dell Inspiron 14", "dell-inspiron-14.webp"),
    ("Dell Inspiron 15", "dell-inspiron-15.webp"),
    ("Dell Inspiron 16 Plus", "dell-inspiron-16-plus.webp"),
    ("Dell Latitude 5440", "dell-latitude-5440.webp"),
    ("Dell Latitude 7440", "dell-latitude-7440.webp"),
    ("Dell Precision 3590", "dell-precision-3590.webp"),
    ("Dell Alienware m18", "dell-alienware-m18.webp"),

    # HP (10)
    ("HP Spectre x360 14", "hp-spectre-x360-14.webp"),
    ("HP Spectre x360 16", "hp-spectre-x360-16.webp"),
    ("HP ENVY x360 14", "hp-envy-x360-14.webp"),
    ("HP ENVY 16", "hp-envy-16.webp"),
    ("HP Pavilion 15", "hp-pavilion-15.webp"),
    ("HP Pavilion Plus 14", "hp-pavilion-plus-14.webp"),
    ("HP Victus 15", "hp-victus-15.webp"),
    ("HP OMEN 16", "hp-omen-16.webp"),
    ("HP EliteBook 840 G11", "hp-elitebook-840-g11.webp"),
    ("HP ProBook 450 G10", "hp-probook-450-g10.webp"),

    # APPLE (10)
    ("MacBook Air 13-inch (M2)", "macbook-air-13-m2.webp"),
    ("MacBook Air 15-inch (M2)", "macbook-air-15-m2.webp"),
    ("MacBook Air 13-inch (M3)", "macbook-air-13-m3.webp"),
    ("MacBook Air 15-inch (M3)", "macbook-air-15-m3.webp"),
    ("MacBook Pro 14-inch (M3)", "macbook-pro-14-m3.webp"),
    ("MacBook Pro 14-inch (M3 Pro)", "macbook-pro-14-m3-pro.webp"),
    ("MacBook Pro 14-inch (M3 Max)", "macbook-pro-14-m3-max.webp"),
    ("MacBook Pro 16-inch (M3 Pro)", "macbook-pro-16-m3-pro.webp"),
    ("MacBook Pro 16-inch (M3 Max)", "macbook-pro-16-m3-max.webp"),
    ("MacBook Pro 14-inch (M4)", "macbook-pro-14-m4.webp"),

    # LENOVO (10)
    ("Lenovo ThinkPad X1 Carbon Gen 12", "lenovo-thinkpad-x1-carbon-gen-12.webp"),
    ("Lenovo ThinkPad T14 Gen 5", "lenovo-thinkpad-t14-gen-5.webp"),
    ("Lenovo ThinkPad E14 Gen 6", "lenovo-thinkpad-e14-gen-6.webp"),
    ("Lenovo ThinkBook 14 Gen 7", "lenovo-thinkbook-14-gen-7.webp"),
    ("Lenovo Yoga 7i", "lenovo-yoga-7i.webp"),
    ("Lenovo Yoga 9i", "lenovo-yoga-9i.webp"),
    ("Lenovo IdeaPad Slim 5", "lenovo-ideapad-slim-5.webp"),
    ("Lenovo IdeaPad Pro 5", "lenovo-ideapad-pro-5.webp"),
    ("Lenovo Legion Pro 5i", "lenovo-legion-pro-5i.webp"),
    ("Lenovo LOQ 15", "lenovo-loq-15.webp"),

    # ACER (10)
    ("Acer Aspire 3", "acer-aspire-3.webp"),
    ("Acer Aspire 5", "acer-aspire-5.webp"),
    ("Acer Aspire 7", "acer-aspire-7.webp"),
    ("Acer Swift Go 14", "acer-swift-go-14.webp"),
    ("Acer Swift X 14", "acer-swift-x-14.webp"),
    ("Acer Swift Edge 16", "acer-swift-edge-16.webp"),
    ("Acer Nitro V 15", "acer-nitro-v-15.webp"),
    ("Acer Nitro 16", "acer-nitro-16.webp"),
    ("Acer Predator Helios Neo 16", "acer-predator-helios-neo-16.webp"),
    ("Acer Predator Helios 18", "acer-predator-helios-18.webp"),
]

def search_ddg_images(query):
    try:
        url_token = f"https://duckduckgo.com/?q={requests.utils.quote(query)}&iax=images&ia=images"
        res = requests.get(url_token, headers=HEADERS, timeout=8)
        match = re.search(r'vqd=([\d-]+)\b', res.text) or re.search(r'vqd="([^"]+)"', res.text)
        if not match:
            return []
        vqd = match.group(1)
        
        img_url = "https://duckduckgo.com/i.js"
        params = {'l': 'us-en', 'o': 'json', 'q': query, 'vqd': vqd, 'f': ',,,', 'p': '1'}
        res2 = requests.get(img_url, headers=HEADERS, params=params, timeout=8)
        if res2.status_code == 200:
            results = res2.json().get('results', [])
            urls = []
            for r in results:
                image_src = r.get('image')
                # Filter out stock photo sites and non-product sites
                if image_src and not any(bad in image_src.lower() for bad in ['unsplash', 'pexels', 'pixabay', 'freepik', 'shutterstock', 'stock', 'depositphotos', 'dreamstime']):
                    urls.append(image_src)
            return urls
    except Exception as e:
        print(f"  [search error]: {e}")
    return []

print("Starting fetch of exact real manufacturer laptop product photos...")

successful = 0
for idx, (name, filename) in enumerate(LAPTOP_MODELS, 1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/50] Processing {name} -> {filename}")

    query = f"{name} laptop official product photo white background"
    image_candidates = search_ddg_images(query)
    
    # Fallback query if first list empty
    if not image_candidates:
        query_alt = f"{name} laptop front view isolated png"
        image_candidates = search_ddg_images(query_alt)

    downloaded = False
    for candidate_url in image_candidates[:5]:
        try:
            resp = requests.get(candidate_url, headers=HEADERS, timeout=10)
            if resp.status_code == 200 and len(resp.content) > 10000:
                img = Image.open(io.BytesIO(resp.content))
                width, height = img.size
                if width >= 350 and height >= 300:
                    # Format conversion
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                        img = bg
                    else:
                        img = img.convert('RGB')

                    img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
                    img.save(file_path, 'WEBP', quality=92)

                    # Update Database
                    rel_path = f"/images/products/laptops/{filename}"
                    Product.objects.filter(name=name).update(image_url=rel_path)

                    downloaded = True
                    successful += 1
                    print(f"  ✓ Saved clean product shot ({width}x{height}) -> {filename}")
                    break
        except Exception as e:
            continue

    if not downloaded:
        print(f"  ⚠️ Could not download new image for {name}, preserving existing file.")

print(f"\nCompleted! {successful}/50 products updated with exact model product photography.")
