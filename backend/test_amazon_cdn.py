import requests
from PIL import Image
import io

test_urls = {
    "dell_xps_13": "https://m.media-amazon.com/images/I/71wF7YDIQkL._AC_SL1500_.jpg",
    "macbook_pro_14": "https://m.media-amazon.com/images/I/61bwiPR79tL._AC_SL1500_.jpg",
    "hp_omen_16": "https://m.media-amazon.com/images/I/71Y-C685ZlL._AC_SL1500_.jpg",
    "lenovo_legion": "https://m.media-amazon.com/images/I/71d1V1c4b7L._AC_SL1500_.jpg",
    "acer_predator": "https://m.media-amazon.com/images/I/81k45Y1cIHL._AC_SL1500_.jpg"
}

headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in test_urls.items():
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            print(f"Success {name}: {img.size}, {img.format}, {len(r.content)} bytes")
        else:
            print(f"Failed {name}: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error {name}: {e}")
