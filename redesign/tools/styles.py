# -*- coding: utf-8 -*-
"""Style configs for the siyulio candidate design systems."""

USAGE = {
    "bg": "Page background.",
    "surface": "Cards, header, raised panels.",
    "line": "Hairlines, dividers, input and card borders.",
    "ink": "Primary text and headings, on bg, surface, brand-soft and accent-soft.",
    "ink-muted": "Secondary text, descriptions, metadata — on bg and surface.",
    "brand": "The identity colour as a fill: primary button, logo mark, large cover block.",
    "brand-text": "The identity colour as text: links, kicker, dates, logo accent — on bg and surface.",
    "brand-soft": "Tinted ground behind tags and media placeholders; text on it is ink.",
    "on-brand": "Text and icons on a brand fill (primary button label).",
    "accent": "Second hue, used sparingly: status dot, one highlight per view.",
    "accent-soft": "Tinted ground for accent tags; text on it is ink.",
    "on-accent": "Text on an accent fill.",
    "focus": "Keyboard focus ring, 2px solid, offset 3px.",
}


def colors(d, extra_usage=None):
    out = []
    for name, val in d.items():
        u = (extra_usage or {}).get(name) or USAGE.get(name, "")
        v = {"light": val[0], "dark": val[1]} if isinstance(val, tuple) else val
        out.append({"name": name, "value": v, "usage": u})
    return out


def dark_first(d, extra_usage=None):
    out = []
    for name, val in d.items():
        u = (extra_usage or {}).get(name) or USAGE.get(name, "")
        v = {"dark": val[0], "light": val[1]} if isinstance(val, tuple) else val
        out.append({"name": name, "value": v, "usage": u})
    return out


LIGHT_DARK = [{"id": "light", "name": "Light"}, {"id": "dark", "name": "Dark"}]
DARK_LIGHT = [{"id": "dark", "name": "Dark"}, {"id": "light", "name": "Light"}]


def fam(display, sans, label):
    return {"display": display, "sans": sans, "label": label}


def scale(
    d=(64, 68),
    h1=(40, 48),
    h2=(28, 36),
    dw=700,
    lead=(20, 32),
    body=(16, 28),
    small=(14, 22),
    label=(12, 16),
    lw=500,
    ls_d="-0.02em",
):
    return [
        {
            "name": "Display",
            "family": "display",
            "styles": [
                {
                    "name": "display",
                    "fontSize": f"{d[0]}px",
                    "lineHeight": f"{d[1]}px",
                    "fontWeight": dw,
                    "letterSpacing": ls_d,
                    "sample": "把 AI 變成每天會跑的產線",
                    "usage": "Hero statement, once per page.",
                },
                {
                    "name": "h1",
                    "fontSize": f"{h1[0]}px",
                    "lineHeight": f"{h1[1]}px",
                    "fontWeight": dw,
                    "letterSpacing": ls_d,
                    "sample": "作品集",
                    "usage": "Page titles.",
                },
                {
                    "name": "h2",
                    "fontSize": f"{h2[0]}px",
                    "lineHeight": f"{h2[1]}px",
                    "fontWeight": dw,
                    "sample": "Jarvis 語音 OS",
                    "usage": "Section titles, project names on detail pages.",
                },
            ],
        },
        {
            "name": "Text",
            "family": "sans",
            "styles": [
                {
                    "name": "lead",
                    "fontSize": f"{lead[0]}px",
                    "lineHeight": f"{lead[1]}px",
                    "fontWeight": 400,
                    "sample": "我設計並維運 24 小時運作的 AI agent。",
                    "usage": "Intro paragraph under a title.",
                },
                {
                    "name": "body",
                    "fontSize": f"{body[0]}px",
                    "lineHeight": f"{body[1]}px",
                    "fontWeight": 400,
                    "sample": "語音助理、第二大腦、本地大模型與自動化報表。",
                    "usage": "Article and description text.",
                },
                {
                    "name": "small",
                    "fontSize": f"{small[0]}px",
                    "lineHeight": f"{small[1]}px",
                    "fontWeight": 400,
                    "sample": "最後更新 2026.10",
                    "usage": "Captions, card descriptions, footnotes.",
                },
            ],
        },
        {
            "name": "Label",
            "family": "label",
            "styles": [
                {
                    "name": "label",
                    "fontSize": f"{label[0]}px",
                    "lineHeight": f"{label[1]}px",
                    "fontWeight": lw,
                    "letterSpacing": "0.08em",
                    "sample": "SELECTED WORK · 2026",
                    "usage": "Kickers, tags, dates, nav on some layouts.",
                },
            ],
        },
    ]


def shadows(card_l, card_d, ctrl_l="none", ctrl_d="none"):
    return [
        {
            "name": "shadow-card",
            "value": {"light": card_l, "dark": card_d},
            "usage": "Project cards and raised panels.",
        },
        {
            "name": "shadow-control",
            "value": {"light": ctrl_l, "dark": ctrl_d},
            "usage": "Buttons.",
        },
    ]


def shadows_df(card_d, card_l, ctrl_d="none", ctrl_l="none"):
    return [
        {
            "name": "shadow-card",
            "value": {"dark": card_d, "light": card_l},
            "usage": "Project cards and raised panels.",
        },
        {
            "name": "shadow-control",
            "value": {"dark": ctrl_d, "light": ctrl_l},
            "usage": "Buttons.",
        },
    ]


GF = "https://fonts.googleapis.com/css2?family="
NOTO_SANS = '"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", system-ui, sans-serif'
NOTO_SERIF = '"Noto Serif TC", "Songti TC", "PMingLiU", serif'

STYLES = []

# ===================================================================== 01
STYLES.append(
    dict(
        id="01-ink-seal",
        title="siyulio · 01 墨與印",
        namespace="SiyulioInk",
        tagline="像一本好讀的技術專欄：紙、墨、一顆朱印。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f6f1e7", "#171513"),
                "surface": ("#fffdf8", "#211e1b"),
                "line": ("#d9cfbd", "#3b352e"),
                "ink": ("#1c1a17", "#f1ebe0"),
                "ink-muted": ("#5f574b", "#b5aa99"),
                "brand": ("#b3261e", "#e0533f"),
                "brand-text": ("#a3211a", "#f07a63"),
                "brand-soft": ("#f3dcd2", "#3d1d17"),
                "on-brand": ("#fffdf8", "#171513"),
                "accent": ("#1f3a5f", "#8fb0d9"),
                "accent-soft": ("#dde4ee", "#1f2a38"),
                "on-accent": ("#fffdf8", "#171513"),
                "focus": ("#a3211a", "#f07a63"),
            },
            {
                "brand": "朱印紅 as a fill: primary button, the seal block on the cover. Never as a page ground.",
                "accent": "靛青 indigo ink: the status dot and rare second emphasis.",
            },
        ),
        families=fam(
            '"Fraunces", ' + NOTO_SERIF,
            '"Noto Sans TC", "Source Sans 3", system-ui, sans-serif',
            '"IBM Plex Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Fraunces:opsz,wght@9..144,400;9..144,600;9..144,800&family=Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap",
        typegroups=scale(d=(60, 66), dw=600),
        radius=(2, 4, 6),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=600,
            label_upper=True,
            em_style="italic",
            header_bg="bg",
            hero_bg="bg",
            card_hover="border-color: var(--brand);",
            nav_current="color: var(--ink); border-bottom: 2px solid var(--brand); padding-bottom: 4px;",
        ),
        extra_css="""
.sy-hero { border-top: 4px double var(--ink); }
.sy-hero h1 { font-variation-settings: 'opsz' 144; }
.sy-hero p::first-letter { font-family: var(--font-display); color: var(--brand-text); font-size: 1.3em; }
.sy-card { box-shadow: none; }
.sy-card .sy-media { border-radius: 0; border-bottom: 1px solid var(--line); background: var(--brand-soft); }
.sy-card h3 { font-style: italic; }
.sy-logo::after { content: "印"; display: inline-grid; place-items: center; width: 22px; height: 22px; margin-left: 8px; background: var(--brand); color: var(--on-brand); font-family: var(--font-display); font-size: 13px; border-radius: 2px; vertical-align: 2px; }
""",
        cover=dict(
            arrangement="bleed",
            pattern="rules",
            blocks=["brand", "ink", "brand-soft", "accent"],
            ptoken="ink",
            pitch=24,
            count=4,
            stroke=1,
            em=0.55,
            name_w=600,
            corner="radius-sm",
            pattern_over=False,
            why="editorial serif, borders not shadows: a few hairlines like the rules of a newspaper column",
        ),
        readme=dict(
            intro="**墨與印** 把個人網站當成一份長期連載的技術專欄來設計：米白紙張、深墨文字、一顆朱紅印章作為唯一的強調色。讀的人先感受到「這個人寫東西很認真」，再看到作品。",
            fit="你想讓人覺得你是會思考、會寫、能把複雜系統講清楚的人；網站會放很多長文筆記與專案寫作。適合想走顧問、PM、技術寫作或管理職方向。",
            voice=[
                "第一人稱「我」，句子完整、語氣沉穩，不用驚嘆號。",
                "先講結論再講過程；標題是陳述句，不是口號。",
                "英文術語保留原文（agent、LLM），第一次出現加一句白話。",
                "不用 emoji；強調用斜體 `<em>`，不用粗體堆疊。",
            ],
            examples=[
                "在製造業裡，把 AI 變成每天會跑的產線。",
                "這個系統每天早上 8 點自動整理信件與會議，讓我省下第一個小時。",
            ],
            color="紙（`bg`）與墨（`ink`）是全部的基調；`brand` 朱印紅只出現在主要按鈕、logo 印章、封面印塊。一個畫面裡紅色面積不超過 5%。`accent` 靛青只用在狀態點。深色主題是「夜讀模式」：暖黑底、米色字，紅色提亮成 `#e0533f`，上面的字改用 `on-brand` 深色。",
            type="標題用 `display`（Fraunces + Noto Serif TC），內文用 `body`（Noto Sans TC），日期、標籤、kicker 用 `label`（IBM Plex Mono，全大寫英文、字距 0.08em）。Hero 標題的關鍵片語用 `<em>` 變斜體並上 `brand-text`。內文行高 28px，一行不超過 34 個中文字。",
            layout="單欄閱讀寬度 680px，作品頁可放寬到 1080px。間距用 `space-*`：段落間 `space-4`、區塊間 `space-7`、區段間 `space-8`。結構靠細線（`line`、1px）與雙線（Hero 頂端 4px double），**不用陰影**。圓角極小：`radius-sm` 2px、`radius-lg` 6px。",
            imagery="作品示意圖用截圖加 1px `line` 外框，或以代號字放在 `brand-soft` 底上。圖示用細線條（1.5px stroke）單色，跟文字同色；不畫插圖。目前沒有正式 logo，標誌是純文字「siyulio」加一個「印」字方印。",
            signature=[
                "Hero 上方的雙線，像報紙刊頭。",
                "logo 後面的朱紅「印」字方章。",
                "段落首字以襯線字放大並上朱紅。",
                "作品卡標題用斜體，像書名。",
            ],
            dont=[
                "不要大面積紅底。",
                "不要陰影、漸層、毛玻璃。",
                "不要把襯線字用在 14px 以下的介面文字。",
            ],
        ),
    )
)

