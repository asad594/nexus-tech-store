import requests
import re
import urllib.parse

def search_ddg(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    
    # Get vqd
    token_url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
    res = requests.get(token_url, headers=headers)
    vqd_match = re.search(r'vqd=([\d-]+)', res.text)
    if not vqd_match:
        vqd_match = re.search(r'vqd="([^"]+)"', res.text)
    
    if not vqd_match:
        print("vqd token not found")
        return []

    vqd = vqd_match.group(1)
    
    img_api = "https://duckduckgo.com/i.js"
    params = {
        'l': 'us-en',
        'o': 'json',
        'q': query,
        'vqd': vqd,
        'f': ',,,',
        'p': '1'
    }
    res_img = requests.get(img_api, headers=headers, params=params)
    if res_img.status_code == 200:
        data = res_img.json()
        results = data.get('results', [])
        return [r['image'] for r in results if 'image' in r]
    return []

print(search_ddg("Dell XPS 13 laptop product photo white background")[:3])
