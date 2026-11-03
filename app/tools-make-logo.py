#!/usr/bin/env python3
# Nabız logosu üretir: koyu zemin, yeşil nabız (ECG) dalgası, camgöbeği uç.
# Kullanım: python3 tools-make-logo.py  →  src/common/logo.png
# Gereksinim: pillow  (pip install pillow)
from PIL import Image, ImageDraw
import os

W = 192
img = Image.new("RGB", (W, W), (8, 12, 20))
d = ImageDraw.Draw(img)
d.ellipse([6, 6, W-6, W-6], outline=(18, 28, 42), width=4)
m = W // 2
pts = [(18,m),(54,m),(70,m-12),(86,m+40),(104,m-58),(120,m+16),(136,m),(174,m)]
d.line(pts, fill=(0, 255, 136), width=9, joint="curve")
d.ellipse([174-8, m-8, 174+8, m+8], fill=(0, 229, 255))

out = os.path.join(os.path.dirname(__file__), "src", "common", "logo.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("logo yazildi:", out)