# ===================================================================== 02
STYLES.append(
    dict(
        id="02-night-shift",
        title="siyulio · 02 夜班終端",
        namespace="SiyulioShift",
        tagline="凌晨三點還在跑的 agent，留下的工作日誌。",
        themes=DARK_LIGHT,
        colors=dark_first(
            {
                "bg": ("#0e1111", "#f4f2ec"),
                "surface": ("#151a1a", "#ffffff"),
                "line": ("#2a3433", "#d6d2c6"),
                "ink": ("#e6ede9", "#111414"),
                "ink-muted": ("#93a39e", "#4f5754"),
                "brand": ("#f2b33d", "#8a5a00"),
                "brand-text": ("#f2b33d", "#7a4f00"),
                "brand-soft": ("#2e2715", "#f6e7c4"),
                "on-brand": ("#0e1111", "#ffffff"),
                "accent": ("#4fd1a5", "#0f7a5a"),
                "accent-soft": ("#12302a", "#d3efe5"),
                "on-accent": ("#0e1111", "#ffffff"),
                "focus": ("#f2b33d", "#7a4f00"),
            },
            {
                "brand": "琥珀 amber, the colour of an old monitor: primary button, cursor, cover slab.",
                "accent": "磷光綠: 'running' status only — never decoration.",
            },
        ),
        families=fam(
            '"JetBrains Mono", ui-monospace, "Noto Sans TC", monospace',
            '"IBM Plex Sans", ' + NOTO_SANS,
            '"JetBrains Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "JetBrains+Mono:wght@400;500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(52, 60), h1=(36, 44), h2=(24, 32), dw=700, ls_d="-0.03em"),
        radius=(2, 4, 6),
        bw=1,
        shadows=shadows_df("none", "none"),
        knobs=dict(
            head_w=700,
            head_ls="-0.03em",
            label_upper=False,
            label_ls="0.02em",
            btn_font="label",
            btn_w=500,
            nav_font="label",
            hero_size="52px",
            hero_lh="1.1",
            logo_ls="0",
            card_hover="border-color: var(--brand);",
            nav_current="color: var(--brand-text);",
            media_bg="bg",
            media_ink="accent",
        ),
        extra_css="""
.sy-hero .sy-kicker::before { content: "$ "; color: var(--accent); }
.sy-hero h1::after { content: ""; display: inline-block; width: 0.55em; height: 0.9em; margin-left: 0.15em; background: var(--brand); vertical-align: -0.1em; }
.sy-nav a::before { content: "./"; color: var(--line); }
.sy-nav a[aria-current]::before { color: var(--brand-text); }
.sy-logo::before { content: "~/"; color: var(--accent); }
.sy-card .sy-media { border: 1px dashed var(--line); font-family: var(--font-label); }
.sy-card h3::before { content: "> "; color: var(--brand-text); }
.sy-timeline time::before { content: "["; } .sy-timeline time::after { content: "]"; }
.sy-btn-primary::before { content: "▸"; }
""",
        cover=dict(
            arrangement="bands",
            pattern="dots",
            blocks=["brand", "line", "accent", "ink-muted"],
            ptoken="bg",
            pitch=16,
            dot=2,
            em=0.62,
            name_w=800,
            name_ls="-0.04em",
            corner="none",
            why="precise, mono, a 4px grid: a dot matrix like a phosphor screen, cut out of the amber band",
        ),
        copy=dict(
            kicker="whoami → jason lin",
            hero="我寫會自己醒來工作的程式，<em>讓產線夜裡也在學習</em>",
            cta1="ls ./projects",
            cta2="mail me",
            cta3="cat resume.pdf",
            nav1="projects",
            nav2="about",
            nav3="logs",
            nav4="contact",
        ),
        readme=dict(
            intro="**夜班終端** 把網站做成一個工程師的終端機：深色底、等寬字、琥珀色游標。它說的是「我是動手做系統的人」，作品就是一份份可以執行的日誌。",
            fit="你想被看成扎實的工程師與自動化建造者，訪客主要是技術主管、工程團隊、開源社群。內容以專案紀錄、技術筆記、架構圖為主。",
            voice=[
                "短句、動詞開頭，像 commit message：「接上 PLAUD 語音紀錄」。",
                "數字精確，附單位與日期：「1078 個測試綠燈」。",
                "可以用 CLI 隱喻（`ls`、`cat`）做導覽與按鈕，但內文用正常中文。",
                "不用 emoji；狀態用文字標記 `[ok]` `[wip]`。",
            ],
            examples=[
                "$ whoami → 製造業經企室，負責把 AI agent 接上每天的工作。",
                "[ok] Jarvis 語音 OS · P1–P8 交付 · 2026.07",
            ],
            color="深色主題是正本（第一主題）：近黑 `bg`、灰綠 `ink`。`brand` 琥珀用在主要按鈕、游標、日期；`accent` 磷光綠只代表「運作中」。淺色主題像印出來的報表：米白紙、深墨，琥珀加深到 `#8a5a00` 才夠對比。",
            type="標題、標籤、按鈕、導覽全用 `label` / `display`（JetBrains Mono）；長內文改用 `body`（IBM Plex Sans + Noto Sans TC），避免整頁等寬難讀。標題字距收緊 -0.03em。",
            layout="以 4px 為最小單位，網格嚴格對齊。區塊之間用 1px `line` 分隔或虛線框，不用陰影。圓角 2–6px，接近方角。內容寬度最大 960px，左對齊，不置中。",
            imagery="作品圖用終端截圖、架構圖或 ASCII 示意；佔位圖用虛線框加等寬代號字（`accent` 色）。圖示用 1.5px 線條或文字符號（`▸` `>` `[ ]`）。",
            signature=[
                "Hero kicker 前的 `$ ` 提示字元與標題後閃爍位置的琥珀游標方塊。",
                "導覽連結前的 `./`、logo 前的 `~/`。",
                "時間軸日期包在方括號裡。",
                "主要按鈕前的 `▸`。",
            ],
            dont=[
                "不要綠字黑底的駭客電影風；綠色只表示狀態。",
                "不要整段內文用等寬字。",
                "不要掃描線、CRT 彎曲等假特效。",
            ],
        ),
    )
)

# ===================================================================== 03
STYLES.append(
    dict(
        id="03-swiss-rouge",
        title="siyulio · 03 瑞士紅格",
        namespace="SiyulioSwiss",
        tagline="網格、粗體、一抹紅。資訊先行，裝飾為零。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#ffffff", "#0d0d0d"),
                "surface": ("#f4f4f2", "#181818"),
                "line": ("#d0d0cc", "#3a3a3a"),
                "ink": ("#111111", "#f5f5f3"),
                "ink-muted": ("#555555", "#a8a8a8"),
                "brand": ("#e10600", "#ff3b30"),
                "brand-text": ("#c00500", "#ff5a50"),
                "brand-soft": ("#fde3e1", "#3a1210"),
                "on-brand": ("#ffffff", "#0d0d0d"),
                "accent": ("#111111", "#f5f5f3"),
                "accent-soft": ("#ececea", "#2a2a2a"),
                "on-accent": ("#ffffff", "#0d0d0d"),
                "focus": ("#c00500", "#ff5a50"),
            },
            {
                "brand": "Swiss red: primary button, the big cover field, one rule per page.",
                "accent": "Solid black (white in dark): inverted blocks and the status dot.",
            },
        ),
        families=fam(
            '"Archivo", ' + NOTO_SANS,
            '"Archivo", ' + NOTO_SANS,
            '"Archivo", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Archivo:wght@400;500;700;800;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(
            d=(72, 72), h1=(44, 48), h2=(28, 32), dw=800, ls_d="-0.03em", lw=700
        ),
        radius=(0, 0, 0),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=800,
            head_ls="-0.03em",
            label_upper=True,
            label_w=700,
            label_ls="0.04em",
            hero_size="72px",
            hero_lh="1",
            btn_w=700,
            logo_w=900,
            logo_ls="-0.04em",
            card_border="ink",
            card_hover="background: var(--brand-soft);",
            nav_current="color: var(--ink); font-weight: 700;",
            em_extra="",
            media_bg="brand",
            media_ink="on-brand",
            header_bg="bg",
        ),
        extra_css="""
.sy-hero { grid-template-columns: repeat(12, 1fr); column-gap: var(--space-4); border-top: 8px solid var(--brand); }
.sy-hero > * { grid-column: 1 / span 10; }
.sy-hero .sy-kicker { grid-column: 1 / span 3; color: var(--ink); }
.sy-hero p { grid-column: 5 / span 7; }
.sy-hero .sy-actions { grid-column: 5 / span 7; }
.sy-card { border-width: 0; border-top: 2px solid var(--ink); padding: var(--space-4) 0 0; background: transparent; }
.sy-card .sy-media { border-radius: 0; }
.sy-timeline li { grid-template-columns: 120px 1fr; border-top-color: var(--ink); }
.sy-timeline time { font-weight: 700; color: var(--ink); }
""",
        cover=dict(
            arrangement="grid",
            pattern="plus",
            blocks=["brand", "accent", "line", "brand-text"],
            ptoken="ink",
            pitch=32,
            stroke=1.5,
            em=0.6,
            name_w=800,
            name_ls="-0.05em",
            corner="none",
            why="geometric, modular, square corners: printer's registration crosses on the grid like a Swiss poster's working layer",
        ),
        copy=dict(kicker="Jason Lin / AI 自動化", hero="AI agent<br>系統建造者。"),
        readme=dict(
            intro="**瑞士紅格** 用國際主義平面設計的方法做個人網站：十二欄網格、無襯線粗體、大量留白、一抹正紅。訊息排得清楚就是全部的設計。",
            fit="你想給人「清楚、有方法、可信任」的第一印象，適合要接專案、跨部門合作、或給高階主管看的履歷型網站。內容精簡、重點條列。",
            voice=[
                "短而確定：「AI agent 系統建造者。」不加修飾詞。",
                "一句一個事實；數字放前面。",
                "標籤與 kicker 用全大寫英文或簡短中文。",
                "不用 emoji、不用驚嘆號。",
            ],
            examples=[
                "AI agent 系統建造者。",
                "24 小時 · 13 條自動化迴圈 · 1 個人維運",
            ],
            color="黑、白、紅三色。`brand` 紅是封面大色塊、Hero 頂端 8px 紅條、主要按鈕；`accent` 是純黑（深色主題反白），用於反白區塊。其他一律灰階。",
            type="一個家族 Archivo（中文落到 Noto Sans TC）。`display` 72/72、字重 800、字距 -0.03em；標題行高 1，緊湊如海報。`label` 全大寫 700。中文標題不要拉字距。",
            layout="十二欄網格、4 欄 gutter `space-4`。Hero 文字落在第 5–11 欄形成不對稱。卡片用頂端 2px 黑線分隔而非外框，**零圓角、零陰影**。對齊比間距更重要：每個元素左緣都落在欄線上。",
            imagery="照片與截圖滿版裁切、無圓角。佔位圖用整塊 `brand` 紅底配白色代號字。圖示用 2px 直角線條，僅限箭頭與外連符號。",
            signature=[
                "Hero 頂部 8px 紅線。",
                "不對稱網格：kicker 在左 3 欄、內文在右 7 欄。",
                "卡片只有頂部黑線，沒有框。",
            ],
            dont=["不要圓角、陰影、漸層。", "不要第二個彩色。", "不要置中排版。"],
        ),
    )
)

