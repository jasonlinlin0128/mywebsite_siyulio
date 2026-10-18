# -*- coding: utf-8 -*-
"""Colour variants of 18 一位元: same pixel structure, different palettes."""

import copy
from styles import STYLES, USAGE

BASE = next(s for s in STYLES if s["id"] == "18-one-bit")
NAMES = [
    "bg",
    "surface",
    "line",
    "ink",
    "ink-muted",
    "brand",
    "brand-text",
    "brand-soft",
    "on-brand",
    "accent",
    "accent-soft",
    "on-accent",
    "focus",
]

# id suffix, name, blurb, first theme, {token: (first-theme value, second-theme value)}
P = [
    (
        "b",
        "綠色磷光",
        "老式單色螢幕的綠，深色為主，最有「終端機」感。",
        "dark",
        dict(
            bg=("#071a0c", "#eef7ee"),
            surface=("#0b2412", "#ffffff"),
            line=("#33ff77", "#0b5a26"),
            ink=("#7dffa6", "#0a2a14"),
            **{"ink-muted": ("#4fc779", "#2f5a3d")},
            brand=("#33ff77", "#0b5a26"),
            **{
                "brand-text": ("#7dffa6", "#0b5a26"),
                "brand-soft": ("#103a1d", "#d5efd9"),
                "on-brand": ("#071a0c", "#ffffff"),
            },
            accent=("#e8ff6a", "#5a6b00"),
            **{
                "accent-soft": ("#26330f", "#eef5c8"),
                "on-accent": ("#071a0c", "#ffffff"),
            },
            focus=("#e8ff6a", "#5a6b00"),
        ),
    ),
    (
        "c",
        "琥珀終端",
        "琥珀色單色螢幕，比綠色溫暖，像深夜還亮著的機台。",
        "dark",
        dict(
            bg=("#140c00", "#fbf4e6"),
            surface=("#1d1300", "#ffffff"),
            line=("#ffb000", "#8a5a00"),
            ink=("#ffc23d", "#2a1a00"),
            **{"ink-muted": ("#c98f1c", "#6b4a12")},
            brand=("#ffb000", "#8a5a00"),
            **{
                "brand-text": ("#ffc23d", "#7a4f00"),
                "brand-soft": ("#3a2600", "#f6e3bd"),
                "on-brand": ("#140c00", "#ffffff"),
            },
            accent=("#ff6a3d", "#b33a12"),
            **{
                "accent-soft": ("#3a1a10", "#f8d8cc"),
                "on-accent": ("#140c00", "#ffffff"),
            },
            focus=("#ffe08a", "#b33a12"),
        ),
    ),
    (
        "d",
        "掌機四綠",
        "四階橄欖綠，像早期掌上遊戲機的螢幕，最有玩心。",
        "light",
        dict(
            bg=("#9bbc0f", "#0f380f"),
            surface=("#b3cf3a", "#1d4a1d"),
            line=("#0f380f", "#9bbc0f"),
            ink=("#0f380f", "#d6e89a"),
            **{"ink-muted": ("#24480f", "#b3cf3a")},
            brand=("#0f380f", "#9bbc0f"),
            **{
                "brand-text": ("#0f380f", "#d6e89a"),
                "brand-soft": ("#c5dc6a", "#306230"),
                "on-brand": ("#d6e89a", "#0f380f"),
            },
            accent=("#306230", "#d6e89a"),
            **{
                "accent-soft": ("#c5dc6a", "#2a542a"),
                "on-accent": ("#e7f0c0", "#0f380f"),
            },
            focus=("#0f380f", "#d6e89a"),
        ),
    ),
    (
        "e",
        "系統灰",
        "九〇年代視窗系統的灰底與深藍標題列，熟悉又專業。",
        "light",
        dict(
            bg=("#c0c0c0", "#202020"),
            surface=("#dcdcdc", "#2c2c2c"),
            line=("#000000", "#9a9a9a"),
            ink=("#000000", "#f0f0f0"),
            **{"ink-muted": ("#2e2e2e", "#c0c0c0")},
            brand=("#000080", "#2f5fd6"),
            **{
                "brand-text": ("#000080", "#9ab8ff"),
                "brand-soft": ("#b8b8e0", "#22264a"),
                "on-brand": ("#ffffff", "#ffffff"),
            },
            accent=("#006b6b", "#4fd1c5"),
            **{
                "accent-soft": ("#9ed6d6", "#16393a"),
                "on-accent": ("#ffffff", "#000000"),
            },
            focus=("#000080", "#9ab8ff"),
        ),
    ),
    (
        "f",
        "米色電腦",
        "米白機殼色加一點番茄紅，像老電腦本體，溫和不刺眼。",
        "light",
        dict(
            bg=("#efe9da", "#1c1a16"),
            surface=("#faf6ec", "#26231d"),
            line=("#1c1a16", "#efe9da"),
            ink=("#1c1a16", "#f3eee2"),
            **{"ink-muted": ("#4f4a3e", "#c4bca8")},
            brand=("#1c1a16", "#f3eee2"),
            **{
                "brand-text": ("#1c1a16", "#f3eee2"),
                "brand-soft": ("#e0d8c2", "#3a352b"),
                "on-brand": ("#faf6ec", "#1c1a16"),
            },
            accent=("#c23b22", "#ff7a5c"),
            **{
                "accent-soft": ("#f3d2c6", "#45261d"),
                "on-accent": ("#ffffff", "#1c1a16"),
            },
            focus=("#c23b22", "#ff7a5c"),
        ),
    ),
    (
        "g",
        "夜藍桃紅",
        "深夜藍底配桃紅與檸檬黃，像小型遊戲主機的調色盤，最鮮明。",
        "dark",
        dict(
            bg=("#1d2b53", "#fff1e8"),
            surface=("#22305e", "#ffffff"),
            line=("#c2c3c7", "#5f574f"),
            ink=("#fff1e8", "#1d2b53"),
            **{"ink-muted": ("#c2c3c7", "#5f574f")},
            brand=("#ff77a8", "#7e2553"),
            **{
                "brand-text": ("#ff9fc2", "#7e2553"),
                "brand-soft": ("#3a2f63", "#ffe0ec"),
                "on-brand": ("#1d2b53", "#ffffff"),
            },
            accent=("#ffec27", "#ab5236"),
            **{
                "accent-soft": ("#3c4030", "#fde9c9"),
                "on-accent": ("#1d2b53", "#ffffff"),
            },
            focus=("#ffec27", "#7e2553"),
        ),
    ),
    (
        "h",
        "曬圖藍",
        "藍底白線，像工程曬圖，把像素風和工程感結合。",
        "dark",
        dict(
            bg=("#0d3b8c", "#eef3fb"),
            surface=("#12459e", "#ffffff"),
            line=("#ffffff", "#0d3b8c"),
            ink=("#ffffff", "#0a2a66"),
            **{"ink-muted": ("#c9d8f5", "#3a5288")},
            brand=("#ffffff", "#0d3b8c"),
            **{
                "brand-text": ("#ffffff", "#0d3b8c"),
                "brand-soft": ("#1e57b5", "#dbe6f8"),
                "on-brand": ("#0d3b8c", "#ffffff"),
            },
            accent=("#ffd447", "#a35a00"),
            **{
                "accent-soft": ("#2d4f8a", "#fbeccb"),
                "on-accent": ("#0d3b8c", "#ffffff"),
            },
            focus=("#ffd447", "#a35a00"),
        ),
    ),
]


