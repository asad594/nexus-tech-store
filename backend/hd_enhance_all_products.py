import os
from PIL import Image, ImageEnhance, ImageFilter

PRODUCTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'public', 'images', 'products')

def enhance_image(file_path):
    try:
        im = Image.open(file_path)
        if im.mode != 'RGB':
            bg = Image.new('RGB', im.size, (255, 255, 255))
            if 'A' in im.mode:
                bg.paste(im, mask=im.split()[3])
            else:
                bg.paste(im)
            im = bg

        w, h = im.size
        # If image is small (width < 600 or height < 600), upscale cleanly with Lanczos to HD 1000px
        target_h = 800
        if h < target_h or w < 600:
            scale = max(target_h / h, 600 / w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Apply subtle sharpening filter to eliminate blurriness and pixelation
        enhancer = ImageEnhance.Sharpness(im)
        im = enhancer.enhance(1.4)

        # Contrast enhancement for crisp details
        contrast = ImageEnhance.Contrast(im)
        im = contrast.enhance(1.05)

        im.save(file_path, 'WEBP', quality=95)
        print(f"[OK] Enhanced HD quality for {os.path.relpath(file_path, PRODUCTS_DIR)} ({im.size[0]}x{im.size[1]} px)")
    except Exception as e:
        print(f"Error enhancing {file_path}: {e}")

print("=== ENHANCING HD QUALITY & SHARPNESS FOR ALL PRODUCT IMAGES ===\n")

for root, dirs, files in os.walk(PRODUCTS_DIR):
    for f in files:
        if f.endswith(('.webp', '.png', '.jpg', '.jpeg')):
            enhance_image(os.path.join(root, f))

print("\n=== ALL PRODUCT IMAGES ENHANCED TO HD QUALITY! ===")
