import requests
import re
import os
import io
from PIL import Image
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Product

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

URLS = [
    # Dell
    ("Dell XPS 13", "dell-xps-13.webp", "https://www.dell.com/search/xps-13"),
    ("Dell XPS 14", "dell-xps-14.webp", "https://www.dell.com/search/xps-14"),
    ("Dell XPS 16", "dell-xps-16.webp", "https://www.dell.com/search/xps-16"),
    ("Dell Inspiron 14", "dell-inspiron-14.webp", "https://www.dell.com/search/inspiron-14"),
    ("Dell Inspiron 15", "dell-inspiron-15.webp", "https://www.dell.com/search/inspiron-15"),
    ("Dell Inspiron 16 Plus", "dell-inspiron-16-plus.webp", "https://www.dell.com/search/inspiron-16-plus"),
    ("Dell Latitude 5440", "dell-latitude-5440.webp", "https://www.dell.com/search/latitude-5440"),
    ("Dell Latitude 7440", "dell-latitude-7440.webp", "https://www.dell.com/search/latitude-7440"),
    ("Dell Precision 3590", "dell-precision-3590.webp", "https://www.dell.com/search/precision-3590"),
    ("Dell Alienware m18", "dell-alienware-m18.webp", "https://www.dell.com/search/alienware-m18"),

    # HP
    ("HP Spectre x360 14", "hp-spectre-x360-14.webp", "https://www.hp.com/search?q=Spectre+x360+14"),
    ("HP Spectre x360 16", "hp-spectre-x360-16.webp", "https://www.hp.com/search?q=Spectre+x360+16"),
    ("HP ENVY x360 14", "hp-envy-x360-14.webp", "https://www.hp.com/search?q=ENVY+x360+14"),
    ("HP ENVY 16", "hp-envy-16.webp", "https://www.hp.com/search?q=ENVY+16"),
    ("HP Pavilion 15", "hp-pavilion-15.webp", "https://www.hp.com/search?q=Pavilion+15"),
    ("HP Pavilion Plus 14", "hp-pavilion-plus-14.webp", "https://www.hp.com/search?q=Pavilion+Plus+14"),
    ("HP Victus 15", "hp-victus-15.webp", "https://www.hp.com/search?q=Victus+15"),
    ("HP OMEN 16", "hp-omen-16.webp", "https://www.hp.com/search?q=OMEN+16"),
    ("HP EliteBook 840 G11", "hp-elitebook-840-g11.webp", "https://www.hp.com/search?q=EliteBook+840+G11"),
    ("HP ProBook 450 G10", "hp-probook-450-g10.webp", "https://www.hp.com/search?q=ProBook+450+G10"),

    # Apple
    ("MacBook Air 13-inch (M2)", "macbook-air-13-m2.webp", "https://www.apple.com/macbook-air/"),
    ("MacBook Air 15-inch (M2)", "macbook-air-15-m2.webp", "https://www.apple.com/macbook-air/"),
    ("MacBook Air 13-inch (M3)", "macbook-air-13-m3.webp", "https://www.apple.com/macbook-air/"),
    ("MacBook Air 15-inch (M3)", "macbook-air-15-m3.webp", "https://www.apple.com/macbook-air/"),
    ("MacBook Pro 14-inch (M3)", "macbook-pro-14-m3.webp", "https://www.apple.com/macbook-pro/"),
    ("MacBook Pro 14-inch (M3 Pro)", "macbook-pro-14-m3-pro.webp", "https://www.apple.com/macbook-pro/"),
    ("MacBook Pro 14-inch (M3 Max)", "macbook-pro-14-m3-max.webp", "https://www.apple.com/macbook-pro/"),
    ("MacBook Pro 16-inch (M3 Pro)", "macbook-pro-16-m3-pro.webp", "https://www.apple.com/macbook-pro/"),
    ("MacBook Pro 16-inch (M3 Max)", "macbook-pro-16-m3-max.webp", "https://www.apple.com/macbook-pro/"),
    ("MacBook Pro 14-inch (M4)", "macbook-pro-14-m4.webp", "https://www.apple.com/macbook-pro/"),

    # Lenovo
    ("Lenovo ThinkPad X1 Carbon Gen 12", "lenovo-thinkpad-x1-carbon-gen-12.webp", "https://www.lenovo.com/search?text=ThinkPad%20X1%20Carbon%20Gen%2012"),
    ("Lenovo ThinkPad T14 Gen 5", "lenovo-thinkpad-t14-gen-5.webp", "https://www.lenovo.com/search?text=ThinkPad%20T14%20Gen%205"),
    ("Lenovo ThinkPad E14 Gen 6", "lenovo-thinkpad-e14-gen-6.webp", "https://www.lenovo.com/search?text=ThinkPad%20E14%20Gen%206"),
    ("Lenovo ThinkBook 14 Gen 7", "lenovo-thinkbook-14-gen-7.webp", "https://www.lenovo.com/search?text=ThinkBook%2014%20Gen%207"),
    ("Lenovo Yoga 7i", "lenovo-yoga-7i.webp", "https://www.lenovo.com/search?text=Yoga%207i"),
    ("Lenovo Yoga 9i", "lenovo-yoga-9i.webp", "https://www.lenovo.com/search?text=Yoga%209i"),
    ("Lenovo IdeaPad Slim 5", "lenovo-ideapad-slim-5.webp", "https://www.lenovo.com/search?text=IdeaPad%20Slim%205"),
    ("Lenovo IdeaPad Pro 5", "lenovo-ideapad-pro-5.webp", "https://www.lenovo.com/search?text=IdeaPad%20Pro%205"),
    ("Lenovo Legion Pro 5i", "lenovo-legion-pro-5i.webp", "https://www.lenovo.com/search?text=Legion%20Pro%205i"),
    ("Lenovo LOQ 15", "lenovo-loq-15.webp", "https://www.lenovo.com/search?text=LOQ%2015"),

    # Acer
    ("Acer Aspire 3", "acer-aspire-3.webp", "https://www.acer.com/search?q=Aspire%203"),
    ("Acer Aspire 5", "acer-aspire-5.webp", "https://www.acer.com/search?q=Aspire%205"),
    ("Acer Aspire 7", "acer-aspire-7.webp", "https://www.acer.com/search?q=Aspire%207"),
    ("Acer Swift Go 14", "acer-swift-go-14.webp", "https://www.acer.com/search?q=Swift%20Go%2014"),
    ("Acer Swift X 14", "acer-swift-x-14.webp", "https://www.acer.com/search?q=Swift%20X%2014"),
    ("Acer Swift Edge 16", "acer-swift-edge-16.webp", "https://www.acer.com/search?q=Swift%20Edge%2016"),
    ("Acer Nitro V 15", "acer-nitro-v-15.webp", "https://www.acer.com/search?q=Nitro%20V%2015"),
    ("Acer Nitro 16", "acer-nitro-16.webp", "https://www.acer.com/search?q=Nitro%2016"),
    ("Acer Predator Helios Neo 16", "acer-predator-helios-neo-16.webp", "https://www.acer.com/search?q=Predator%20Helios%20Neo%2016"),
    ("Acer Predator Helios 18", "acer-predator-helios-18.webp", "https://www.acer.com/search?q=Predator%20Helios%2018"),
]

print("Testing direct fetching from official manufacturer search URLs...")
for name, filename, url in URLS[:5]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        print(f"{name}: HTTP {r.status_code}, Length: {len(r.text)}")
    except Exception as e:
        print(f"{name}: Failed -> {e}")