# ===================================================================== 04
STYLES.append(
    dict(
        id="04-blueprint",
        title="siyulio · 04 工程藍圖",
        namespace="SiyulioPrint",
        tagline="把每個系統畫成可以施工的藍圖。",
        themes=DARK_LIGHT,
        colors=dark_first(
            {
                "bg": ("#0b2545", "#f3f6fa"),
                "surface": ("#13315c", "#ffffff"),
                "line": ("#2f5a8a", "#c5d3e3"),
                "ink": ("#eef4fb", "#0b2545"),
                "ink-muted": ("#a9c1dc", "#43597a"),
                "brand": ("#8ecae6", "#1d5c96"),
                "brand-text": ("#8ecae6", "#1d5c96"),
                "brand-soft": ("#1b4170", "#dbe8f5"),
                "on-brand": ("#0b2545", "#ffffff"),
                "accent": ("#ffb703", "#b45f00"),
                "accent-soft": ("#3d3418", "#fbe9cf"),
                "on-accent": ("#0b2545", "#ffffff"),
                "focus": ("#ffb703", "#1d5c96"),
            },
            {
                "brand": "Drafting cyan: primary button, line work, logo accent.",
                "accent": "Safety orange: callouts and the 'live' dot — like a red-line markup on a drawing.",
            },
        ),
        families=fam(
            '"IBM Plex Sans Condensed", ' + NOTO_SANS,
            '"IBM Plex Sans", ' + NOTO_SANS,
            '"IBM Plex Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(56, 60), dw=600),
        radius=(2, 3, 4),
        bw=1,
        shadows=shadows_df("none", "0 1px 0 #c5d3e3"),
        knobs=dict(
            head_w=600,
            label_upper=True,
            label_ls="0.12em",
            hero_bg="bg",
            header_bg="bg",
            btn_upper=True,
            btn_ls="0.06em",
            btn_font="label",
            card_hover="border-color: var(--brand);",
            media_bg="bg",
            media_ink="brand-text",
            nav_upper=True,
            nav_font="label",
            nav_ls="0.1em",
        ),
        extra_css="""
.sy-hero { background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px); background-size: 32px 32px; background-position: -1px -1px; border: 1px solid var(--line); }
.sy-hero h1, .sy-hero p, .sy-hero .sy-kicker { background: var(--bg); justify-self: start; padding: 0 4px; }
.sy-card { position: relative; }
.sy-card::before { content: "DWG-0" counter(card); counter-increment: card; position: absolute; top: 8px; right: 12px; font-family: var(--font-label); font-size: 10px; letter-spacing: .1em; color: var(--ink-muted); }
.sy-cards { counter-reset: card; }
.sy-card .sy-media { border: 1px solid var(--line); background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px); background-size: 16px 16px; }
.sy-card .sy-media span { background: var(--bg); padding: 0 8px; }
.sy-tag { border: 1px solid var(--brand); background: transparent; color: var(--brand-text); }
""",
        cover=dict(
            arrangement="slab",
            pattern="plus",
            blocks=["brand", "ink", "line", "accent"],
            ptoken="brand",
            pitch=24,
            stroke=1.25,
            em=0.55,
            name_w=600,
            corner="radius-sm",
            why="technical, a drafting grid: plus marks at one grid pitch, like the reference crosses on a blueprint sheet",
        ),
        copy=dict(
            kicker="Jason Lin · 系統規劃與 AI 自動化",
            hero="先畫圖，再施工：<em>把工廠的流程變成可以跑的系統</em>。",
        ),
        readme=dict(
            intro="**工程藍圖** 把網站當成一張圖紙：深藍底、青色線稿、方格背景、圖號與標註。它呼應你在製造業做的事──先把流程畫清楚，再把系統蓋起來。",
            fit="你的作品多是系統架構、流程改造、工廠自動化；訪客是製造業主管、工程師、系統整合商。很適合放大量架構圖。",
            voice=[
                "像規格書：主詞清楚、步驟分明。",
                "每個專案寫「問題 → 架構 → 結果」三段。",
                "代號與編號系統化：DWG-01、P13、T-110。",
                "不用 emoji，用標註符號 `→` `▲`。",
            ],
            examples=[
                "先畫圖，再施工：把工廠的流程變成可以跑的系統。",
                "DWG-03 · 本地模型產線 · 不出內網，批次起草 SVG 圖。",
            ],
            color="深色是正本：藍圖紙 `bg` 深藍、`ink` 近白、`brand` 青色線稿。`accent` 安全橘只用在標註與「運作中」點，像圖紙上的紅筆修訂。淺色主題是「影印版」：白紙藍線。",
            type="標題 `display` 用 IBM Plex Sans Condensed（窄體，像圖框標題欄），內文 `body` 用 IBM Plex Sans，標籤、圖號、按鈕用 `label`（Plex Mono 全大寫、字距 0.12em）。",
            layout="32px 方格是整站的骨架：Hero 背景畫出方格線（`line` 1px），文字底下墊 `bg` 色塊讓字浮在格線上。卡片 1px 外框、右上角自動編圖號。圓角 2–4px。",
            imagery="作品圖以架構圖、流程圖為主，線稿風格（1.25px `brand` 線）。佔位圖是 16px 細格加代號字。圖示用工程符號風格的線條圖示。",
            signature=[
                "Hero 的 32px 藍圖方格。",
                "每張作品卡右上角自動編號 `DWG-01`、`DWG-02`。",
                "標籤是青色外框、透明底，像圖面標註。",
            ],
            dont=[
                "不要擬真藍曬紙紋理或折痕。",
                "不要把橘色當主色。",
                "不要粗於 2px 的線。",
            ],
        ),
    )
)

# ===================================================================== 05
STYLES.append(
    dict(
        id="05-neo-brutal",
        title="siyulio · 05 新粗獷",
        namespace="SiyulioBrut",
        tagline="粗框、硬陰影、亮黃。直接到有點吵。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f7f3e8", "#121212"),
                "surface": ("#ffffff", "#1d1d1d"),
                "line": ("#111111", "#f5f5f5"),
                "ink": ("#111111", "#f5f5f5"),
                "ink-muted": ("#3d3d3d", "#c4c4c4"),
                "brand": ("#ffd400", "#ffd400"),
                "brand-text": ("#0047ff", "#ffd400"),
                "brand-soft": ("#fff1a8", "#3a3200"),
                "on-brand": ("#111111", "#111111"),
                "accent": ("#ff5ca8", "#ff5ca8"),
                "accent-soft": ("#ffd6ea", "#3d1a2b"),
                "on-accent": ("#111111", "#111111"),
                "focus": ("#0047ff", "#ffd400"),
            },
            {
                "line": "Every border is ink-strength: 2px solid, cards, buttons, header.",
                "brand-text": "Electric blue on light (yellow can't be text on cream); yellow on dark.",
                "accent": "Hot pink: one sticker-like highlight per view.",
            },
        ),
        families=fam(
            '"Space Grotesk", ' + NOTO_SANS,
            '"Space Grotesk", ' + NOTO_SANS,
            '"Space Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(d=(64, 64), dw=700, ls_d="-0.03em", lw=700),
        radius=(0, 0, 0),
        bw=2,
        shadows=shadows(
            "4px 4px 0 #111111",
            "4px 4px 0 #f5f5f5",
            "3px 3px 0 #111111",
            "3px 3px 0 #f5f5f5",
        ),
        knobs=dict(
            head_w=700,
            head_ls="-0.03em",
            label_upper=True,
            label_w=700,
            btn_border="line",
            btn_primary_border="line",
            btn_w=700,
            btn_upper=True,
            btn_hover="transform: translate(-2px,-2px); box-shadow: 5px 5px 0 var(--line);",
            card_border="line",
            card_hover="transform: translate(-3px,-3px); box-shadow: 7px 7px 0 var(--line);",
            hero_size="64px",
            hero_lh="1",
            tag_border="2px solid var(--line)",
            media_bg="accent",
            media_ink="on-accent",
            header_bg="brand",
            logo_w=700,
            nav_current="background: var(--ink); color: var(--bg); padding: 2px 8px;",
            em_extra="background: var(--brand-soft); padding: 0 .1em;",
        ),
        extra_css="""
.sy-header { border-bottom-width: 2px; }
.sy-header .sy-logo, .sy-header .sy-nav a { color: var(--on-brand); }
.sy-header .sy-logo b { color: var(--on-brand); text-decoration: underline 3px; }
.sy-header .sy-nav a[aria-current] { background: var(--on-brand); color: var(--brand); }
.sy-btn-ghost { border: 0; box-shadow: none; text-decoration: underline 2px; }
.sy-card .sy-media { border: 2px solid var(--line); border-radius: 0; }
.sy-timeline li { border-top-width: 2px; }
.sy-hero h1 em { color: var(--ink); }
.sy-card:nth-child(2) .sy-media { background: var(--brand); }
.sy-card:nth-child(2) .sy-media span { color: var(--on-brand); }
""",
        cover=dict(
            arrangement="bleed",
            pattern="stripes",
            blocks=["brand", "ink", "accent", "brand-text"],
            ptoken="ink",
            pitch=16,
            em=0.6,
            name_w=700,
            name_ls="-0.05em",
            corner="none",
            why="loud, bold, poster type, hard edges: diagonal hazard stripes at one spacing step across the yellow block",
        ),
        copy=dict(
            kicker="嗨，我是 Jason",
            hero="我把 AI 做成<em>真的會上工</em>的工具。",
            cta1="看作品 ↗",
            cta2="寫信給我",
        ),
        readme=dict(
            intro="**新粗獷** 是最大聲的一套：2px 黑框、4px 硬陰影、亮黃頁首、粉紅貼紙。它說「我不裝、我直接做」，第一眼就讓人記住。",
            fit="你想要個性鮮明、年輕、帶點玩心的形象，訪客是新創、社群、同好。適合放 side project、實驗、短影片與 demo。",
            voice=[
                "口語、第一人稱、直接：「我把 AI 做成真的會上工的工具。」",
                "可以有一點幽默與自嘲，但每句都要有資訊。",
                "按鈕可以加箭頭符號 ↗ →。",
                "emoji 最多一頁一個，而且不當裝飾。",
            ],
            examples=[
                "嗨，我是 Jason。我把 AI 做成真的會上工的工具。",
                "這週的實驗：拍兩下手，電腦就醒來。",
            ],
            color="`brand` 亮黃當頁首與主要按鈕的大面積底色，上面的字永遠是 `on-brand` 黑。`brand-text` 在淺色主題是電光藍（黃色不能當米底上的字）。`accent` 粉紅像貼紙，一個畫面一處。所有邊框都是 `line`（黑／白）2px。",
            type="Space Grotesk 當標題與內文，Space Mono 當標籤。標題 700、行高 1、字距 -0.03em。按鈕全大寫英文或短中文。",
            layout="**零圓角**、2px `border-width`、`shadow-card` 是 4px 4px 0 的實色硬陰影；hover 時元件往左上移 3px、陰影變長，像被按起來。區塊之間用粗線分隔。網格可以稍微不規則，但每個框都要對齊。",
            imagery="截圖加 2px 黑框；佔位圖用粉紅或黃色實色塊配黑色代號字。圖示用粗線（2.5px）方角。可以用手繪箭頭點綴，但不畫人物。",
            signature=[
                "亮黃頁首加黑色反白的目前頁面。",
                "4px 實色硬陰影與「按起來」的 hover。",
                "Hero 關鍵字的螢光筆底色。",
            ],
            dont=[
                "不要柔和陰影或圓角混用。",
                "不要超過三個彩色（黃、粉、藍）。",
                "不要讓黃色變成文字色出現在淺底上。",
            ],
        ),
    )
)

