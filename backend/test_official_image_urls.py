import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

URLS = {
    # Apple Official CDN
    "macbook-air-13-m2.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-midnight-select-202206?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1653084303665",
    "macbook-air-15-m2.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-15-starlight-select-202306?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1684430030588",
    "macbook-air-13-m3.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba13-spacegray-select-202402?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1708367688034",
    "macbook-air-15-m3.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba15-midnight-select-202402?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1708367688034",
    "macbook-pro-14-m3.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200",
    "macbook-pro-14-m3-pro.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200",
    "macbook-pro-14-m3-max.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200",
    "macbook-pro-16-m3-pro.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200",
    "macbook-pro-16-m3-max.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-silver-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200",
    "macbook-pro-14-m4.webp": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1697230830200",

    # Dell Official CDN
    "dell-xps-13.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/xps_notebooks/xps_13_9340/media_gallery/touch/notebook_xps_13_9340_nt_platinum_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-xps-14.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/xps_notebooks/xps_14_9440/media_gallery/touch/notebook_xps_14_9440_t_graphite_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-xps-16.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/xps_notebooks/xps_16_9640/media_gallery/touch/notebook_xps_16_9640_t_platinum_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-inspiron-14.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/inspiron_notebooks/inspiron_14_5440/media-gallery/in5440-cn-00055ff090-gy.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-inspiron-15.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/inspiron_notebooks/15_3530/media-gallery/black/notebook-inspiron-15-3530-bk-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-inspiron-16-plus.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/inspiron_notebooks/inspiron_16_7640/media-gallery/notebook-inspiron-16-7640-ice-blue-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-latitude-5440.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/latitude_notebooks/latitude_5440/media-gallery/notebook-latitude-14-5440-t-grey-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-latitude-7440.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/latitude_notebooks/latitude_7440/media-gallery/latitude_7440_alu_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-precision-3590.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/precision_notebooks/3590/media-gallery/mobile-workstation-precision-3590-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200",
    "dell-alienware-m18.webp": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/alienware_notebooks/alienware_m18_r2/media-gallery/laptop-alienware-m18-r2-dark-metallic-moon-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200",
}

print("Testing direct official CDN URLs...")
for name, url in URLS.items():
    try:
        r = requests.head(url, headers=headers, timeout=5)
        if r.status_code != 200:
            r = requests.get(url, headers=headers, timeout=5, stream=True)
        print(f"{name}: {r.status_code}")
    except Exception as e:
        print(f"{name}: ERROR ({e})")
