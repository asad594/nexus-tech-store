import requests
import json

def get_official_product_image(query):
    # DuckDuckGo image search endpoint
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://duckduckgo.com/',
    }
    
    # Step 1: Obtain token
    res = requests.get(f"https://duckduckgo.com/?q={query}&iax=images&ia=images", headers=headers, timeout=10)
    vqd = None
    for line in res.text.split('\n'):
        if 'vqd="' in line:
            vqd = line.split('vqd="')[1].split('"')[0]
            break
        elif "vqd='" in line:
            vqd = line.split("vqd='")[1].split("'")[0]
            break
            
    if not vqd:
        return None
        
    # Step 2: Fetch image search results
    params = {
        'l': 'us-en',
        'o': 'json',
        'q': query,
        'vqd': vqd,
        'f': ',,,',
        'p': '1'
    }
    img_res = requests.get("https://duckduckgo.com/i.js", headers=headers, params=params, timeout=10)
    if img_res.status_code == 200:
        data = img_res.json()
        results = data.get('results', [])
        for r in results:
            img_url = r.get('image')
            # Look for clean product shots
            if img_url and any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                return img_url
    return None

test_models = [
    "Dell Inspiron 16 Plus product photo white background",
    "Dell Precision 3590 laptop product photo white background",
    "MacBook Pro 14 M4 space black official product photo",
    "HP OMEN 16 gaming laptop product photo white background",
    "Lenovo Legion Pro 5i laptop product photo white background",
    "Acer Predator Helios Neo 16 product photo white background"
]

for query in test_models:
    img_url = get_official_product_image(query)
    print(f"Query: {query}\nFound Image: {img_url}\n")
