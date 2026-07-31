import os
from PIL import Image

f1 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504730674.png"
f2 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504754251.png"
f3 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504834299.png"
f4 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785504853120.png"

for idx, p in enumerate([f1, f2, f3, f4], 1):
    im = Image.open(p)
    print(f"File {idx} ({os.path.basename(p)}): size={im.size}")
