import requests

def search_wikimedia(query):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap",
        "gsrnamespace": "6",
        "gsrlimit": "5",
        "prop": "imageinfo",
        "iiprop": "url|mime|size"
    }
    r = requests.get(url, params=params, headers={"User-Agent": "NexusStoreBot/1.0"})
    if r.status_code == 200:
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        urls = []
        for page_id, page in pages.items():
            info = page.get("imageinfo", [{}])[0]
            img_url = info.get("url")
            if img_url:
                urls.append(img_url)
        return urls
    return []

test_models = ["MacBook Air M2", "Dell XPS 13", "Lenovo ThinkPad X1 Carbon", "HP Spectre x360"]
for model in test_models:
    results = search_wikimedia(model)
    print(f"Results for {model}: {results[:2]}")
