import os
from PIL import Image, ImageChops

PHONES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products', 'phones')

def trim_white_borders(image_path):
    try:
        im = Image.open(image_path)
        if im.mode != 'RGB':
            bg = Image.new('RGB', im.size, (255, 255, 255))
            if 'A' in im.mode:
                bg.paste(im, mask=im.split()[3])
            else:
                bg.paste(im)
            im = bg

        # Find bounding box of non-white content
        bg_white = Image.new('RGB', im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg_white)
        bbox = diff.getbbox()

        if bbox:
            # Crop tightly to phone content with 2px margin
            left, upper, right, lower = bbox
            w, h = im.size
            margin = 3
            left = max(0, left - margin)
            upper = max(0, upper - margin)
            right = min(w, right + margin)
            lower = min(h, lower + margin)
            
            cropped = im.crop((left, upper, right, lower))
            
            # Save tightly cropped WebP
            cropped.save(image_path, 'WEBP', quality=95)
            print(f"[OK] Tight crop for {os.path.basename(image_path)}: orig {im.size} -> cropped {cropped.size}")
    except Exception as e:
        print(f"Error trimming {image_path}: {e}")

print("=== TRIMMING ALL PHONE IMAGE ASSETS TIGHTLY FOR MAXIMUM DISPLAY SIZE ===\n")

for root, dirs, files in os.walk(PHONES_DIR):
    for f in files:
        if f.endswith('.webp'):
            trim_white_borders(os.path.join(root, f))

print("\n=== ALL PHONE PRODUCT IMAGES TIGHTLY CROPPED! ===")
