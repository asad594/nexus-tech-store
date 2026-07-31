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

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'laptops')
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

LAPTOPS = [
    # DELL (10)
    ("Dell XPS 13", "dell-xps-13.webp", "Dell XPS 13 9340 laptop white background product photo"),
    ("Dell XPS 14", "dell-xps-14.webp", "Dell XPS 14 9440 laptop white background product photo"),
    ("Dell XPS 16", "dell-xps-16.webp", "Dell XPS 16 9640 laptop white background product photo"),
    ("Dell Inspiron 14", "dell-inspiron-14.webp", "Dell Inspiron 14 5440 laptop white background product photo"),
    ("Dell Inspiron 15", "dell-inspiron-15.webp", "Dell Inspiron 15 3530 laptop white background product photo"),
    ("Dell Inspiron 16 Plus", "dell-inspiron-16-plus.webp", "Dell Inspiron 16 Plus 7640 laptop white background product photo"),
    ("Dell Latitude 5440", "dell-latitude-5440.webp", "Dell Latitude 5440 business laptop white background product photo"),
    ("Dell Latitude 7440", "dell-latitude-7440.webp", "Dell Latitude 7440 laptop white background product photo"),
    ("Dell Precision 3590", "dell-precision-3590.webp", "Dell Precision 3590 workstation laptop white background product photo"),
    ("Dell Alienware m18", "dell-alienware-m18.webp", "Dell Alienware m18 R2 gaming laptop white background product photo"),

    # HP (10)
    ("HP Spectre x360 14", "hp-spectre-x360-14.webp", "HP Spectre x360 14 convertible laptop white background product photo"),
    ("HP Spectre x360 16", "hp-spectre-x360-16.webp", "HP Spectre x360 16 laptop white background product photo"),
    ("HP ENVY x360 14", "hp-envy-x360-14.webp", "HP ENVY x360 14 2-in-1 laptop white background product photo"),
    ("HP ENVY 16", "hp-envy-16.webp", "HP ENVY 16 laptop white background product photo"),
    ("HP Pavilion 15", "hp-pavilion-15.webp", "HP Pavilion 15 laptop white background product photo"),
    ("HP Pavilion Plus 14", "hp-pavilion-plus-14.webp", "HP Pavilion Plus 14 OLED laptop white background product photo"),
    ("HP Victus 15", "hp-victus-15.webp", "HP Victus 15 gaming laptop white background product photo"),
    ("HP OMEN 16", "hp-omen-16.webp", "HP OMEN 16 gaming laptop white background product photo"),
    ("HP EliteBook 840 G11", "hp-elitebook-840-g11.webp", "HP EliteBook 840 G11 business laptop white background product photo"),
    ("HP ProBook 450 G10", "hp-probook-450-g10.webp", "HP ProBook 450 G10 notebook white background product photo"),

    # APPLE MACBOOK (10)
    ("MacBook Air 13-inch (M2)", "macbook-air-13-m2.webp", "Apple MacBook Air 13 M2 midnight official product photo"),
    ("MacBook Air 15-inch (M2)", "macbook-air-15-m2.webp", "Apple MacBook Air 15 M2 starlight official product photo"),
    ("MacBook Air 13-inch (M3)", "macbook-air-13-m3.webp", "Apple MacBook Air 13 M3 space gray official product photo"),
    ("MacBook Air 15-inch (M3)", "macbook-air-15-m3.webp", "Apple MacBook Air 15 M3 midnight official product photo"),
    ("MacBook Pro 14-inch (M3)", "macbook-pro-14-m3.webp", "Apple MacBook Pro 14 M3 space gray official product photo"),
    ("MacBook Pro 14-inch (M3 Pro)", "macbook-pro-14-m3-pro.webp", "Apple MacBook Pro 14 M3 Pro space black official product photo"),
    ("MacBook Pro 14-inch (M3 Max)", "macbook-pro-14-m3-max.webp", "Apple MacBook Pro 14 M3 Max space black official product photo"),
    ("MacBook Pro 16-inch (M3 Pro)", "macbook-pro-16-m3-pro.webp", "Apple MacBook Pro 16 M3 Pro space black official product photo"),
    ("MacBook Pro 16-inch (M3 Max)", "macbook-pro-16-m3-max.webp", "Apple MacBook Pro 16 M3 Max silver official product photo"),
    ("MacBook Pro 14-inch (M4)", "macbook-pro-14-m4.webp", "Apple MacBook Pro 14 M4 space black official product photo"),

    # LENOVO (10)
    ("Lenovo ThinkPad X1 Carbon Gen 12", "lenovo-thinkpad-x1-carbon-gen-12.webp", "Lenovo ThinkPad X1 Carbon Gen 12 laptop white background product photo"),
    ("Lenovo ThinkPad T14 Gen 5", "lenovo-thinkpad-t14-gen-5.webp", "Lenovo ThinkPad T14 Gen 5 laptop white background product photo"),
    ("Lenovo ThinkPad E14 Gen 6", "lenovo-thinkpad-e14-gen-6.webp", "Lenovo ThinkPad E14 Gen 6 laptop white background product photo"),
    ("Lenovo ThinkBook 14 Gen 7", "lenovo-thinkbook-14-gen-7.webp", "Lenovo ThinkBook 14 Gen 7 laptop white background product photo"),
    ("Lenovo Yoga 7i", "lenovo-yoga-7i.webp", "Lenovo Yoga 7i 2-in-1 laptop white background product photo"),
    ("Lenovo Yoga 9i", "lenovo-yoga-9i.webp", "Lenovo Yoga 9i convertible laptop white background product photo"),
    ("Lenovo IdeaPad Slim 5", "lenovo-ideapad-slim-5.webp", "Lenovo IdeaPad Slim 5 16 laptop white background product photo"),
    ("Lenovo IdeaPad Pro 5", "lenovo-ideapad-pro-5.webp", "Lenovo IdeaPad Pro 5 16 laptop white background product photo"),
    ("Lenovo Legion Pro 5i", "lenovo-legion-pro-5i.webp", "Lenovo Legion Pro 5i gaming laptop white background product photo"),
    ("Lenovo LOQ 15", "lenovo-loq-15.webp", "Lenovo LOQ 15 gaming laptop white background product photo"),

    # ACER (10)
    ("Acer Aspire 3", "acer-aspire-3.webp", "Acer Aspire 3 A315 laptop white background product photo"),
    ("Acer Aspire 5", "acer-aspire-5.webp", "Acer Aspire 5 A515 laptop white background product photo"),
    ("Acer Aspire 7", "acer-aspire-7.webp", "Acer Aspire 7 A715 laptop white background product photo"),
    ("Acer Swift Go 14", "acer-swift-go-14.webp", "Acer Swift Go 14 OLED laptop white background product photo"),
    ("Acer Swift X 14", "acer-swift-x-14.webp", "Acer Swift X 14 creator laptop white background product photo"),
    ("Acer Swift Edge 16", "acer-swift-edge-16.webp", "Acer Swift Edge 16 OLED laptop white background product photo"),
    ("Acer Nitro V 15", "acer-nitro-v-15.webp", "Acer Nitro V 15 gaming laptop white background product photo"),
    ("Acer Nitro 16", "acer-nitro-16.webp", "Acer Nitro 16 gaming laptop white background product photo"),
    ("Acer Predator Helios Neo 16", "acer-predator-helios-neo-16.webp", "Acer Predator Helios Neo 16 gaming laptop white background product photo"),
    ("Acer Predator Helios 18", "acer-predator-helios-18.webp", "Acer Predator Helios 18 gaming laptop white background product photo"),
]

