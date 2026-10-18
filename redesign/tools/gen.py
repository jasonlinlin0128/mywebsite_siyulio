# -*- coding: utf-8 -*-
"""Design-system generator for siyulio candidate systems.
usage: py gen.py <style_id|all>  -> writes out/<id>/project/...
"""

import json, os, sys, math, datetime, re

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from styles import STYLES

OUT = os.path.join(HERE, "out")
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- colour math
def _hex(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(x * 2 for x in c)
    return tuple(int(c[i : i + 2], 16) / 255 for i in (0, 2, 4))


def lum(c):
    def ch(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (ch(v) for v in _hex(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


# text pairs every system must hold: (fg, bg, min)
PAIRS = [
    ("ink", "bg", 4.5),
    ("ink", "surface", 4.5),
    ("ink-muted", "bg", 4.5),
    ("ink-muted", "surface", 4.5),
    ("brand-text", "bg", 4.5),
    ("brand-text", "surface", 4.5),
    ("on-brand", "brand", 4.5),
    ("on-accent", "accent", 4.5),
    ("ink", "brand-soft", 4.5),
    ("focus", "bg", 3.0),
    ("focus", "surface", 3.0),
    ("ink", "accent-soft", 4.5),
]


def resolve(colors, name, theme, themes):
    v = colors[name]["value"]
    if isinstance(v, str):
        val = v
    else:
        val = v.get(theme, v[themes[0]])
    if val.startswith("{"):
        return resolve(colors, val[1:-1], theme, themes)
    return val


def check(st):
    colors = {c["name"]: c for c in st["colors"]}
    themes = [t["id"] for t in st["themes"]]
    bad = []
    for th in themes:
        for fg, bg, mn in PAIRS:
            if fg not in colors or bg not in colors:
                bad.append(f"missing {fg}/{bg}")
                continue
            r = contrast(
                resolve(colors, fg, th, themes), resolve(colors, bg, th, themes)
            )
            if r < mn:
                bad.append(f"[{th}] {fg} on {bg} = {r:.2f} < {mn}")
        # cover blocks must not vanish into the ground
        for b in st["cover"]["blocks"]:
            r = contrast(
                resolve(colors, b, th, themes), resolve(colors, "bg", th, themes)
            )
            if r < 1.12:
                bad.append(f"[{th}] cover block {b} vs bg = {r:.2f}")
    return bad


# ---------------------------------------------------------------- tokens.json
SPACE_DEFAULT = [4, 8, 12, 16, 24, 32, 48, 64, 96]


def tokens_json(st):
    sp = st.get("space", SPACE_DEFAULT)
    space_usage = [
        "Hairline gaps, icon-to-label.",
        "Tag padding, tight stacks.",
        "Inline gaps between buttons and tags.",
        "Card padding (compact), paragraph gaps.",
        "Card padding, gutters between cards.",
        "Gaps between blocks inside a section.",
        "Space between sections on mobile.",
        "Space between sections on desktop.",
        "Hero top and bottom padding.",
    ]
    rad = st["radius"]
    t = {
        "name": st["title"],
        "version": 1,
        "color": {"themes": st["themes"], "tokens": st["colors"]},
        "type": {
            "fonts": [],
            "families": st["families"],
            "groups": st["typegroups"],
        },
        "spacing": {
            "tokens": [
                {"name": f"space-{i + 1}", "value": f"{v}px", "usage": space_usage[i]}
                for i, v in enumerate(sp)
            ]
        },
        "radius": {
            "tokens": [
                {
                    "name": "radius-sm",
                    "value": f"{rad[0]}px",
                    "usage": "Tags, inputs, small chips.",
                },
                {
                    "name": "radius-md",
                    "value": f"{rad[1]}px",
                    "usage": "Buttons and the site header.",
                },
                {
                    "name": "radius-lg",
                    "value": f"{rad[2]}px",
                    "usage": "Project cards, hero media, large panels.",
                },
                {
                    "name": "radius-pill",
                    "value": "999px",
                    "usage": "Pill tags and status dots only.",
                },
            ]
        },
        "shadow": {"tokens": st["shadows"]},
        "border": {
            "tokens": [
                {
                    "name": "border-width",
                    "value": f"{st['bw']}px",
                    "usage": "Every structural border: cards, header, buttons.",
                },
            ]
        },
    }
    return t


# ---------------------------------------------------------------- bundle.css
def bundle_css(st):
    k = st["knobs"]
    fonts = f"@import url('{st['gfonts']}');\n" if st.get("gfonts") else ""
    label_tf = "uppercase" if k.get("label_upper") else "none"
    head_tf = "uppercase" if k.get("head_upper") else "none"
    css = (
        fonts
        + f"""
/* siyulio · {st["title"]} — component styles. Values come from tokens.css; nothing here re-declares a token. */
html, body {{ margin: 0; }}
body {{ font-family: var(--font-sans); background: var(--bg); color: var(--ink); -webkit-font-smoothing: antialiased; }}
.sy-pad {{ padding: var(--space-5); }}
.sy-row {{ display: flex; flex-wrap: wrap; gap: var(--space-3); align-items: center; padding: var(--space-5); }}
.sy-label {{ font-family: var(--font-label); font-size: 12px; line-height: 16px; letter-spacing: {k.get("label_ls", "0.08em")}; text-transform: {label_tf}; color: var(--ink-muted); font-weight: {k.get("label_w", 500)}; }}
.sy-h {{ font-family: var(--font-display); font-weight: {k.get("head_w", 700)}; letter-spacing: {k.get("head_ls", "-0.01em")}; text-transform: {head_tf}; color: var(--ink); margin: 0; }}

/* Button */
.sy-btn {{ font: inherit; font-family: var(--font-{k.get("btn_font", "sans")}); font-size: 15px; font-weight: {k.get("btn_w", 600)}; line-height: 20px; height: 44px; padding: 0 var(--space-5);
  display: inline-flex; align-items: center; gap: var(--space-2); border-radius: var(--radius-md); border: var(--border-width) solid var(--{k.get("btn_border", "line")});
  background: var(--surface); color: var(--ink); cursor: pointer; text-decoration: none; text-transform: {"uppercase" if k.get("btn_upper") else "none"}; letter-spacing: {k.get("btn_ls", "0")}; box-shadow: var(--shadow-control); }}
.sy-btn-primary {{ background: var(--brand); border-color: var(--{k.get("btn_primary_border", "brand")}); color: var(--on-brand); }}
.sy-btn-ghost {{ background: transparent; border-color: transparent; box-shadow: none; color: var(--brand-text); padding: 0 var(--space-2); }}
.sy-btn:hover {{ {k.get("btn_hover", "filter: brightness(0.96);")} }}
.sy-btn:focus-visible, .sy-tag:focus-visible, .sy-nav a:focus-visible, .sy-card:focus-visible {{ outline: 2px solid var(--focus); outline-offset: 3px; }}

/* Tag */
.sy-tag {{ display: inline-flex; align-items: center; gap: var(--space-1); font-family: var(--font-label); font-size: 12px; line-height: 16px; padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-{k.get("tag_radius", "sm")}); background: var(--brand-soft); color: var(--ink); border: {k.get("tag_border", "0")}; text-transform: {label_tf}; letter-spacing: {k.get("label_ls", "0.08em")}; }}
.sy-tag-accent {{ background: var(--accent-soft); }}
.sy-tag-outline {{ background: transparent; border: var(--border-width) solid var(--line); color: var(--ink-muted); }}
.sy-dot {{ width: 8px; height: 8px; border-radius: var(--radius-pill); background: var(--accent); display: inline-block; }}

/* SiteHeader */
.sy-header {{ display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); padding: var(--space-3) var(--space-5);
  background: var(--{k.get("header_bg", "surface")}); border-bottom: var(--border-width) solid var(--line); {k.get("header_extra", "")} }}
.sy-logo {{ font-family: var(--font-display); font-weight: {k.get("logo_w", 700)}; font-size: 20px; letter-spacing: {k.get("logo_ls", "-0.01em")}; color: var(--ink); text-decoration: none; text-transform: {"uppercase" if k.get("logo_upper") else "none"}; }}
.sy-logo b {{ color: var(--brand-text); font-weight: inherit; }}
.sy-nav {{ display: flex; gap: var(--space-5); align-items: center; }}
.sy-nav a {{ font-family: var(--font-{k.get("nav_font", "sans")}); font-size: 14px; color: var(--ink-muted); text-decoration: none; text-transform: {label_tf if k.get("nav_upper") else "none"}; letter-spacing: {k.get("nav_ls", "0")}; }}
.sy-nav a[aria-current] {{ color: var(--ink); {k.get("nav_current", "text-decoration: underline; text-decoration-color: var(--brand); text-underline-offset: 6px; text-decoration-thickness: 2px;")} }}

/* Hero */
.sy-hero {{ padding: var(--space-8) var(--space-6); background: var(--{k.get("hero_bg", "bg")}); display: grid; gap: var(--space-5); {k.get("hero_extra", "")} }}
.sy-hero .sy-kicker {{ font-family: var(--font-label); font-size: 13px; letter-spacing: {k.get("label_ls", "0.08em")}; text-transform: {label_tf}; color: var(--brand-text); margin: 0; }}
.sy-hero h1 {{ font-family: var(--font-display); font-size: {k.get("hero_size", "56px")}; line-height: {k.get("hero_lh", "1.05")}; font-weight: {k.get("head_w", 700)}; letter-spacing: {k.get("head_ls", "-0.01em")}; text-transform: {head_tf}; margin: 0; max-width: 16em; }}
.sy-hero h1 em {{ font-style: {k.get("em_style", "normal")}; color: var(--brand-text); {k.get("em_extra", "")} }}
.sy-hero p {{ font-size: 18px; line-height: 30px; color: var(--ink-muted); margin: 0; max-width: 34em; }}
.sy-hero .sy-actions {{ display: flex; gap: var(--space-3); flex-wrap: wrap; }}

/* ProjectCard */
.sy-cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: var(--space-5); padding: var(--space-5); }}
.sy-card {{ display: grid; gap: var(--space-3); align-content: start; padding: var(--space-{k.get("card_pad", "5")}); background: var(--surface); border: var(--border-width) solid var(--{k.get("card_border", "line")});
  border-radius: var(--radius-lg); box-shadow: var(--shadow-card); color: var(--ink); text-decoration: none; {k.get("card_extra", "")} }}
.sy-card .sy-media {{ aspect-ratio: 16 / 10; border-radius: calc(var(--radius-lg) - 4px); background: var(--{k.get("media_bg", "brand-soft")}); display: grid; place-items: center; overflow: hidden; {k.get("media_extra", "")} }}
.sy-card .sy-media span {{ font-family: var(--font-display); font-size: 40px; color: var(--{k.get("media_ink", "brand-text")}); font-weight: {k.get("head_w", 700)}; }}
.sy-card h3 {{ font-family: var(--font-display); font-size: 22px; line-height: 28px; font-weight: {k.get("head_w", 700)}; letter-spacing: {k.get("head_ls", "-0.01em")}; text-transform: {head_tf}; margin: 0; }}
.sy-card p {{ font-size: 15px; line-height: 24px; color: var(--ink-muted); margin: 0; }}
.sy-card .sy-tags {{ display: flex; gap: var(--space-2); flex-wrap: wrap; }}
.sy-card:hover {{ {k.get("card_hover", "border-color: var(--ink);")} }}

/* Timeline */
.sy-timeline {{ list-style: none; margin: 0; padding: var(--space-5); display: grid; gap: 0; }}
.sy-timeline li {{ display: grid; grid-template-columns: 96px 1fr; gap: var(--space-4); padding: var(--space-4) 0; border-top: var(--border-width) solid var(--line); }}
.sy-timeline li:last-child {{ border-bottom: var(--border-width) solid var(--line); }}
.sy-timeline time {{ font-family: var(--font-label); font-size: 13px; line-height: 24px; color: var(--brand-text); letter-spacing: {k.get("label_ls", "0.08em")}; }}
.sy-timeline h4 {{ font-family: var(--font-display); font-size: 18px; line-height: 24px; margin: 0; font-weight: {k.get("head_w", 700)}; text-transform: {head_tf}; }}
.sy-timeline p {{ font-size: 15px; line-height: 24px; margin: var(--space-1) 0 0; color: var(--ink-muted); }}
"""
    )
    return css + "\n/* signature details */\n" + st.get("extra_css", "") + "\n"


# ---------------------------------------------------------------- previews
def doc(marker, body, st, title):
    link = f'<link rel="stylesheet" href="{st["gfonts"]}">' if st.get("gfonts") else ""
    return f"""{marker}
<!doctype html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><title>{title}</title>{link}</head>
<body>
{body}
</body>
</html>
"""


def C(st, key, default):
    return st.get("copy", {}).get(key, default)


def previews(st):
    p = {}
    brand = st.get("logo", "siyu<b>lio</b>")
    p["Button"] = doc(
        '<!-- @dsCard group="Actions" height=100 subtitle="主要、次要、文字按鈕" -->',
        f"""<div class="sy-row">
  <a class="sy-btn sy-btn-primary" href="#">{C(st, "cta1", "看作品集")}</a>
  <a class="sy-btn" href="#">{C(st, "cta2", "聯絡我")}</a>
  <a class="sy-btn sy-btn-ghost" href="#">{C(st, "cta3", "下載履歷 →")}</a>
</div>""",
        st,
        "Button",
    )
    p["Tag"] = doc(
        '<!-- @dsCard group="Actions" height=90 subtitle="技術標籤、狀態" -->',
        """<div class="sy-row">
  <span class="sy-tag">AI Agent</span>
  <span class="sy-tag">Python</span>
  <span class="sy-tag sy-tag-accent"><span class="sy-dot"></span>運作中</span>
  <span class="sy-tag sy-tag-outline">2026</span>
</div>""",
        st,
        "Tag",
    )
    p["SiteHeader"] = doc(
        '<!-- @dsCard group="Layout" height=90 subtitle="全站頂部導覽" -->',
        f"""<header class="sy-header">
  <a class="sy-logo" href="#">{brand}</a>
  <nav class="sy-nav" aria-label="主要導覽">
    <a href="#" aria-current="page">{C(st, "nav1", "作品")}</a><a href="#">{C(st, "nav2", "關於")}</a><a href="#">{C(st, "nav3", "筆記")}</a><a href="#">{C(st, "nav4", "聯絡")}</a>
  </nav>
</header>""",
        st,
        "SiteHeader",
    )
    p["Hero"] = doc(
        '<!-- @dsCard group="Layout" height=430 subtitle="首頁自我介紹" -->',
        f"""<section class="sy-hero">
  <p class="sy-kicker">{C(st, "kicker", "Jason Lin · 林佳賢")}</p>
  <h1>{C(st, "hero", "在製造業裡，<em>把 AI 變成每天會跑的產線</em>。")}</h1>
  <p>{C(st, "lead", "我設計並維運 24 小時運作的 AI agent：語音助理、第二大腦、本地大模型與自動化報表。這裡收錄我做過的系統、寫下的筆記，以及正在進行的實驗。")}</p>
  <div class="sy-actions"><a class="sy-btn sy-btn-primary" href="#">{C(st, "cta1", "看作品集")}</a><a class="sy-btn" href="#">{C(st, "cta2", "聯絡我")}</a></div>
</section>""",
        st,
        "Hero",
    )
    cards = [
        (
            "Jarvis",
            "Jarvis 語音 OS",
            "雙拍喚醒、零 LLM 快路徑，能開檔、搜尋、鍵入的桌面語音助理。",
            ["Voice", "Agent"],
        ),
        (
            "Hub",
            "第二大腦 Hub",
            "跨專案事實源與儀表板：會議、日誌、專案狀態自動匯流成一頁。",
            ["Python", "Vercel"],
        ),
        (
            "GB10",
            "本地模型產線",
            "在 DGX Spark 上跑本地 LLM，批次起草圖表與報告，不出內網。",
            ["LLM", "On-prem"],
        ),
    ]
    html = (
        '<div class="sy-cards">\n'
        + "\n".join(
            f'  <a class="sy-card" href="#"><div class="sy-media"><span>{m}</span></div><h3>{t}</h3><p>{d}</p><div class="sy-tags">'
            + "".join(f'<span class="sy-tag">{g}</span>' for g in tags)
            + "</div></a>"
            for m, t, d, tags in cards
        )
        + "\n</div>"
    )
    p["ProjectCard"] = doc(
        '<!-- @dsCard group="Content" height=470 subtitle="作品集卡片" -->',
        html,
        st,
        "ProjectCard",
    )
    p["Timeline"] = doc(
        '<!-- @dsCard group="Content" height=340 subtitle="經歷與里程碑" -->',
        """<ol class="sy-timeline">
  <li><time>2026.10</time><div><h4>Agent OS 五狀態看板</h4><p>登入自啟、生命週期看板，讓背景 agent 的健康狀態一眼可見。</p></div></li>
  <li><time>2026.07</time><div><h4>Jarvis 語音 OS 上線</h4><p>STT、TTS、HUD 到行動能力，八個階段全數交付。</p></div></li>
  <li><time>2026.04</time><div><h4>買下 siyulio.com</h4><p>決定把作品與思考集中在一個屬於自己的地方。</p></div></li>
</ol>""",
        st,
        "Timeline",
    )
    return p


COMP_README = {
    "Button": '# Button\n\n行動按鈕，一個畫面最多一顆 `sy-btn-primary`，留給這頁最想讓人做的事（看作品、聯絡）。\n\n- 結構：`<a class="sy-btn sy-btn-primary">` / `sy-btn` / `sy-btn-ghost`；使用者提供文字與 href。\n- 文案動詞開頭、四到六個字：「看作品集」「聯絡我」。\n- 主要按鈕底色 `brand`、字色 `on-brand`；次要按鈕 `surface` 底配 `ink`；文字按鈕用 `brand-text`。\n- 焦點環一律 `focus`，2px 實線、外移 3px。\n- 不要：同一列兩顆主要按鈕、全大寫中文、圖示取代文字。\n',
    "Tag": "# Tag\n\n短標籤，標示技術、領域或狀態，放在作品卡與文章頁。\n\n- `sy-tag`：技術名（`brand-soft` 底、`ink` 字）。`sy-tag-accent` 搭配 `sy-dot` 表示狀態（運作中、維護中）。`sy-tag-outline`：年份、次要資訊。\n- 每張卡最多三個標籤；超過就改寫描述。\n- 狀態一定有文字，不只靠顏色。\n",
    "SiteHeader": '# SiteHeader\n\n全站頂部導覽：左邊名字標誌、右邊四個以內的頁面連結。\n\n- 使用者提供連結清單；目前頁面加 `aria-current="page"`。\n- 標誌是純文字 `sy-logo`，`<b>` 包住的部分以 `brand-text` 著色。沒有圖形 logo，在有正式標誌前不要畫一個。\n- 手機版收成單列可橫向捲動，不做漢堡選單以外的花樣。\n',
    "Hero": "# Hero\n\n首頁第一屏：一行身分、一句主張、一段說明、兩顆按鈕。\n\n- 結構：`.sy-kicker`（姓名或身分）→ `h1`（主張，`<em>` 包住關鍵片語）→ `p`（兩三句說明）→ `.sy-actions`。\n- 主張寫你「做出什麼結果」，不寫形容詞自誇。\n- 一頁只有一個 Hero；內頁用較小的標題區，不重用它。\n",
    "ProjectCard": '# ProjectCard\n\n作品集卡片：示意圖、名稱、一句話成果、技術標籤，整張可點。\n\n- 結構：`<a class="sy-card">` 內含 `.sy-media`（截圖或代號字）、`h3`、`p`、`.sy-tags`。\n- 放進 `.sy-cards` 網格，自動 240px 起排列。\n- 描述寫「做到什麼」，一句話、不超過 40 字。\n- 公司內部系統用代號與示意圖，不放真實客戶名或內部畫面。\n',
    "Timeline": '# Timeline\n\n經歷與里程碑列表，逆時序。\n\n- 結構：`<ol class="sy-timeline">` 每個 `li` 是 `time` + 標題 `h4` + 一句說明。\n- 日期格式 `YYYY.MM`。\n- 用在「關於」頁與履歷頁；首頁最多放三筆。\n',
}


# ---------------------------------------------------------------- cover
def name_size(st):
    k = st["cover"].get("em", 0.6)
    n = len(st["cover"].get("name", "siyulio"))
    return min(120, int(440 / (n * k)))


def cover(st):
    cv = st["cover"]
    H = cv.get("height", 288)
    g = 16
    B = cv["blocks"]  # [primary, deep, tint, accent, (extra)]
    rad = st["radius"]
    rk = cv.get("corner", "radius-md")
    rv = {"radius-sm": rad[0], "radius-md": rad[1], "radius-lg": rad[2], "none": 0}[rk]
    arr = cv["arrangement"]
    rects = []
    region = None
    notes = {}

    def R(cls, x, y, w, h, r=rv):
        rects.append((cls, x, y, w, h, r))

    if arr == "slab":
        R("b0", g, -g, 9 * g, 15 * g)
        R("b3", g, 15 * g, 4 * g, int(1.5 * g), rad[0])
        R("b2", 11 * g, 5 * g, 8 * g, 11 * g)
        R("b1", 20 * g, 3 * g, 11 * g, 13 * g)
        region = (11 * g, 0, 8 * g, 16 * g)
        notes["arr"] = (
            "one tall primary slab bled off the top with satellites, bottoms on one line space-6 above the edge"
        )
    elif arr == "grid":
        R("b0", 0, 0, 15 * g, 10 * g, 0)
        R("b1", 15 * g, 0, 15 * g, 6 * g, 0)
        R("b2", 15 * g, 6 * g, 15 * g, 12 * g, 0)
        R("b3", 0, 10 * g, 7 * g, 8 * g, 0)
        region = (15 * g, 6 * g, 15 * g, 12 * g)
        notes["arr"] = (
            "a flush modular grid filling the right half, one cell left as ground"
        )
    elif arr == "bands":
        R("b0", 0, 2 * g, 30 * g, 6 * g, 0)
        R("b1", 6 * g, 9 * g, 24 * g, 3 * g, 0)
        R("b2", 0, 13 * g, 30 * g, 5 * g, 0)
        R("b3", 0, 9 * g, 5 * g, 3 * g, 0)
        region = (0, 2 * g, 30 * g, 6 * g)
        notes["arr"] = (
            "unequal horizontal bands bleeding off the right edge, a ground gutter between each"
        )
    elif arr == "stagger":
        R("b2", 2 * g, 1 * g, 12 * g, 9 * g)
        R("b0", 8 * g, 5 * g, 13 * g, 10 * g)
        R("b1", 16 * g, 10 * g, 14 * g, 9 * g)
        R("b3", 24 * g, 2 * g, 4 * g, 4 * g, rad[0])
        region = (2 * g, 1 * g, 6 * g, 9 * g)
        notes["arr"] = (
            "a staggered stack stepping down and right, the last block bleeding off the bottom"
        )
    elif arr == "bleed":
        R("b0", 9 * g, -4 * g, 22 * g, 14 * g)
        R("b1", 2 * g, 7 * g, 10 * g, 12 * g)
        R("b2", 13 * g, 11 * g, 9 * g, 5 * g)
        R("b3", 24 * g, 11 * g, 5 * g, 5 * g, rad[0])
        region = (9 * g, -4 * g, 22 * g, 14 * g)
        notes["arr"] = (
            "a large primary block bleeding off the top and right, satellites below"
        )
    elif arr == "columns":
        R("b0", 2 * g, 0, 7 * g, 18 * g, 0)
        R("b2", 10 * g, 4 * g, 7 * g, 14 * g, 0)
        R("b1", 18 * g, 8 * g, 7 * g, 10 * g, 0)
        R("b3", 26 * g, 12 * g, 4 * g, 6 * g, 0)
        region = (10 * g, 4 * g, 7 * g, 14 * g)
        notes["arr"] = (
            "four columns rising right-to-left like a bar chart, all standing on the bottom edge"
        )
    else:
        raise ValueError(arr)

    pat = cv["pattern"]
    pc = cv.get("pclass", "p0")
    units = []
    px, py, pw, ph = region
    pitch = cv.get("pitch", 24)
    if pat == "dots":
        n = 0
        for yy in range(py + pitch // 2, py + ph, pitch):
            for xx in range(px + pitch // 2, px + pw, pitch):
                if yy < 0:
                    continue
                if n >= 60:
                    break
                units.append(
                    f'<circle class="{pc}" cx="{xx}" cy="{yy}" r="{cv.get("dot", 2.5)}"/>'
                )
                n += 1
    elif pat == "plus":
        n = 0
        for yy in range(py + pitch // 2, py + ph, pitch):
            for xx in range(px + pitch // 2, px + pw, pitch):
                if yy < 0 or n >= 40:
                    continue
                units.append(
                    f'<path class="{pc}s" d="M{xx - 5} {yy}H{xx + 5}M{xx} {yy - 5}V{yy + 5}"/>'
                )
                n += 1
    elif pat == "rules":
        for i in range(cv.get("count", 4)):
            yy = py + ph - 8 - i * pitch
            units.append(f'<line class="{pc}s" x1="0" y1="{yy}" x2="480" y2="{yy}"/>')
    elif pat == "pills":
        ws = [40, 24, 32, 16, 48, 24, 16, 32, 40, 24, 32, 16, 24, 40, 16, 32, 24, 48]
        i = 0
        yy = py + ph - 16
        while yy > max(py, 8) and i < 24:
            xx = px + 8 + (i % 3) * 8
            while xx + ws[i % len(ws)] < px + pw - 8 and i < 24:
                w = ws[i % len(ws)]
                units.append(
                    f'<rect class="{pc}" x="{xx}" y="{yy}" width="{w}" height="8" rx="4"/>'
                )
                xx += w + 12
                i += 1
            yy -= pitch
    elif pat == "discs":
        r = cv.get("disc", 14)
        n = 0
        for yy in range(py + pitch // 2, py + ph, pitch):
            for xx in range(px + pitch // 2, px + pw, pitch):
                if yy < 0 or n >= 24:
                    continue
                rr = r if (n % 3) else r * 0.6
                units.append(f'<circle class="{pc}" cx="{xx}" cy="{yy}" r="{rr:.0f}"/>')
                n += 1
    elif pat == "stripes":
        units.append(
            f'<clipPath id="cp"><rect x="{px}" y="{py}" width="{pw}" height="{ph}"/></clipPath>'
        )
        n = 0
        for d in range(-ph, pw + ph, pitch):
            if n >= 30:
                break
            units.append(
                f'<line class="{pc}w" clip-path="url(#cp)" x1="{px + d}" y1="{py + ph}" x2="{px + d + ph}" y2="{py}"/>'
            )
            n += 1
    elif pat == "checker":
        n = 0
        for j, yy in enumerate(range(py, py + ph, pitch)):
            for i, xx in enumerate(range(px, px + pw, pitch)):
                if (i + j) % 2 == 0 and n < 48 and yy >= 0:
                    units.append(
                        f'<rect class="{pc}" x="{xx}" y="{yy}" width="{pitch}" height="{pitch}"/>'
                    )
                    n += 1
    elif pat == "quarter":
        n = 0
        s = pitch
        for j, yy in enumerate(range(py, py + ph - s + 1, s)):
            for i, xx in enumerate(range(px, px + pw - s + 1, s)):
                if n >= 24 or yy < 0:
                    continue
                q = (i * 3 + j) % 4
                cx, cy = [(xx, yy), (xx + s, yy), (xx + s, yy + s), (xx, yy + s)][q]
                sx = 1 if cx == xx else -1
                sy = 1 if cy == yy else -1
                units.append(
                    f'<path class="{pc}" d="M{cx} {cy}L{cx + sx * s} {cy}A{s} {s} 0 0 {1 if sx * sy > 0 else 0} {cx} {cy + sy * s}Z"/>'
                )
                n += 1
    elif pat == "halftone":
        n = 0
        for j, yy in enumerate(range(py + pitch // 2, py + ph, pitch)):
            for i, xx in enumerate(range(px + pitch // 2, px + pw, pitch)):
                if n >= 60 or yy < 0:
                    continue
                r = max(1.0, (pitch / 2 - 1) * (1 - i / max(1, pw // pitch)))
                units.append(f'<circle class="{pc}" cx="{xx}" cy="{yy}" r="{r:.1f}"/>')
                n += 1
    elif pat == "glyph":
        ch = cv.get("glyph", "思")
        units.append(
            f'<clipPath id="cg"><rect x="{px}" y="{max(py, 0)}" width="{pw}" height="{ph}"/></clipPath>'
        )
        units.append(
            f'<text class="{pc} glyph" clip-path="url(#cg)" x="{px + pw // 2}" y="{max(py, 0) + ph - cv.get("glyph_drop", 10)}" text-anchor="middle">{ch}</text>'
        )
    elif pat == "tiles":
        n = 0
        s = pitch
        for j, yy in enumerate(range(py + 8, py + ph - s, s + 8)):
            for i, xx in enumerate(range(px + 8, px + pw - s, s + 8)):
                if n >= 30 or yy < 0:
                    continue
                w = (
                    s * 2 + 8
                    if (i + j * 2) % 5 == 0 and xx + 2 * s + 8 < px + pw
                    else s
                )
                units.append(
                    f'<rect class="{pc} tile" x="{xx}" y="{yy}" width="{w}" height="{s}"/>'
                )
                n += 1
    elif pat == "chevrons":
        n = 0
        for j, yy in enumerate(range(py + pitch, py + ph, pitch)):
            if n >= 10:
                break
            units.append(
                f'<path class="{pc}w" d="M{px} {yy}L{px + pw // 2} {yy - pitch // 2}L{px + pw} {yy}"/>'
            )
            n += 1
    else:
        raise ValueError(pat)

    # classes
    cls_css = []
    for i, tok in enumerate(B[:4]):
        cls_css.append(f".b{i}{{fill:var(--{tok});}}")
    pt = cv.get("ptoken", B[2])
    cls_css.append(
        f".{pc}{{fill:var(--{pt});}} .{pc}s{{stroke:var(--{pt});stroke-width:{cv.get('stroke', 1.5)};fill:none;}} .{pc}w{{stroke:var(--{pt});stroke-width:{pitch / 2:.0f};fill:none;}}"
    )
    cls_css.append(
        f".tile{{rx:var(--radius-sm);}} .glyph{{font-family:var(--font-display);font-size:{cv.get('glyph_size', 300)}px;font-weight:{cv.get('glyph_w', 900)};}}"
    )
    deriv = f"""
  blocks      {B[0]} (primary, largest) · {B[1]} (deep) · {B[2]} (tint) · {B[3]} (accent, small) — roughly a third of 960×{H}
  arrangement {notes["arr"]}
  pattern     {pat} in {pt} — {cv["why"]}
  scales      sides in space-4 (16px) multiples; pitch {pitch}px; corners {rk}; small block radius-sm
"""
    svg_rects = "\n".join(
        f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
        for c, x, y, w, h, r in rects
    )
    order = cv.get("pattern_over", True)
    inner = (
        (svg_rects + "\n" + "\n".join(units))
        if order
        else ("\n".join(units) + "\n" + svg_rects)
    )
    ns = name_size(st)
    link = f'<link rel="stylesheet" href="{st["gfonts"]}">' if st.get("gfonts") else ""
    return f"""<!-- @dsCard height={H} -->
<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>{st["title"]}</title>{link}
<style>
  html, body {{ margin:0; height:100%; }}
  body {{ background:var(--bg); color:var(--ink); font-family:var(--font-sans); overflow:hidden; }}
  .cover {{ position:relative; height:{H}px; overflow:hidden; }}
  .art {{ position:absolute; top:0; left:480px; width:480px; height:{H}px; overflow:hidden; }}
  .art svg {{ display:block; width:480px; height:{H}px; }}
  {" ".join(cls_css)}
  .words {{ position:absolute; left:var(--space-6); bottom:var(--space-6); max-width:440px; }}
  .name {{ margin:0; font-family:var(--font-display); font-size:{ns}px; line-height:.92; font-weight:{cv.get("name_w", 700)}; letter-spacing:{cv.get("name_ls", "-0.02em")}; color:var(--ink); {cv.get("name_extra", "")} }}
  .tag {{ margin:var(--space-2) 0 0 4px; font-size:14px; line-height:20px; color:var(--ink-muted); }}
</style>
</head>
<body>
<div class="cover">
<div class="art" aria-hidden="true">
<svg viewBox="0 0 480 {H}" width="480" height="{H}">
<!--{deriv}-->
{inner}
</svg>
</div>
<div class="words">
<h1 class="name">{cv.get("name", "siyulio")}</h1>
<p class="tag">{st["tagline"]}</p>
</div>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------- README
def readme(st):
    r = st["readme"]
    colors = st["colors"]
    lines = []
    lines.append(r["intro"].strip() + "\n")
    lines.append("## 適合的你\n")
    lines.append(r["fit"].strip() + "\n")
    lines.append("## 語氣與文案\n")
    for b in r["voice"]:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("範例：\n")
    for q in r["examples"]:
        lines.append(f"> {q}\n")
    lines.append("## 色彩\n")
    lines.append(r["color"].strip() + "\n")
    lines.append("| token | 用途 |\n| --- | --- |")
    for c in colors:
        lines.append(f"| `{c['name']}` | {c['usage']} |")
    lines.append("")
    lines.append(
        f"焦點環一律是 `focus` 色 2px 實線、外移 3px，在 `bg` 與 `surface` 上都至少 3:1。所有文字配對（`ink`、`ink-muted`、`brand-text` 在 `bg`／`surface` 上；`on-brand` 在 `brand` 上）在每個主題都達 4.5:1。\n"
    )
    lines.append("## 字體\n")
    lines.append(r["type"].strip() + "\n")
    lines.append("## 間距、版面與形狀\n")
    lines.append(r["layout"].strip() + "\n")
    lines.append("## 圖像與圖示\n")
    lines.append(r["imagery"].strip() + "\n")
    lines.append("## 元件\n")
    lines.append(
        "元件都是純 HTML + `components/bundle.css` 的 class（前綴 `sy-`），不需要 JavaScript：`SiteHeader`、`Hero`、`ProjectCard`、`Timeline`、`Button`、`Tag`。各元件的使用規則在它自己的 README。\n"
    )
    lines.append("## 這套的招牌細節\n")
    for b in r["signature"]:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("## 不要\n")
    for b in r["dont"]:
        lines.append(f"- {b}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- local tokens.css (for local render checks only; never published)
def tokens_css(st):
    t = tokens_json(st)
    themes = [x["id"] for x in st["themes"]]

    def val(c, th):
        v = c["value"]
        v = v if isinstance(v, str) else v.get(th, v[themes[0]])
        return f"var(--{v[1:-1]})" if v.startswith("{") else v

    out = []
    for i, th in enumerate(themes):
        sel = f':root, [data-theme="{th}"]' if i == 0 else f'[data-theme="{th}"]'
        decl = [f"--{c['name']}: {val(c, th)};" for c in t["color"]["tokens"]]
        decl += [
            f"--{s['name']}: {(s['value'] if isinstance(s['value'], str) else s['value'].get(th, s['value'][themes[0]]))};"
            for s in t["shadow"]["tokens"]
        ]
        out.append(sel + " { " + " ".join(decl) + " }")
    root = [
        f"--{s['name']}: {s['value']};"
        for fam in ("spacing", "radius", "border")
        for s in t[fam]["tokens"]
    ]
    root += [f"--font-{k}: {v};" for k, v in t["type"]["families"].items()]
    out.append(":root { " + " ".join(root) + " }")
    return "\n".join(out)


def compose(html, st, theme):
    css = tokens_css(st) + "\n" + bundle_css(st)
    html = html.split("\n", 1)[1]  # drop marker
    html = html.replace(
        '<html lang="zh-Hant">', f'<html lang="zh-Hant" data-theme="{theme}">'
    )
    return html.replace("</head>", f"<style>{css}</style></head>")


# ---------------------------------------------------------------- write
def build(st):
    bad = check(st)
    if bad:
        print(f"!! {st['id']} contrast problems:")
        [print("   ", b) for b in bad]
    root = os.path.join(OUT, st["id"])
    proj = os.path.join(root, "project")
    files = {}
    files["tokens.json"] = json.dumps(tokens_json(st), ensure_ascii=False, indent=2)
    files["README.md"] = readme(st)
    files["components/bundle.css"] = bundle_css(st)
    for name, html in previews(st).items():
        files[f"components/{name}/preview.html"] = html
        files[f"components/{name}/README.md"] = COMP_README[name]
    files["components/Cover/preview.html"] = cover(st)
    index = {
        "v": 3,
        "layout": "files",
        "createdOnFiles": {"v": 1, "at": NOW},
        "title": st["title"],
        "namespace": st["namespace"],
        "libraries": [],
        "sections": {},
        "groups": [],
        "assetGroups": {},
        "blobs": {},
        "docs": {"readme": "project/README.md", "sections": []},
        "lastChange": {
            "by": "Jason Lin",
            "at": NOW,
            "via": "Claude Code",
            "note": "First version: candidate style for siyulio.com",
        },
    }
    files["design-system.json"] = json.dumps(index, ensure_ascii=False, indent=2)
    for rel, txt in files.items():
        fp = os.path.join(proj, rel)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
    print(f"ok {st['id']}: {len(files)} files, name size {name_size(st)}px")
    return root


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for st in STYLES:
        if which in ("all", st["id"]):
            build(st)