# ===================================================================== 06
STYLES.append(
    dict(
        id="06-washi-soft",
        title="siyulio · 06 和紙柔光",
        namespace="SiyulioWashi",
        tagline="慢慢讀也不累的網站：圓、暖、安靜。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f3efe6", "#1c1b18"),
                "surface": ("#fbf9f4", "#25231f"),
                "line": ("#ddd5c5", "#3b3832"),
                "ink": ("#2f2a24", "#ede6da"),
                "ink-muted": ("#6b6256", "#b3a998"),
                "brand": ("#5f7148", "#a9bd8f"),
                "brand-text": ("#55663f", "#b5c99b"),
                "brand-soft": ("#e3e8d6", "#2c3324"),
                "on-brand": ("#fbf9f4", "#1c1b18"),
                "accent": ("#c97b5a", "#e0a183"),
                "accent-soft": ("#f3ddd2", "#3a2a22"),
                "on-accent": ("#1a1612", "#1c1b18"),
                "focus": ("#55663f", "#b5c99b"),
            },
            {
                "brand": "抹茶 sage: primary button, logo dot, the largest cover disc.",
                "accent": "陶土 clay: the status dot and one warm highlight.",
            },
        ),
        families=fam(
            '"Zen Maru Gothic", ' + NOTO_SANS,
            '"Zen Maru Gothic", ' + NOTO_SANS,
            '"Zen Maru Gothic", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Zen+Maru+Gothic:wght@400;500;700;900&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(
            d=(52, 64), h1=(36, 48), dw=700, ls_d="0", body=(16, 30), lw=500
        ),
        radius=(10, 16, 28),
        bw=1,
        shadows=shadows(
            "0 1px 2px rgba(47,42,36,0.06), 0 8px 24px rgba(47,42,36,0.06)",
            "0 1px 2px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.25)",
        ),
        knobs=dict(
            head_w=700,
            head_ls="0",
            label_upper=False,
            label_ls="0.04em",
            tag_radius="pill",
            hero_size="52px",
            hero_lh="1.25",
            card_border="line",
            card_hover="transform: translateY(-2px);",
            nav_current="color: var(--ink); background: var(--brand-soft); padding: 6px 14px; border-radius: 999px;",
            logo_w=900,
            em_extra="background: linear-gradient(transparent 62%, var(--accent-soft) 62%);",
        ),
        extra_css="""
.sy-btn { border-radius: 999px; }
.sy-header { border-bottom: 0; margin: var(--space-3); border-radius: 999px; box-shadow: var(--shadow-card); }
.sy-logo::before { content: ""; display: inline-block; width: 12px; height: 12px; border-radius: 999px; background: var(--brand); margin-right: 8px; }
.sy-card .sy-media { border-radius: 20px; }
.sy-card .sy-media span { font-size: 32px; }
.sy-timeline li { border-top-style: dashed; }
.sy-timeline time { background: var(--brand-soft); border-radius: 999px; padding: 0 10px; justify-self: start; height: 24px; color: var(--ink); }
""",
        cover=dict(
            arrangement="stagger",
            pattern="discs",
            blocks=["brand", "accent", "line", "ink-muted"],
            ptoken="surface",
            pitch=32,
            disc=9,
            em=0.62,
            name_w=900,
            name_ls="-0.01em",
            corner="radius-lg",
            why="soft, friendly, large radii: small discs like pebbles in a garden, cut out of the sage tint",
        ),
        copy=dict(
            kicker="Jason 的工作室",
            hero="我做的 AI 工具，<em>是給人用的</em>，不是給人看的。",
        ),
        readme=dict(
            intro="**和紙柔光** 是最溫和的一套：和紙米色、抹茶綠、陶土橘、大圓角、圓體字。它讓訪客覺得你親切、好溝通，技術藏在溫度後面。",
            fit="你希望被看成會照顧使用者、懂人也懂技術的人；訪客包含非技術背景的主管、同事、HR。適合寫 AI 導入心得、教學、內訓。",
            voice=[
                "溫和、說明式，像在跟同事解釋：「這個工具會幫你…」",
                "先講對人的好處，再講技術。",
                "可以用問句開場，但不賣弄。",
                "不用 emoji；強調用螢光筆底線。",
            ],
            examples=[
                "我做的 AI 工具，是給人用的，不是給人看的。",
                "每天早上，助理會先幫你整理好昨天的會議重點。",
            ],
            color="`bg` 和紙米、`ink` 深棕灰，不用純黑。`brand` 抹茶綠是主要按鈕與 logo 圓點；`accent` 陶土橘只當狀態點與 Hero 螢光筆底線（`accent-soft`）。深色主題是「茶室夜燈」：深棕底，綠與橘都提亮。",
            type="一家族 Zen Maru Gothic（圓體），標題 700、logo 900。行高放寬：內文 30px、Hero 1.25。字距不收緊，中文圓體保持舒展。",
            layout="大圓角：`radius-sm` 10、`radius-md` 16、`radius-lg` 28，按鈕與標籤用 `radius-pill`。頁首是一顆浮起的膠囊。陰影非常淡（`shadow-card`），只為分層。留白多，一行內容不超過 32 字。",
            imagery="照片偏暖、低飽和；佔位圖是 `brand-soft` 圓角塊。圖示用 2px 圓頭線條。可以用簡單幾何（圓、半圓）當裝飾，不用插畫人物。",
            signature=[
                "膠囊形頁首。",
                "logo 前的抹茶小圓點。",
                "Hero 關鍵句下方的陶土色螢光筆底線。",
                "時間軸日期是圓角小膠囊。",
            ],
            dont=["不要純黑、純白。", "不要尖角與粗框。", "不要高飽和色。"],
        ),
    )
)