def M(*vals):
    """Positional palette in NAMES order; each value is (first, second)."""
    return dict(zip(NAMES, vals))


# second batch: mixes — warm paper grounds with one strong accent, and darker grounds
P += [
    (
        "i",
        "米白深綠",
        "米白機殼底、黑字，強調色換成深綠，穩重像工廠控制盤。",
        "light",
        M(
            ("#f1ecdf", "#14181a"),
            ("#fbf8f0", "#1d2326"),
            ("#1a1a17", "#e6e2d6"),
            ("#1a1a17", "#efece3"),
            ("#4d493f", "#b9b5a8"),
            ("#1a1a17", "#efece3"),
            ("#1a1a17", "#efece3"),
            ("#e2dccb", "#2b3236"),
            ("#fbf8f0", "#14181a"),
            ("#1f6b3a", "#5fd38d"),
            ("#d3e6d6", "#1b3526"),
            ("#ffffff", "#0d1a12"),
            ("#1f6b3a", "#5fd38d"),
        ),
    ),
    (
        "j",
        "米白鈷藍",
        "米白底配鈷藍強調，像老式說明書的印刷藍，清楚又可靠。",
        "light",
        M(
            ("#f1ecdf", "#121522"),
            ("#fbf8f0", "#1b1f30"),
            ("#1a1a17", "#e3e5ef"),
            ("#1a1a17", "#eef0f7"),
            ("#4d493f", "#b4b8c8"),
            ("#1a1a17", "#eef0f7"),
            ("#1a1a17", "#eef0f7"),
            ("#e2dccb", "#272c42"),
            ("#fbf8f0", "#121522"),
            ("#1d4ed8", "#7aa2ff"),
            ("#d6e0fa", "#1f2a52"),
            ("#ffffff", "#0b1230"),
            ("#1d4ed8", "#7aa2ff"),
        ),
    ),
    (
        "k",
        "黑白番茄紅",
        "原版黑白，只把連結藍換成番茄紅，最接近原版又多一點個性。",
        "light",
        M(
            ("#ffffff", "#000000"),
            ("#ffffff", "#111111"),
            ("#000000", "#ffffff"),
            ("#000000", "#ffffff"),
            ("#3a3a3a", "#c8c8c8"),
            ("#000000", "#ffffff"),
            ("#000000", "#ffffff"),
            ("#e6e6e6", "#262626"),
            ("#ffffff", "#000000"),
            ("#d0261c", "#ff6b5e"),
            ("#fbdad6", "#3a1210"),
            ("#ffffff", "#000000"),
            ("#d0261c", "#ff6b5e"),
        ),
    ),
    (
        "l",
        "紙白墨藍",
        "淺紙色底、深墨藍線條與文字、芥末黃點綴，像工程筆記本。",
        "light",
        M(
            ("#f6f4ee", "#0f1b33"),
            ("#ffffff", "#16244a"),
            ("#13284f", "#d9e2f2"),
            ("#13284f", "#e9eef8"),
            ("#4a5674", "#a9b6d0"),
            ("#13284f", "#e9eef8"),
            ("#13284f", "#e9eef8"),
            ("#dfe5f0", "#223463"),
            ("#ffffff", "#0f1b33"),
            ("#9a6a00", "#f2c14e"),
            ("#f5e7c2", "#3a3220"),
            ("#ffffff", "#0f1b33"),
            ("#13284f", "#f2c14e"),
        ),
    ),
    (
        "m",
        "炭黑亮橘",
        "炭黑底、米白線條，強調色是工業亮橘，像機台警示燈。",
        "dark",
        M(
            ("#151515", "#f4f1ea"),
            ("#1f1f1f", "#ffffff"),
            ("#ece7dc", "#151515"),
            ("#ece7dc", "#151515"),
            ("#a9a397", "#55524a"),
            ("#ece7dc", "#151515"),
            ("#ece7dc", "#151515"),
            ("#2c2c2c", "#e4dfd3"),
            ("#151515", "#ffffff"),
            ("#ff7a1a", "#b84a00"),
            ("#3a2414", "#fadbc4"),
            ("#151515", "#ffffff"),
            ("#ff7a1a", "#b84a00"),
        ),
    ),
    (
        "n",
        "深海青綠",
        "近黑的深藍底配青綠，比綠色磷光收斂，偏現代科技感。",
        "dark",
        M(
            ("#0b1117", "#eef6f5"),
            ("#111a22", "#ffffff"),
            ("#3ee6c4", "#0b5e50"),
            ("#d8f3ee", "#0b1d1a"),
            ("#8fb3ad", "#3d5c57"),
            ("#3ee6c4", "#0b5e50"),
            ("#6ff0d6", "#0b5e50"),
            ("#123129", "#d3efe9"),
            ("#0b1117", "#ffffff"),
            ("#ffd166", "#8a5a00"),
            ("#2f2a1a", "#f7e8c4"),
            ("#0b1117", "#ffffff"),
            ("#ffd166", "#8a5a00"),
        ),
    ),
]

