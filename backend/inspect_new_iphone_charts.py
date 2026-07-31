import os
from PIL import Image

p1 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785506096465.png"
p2 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785506104183.png"

im1 = Image.open(p1)
im2 = Image.open(p2)

print(f"Chart 1 (X, XS, XS Max) size: {im1.size}")
print(f"Chart 2 (Rest) size: {im2.size}")
