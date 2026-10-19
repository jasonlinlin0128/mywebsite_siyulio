# -*- coding: utf-8 -*-
"""1-bit flow diagrams for cards that must not show real screens (company data).

py redesign/tools/diagrams.py      -> tools/shots/<id>-1bit.png (1000x625)
"""

import os
from PIL import Image, ImageDraw, ImageFont

SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
F = "C:/Windows/Fonts/"
zh = lambda s: ImageFont.truetype(F + "msjhbd.ttc", s)
mono = lambda s: ImageFont.truetype(F + "consolab.ttf", s)
W, H = 1000, 625

# id: (title, [nodes as (label, sublabel)], note)
D = {
    "jarvis": (
        "jarvis.voice_os",
        [
            ("雙拍喚醒", "麥克風常駐"),
            ("快路徑", "零 LLM 判斷"),
            ("桌面動作", "開檔／搜尋／鍵入"),
        ],
        "常用指令不經大模型",
    ),
    "gb10": (
        "local_llm.pipeline",
        [
            ("需求清單", "batch"),
            ("本地 GPU 主機", "LLM 推論"),
            ("圖表／報告草稿", "人審後採用"),
        ],
        "資料不出內網",
    ),
    "warroom": (
        "war_room.board",
        [("各部門工作項", "代號化"), ("稽核鏈", "狀態 + 期限"), ("看板", "手機可看")],
        "跨部門一頁看完",
    ),
    "voicein": (
        "voice_in.flow",
        [("會議錄音", "自動上傳"), ("轉錄 + 摘要", "待辦抽取"), ("人審", "通過才入庫")],
        "知識庫只收審過的內容",
    ),
    "brief": (
        "morning_brief.cron",
        [
            ("行程／待辦", "專案異常"),
            ("每日彙整", "固定時間"),
            ("手機推播", "一則看完"),
        ],
        "每天早上自動送達",
    ),
}


def box(d, x, y, w, h, title, sub):
    d.rectangle([x + 8, y + 8, x + w + 8, y + h + 8], fill=0)  # hard shadow
    d.rectangle([x, y, x + w, y + h], fill=1, outline=0, width=4)
    d.rectangle([x, y, x + w, y + 34], fill=0)
    d.text((x + 12, y + 3), "■", font=mono(24), fill=1)
    tw = d.textlength(title, font=zh(34))
    d.text((x + (w - tw) / 2, y + 62), title, font=zh(34), fill=0)
    sw = d.textlength(sub, font=zh(24))
    d.text((x + (w - sw) / 2, y + 116), sub, font=zh(24), fill=0)


def arrow(d, x0, x1, y):
    for x in range(x0, x1 - 18, 16):  # dashed pixel line
        d.rectangle([x, y - 2, x + 8, y + 2], fill=0)
    d.polygon([(x1 - 18, y - 12), (x1, y), (x1 - 18, y + 12)], fill=0)


os.makedirs(SHOTS, exist_ok=True)
for key, (title, nodes, note) in D.items():
    im = Image.new("1", (W, H), 1)
    d = ImageDraw.Draw(im)
    d.text((40, 36), title, font=mono(34), fill=0)
    d.rectangle([40, 84, W - 40, 88], fill=0)
    bw, bh, y = 250, 170, 220
    xs = [40, 375, 710]
    for (t, s), x in zip(nodes, xs):
        box(d, x, y, bw, bh, t, s)
    for a, b in zip(xs, xs[1:]):
        arrow(d, a + bw + 16, b - 8, y + bh // 2 + 17)
    # 1-bit checker strip as the only grey
    for yy in range(H - 96, H - 40, 8):
        for xx in range(40 + (yy // 8 % 2) * 8, W - 40, 16):
            d.rectangle([xx, yy, xx + 7, yy + 7], fill=0)
    nw = d.textlength(note, font=zh(30))
    d.rectangle([40, H - 150, 40 + nw + 32, H - 104], fill=0)
    d.text((56, H - 147), note, font=zh(30), fill=1)
    im.save(os.path.join(SHOTS, f"{key}-1bit.png"))
print("diagrams:", ", ".join(D))
