import requests
import re
import urllib.parse
from PIL import Image
import io

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def search_bing_images(query):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            # Bing encodes direct image URLs in murl":"https://..."
            murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+)&quot;', r.text)
            if not murls:
                murls = re.findall(r'"murl":"(https?://[^"]+)"', r.text)
            
            clean_urls = []
            for u in murls:
                if not any(bad in u.lower() for bad in ['stock', 'unsplash', 'pexels', 'pixabay', 'freepik', 'shutterstock', 'dreamstime', 'depositphotos', 'vector', 'illustration']):
                    clean_urls.append(u)
            return clean_urls
    except Exception as e:
        print(f"Error searching Bing: {e}")
    return []

test_models = [
    "Dell XPS 13 laptop front view white background",
    "Dell Inspiron 16 Plus laptop white background",
    "MacBook Pro 14 M4 space black official photo",
    "HP OMEN 16 gaming laptop front view white background",
    "Lenovo Legion Pro 5i laptop white background",
    "Acer Predator Helios Neo 16 laptop white background"
]

for query in test_models:
    urls = search_bing_images(query)
    print(f"Query: {query}")
    if urls:
        print(f"  Found {len(urls)} URLs. First: {urls[0]}")
    else:
        print("  Found 0 URLs.")