def fetch_real_image(query):
    search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            return None
        murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text)
        if not murls:
            murls = re.findall(r'"murl":"(https?://[^"]+)"', r.text)

        for u in murls[:20]:
            u_lower = u.lower()
            if any(bad in u_lower for bad in ['logo', 'banner', 'icon', 'cookielaw', 'wallpaper', 'vector', 'illustration', 'stock', 'unsplash', 'pexels', 'pixabay', 'shutterstock', 'avatar', 'horoscope', 'sign', 'hand', 'desk', 'person', 'people', 'girl', 'man', 'woman']):
                continue
            if not any(ext in u_lower for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                continue

            try:
                resp = requests.get(u, headers=HEADERS, timeout=6)
                if resp.status_code == 200 and len(resp.content) > 15000:
                    img = Image.open(io.BytesIO(resp.content))
                    w, h = img.size
                    if w >= 350 and h >= 300 and 0.8 <= (w / h) <= 2.2:
                        return img
            except Exception:
                continue
    except Exception as e:
        print(f"Error fetching for query {query}: {e}")
    return None

print("Starting full update of all 50 laptops with real model product images...")

updated_count = 0
for idx, (name, filename, query) in enumerate(LAPTOPS, start=1):
    file_path = os.path.join(DEST_DIR, filename)
    print(f"[{idx}/50] Searching image for: {name}...")

    img = fetch_real_image(query)
    if not img:
        # Fallback query
        img = fetch_real_image(f"{name} laptop front view isolated png")

    if img:
        # Process and convert to clean WebP
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
            img = bg
        else:
            img = img.convert('RGB')

        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        img.save(file_path, 'WEBP', quality=92)

        rel_url = f"/images/products/laptops/{filename}"
        Product.objects.filter(name=name).update(image_url=rel_url)

        updated_count += 1
        print(f"  [OK] Saved real photo for {name} ({img.size[0]}x{img.size[1]}) -> {filename}")
    else:
        print(f"  [WARN] Image update skipped for {name}")

print(f"\nFinished updating {updated_count}/50 products with real product images!")