# ===================================================================== 07
STYLES.append(
    dict(
        id="07-night-market",
        title="siyulio · 07 夜市霓虹",
        namespace="SiyulioNeon",
        tagline="台北夜市的招牌光：桃紅、青綠、深夜。",
        themes=DARK_LIGHT,
        colors=dark_first(
            {
                "bg": ("#120d12", "#fff6f9"),
                "surface": ("#1c141c", "#ffffff"),
                "line": ("#3a2a38", "#f0cfdc"),
                "ink": ("#fbeff5", "#1d0f17"),
                "ink-muted": ("#c6aebc", "#6b4b5c"),
                "brand": ("#ff3d7f", "#d1004f"),
                "brand-text": ("#ff6d9d", "#b80046"),
                "brand-soft": ("#3c1427", "#ffd9e7"),
                "on-brand": ("#120d12", "#ffffff"),
                "accent": ("#19e3d0", "#007a72"),
                "accent-soft": ("#0f3533", "#c9f2ee"),
                "on-accent": ("#120d12", "#ffffff"),
                "focus": ("#19e3d0", "#007a72"),
            },
            {
                "brand": "桃紅 neon pink: primary button, logo, the big cover band.",
                "accent": "青綠 cyan tube: status dot, focus ring, one glow per view.",
            },
        ),
        families=fam(
            '"Bungee", "Noto Sans TC", sans-serif',
            NOTO_SANS,
            '"Space Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Bungee&family=Noto+Sans+TC:wght@400;500;700;900&family=Space+Mono:wght@400;700&display=swap",
        typegroups=scale(d=(56, 64), dw=400, ls_d="0"),
        radius=(4, 8, 12),
        bw=1,
        shadows=shadows_df(
            "0 0 0 1px #3a2a38, 0 0 24px rgba(255,61,127,0.18)",
            "0 6px 20px rgba(209,0,79,0.10)",
            "0 0 16px rgba(255,61,127,0.35)",
            "none",
        ),
        knobs=dict(
            head_w=400,
            head_ls="0",
            label_upper=True,
            hero_size="56px",
            hero_lh="1.15",
            logo_w=400,
            card_hover="border-color: var(--brand);",
            nav_current="color: var(--accent);",
            media_bg="bg",
            media_ink="brand-text",
            btn_upper=True,
            btn_ls="0.04em",
        ),
        extra_css="""
[data-theme="dark"] .sy-hero h1 em, [data-theme="dark"] .sy-logo b { text-shadow: 0 0 12px rgba(255,61,127,0.6); }
[data-theme="dark"] .sy-nav a[aria-current] { text-shadow: 0 0 10px rgba(25,227,208,0.6); }
.sy-hero h1 { font-weight: 900; }
.sy-card .sy-media { border: 1px solid var(--brand); }
.sy-card:nth-child(2) .sy-media { border-color: var(--accent); }
.sy-card:nth-child(2) .sy-media span { color: var(--accent); }
.sy-card h3 { font-size: 20px; }
.sy-tag { border-radius: 4px; }
.sy-timeline time { color: var(--accent); }
""",
        cover=dict(
            arrangement="bands",
            pattern="chevrons",
            blocks=["brand", "accent", "brand-soft", "ink"],
            ptoken="bg",
            pitch=24,
            em=0.74,
            name_w=400,
            name_ls="0",
            corner="radius-md",
            why="loud signage: chevrons cut out of the pink band, like the arrow tubes over a night-market stall",
        ),
        copy=dict(
            kicker="JASON LIN · 夜裡也在跑",
            hero="白天開會，晚上讓 <em>AI 替我值夜班</em>。",
            cta1="逛作品",
            cta2="打聲招呼",
        ),
        readme=dict(
            intro="**夜市霓虹** 從台北夜市的招牌取色：深夜底、桃紅與青綠的燈管光。它有在地感、有熱度，讓人記得你是在台灣做 AI 的那個人。",
            fit="你想要有記憶點、有台灣味的個人品牌，適合經營社群、演講、YouTube 或 Podcast；訪客偏年輕、偏社群。",
            voice=[
                "口語、有畫面感：「白天開會，晚上讓 AI 替我值夜班。」",
                "中英混用自然，英文用 Bungee 招牌字。",
                "標題可以玩雙關，但內文要具體。",
                "不用 emoji 取代文字。",
            ],
            examples=[
                "白天開會，晚上讓 AI 替我值夜班。",
                "這攤賣的是：語音助理、自動晨報、本地大模型。",
            ],
            color="深色主題是正本：近黑紫 `bg`、粉白 `ink`。`brand` 桃紅是招牌主色，`accent` 青綠是第二根燈管。暗色下關鍵字與 logo 有輕微光暈（text-shadow），淺色主題取消光暈改用深桃紅。",
            type="英文標題用 Bungee（招牌字，單一字重），中文落到 Noto Sans TC 900。內文 Noto Sans TC，標籤 Space Mono 全大寫。Bungee 只用在 20px 以上。",
            layout="中等圓角（4/8/12）。卡片用 1px 色框，第二張卡換青綠框，像不同攤位的招牌。光暈只在暗色主題、只在 logo、Hero 關鍵字、目前頁面三處。",
            imagery="夜景、招牌、街拍可以當背景照，但要壓暗到文字可讀。佔位圖是黑底加彩色外框代號字。圖示用 1.5px 線條，像霓虹燈管的單線。",
            signature=[
                "暗色下 logo 與關鍵字的桃紅光暈。",
                "Bungee 招牌字英文標題。",
                "封面的箭頭燈管 chevrons。",
            ],
            dont=[
                "不要藍紫漸層的「科技感」背景。",
                "不要全頁發光；光暈最多三處。",
                "不要用 Bungee 寫長句。",
            ],
        ),
    )
)

# ===================================================================== 08
STYLES.append(
    dict(
        id="08-bauhaus",
        title="siyulio · 08 包浩斯",
        namespace="SiyulioBau",
        tagline="紅、黃、藍與幾何：形狀本身就是內容。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f2ede3", "#161512"),
                "surface": ("#faf7f0", "#201f1b"),
                "line": ("#1b1b1b", "#e9e4d8"),
                "ink": ("#1b1b1b", "#f1ece0"),
                "ink-muted": ("#4a463f", "#bdb6a6"),
                "brand": ("#d62828", "#f0513f"),
                "brand-text": ("#b51f1f", "#ff6b59"),
                "brand-soft": ("#f6d6cf", "#3e1a14"),
                "on-brand": ("#ffffff", "#161512"),
                "accent": ("#f6bd16", "#f6bd16"),
                "accent-soft": ("#fbe8b0", "#3b3010"),
                "on-accent": ("#1b1b1b", "#161512"),
                "blue": ("#1d4e89", "#6f9ed8"),
                "focus": ("#1d4e89", "#f6bd16"),
            },
            {
                "brand": "Bauhaus red: primary button, the circle in the logo, cover block.",
                "accent": "Bauhaus yellow: fills only (status dot, triangle), never text.",
                "blue": "Bauhaus blue: geometric shapes and the third cover block; on light it is also the focus ring.",
                "line": "Ink-strength 2px borders, like the black bars of a poster.",
            },
        ),
        families=fam(
            '"Jost", ' + NOTO_SANS, '"Jost", ' + NOTO_SANS, '"Jost", ' + NOTO_SANS
        ),
        gfonts=GF
        + "Jost:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(64, 68), dw=600, ls_d="-0.01em", lw=600),
        radius=(0, 0, 0),
        bw=2,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=600,
            label_upper=True,
            label_w=600,
            label_ls="0.14em",
            hero_size="64px",
            card_border="line",
            btn_border="line",
            btn_primary_border="line",
            card_hover="background: var(--accent-soft);",
            media_bg="blue",
            media_ink="bg",
            nav_upper=True,
            nav_ls="0.12em",
            nav_current="color: var(--ink); box-shadow: inset 0 -4px 0 var(--accent);",
        ),
        extra_css="""
.sy-logo::before { content: ""; display: inline-block; width: 14px; height: 14px; border-radius: 999px; background: var(--brand); margin-right: 4px; vertical-align: 0; }
.sy-logo::after { content: ""; display: inline-block; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 14px solid var(--accent); margin-left: 6px; }
.sy-hero { grid-template-columns: 1fr 200px; }
.sy-hero > * { grid-column: 1; }
.sy-hero::after { content: ""; grid-column: 2; grid-row: 1 / span 4; width: 180px; height: 180px; border-radius: 999px; background: var(--brand); align-self: center; box-shadow: 60px 60px 0 -40px var(--blue); }
.sy-card .sy-media { border-radius: 0; }
.sy-card:nth-child(2) .sy-media { background: var(--brand); } .sy-card:nth-child(2) .sy-media span { color: var(--on-brand); }
.sy-card:nth-child(3) .sy-media { background: var(--accent); } .sy-card:nth-child(3) .sy-media span { color: var(--on-accent); }
""",
        cover=dict(
            arrangement="grid",
            pattern="quarter",
            blocks=["brand", "blue", "accent", "ink"],
            ptoken="blue",
            pitch=48,
            em=0.55,
            name_w=600,
            corner="none",
            pattern_over=True,
            why="geometric, modular, primaries: quarter-circles turning across the yellow cell, the Bauhaus tile game",
        ),
        copy=dict(
            kicker="JASON LIN — FORM FOLLOWS FUNCTION",
            hero="形式追隨功能：<em>我先做能用的</em>，再讓它好看。",
        ),
        readme=dict(
            intro="**包浩斯** 用紅、黃、藍三原色與圓、三角、方塊說話。它說「我在乎功能與結構」，同時有很強的視覺記憶點。",
            fit="你想要理性又有設計感、能代表「工業 × 設計」的形象；適合做 portfolio 給設計、產品與製造業界看。",
            voice=[
                "宣言式短句：「形式追隨功能。」",
                "說明時條理分明，用編號。",
                "標籤全大寫英文、字距拉開。",
                "不用 emoji，用幾何符號 ● ▲ ■ 當列表點。",
            ],
            examples=[
                "形式追隨功能：我先做能用的，再讓它好看。",
                "● 問題　▲ 方法　■ 結果",
            ],
            color="三原色各司其職：`brand` 紅是行動（按鈕、logo 圓）、`accent` 黃只當填色（不當字）、`blue` 藍是幾何形狀與淺色焦點環。其餘是 `bg` 米與 `ink` 黑。2px 黑框像海報的黑色分隔條。",
            type="一家族 Jost（Futura 系幾何體），中文落到 Noto Sans TC。標題 600；標籤全大寫、字距 0.14em。",
            layout="**零圓角**（除了真正的圓）、2px 黑框、不用陰影。Hero 右側放一個 `brand` 大圓疊一個 `blue` 小圓。作品卡的示意塊依序輪流藍、紅、黃。",
            imagery="用純幾何構成當主視覺：圓、三角、方塊、四分之一圓。照片要黑白或去飽和，加上一個原色幾何。圖示是實心幾何形。",
            signature=[
                "logo 前紅圓、後黃三角。",
                "Hero 旁的紅色大圓與藍色小圓。",
                "卡片示意塊三原色輪替。",
            ],
            dont=["不要第四個彩色。", "不要漸層與陰影。", "不要黃色文字。"],
        ),
    )
)

