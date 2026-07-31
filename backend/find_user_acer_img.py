import os
import glob

brain_dir = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397"
print("Brain files:")
for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
            print(os.path.join(root, f))

appdata_dir = r"C:\Users\RB Tech\.gemini\antigravity-ide"
print("\nRecent image files in AppData:")
for root, dirs, files in os.walk(appdata_dir):
    for f in files:
        if any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
            p = os.path.join(root, f)
            print(p)