VARIANTS = []
a = copy.deepcopy(BASE)
a["id"] = "18a-one-bit"
a["title"] = "siyulio · 18a 黑白原版"
a["blurb"] = "原版：純黑白加一個超連結藍，最乾淨、最經典。"
VARIANTS.append(a)

for suf, name, blurb, first, pal in P:
    st = copy.deepcopy(BASE)
    second = "light" if first == "dark" else "dark"
    st["id"] = f"18{suf}-pixel"
    st["title"] = f"siyulio · 18{suf} {name}"
    st["blurb"] = blurb
    st["themes"] = [
        {"id": first, "name": first.title()},
        {"id": second, "name": second.title()},
    ]
    st["colors"] = [
        {
            "name": n,
            "value": {first: pal[n][0], second: pal[n][1]},
            "usage": USAGE.get(n, ""),
        }
        for n in NAMES
    ]
    ln = pal["line"]
    st["shadows"] = [
        {
            "name": "shadow-card",
            "value": {first: f"4px 4px 0 {ln[0]}", second: f"4px 4px 0 {ln[1]}"},
            "usage": "Project cards and raised panels.",
        },
        {
            "name": "shadow-control",
            "value": {first: f"2px 2px 0 {ln[0]}", second: f"2px 2px 0 {ln[1]}"},
            "usage": "Buttons.",
        },
    ]
    VARIANTS.append(st)