# ===================================================================== 09
STYLES.append(
    dict(
        id="09-quiet-mono",
        title="siyulio · 09 留白單色",
        namespace="SiyulioQuiet",
        tagline="黑、白、一點橘。讓作品自己說話。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#fafafa", "#0a0a0a"),
                "surface": ("#ffffff", "#141414"),
                "line": ("#e4e4e4", "#2a2a2a"),
                "ink": ("#0a0a0a", "#f5f5f5"),
                "ink-muted": ("#5c5c5c", "#a3a3a3"),
                "brand": ("#0a0a0a", "#f5f5f5"),
                "brand-text": ("#0a0a0a", "#f5f5f5"),
                "brand-soft": ("#efefef", "#1f1f1f"),
                "on-brand": ("#fafafa", "#0a0a0a"),
                "accent": ("#ff5b00", "#ff7a2e"),
                "accent-soft": ("#ffe4d4", "#33200f"),
                "on-accent": ("#0a0a0a", "#0a0a0a"),
                "gray": ("#9a9a9a", "#4a4a4a"),
                "focus": ("#0a0a0a", "#ff7a2e"),
            },
            {
                "brand": "Black (white in dark): the primary button and big type. The system's identity is the absence of colour.",
                "accent": "One orange: the status dot and a single mark per page.",
                "gray": "Mid grey for the second cover block and image placeholders.",
            },
        ),
        families=fam(
            '"Instrument Serif", ' + NOTO_SERIF,
            '"Instrument Sans", ' + NOTO_SANS,
            '"DM Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500&family=Noto+Serif+TC:wght@400;500&display=swap",
        typegroups=scale(
            d=(80, 80), h1=(48, 52), h2=(32, 36), dw=400, ls_d="-0.02em", lw=400
        ),
        radius=(2, 999, 8),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=400,
            head_ls="-0.02em",
            label_upper=False,
            label_ls="0.02em",
            label_w=400,
            hero_size="80px",
            hero_lh="1",
            em_style="italic",
            em_extra="color: var(--ink-muted);",
            btn_w=500,
            card_border="bg",
            card_hover="opacity: .8;",
            media_bg="brand-soft",
            media_ink="gray",
            nav_current="color: var(--ink);",
            header_bg="bg",
            logo_w=400,
            logo_ls="-0.02em",
        ),
        extra_css="""
.sy-header { border-bottom: 0; }
.sy-logo { font-size: 24px; }
.sy-logo b { color: var(--ink); font-style: italic; }
.sy-hero { padding-top: var(--space-9); padding-bottom: var(--space-9); }
.sy-card { background: transparent; padding: 0; box-shadow: none; border: 0; }
.sy-card .sy-media { border-radius: 8px; aspect-ratio: 4 / 3; }
.sy-card .sy-media span { font-family: var(--font-label); font-size: 13px; letter-spacing: .04em; }
.sy-card h3 { font-size: 26px; }
.sy-timeline li { grid-template-columns: 120px 1fr; }
.sy-timeline time { color: var(--ink-muted); }
.sy-hero .sy-kicker { color: var(--ink-muted); }
.sy-hero .sy-kicker::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 999px; background: var(--accent); margin-right: 10px; vertical-align: 1px; }
""",
        cover=dict(
            arrangement="columns",
            pattern="rules",
            blocks=["brand", "gray", "ink-muted", "accent"],
            ptoken="ink-muted",
            pitch=40,
            count=3,
            stroke=1,
            em=0.48,
            name_w=400,
            name_ls="-0.03em",
            corner="none",
            pattern_over=False,
            why="quiet, editorial serif, nothing but type: three hairlines behind the columns, a baseline the eye can rest on",
        ),
        copy=dict(
            kicker="目前在製造業做 AI 自動化",
            hero="我做系統，<em>也寫下為什麼這樣做</em>。",
            cta1="作品",
            cta2="聯絡",
            cta3="履歷 PDF",
        ),
        readme=dict(
            intro="**留白單色** 幾乎沒有顏色：黑白灰、超大的襯線字、大量留白，只在一處放一點橘。它讓作品截圖成為畫面的主角，你本人退到後面。",
            fit="你的作品有好看的畫面（儀表板、截圖、圖表），想要一個不會跟作品搶戲、經得起時間的網站。換工作十年後還能用。",
            voice=[
                "極簡：能刪的字都刪。",
                "標題可以是一句完整的話，不加標點以外的符號。",
                "說明用平實的陳述，不形容自己。",
                "不用 emoji、不用驚嘆號。",
            ],
            examples=["我做系統，也寫下為什麼這樣做。", "Jarvis — 桌面語音助理，2026"],
            color="`brand` 就是黑（深色主題是白），整套系統的識別是「沒有顏色」。`accent` 橘一頁只出現一次：kicker 前的小圓點或一個狀態。`gray` 是示意圖與封面的中灰。",
            type="標題 Instrument Serif 400（細、優雅，斜體做強調）、內文 Instrument Sans、標籤 DM Mono。Hero 80px 行高 1。中文標題落到 Noto Serif TC。",
            layout="留白是主要元素：Hero 上下各 96px（`space-9`）。卡片沒有框、沒有底色，只有 4:3 圖與文字。按鈕是 `radius-md` 膠囊（999px）。對齊左緣，不置中。",
            imagery="作品圖是全部的顏色來源：大張、4:3、8px 圓角。沒有截圖時用 `brand-soft` 淺灰塊加等寬小字。圖示用 1px 線條，能不用就不用。",
            signature=[
                "80px 細襯線 Hero。",
                "kicker 前一顆橘點，全站唯一的彩色。",
                "無框卡片，只有圖與字。",
            ],
            dont=[
                "不要第二個彩色。",
                "不要粗體大標（標題保持 400）。",
                "不要把留白填滿。",
            ],
        ),
    )
)

# ===================================================================== 10
STYLES.append(
    dict(
        id="10-riso-press",
        title="siyulio · 10 Riso 印刷",
        namespace="SiyulioRiso",
        tagline="兩色孔版印刷的手工感：螢光粉、印刷藍、套印偏移。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f5f0e6", "#1a1720"),
                "surface": ("#fffaf0", "#24202b"),
                "line": ("#d8cfbf", "#3c3646"),
                "ink": ("#22201c", "#f4eee4"),
                "ink-muted": ("#5d574d", "#bbb2a6"),
                "brand": ("#ff48b0", "#ff6dc0"),
                "brand-text": ("#c2186f", "#ff8fce"),
                "brand-soft": ("#ffd9ec", "#3f1a33"),
                "on-brand": ("#22201c", "#1a1720"),
                "accent": ("#0078bf", "#4fb3f0"),
                "accent-soft": ("#d4e9f7", "#15304a"),
                "on-accent": ("#ffffff", "#1a1720"),
                "focus": ("#0078bf", "#4fb3f0"),
            },
            {
                "brand": "Fluorescent pink ink: primary button, the offset 'misprint' shadow, cover block.",
                "accent": "Riso blue ink: second plate — tags, dots, the second cover block.",
            },
        ),
        families=fam(
            '"DM Serif Display", ' + NOTO_SERIF,
            '"Work Sans", ' + NOTO_SANS,
            '"Courier Prime", ui-monospace, monospace',
        ),
        gfonts=GF
        + "DM+Serif+Display:ital@0;1&family=Work+Sans:wght@400;500;600&family=Courier+Prime:wght@400;700&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@700;900&display=swap",
        typegroups=scale(d=(64, 68), dw=400, ls_d="-0.01em"),
        radius=(4, 6, 10),
        bw=1,
        shadows=shadows(
            "6px 6px 0 #ff48b0",
            "6px 6px 0 #ff6dc0",
            "3px 3px 0 #0078bf",
            "3px 3px 0 #4fb3f0",
        ),
        knobs=dict(
            head_w=400,
            label_upper=True,
            hero_size="64px",
            em_style="italic",
            card_border="ink",
            card_hover="box-shadow: 9px 9px 0 var(--accent);",
            media_bg="accent-soft",
            media_ink="accent",
            btn_border="ink",
            nav_current="color: var(--ink); text-decoration: underline wavy var(--brand); text-underline-offset: 6px;",
        ),
        extra_css="""
.sy-hero h1 { text-shadow: 3px 2px 0 var(--brand-soft); }
.sy-hero h1 em { color: var(--accent); text-shadow: 3px 2px 0 var(--brand); }
.sy-card .sy-media { background-image: radial-gradient(var(--accent) 1.2px, transparent 1.4px); background-size: 8px 8px; background-color: var(--accent-soft); }
.sy-card .sy-media span { background: var(--surface); padding: 0 10px; }
.sy-tag { background: transparent; border: 1px solid var(--accent); color: var(--ink); }
.sy-tag-accent { background: var(--brand-soft); border-color: var(--brand); }
.sy-btn-primary { border-color: var(--ink); }
""",
        cover=dict(
            arrangement="stagger",
            pattern="halftone",
            blocks=["brand", "accent", "brand-soft", "ink"],
            ptoken="accent",
            pitch=16,
            em=0.55,
            name_w=400,
            corner="radius-md",
            pattern_over=True,
            why="print, two-ink overprint: a halftone fade in the blue plate across the pink tint, like a riso screen",
        ),
        copy=dict(
            kicker="ISSUE 01 · JASON LIN",
            hero="一個人的 AI 工作室，<em>手工印刷中</em>。",
            cta1="翻閱作品",
            cta2="寄信",
        ),
        readme=dict(
            intro="**Riso 印刷** 借用孔版印刷的語言：螢光粉、印刷藍兩個版、網點、套印偏移的陰影。它有獨立刊物（zine）的手工感，讓 AI 這種冷題目變得有溫度。",
            fit="你喜歡寫作、出刊、做電子報或社群貼文，想讓網站像一本持續出刊的個人刊物。訪客是創作者、設計師、對 AI 好奇的一般讀者。",
            voice=[
                "像刊物編輯：期數、專欄、本期主題。",
                "標題有一點文學感，內文具體。",
                "可以用「本期」「下期預告」這類刊物用語。",
                "不用 emoji，用印刷符號 ※ ★。",
            ],
            examples=["一個人的 AI 工作室，手工印刷中。", "本期：讓電腦聽懂拍手聲。"],
            color="兩個版：`brand` 螢光粉、`accent` 印刷藍，加 `ink` 黑。陰影不是光影，是「套印偏移」：`shadow-card` 是 6px 實色粉紅位移。Hero 標題有淡粉的錯版陰影，關鍵字是藍字配粉色錯版。",
            type="標題 DM Serif Display（粗襯線）、內文 Work Sans、標籤 Courier Prime（打字機）。中文標題落到 Noto Serif TC。",
            layout="中等圓角、1px 黑框、粉色偏移陰影。示意圖用 8px 網點底。版面可以像刊物：大標題、欄位、期數標記。",
            imagery="照片轉雙色調（粉＋藍）或網點化。圖示用 1.5px 線條、略帶手繪感。佔位圖是網點塊。",
            signature=[
                "粉紅實色偏移陰影，像套印沒對準。",
                "網點示意圖。",
                "波浪底線標示目前頁面。",
            ],
            dont=["不要用軟陰影。", "不要第三個彩色版。", "不要讓網點蓋住文字。"],
        ),
    )
)

