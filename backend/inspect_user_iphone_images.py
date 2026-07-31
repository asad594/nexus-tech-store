import os
from PIL import Image

path1 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495191289.png"
path2 = r"C:\Users\RB Tech\.gemini\antigravity-ide\brain\57493fa7-f1ca-45a9-bb3a-13c241a9d397\media__1785495193880.png"

im1 = Image.open(path1)
im2 = Image.open(path2)

print(f"Chart 1 (X, XS, XS Max) Size: {im1.size}")
print(f"Chart 2 (Rest of iPhones) Size: {im2.size}")
