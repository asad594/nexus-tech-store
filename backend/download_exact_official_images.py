import os
import requests
from PIL import Image, ImageOps
import io
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_backend.settings')
django.setup()

from store.models import Category, Product

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'laptops')
os.makedirs(DEST_DIR, exist_ok=True)

# 50 Official Product Image Source Mapping
OFFICIAL_IMAGES = {
    # --- DELL ---
    "Dell XPS 13": {
        "filename": "dell-xps-13.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/xps_notebooks/xps_13_9340/media_gallery/touch/notebook_xps_13_9340_nt_platinum_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell XPS 14": {
        "filename": "dell-xps-14.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/xps_notebooks/xps_14_9440/media_gallery/touch/notebook_xps_14_9440_t_graphite_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell XPS 16": {
        "filename": "dell-xps-16.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/xps_notebooks/xps_16_9640/media_gallery/touch/notebook_xps_16_9640_t_platinum_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Inspiron 14": {
        "filename": "dell-inspiron-14.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/inspiron_notebooks/inspiron_14_5440/media-gallery/in5440-cn-00055ff090-gy.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Inspiron 15": {
        "filename": "dell-inspiron-15.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/inspiron_notebooks/15_3530/media-gallery/black/notebook-inspiron-15-3530-bk-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Inspiron 16 Plus": {
        "filename": "dell-inspiron-16-plus.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/inspiron_notebooks/inspiron_16_7640/media-gallery/notebook-inspiron-16-7640-ice-blue-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Latitude 5440": {
        "filename": "dell-latitude-5440.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/latitude_notebooks/latitude_5440/media-gallery/notebook-latitude-14-5440-t-grey-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Latitude 7440": {
        "filename": "dell-latitude-7440.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/latitude_notebooks/latitude_7440/media-gallery/latitude_7440_alu_gallery_1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Precision 3590": {
        "filename": "dell-precision-3590.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/precision_notebooks/3590/media-gallery/mobile-workstation-precision-3590-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200"
    },
    "Dell Alienware m18": {
        "filename": "dell-alienware-m18.webp",
        "url": "https://i.dell.com/is/image/DellContent/content/dam/global-site-design/product_images/dell_client_products/notebooks/alienware_notebooks/alienware_m18_r2/media-gallery/laptop-alienware-m18-r2-dark-metallic-moon-gallery-1.psd?fmt=png-alpha&psys=1&wid=1200"
    },

    # --- HP ---
    "HP Spectre x360 14": {
        "filename": "hp-spectre-x360-14.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08874627.png"
    },
    "HP Spectre x360 16": {
        "filename": "hp-spectre-x360-16.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08874708.png"
    },
    "HP ENVY x360 14": {
        "filename": "hp-envy-x360-14.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08920401.png"
    },
    "HP ENVY 16": {
        "filename": "hp-envy-16.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08528994.png"
    },
    "HP Pavilion 15": {
        "filename": "hp-pavilion-15.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08479532.png"
    },
    "HP Pavilion Plus 14": {
        "filename": "hp-pavilion-plus-14.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08795055.png"
    },
    "HP Victus 15": {
        "filename": "hp-victus-15.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08132470.png"
    },
    "HP OMEN 16": {
        "filename": "hp-omen-16.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08560867.png"
    },
    "HP EliteBook 840 G11": {
        "filename": "hp-elitebook-840-g11.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08915421.png"
    },
    "HP ProBook 450 G10": {
        "filename": "hp-probook-450-g10.webp",
        "url": "https://ssl-product-images.www8.hp.com/digmedialib/prodimg/lowres/c08527351.png"
    },

    # --- APPLE MACBOOK ---
    "MacBook Air 13-inch (M2)": {
        "filename": "macbook-air-13-m2.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-midnight-select-202206?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Air 15-inch (M2)": {
        "filename": "macbook-air-15-m2.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-15-starlight-select-202306?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Air 13-inch (M3)": {
        "filename": "macbook-air-13-m3.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba13-spacegray-select-202402?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Air 15-inch (M3)": {
        "filename": "macbook-air-15-m3.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba15-midnight-select-202402?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Pro 14-inch (M3)": {
        "filename": "macbook-pro-14-m3.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202310?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Pro 14-inch (M3 Pro)": {
        "filename": "macbook-pro-14-m3-pro.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Pro 14-inch (M3 Max)": {
        "filename": "macbook-pro-14-m3-max.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spaceblack-gallery1-202310?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Pro 16-inch (M3 Pro)": {
        "filename": "macbook-pro-16-m3-pro.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-spaceblack-select-202310?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Pro 16-inch (M3 Max)": {
        "filename": "macbook-pro-16-m3-max.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-silver-select-202310?wid=1200&hei=1200&fmt=jpeg"
    },
    "MacBook Pro 14-inch (M4)": {
        "filename": "macbook-pro-14-m4.webp",
        "url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spaceblack-select-202310?wid=1200&hei=1200&fmt=jpeg"
    },

    # --- LENOVO ---
    "Lenovo ThinkPad X1 Carbon Gen 12": {
        "filename": "lenovo-thinkpad-x1-carbon-gen-12.webp",
        "url": "https://p1-ofp.static.pub//medias/26137637746_ThinkPad_X1_Carbon_Gen12_Black_202311130319401704207907993.png"
    },
    "Lenovo ThinkPad T14 Gen 5": {
        "filename": "lenovo-thinkpad-t14-gen-5.webp",
        "url": "https://p3-ofp.static.pub//medias/26330999519_T14_Gen5_Intel_EclipseBlack_202402190302301708480373809.png"
    },
    "Lenovo ThinkPad E14 Gen 6": {
        "filename": "lenovo-thinkpad-e14-gen-6.webp",
        "url": "https://p4-ofp.static.pub//medias/26343588267_E14_Gen6_Intel_Black_202402280209421709257635900.png"
    },
    "Lenovo ThinkBook 14 Gen 7": {
        "filename": "lenovo-thinkbook-14-gen-7.webp",
        "url": "https://p2-ofp.static.pub//medias/26307409254_ThinkBook14_Gen7_Intel_ArcticGrey_202402210444391708688463991.png"
    },
    "Lenovo Yoga 7i": {
        "filename": "lenovo-yoga-7i.webp",
        "url": "https://p1-ofp.static.pub//medias/26190753896_Yoga7_14_Gen9_TidalTeal_202312070335011702206413200.png"
    },
    "Lenovo Yoga 9i": {
        "filename": "lenovo-yoga-9i.webp",
        "url": "https://p2-ofp.static.pub//medias/26193798539_Yoga9_14_Gen9_CosmicBlue_202312080948211702081512400.png"
    },
    "Lenovo IdeaPad Slim 5": {
        "filename": "lenovo-ideapad-slim-5.webp",
        "url": "https://p3-ofp.static.pub//medias/26164219460_IdeaPad_Slim_5_16_AMD_CloudGrey_202311270222041701331779900.png"
    },
    "Lenovo IdeaPad Pro 5": {
        "filename": "lenovo-ideapad-pro-5.webp",
        "url": "https://p4-ofp.static.pub//medias/26168579124_IdeaPad_Pro_5_16_Intel_ArcticGrey_202311280336211701421034100.png"
    },
    "Lenovo Legion Pro 5i": {
        "filename": "lenovo-legion-pro-5i.webp",
        "url": "https://p2-ofp.static.pub//medias/26149463219_Legion_Pro_5_16_Gen9_OnyxGrey_202311200257321700732890000.png"
    },
    "Lenovo LOQ 15": {
        "filename": "lenovo-loq-15.webp",
        "url": "https://p1-ofp.static.pub//medias/26155987114_LOQ_15_Gen9_LunaGrey_202311220942181700995180000.png"
    },

    # --- ACER ---
    "Acer Aspire 3": {
        "filename": "acer-aspire-3.webp",
        "url": "https://images.acer.com/is/image/acer/Aspire3_A315-59_KSP1-1?$png-large$"
    },
    "Acer Aspire 5": {
        "filename": "acer-aspire-5.webp",
        "url": "https://images.acer.com/is/image/acer/Aspire5_A515-58M_KSP1-1?$png-large$"
    },
    "Acer Aspire 7": {
        "filename": "acer-aspire-7.webp",
        "url": "https://images.acer.com/is/image/acer/Aspire7_A715-76G_KSP1-1?$png-large$"
    },
    "Acer Swift Go 14": {
        "filename": "acer-swift-go-14.webp",
        "url": "https://images.acer.com/is/image/acer/SwiftGo14_SFG14-72_KSP1-1?$png-large$"
    },
    "Acer Swift X 14": {
        "filename": "acer-swift-x-14.webp",
        "url": "https://images.acer.com/is/image/acer/SwiftX14_SFX14-71G_KSP1-1?$png-large$"
    },
    "Acer Swift Edge 16": {
        "filename": "acer-swift-edge-16.webp",
        "url": "https://images.acer.com/is/image/acer/SwiftEdge16_SFE16-43_KSP1-1?$png-large$"
    },
    "Acer Nitro V 15": {
        "filename": "acer-nitro-v-15.webp",
        "url": "https://images.acer.com/is/image/acer/NitroV15_ANV15-51_KSP1-1?$png-large$"
    },
    "Acer Nitro 16": {
        "filename": "acer-nitro-16.webp",
        "url": "https://images.acer.com/is/image/acer/Nitro16_AN16-41_KSP1-1?$png-large$"
    },
    "Acer Predator Helios Neo 16": {
        "filename": "acer-predator-helios-neo-16.webp",
        "url": "https://images.acer.com/is/image/acer/Predator_Helios_Neo16_PHN16-72_KSP1-1?$png-large$"
    },
    "Acer Predator Helios 18": {
        "filename": "acer-predator-helios-18.webp",
        "url": "https://images.acer.com/is/image/acer/Predator_Helios18_PH18-72_KSP1-1?$png-large$"
    }
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
}

print("Downloading official manufacturer product images for all 50 laptop models...")

success_count = 0
for name, data in OFFICIAL_IMAGES.items():
    filename = data["filename"]
    url = data["url"]
    file_path = os.path.join(DEST_DIR, filename)

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code == 200 and len(resp.content) > 5000:
            img = Image.open(io.BytesIO(resp.content))
            
            # Convert RGBA / P images cleanly to WebP
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = background
            else:
                img = img.convert('RGB')

            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            img.save(file_path, 'WEBP', quality=92)
            
            # Update database record
            rel_url = f"/images/products/laptops/{filename}"
            Product.objects.filter(name=name).update(image_url=rel_url)
            
            success_count += 1
            print(f"[✓] {name} -> {filename} ({os.path.getsize(file_path) // 1024} KB)")
        else:
            print(f"[x] Failed HTTP {resp.status_code} for {name}")
    except Exception as e:
        print(f"[x] Error processing {name}: {e}")

print(f"\nCompleted! {success_count}/50 official product images downloaded and updated in DB.")