# ===================================================================== 11
STYLES.append(
    dict(
        id="11-field-notes",
        title="siyulio · 11 田野筆記",
        namespace="SiyulioField",
        tagline="現場觀察、手寫記錄、慢慢長出來的系統。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#eee7d6", "#161a15"),
                "surface": ("#f8f3e7", "#1f241d"),
                "line": ("#cfc3a8", "#374033"),
                "ink": ("#23291f", "#ece6d6"),
                "ink-muted": ("#565b4c", "#b0aa98"),
                "brand": ("#2f5d3a", "#8fbf8f"),
                "brand-text": ("#2f5d3a", "#9fcc9c"),
                "brand-soft": ("#d7e2cf", "#253325"),
                "on-brand": ("#f8f3e7", "#161a15"),
                "accent": ("#d98b2b", "#e5a24a"),
                "accent-soft": ("#f2dcb8", "#3b2d17"),
                "on-accent": ("#23291f", "#161a15"),
                "focus": ("#2f5d3a", "#9fcc9c"),
            },
            {
                "brand": "森林綠 forest: primary button, links, the notebook-cover block.",
                "accent": "黃土 ochre: highlighter marks and the status dot.",
            },
        ),
        families=fam(
            '"Newsreader", ' + NOTO_SERIF,
            '"Source Sans 3", ' + NOTO_SANS,
            '"Overpass Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,700;1,6..72,500&family=Source+Sans+3:wght@400;600&family=Overpass+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@500;700&display=swap",
        typegroups=scale(d=(56, 64), dw=500, ls_d="-0.01em"),
        radius=(3, 6, 10),
        bw=1,
        shadows=shadows(
            "0 1px 0 #cfc3a8, 0 2px 6px rgba(35,41,31,0.06)", "0 1px 0 #374033"
        ),
        knobs=dict(
            head_w=500,
            label_upper=True,
            hero_size="56px",
            hero_lh="1.15",
            em_style="italic",
            card_hover="border-color: var(--brand);",
            media_bg="brand-soft",
            media_ink="brand-text",
            header_bg="bg",
            nav_current="color: var(--ink); background: linear-gradient(transparent 60%, var(--accent-soft) 60%);",
        ),
        extra_css="""
.sy-hero { background-image: repeating-linear-gradient(transparent 0 31px, var(--line) 31px 32px); }
.sy-hero h1, .sy-hero p { background: transparent; }
.sy-card { border-top: 6px solid var(--brand); }
.sy-card:nth-child(2) { border-top-color: var(--accent); }
.sy-card .sy-media { border: 1px dashed var(--line); background: var(--surface); }
.sy-card .sy-media span { font-style: italic; }
.sy-timeline time { color: var(--ink-muted); }
.sy-timeline h4 { font-style: italic; font-weight: 500; }
""",
        cover=dict(
            arrangement="slab",
            pattern="quarter",
            blocks=["brand", "accent", "line", "ink"],
            ptoken="brand",
            pitch=32,
            em=0.55,
            name_w=500,
            corner="radius-md",
            why="a literal motif, leaves: quarter-circle arcs from the radius scale growing across the moss tint",
        ),
        copy=dict(
            kicker="FIELD NOTES · 現場筆記",
            hero="我在工廠現場觀察，<em>然後寫出會自己跑的流程</em>。",
        ),
        readme=dict(
            intro="**田野筆記** 像一本放在工作服口袋的野帳：牛皮紙色、森林綠封面、橫線筆記頁。它強調「我是去現場看、去聽、再動手」的人。",
            fit="你的強項是需求訪談、現場觀察、跨部門溝通，然後把它變成系統。適合寫專案回顧、訪談紀錄、導入故事。",
            voice=[
                "觀察式：「我在現場看到…所以…」",
                "用時間與地點錨定故事。",
                "可以引用使用者原話（去識別化）。",
                "不用 emoji；註記用 ※ 與手寫感底線。",
            ],
            examples=[
                "我在工廠現場觀察，然後寫出會自己跑的流程。",
                "※ 品保同仁說：「我每天要開六個檔案才知道今天要驗什麼。」",
            ],
            color="`bg` 牛皮紙、`ink` 墨綠黑。`brand` 森林綠是主色（按鈕、連結、卡片頂端書背色）；`accent` 黃土色是螢光筆與狀態。深色主題是「夜間營地」：深綠黑底，綠色提亮。",
            type="標題 Newsreader（新聞體襯線，可用斜體）、內文 Source Sans 3 + Noto Sans TC、標籤 Overpass Mono 全大寫。",
            layout="Hero 底是 32px 橫線筆記頁（`line`）。卡片頂端 6px 色帶像筆記本書背，綠黃輪替。圓角 3/6/10，陰影極淡。",
            imagery="現場照片（去識別、無人臉）、手繪草圖掃描、白板照。佔位圖是虛線框加斜體代號。圖示用 1.5px 線條。",
            signature=[
                "Hero 橫線筆記紙背景。",
                "卡片頂端的書背色帶。",
                "目前頁面用螢光筆劃記。",
            ],
            dont=[
                "不要擬真紙張材質圖。",
                "不要手寫字型當內文。",
                "不要放可辨識的同仁或客戶。",
            ],
        ),
    )
)

# ===================================================================== 12
STYLES.append(
    dict(
        id="12-control-room",
        title="siyulio · 12 控制室",
        namespace="SiyulioOps",
        tagline="像產線中控台：狀態一眼可見，警示只用一個顏色。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#eceef0", "#0f1215"),
                "surface": ("#ffffff", "#171b20"),
                "line": ("#c9ced4", "#2c333b"),
                "ink": ("#14181d", "#e8ecf0"),
                "ink-muted": ("#4b5560", "#9aa5b1"),
                "brand": ("#ff6a13", "#ff7a2b"),
                "brand-text": ("#b04100", "#ff8c47"),
                "brand-soft": ("#ffe0cc", "#3a2112"),
                "on-brand": ("#14181d", "#0f1215"),
                "accent": ("#1a7f5a", "#3ccf91"),
                "accent-soft": ("#d2eee3", "#12301f"),
                "on-accent": ("#ffffff", "#0f1215"),
                "focus": ("#b04100", "#ff8c47"),
            },
            {
                "brand": "Safety orange: primary button, the one alert per view, cover slab.",
                "accent": "Run green: the 'running' status only — paired with a word, never colour alone.",
            },
        ),
        families=fam(
            '"Barlow Condensed", ' + NOTO_SANS,
            '"Barlow", ' + NOTO_SANS,
            '"Barlow Semi Condensed", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=Barlow+Semi+Condensed:wght@500;600&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(60, 60), dw=600, ls_d="0", lw=600),
        radius=(2, 4, 6),
        bw=1,
        shadows=shadows("0 1px 2px rgba(20,24,29,0.08)", "none"),
        knobs=dict(
            head_w=600,
            head_ls="0",
            head_upper=True,
            label_upper=True,
            label_w=600,
            label_ls="0.1em",
            hero_size="60px",
            hero_lh="1",
            btn_upper=True,
            btn_ls="0.06em",
            card_hover="border-color: var(--ink-muted);",
            nav_upper=True,
            nav_ls="0.1em",
            nav_font="label",
            media_bg="bg",
            media_ink="ink-muted",
            nav_current="color: var(--ink); box-shadow: inset 0 -3px 0 var(--brand);",
        ),
        extra_css="""
.sy-cards { gap: 1px; background: var(--line); padding: 1px; }
.sy-card { border: 0; border-radius: 0; box-shadow: none; }
.sy-card .sy-media { border-radius: 2px; }
.sy-card .sy-media span { font-size: 28px; letter-spacing: .06em; }
.sy-card .sy-tags::after { content: "● RUNNING"; font-family: var(--font-label); font-size: 11px; letter-spacing: .1em; color: var(--accent); margin-left: auto; align-self: center; }
.sy-hero .sy-kicker::before { content: "■ "; color: var(--brand); }
.sy-timeline time { font-variant-numeric: tabular-nums; }
.sy-header { box-shadow: inset 0 3px 0 var(--brand); }
""",
        cover=dict(
            arrangement="grid",
            pattern="tiles",
            blocks=["brand", "ink", "line", "accent"],
            ptoken="surface",
            pitch=24,
            em=0.45,
            name_w=600,
            name_ls="0",
            corner="none",
            name_extra="text-transform: uppercase;",
            why="geometric, modular, dense UI: small tiles cut by radius-sm, some merged two-wide like dashboard widgets",
        ),
        copy=dict(
            kicker="JASON LIN · OPS",
            hero="13 條自動化迴圈，<em>每天 24 小時</em>在線。",
            cta1="看系統",
            cta2="聯絡",
        ),
        readme=dict(
            intro="**控制室** 把網站做成工廠的中央控制台：灰底、窄體大寫標題、密集的網格面板、只有一個警示橘與一個運轉綠。它說「我管的是會動的系統」。",
            fit="你的作品是看板、監控、自動化排程、數據整合；訪客是廠長、IT 主管、數位轉型負責人。適合放儀表板截圖與營運數字。",
            voice=[
                "像儀表板標籤：名詞 + 數字 + 單位。",
                "狀態用固定詞彙：RUNNING、IDLE、ALERT，搭中文說明。",
                "數字只放真實、可驗證的。",
                "不用 emoji。",
            ],
            examples=[
                "13 條自動化迴圈，每天 24 小時在線。",
                "● RUNNING · 晨報 agent · 08:00 每日",
            ],
            color="灰階為底。`brand` 安全橘是唯一的強調與警示（主要按鈕、頁首頂線、目前頁面）；`accent` 運轉綠只代表 RUNNING，永遠跟文字一起出現。不要用紅綠區分狀態。",
            type="標題 Barlow Condensed 600 全大寫（像機台面板）、內文 Barlow、標籤 Barlow Semi Condensed 全大寫字距 0.1em。數字用 tabular-nums 對齊。",
            layout="面板網格：卡片之間 1px 縫（`line` 透出），沒有外框與圓角，像拼起來的螢幕牆。頁首頂端 3px 橘線。密度高、間距小（`space-3`～`space-5`）。",
            imagery="儀表板、圖表、排程表的真實截圖（去敏）。佔位圖是灰塊加大寫代號。圖示用 1.5px 方頭線條，狀態用實心點加文字。",
            signature=[
                "面板間 1px 縫的拼接網格。",
                "每張卡右下角 `● RUNNING`。",
                "頁首頂部 3px 安全橘。",
            ],
            dont=["不要假數據、假圖表。", "不要多個警示色。", "不要只靠顏色表示狀態。"],
        ),
    )
)

