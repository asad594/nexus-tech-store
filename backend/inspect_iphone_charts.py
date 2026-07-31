import os
from PIL import Image

img1_path = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495221700.png"
img2_path = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495229984.png"

im1 = Image.open(img1_path)
im2 = Image.open(img2_path)

print(f"Img 1 size: {im1.size}")
print(f"Img 2 size: {im2.size}")
