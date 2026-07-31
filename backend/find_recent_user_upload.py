import os
import time

search_paths = [
    r"C:\Users\RB Tech\AppData\Local\Temp",
    r"C:\Users\RB Tech\.gemini\antigravity-ide",
    r"C:\Users\RB Tech\Desktop\nexus-tech-store-main"
]

now = time.time()
found = []

for s in search_paths:
    for root, dirs, files in os.walk(s):
        for f in files:
            if any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
                p = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(p)
                    if now - mtime < 600: # last 10 mins
                        found.append((mtime, p))
                except Exception:
                    pass

found.sort(reverse=True)
for mtime, p in found[:20]:
    print(f"{time.ctime(mtime)}: {p}")