# ===================================================================== 13
STYLES.append(
    dict(
        id="13-hanzi-poster",
        title="siyulio · 13 漢字海報",
        namespace="SiyulioHanzi",
        tagline="一個大字、一抹朱紅：用中文排出氣勢。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#efe8dc", "#121010"),
                "surface": ("#f8f3ea", "#1c1918"),
                "line": ("#cbbfae", "#3a3431"),
                "ink": ("#141210", "#f2ebe0"),
                "ink-muted": ("#57504a", "#b8ada0"),
                "brand": ("#c8102e", "#ef4a5f"),
                "brand-text": ("#a80d26", "#ff6b7c"),
                "brand-soft": ("#f3d5d0", "#3d1519"),
                "on-brand": ("#ffffff", "#121010"),
                "accent": ("#141210", "#f2ebe0"),
                "accent-soft": ("#e2dace", "#2a2523"),
                "on-accent": ("#efe8dc", "#121010"),
                "focus": ("#a80d26", "#ff6b7c"),
            },
            {
                "brand": "中國紅 vermilion: the big character block, primary button.",
                "accent": "Ink black (paper white in dark): inverted blocks, the second cover block.",
            },
        ),
        families=fam('"Noto Serif TC", "Songti TC", serif', NOTO_SANS, NOTO_SANS),
        gfonts=GF
        + "Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(72, 84), dw=900, ls_d="0.02em", lw=700),
        radius=(0, 2, 2),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=900,
            head_ls="0.02em",
            label_upper=False,
            label_ls="0.2em",
            label_w=700,
            hero_size="72px",
            hero_lh="1.15",
            card_hover="border-color: var(--brand);",
            media_bg="brand",
            media_ink="on-brand",
            logo_w=900,
            nav_current="color: var(--brand-text); font-weight: 700;",
        ),
        extra_css="""
.sy-hero { grid-template-columns: auto 1fr; column-gap: var(--space-6); }
.sy-hero::before { content: "造"; grid-row: 1 / span 4; font-family: var(--font-display); font-weight: 900; font-size: 200px; line-height: 1; color: var(--brand); writing-mode: vertical-rl; }
.sy-hero > * { grid-column: 2; }
.sy-hero h1 em { color: var(--brand-text); }
.sy-card .sy-media { border-radius: 0; }
.sy-card .sy-media span { font-size: 64px; font-weight: 900; }
.sy-card h3 { font-size: 24px; letter-spacing: .04em; }
.sy-timeline time { letter-spacing: .1em; }
.sy-logo { letter-spacing: .02em; }
""",
        cover=dict(
            arrangement="bleed",
            pattern="glyph",
            blocks=["brand", "accent", "brand-soft", "ink-muted"],
            ptoken="bg",
            glyph="造",
            glyph_size=280,
            glyph_drop=-30,
            em=0.55,
            name_w=900,
            name_ls="0",
            corner="none",
            pattern_over=True,
            why="a distinctive display face: one oversized 造 (to make, as in 製造) clipped by the red block",
        ),
        copy=dict(
            kicker="林佳賢 · 製造業 AI 自動化",
            hero="把 AI 造進工廠，<em>造進每一天</em>。",
            lead="我在製造業的經營企劃室工作，設計並維運 24 小時運作的 AI agent。這裡是我的作品、筆記與正在進行的實驗。",
            cta1="看作品",
            cta2="聯絡我",
        ),
        readme=dict(
            intro="**漢字海報** 用一個大大的中文字當主視覺：「造」——製造、創造、打造。粗宋體、米色宣紙、朱紅大字，有東方海報的氣勢，一看就知道是中文世界的作者。",
            fit="你的主要讀者用中文，想強調在地、製造業、以及「動手造東西」的身份；適合演講、出版、對台灣企業的個人品牌。",
            voice=[
                "中文為主，句子對仗、有節奏：「把 AI 造進工廠，造進每一天。」",
                "標題可以四字、七字成句。",
                "英文只出現在技術名詞。",
                "不用 emoji。",
            ],
            examples=["把 AI 造進工廠，造進每一天。", "語音之造 · 記憶之造 · 模型之造"],
            color="`bg` 宣紙米、`ink` 墨黑；`brand` 朱紅是大字與主要按鈕。`accent` 是墨黑（深色主題反白），用於反白區塊。紅色可以大面積，但一頁只有一個紅色大塊。",
            type="標題 Noto Serif TC 900（粗宋），字距 +0.02em；內文 Noto Sans TC；標籤 Noto Sans TC 700 字距 0.2em。Hero 左側放一個 200px 直排「造」。",
            layout="海報式構圖：大字佔左、文字靠右。零到 2px 圓角、無陰影。中文標題不要壓字距。",
            imagery="主視覺是文字本身；照片用黑白或去飽和。作品示意塊用紅底白色單字（「聲」「憶」「模」）。圖示越少越好。",
            signature=[
                "Hero 左側直排 200px 朱紅「造」。",
                "作品卡示意塊用單一漢字。",
                "封面的超大「造」被紅塊裁切。",
            ],
            dont=[
                "不要書法字體或毛筆筆觸。",
                "不要龍、祥雲等傳統紋樣。",
                "不要一頁兩個紅色大塊。",
            ],
        ),
    )
)

# ===================================================================== 14
STYLES.append(
    dict(
        id="14-solar",
        title="siyulio · 14 日光派",
        namespace="SiyulioSolar",
        tagline="樂觀的科技：陽光黃、植物綠、圓潤的字。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#fbf8ec", "#141a12"),
                "surface": ("#ffffff", "#1d241a"),
                "line": ("#e3dcc0", "#34402e"),
                "ink": ("#1f2a1c", "#f1f0e2"),
                "ink-muted": ("#586150", "#b6b8a3"),
                "brand": ("#f5b700", "#ffcc33"),
                "brand-text": ("#7a5a00", "#ffd45c"),
                "brand-soft": ("#fdf0c2", "#3a3212"),
                "on-brand": ("#1f2a1c", "#141a12"),
                "accent": ("#237347", "#5cc98a"),
                "accent-soft": ("#d7efe0", "#183324"),
                "on-accent": ("#ffffff", "#141a12"),
                "focus": ("#237347", "#ffd45c"),
            },
            {
                "brand": "Sun yellow as a fill: primary button, the sun disc, cover column. Never as text on light.",
                "accent": "Leaf green: status, links on cards, second cover column.",
            },
        ),
        families=fam(
            '"Bricolage Grotesque", ' + NOTO_SANS,
            '"Bricolage Grotesque", ' + NOTO_SANS,
            '"Bricolage Grotesque", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(d=(64, 68), dw=800, ls_d="-0.03em"),
        radius=(12, 20, 32),
        bw=1,
        shadows=shadows("0 2px 0 #e3dcc0", "0 2px 0 #34402e"),
        knobs=dict(
            head_w=800,
            head_ls="-0.03em",
            label_upper=False,
            label_ls="0.02em",
            label_w=600,
            hero_size="64px",
            tag_radius="pill",
            card_hover="transform: translateY(-3px);",
            media_bg="brand-soft",
            media_ink="brand-text",
            logo_w=800,
            nav_current="color: var(--on-brand); background: var(--brand); padding: 6px 14px; border-radius: 999px;",
            em_extra="color: var(--accent);",
        ),
        extra_css="""
.sy-btn { border-radius: 999px; }
.sy-hero { position: relative; overflow: hidden; }
.sy-hero::after { content: ""; position: absolute; right: -60px; top: -60px; width: 240px; height: 240px; border-radius: 999px; background: var(--brand); z-index: 0; }
.sy-hero > * { position: relative; z-index: 1; }
.sy-card .sy-media { border-radius: 24px; }
.sy-card:nth-child(2) .sy-media { background: var(--accent-soft); } .sy-card:nth-child(2) .sy-media span { color: var(--accent); }
.sy-timeline time { color: var(--accent); }
""",
        cover=dict(
            arrangement="columns",
            pattern="discs",
            blocks=["brand", "accent", "line", "ink"],
            ptoken="surface",
            pitch=40,
            disc=12,
            em=0.58,
            name_w=800,
            name_ls="-0.04em",
            corner="radius-lg",
            why="soft, large radii, optimism: sun discs cut out of the tint column, rising with the bars",
        ),
        copy=dict(
            kicker="Hi，我是 Jason",
            hero="AI 不可怕，<em>它可以讓上班變輕鬆</em>。",
            cta1="看看我做了什麼",
            cta2="聊聊",
        ),
        readme=dict(
            intro="**日光派** 是樂觀科技的語氣：陽光黃、植物綠、圓潤有個性的字體、大圓角。它傳達「AI 讓工作變好」，親切又有活力，不走冷冰冰的科技風。",
            fit="你想推廣 AI 導入、做內訓或演講，讓非技術同仁也覺得 AI 可親近；也適合個人品牌經營。",
            voice=[
                "正向、具體：「它可以讓上班變輕鬆」，而不是「顛覆產業」。",
                "用日常例子解釋技術。",
                "第一人稱、輕鬆，但不撒嬌。",
                "emoji 可有可無，最多一處。",
            ],
            examples=[
                "AI 不可怕，它可以讓上班變輕鬆。",
                "以前要開六個檔案，現在早上打開手機就看得到。",
            ],
            color="`brand` 陽光黃只當填色（按鈕、太陽圓、目前頁面膠囊），上面的字用 `on-brand` 深綠黑；淺色主題的黃色文字改用 `brand-text` 深芥末。`accent` 葉綠用在狀態與強調字。",
            type="一家族 Bricolage Grotesque（有個性的 grotesque，可變寬度），中文落到 Noto Sans TC。標題 800、字距 -0.03em。",
            layout="大圓角（12/20/32）、膠囊按鈕、Hero 右上角露出半顆太陽。陰影只是 2px 的底線，像紙片立起來。",
            imagery="明亮、自然光的照片；植物、陽光、桌面工作照（無人臉）。佔位圖是黃／綠淺色圓角塊。圖示用 2px 圓頭線條。",
            signature=[
                "Hero 右上角半顆太陽。",
                "黃色膠囊標示目前頁面。",
                "作品卡示意塊黃綠輪替。",
            ],
            dont=[
                "不要黃色文字在淺底上。",
                "不要冷色漸層。",
                "不要過度可愛的插畫角色。",
            ],
        ),
    )
)

import styles_more  # noqa: E402,F401  (appends 15+)
import styles_more2  # noqa: E402,F401  (appends 19+)
