# -*- coding: utf-8 -*-
"""One-off: draw og.png (1200x630) and favicon.ico in the 1-bit style. Needs Pillow + Windows fonts.

py redesign/tools/og.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "C:/Windows/Fonts/"
bold = lambda s: ImageFont.truetype(F + "msjhbd.ttc", s)
mono = lambda s: ImageFont.truetype(F + "consolab.ttf", s)

W, H = 1200, 630
im = Image.new("1", (W, H), 1)
d = ImageDraw.Draw(im)
# 1-bit dither strip on the right, the system's only grey
for y in range(0, H, 8):
    for x in range(820 + (y // 8 % 2) * 8, W, 16):
        d.rectangle([x, y, x + 7, y + 7], fill=0)
# window: hard shadow, frame, black title bar
d.rectangle([88, 108, 908, 548], fill=0)
d.rectangle([72, 92, 892, 532], fill=1, outline=0, width=4)
d.rectangle([72, 92, 892, 136], fill=0)
d.text((92, 98), "siyulio.exe", font=mono(30), fill=1)
d.text((112, 176), "siyulio", font=mono(112), fill=0)
d.text((116, 318), "在製造業裡，把 AI 變成", font=bold(48), fill=0)
d.text((116, 382), "每天會跑的產線。", font=bold(48), fill=0)
d.text((116, 462), "Jason Lin · siyulio.com", font=mono(30), fill=0)
im.convert("RGB").save(os.path.join(OUT, "og.png"), optimize=True)

# favicon: the same 8x8 pixel "s" as the inline SVG
ico = Image.new("1", (8, 8), 0)
p = ico.load()
for x0, y0, w, h in [
    (2, 1, 4, 1),
    (1, 2, 1, 2),
    (2, 4, 4, 1),
    (6, 5, 1, 2),
    (2, 6, 4, 1),
]:
    for x in range(x0, x0 + w):
        for y in range(y0, y0 + h):
            p[x, y] = 1
ico.resize((32, 32), Image.NEAREST).convert("RGB").save(
    os.path.join(OUT, "favicon.ico"), sizes=[(32, 32)]
)
print("og.png + favicon.ico written")
