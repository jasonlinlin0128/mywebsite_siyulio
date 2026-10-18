# -*- coding: utf-8 -*-
"""Styles 15+ (appended to styles.STYLES at import time)."""

from styles import (
    STYLES,
    colors,
    dark_first,
    LIGHT_DARK,
    DARK_LIGHT,
    fam,
    scale,
    shadows,
    shadows_df,
    GF,
    NOTO_SANS,
    NOTO_SERIF,
)

# ===================================================================== 15
STYLES.append(
    dict(
        id="15-circuit",
        title="siyulio · 15 電路板",
        namespace="SiyulioCircuit",
        tagline="防焊綠、銅箔線、白色絲印：把系統畫成一塊板子。",
        themes=DARK_LIGHT,
        colors=dark_first(
            {
                "bg": ("#0b1c15", "#eef3ec"),
                "surface": ("#11281e", "#ffffff"),
                "line": ("#24493a", "#c7d6c9"),
                "ink": ("#eef4ea", "#0f2219"),
                "ink-muted": ("#a7bfae", "#46594d"),
                "brand": ("#d0883a", "#975812"),
                "brand-text": ("#e6a45c", "#8a4f0e"),
                "brand-soft": ("#2c2a16", "#f6e6cf"),
                "on-brand": ("#0b1c15", "#ffffff"),
                "accent": ("#5fd38d", "#1a7a43"),
                "accent-soft": ("#16392a", "#d6efdf"),
                "on-accent": ("#0b1c15", "#ffffff"),
                "focus": ("#e6a45c", "#1a7a43"),
            },
            {
                "brand": "Copper: primary button, trace highlights, cover pad. On light it darkens to tinned copper.",
                "accent": "LED green: status dot, 'running' tags, one highlight per view.",
            },
        ),
        families=fam(
            '"Space Grotesk", ' + NOTO_SANS,
            '"Space Grotesk", ' + NOTO_SANS,
            '"JetBrains Mono", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(60, 64), dw=700, ls_d="-0.02em", lw=600),
        radius=(2, 4, 8),
        bw=1,
        shadows=shadows_df("0 0 0 1px #24493a", "0 0 0 1px #c7d6c9"),
        knobs=dict(
            head_w=700,
            head_ls="-0.02em",
            label_upper=True,
            label_ls="0.12em",
            label_w=600,
            hero_size="58px",
            tag_radius="sm",
            card_hover="border-color: var(--brand);",
            media_bg="bg",
            media_ink="brand-text",
            nav_font="label",
            nav_upper=True,
            nav_ls="0.12em",
            nav_current="color: var(--brand-text); text-decoration: none;",
            btn_font="label",
            btn_upper=True,
            btn_ls="0.08em",
        ),
        extra_css="""
.sy-card .sy-media { background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px); background-size: 16px 16px; border: 1px solid var(--line); }
.sy-hero { border-left: 4px solid var(--brand); }
.sy-hero h1 em::before { content: ""; display: inline-block; width: 10px; height: 10px; border-radius: 999px; border: 3px solid var(--brand); margin-right: 8px; vertical-align: middle; }
.sy-timeline time::before { content: "◉ "; color: var(--accent); }
.sy-logo::before { content: "U1 "; font-family: var(--font-label); font-size: 12px; color: var(--ink-muted); letter-spacing: 0.1em; }
""",
        cover=dict(
            arrangement="grid",
            pattern="plus",
            blocks=["brand", "line", "ink-muted", "accent"],
            ptoken="bg",
            pitch=24,
            stroke=2,
            em=0.6,
            name_w=700,
            name_ls="-0.03em",
            corner="none",
            why="via crosses drilled through the copper plane, the board's own grid",
        ),
        copy=dict(
            kicker="REV 2026 · JASON LIN",
            hero="訊號從感測器走到報表，<em>中間每一條線都是我拉的</em>。",
            cta1="看電路圖",
            cta2="聯絡我",
        ),
        readme=dict(
            intro="**電路板** 把網站當成一塊 PCB：深防焊綠底、銅色走線、白色絲印字。它說的是「我把系統一條條接起來」，適合在製造業做 AI 與自動化整合的人。",
            fit="你的作品偏系統整合、硬體與軟體交界（感測、產線、本地模型、自動化）；讀者是工程師與技術主管。",
            voice=[
                "像規格書：元件、訊號、流向。",
                "數字帶單位：42 tok/s、24 小時、6 個資料源。",
                "標籤用板上絲印格式：U1、REV、J3。",
                "不寫「賦能」「生態系」。",
            ],
            examples=[
                "訊號從感測器走到報表，中間每一條線都是我拉的。",
                "J3：Discord → 第二大腦，延遲 < 60 秒。",
            ],
            color="深色是主題：`bg` 防焊綠，`brand` 銅箔只做填色與焊盤，文字用 `brand-text`。`accent` LED 綠只給狀態。淺色主題像白色防焊油墨板。",
            type="Space Grotesk 做標題與內文，JetBrains Mono 做絲印標籤、按鈕、導覽（全大寫、字距 0.12em）。中文落到 Noto Sans TC。",
            layout="小圓角（2/4/8），1px 線框代替陰影。作品卡示意塊是 16px 格點，像空板。Hero 左側一條 4px 銅線。",
            imagery="電路板微距、示波器畫面、接線圖；作品圖用線框系統圖而不是照片。圖示 1.5px 直角線。",
            signature=[
                "Logo 前面的 U1 絲印。",
                "Hero 強調字前的焊盤圓圈。",
                "16px 格點示意塊。",
            ],
            dont=[
                "不要霓虹發光、矩陣雨。",
                "不要把銅色當小字用在淺底。",
                "不要圓潤的泡泡按鈕。",
            ],
        ),
    )
)

# ===================================================================== 16
STYLES.append(
    dict(
        id="16-safety-sign",
        title="siyulio · 16 工安標示",
        namespace="SiyulioSafety",
        tagline="工廠看得懂的視覺：安全橘、警示斜紋、粗黑字。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f3f0e8", "#151515"),
                "surface": ("#ffffff", "#202020"),
                "line": ("#d6d0c2", "#3a3a3a"),
                "ink": ("#141414", "#f3f0e8"),
                "ink-muted": ("#55524b", "#b9b4a8"),
                "brand": ("#ff6b12", "#ff7a26"),
                "brand-text": ("#b13f00", "#ff9a5a"),
                "brand-soft": ("#ffe1cc", "#3d2416"),
                "on-brand": ("#141414", "#141414"),
                "accent": ("#ffd100", "#ffd100"),
                "accent-soft": ("#fff2b0", "#3a3310"),
                "on-accent": ("#141414", "#141414"),
                "focus": ("#141414", "#ffd100"),
            },
            {
                "brand": "Safety orange as a fill: primary button, sign blocks, cover panel. Text on it is near-black.",
                "accent": "Caution yellow: hazard stripe, status tag, current-page marker.",
            },
        ),
        families=fam(
            '"Archivo", ' + NOTO_SANS,
            '"Archivo", ' + NOTO_SANS,
            '"Archivo", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Archivo:wdth,wght@62..125,400;62..125,600;62..125,800;62..125,900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(d=(68, 68), dw=900, ls_d="-0.01em", lw=800),
        radius=(0, 2, 4),
        bw=2,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=900,
            head_ls="-0.01em",
            head_upper=True,
            label_upper=True,
            label_ls="0.06em",
            label_w=800,
            hero_size="64px",
            hero_lh="1.0",
            tag_radius="sm",
            btn_border="ink",
            btn_primary_border="ink",
            btn_upper=True,
            btn_w=800,
            card_border="ink",
            card_hover="background: var(--accent-soft);",
            media_bg="brand",
            media_ink="on-brand",
            logo_w=900,
            logo_upper=True,
            nav_upper=True,
            nav_ls="0.04em",
            nav_current="color: var(--on-accent); background: var(--accent); padding: 4px 10px;",
        ),
        extra_css="""
.sy-header { border-bottom: 0; box-shadow: 0 6px 0 0 transparent; position: relative; margin-bottom: 8px; }
.sy-header::after { content: ""; position: absolute; left: 0; right: 0; bottom: -8px; height: 8px; background: repeating-linear-gradient(-45deg, var(--accent) 0 12px, #141414 12px 24px); }
.sy-hero { border-left: 16px solid var(--brand); }
.sy-hero .sy-kicker { display: inline-block; justify-self: start; background: var(--ink); color: var(--bg); padding: 4px 10px; }
.sy-card .sy-media { border-radius: 0; background-image: repeating-linear-gradient(-45deg, transparent 0 14px, rgba(0,0,0,.12) 14px 28px); }
.sy-tag { font-weight: 800; }
.sy-timeline time { color: var(--ink); font-weight: 800; border-left: 6px solid var(--brand); padding-left: 8px; }
""",
        cover=dict(
            arrangement="bands",
            pattern="stripes",
            blocks=["brand", "ink", "accent", "ink-muted"],
            ptoken="ink",
            pitch=24,
            em=0.62,
            name_w=900,
            name_ls="-0.02em",
            name_extra="text-transform: uppercase;",
            corner="none",
            why="hazard stripes across the main orange band, the language every factory floor already reads",
        ),
        copy=dict(
            kicker="現場出身 · Jason Lin",
            hero="AI 要在<em>現場</em>能用，才算數。",
            cta1="看案例",
            cta2="找我聊",
        ),
        readme=dict(
            intro="**工安標示** 借用工廠的標示語言：安全橘、警示黃黑斜紋、粗壯的黑體。它在說「我的東西是給現場用的」，跟製造業背景直接連結，一眼就分得出你不是一般的軟體人。",
            fit="你想強調製造業現場經驗、導入落地、跟產線同仁一起做事；讀者是工廠主管、顧問、想找導入夥伴的公司。",
            voice=[
                "短、硬、直接，像現場告示：「先停機，再處理。」",
                "動詞開頭。",
                "標題可以全大寫英文，中文不變。",
                "不拐彎、不用比喻。",
            ],
            examples=[
                "AI 要在現場能用，才算數。",
                "從 ERP 抓數據 → 每天 07:30 自動出報表。",
            ],
            color="`brand` 安全橘只當大面積填色，上面的字用 `on-brand` 近黑；淺色主題的橘色文字改用 `brand-text` 深橘。`accent` 警示黃與黑色組成斜紋。",
            type="Archivo 可變寬度，標題 900、全大寫英文；中文 Noto Sans TC Black。字距收緊，行高 1.0。",
            layout="零圓角、2px 黑框、沒有陰影。Header 底下一條警示斜紋，Hero 左側 16px 橘色色帶。",
            imagery="現場照片（設備、看板、工具），高對比、不加濾鏡；人物不露臉。圖示用 ISO 7010 風格的實心圖形。",
            signature=[
                "Header 下緣的黃黑警示斜紋。",
                "反白的 kicker 標籤。",
                "作品卡示意塊是橘色斜紋板。",
            ],
            dont=[
                "不要把整頁都塗成橘色。",
                "不要用紅色表達「危險」以外的意思。",
                "不要細字、不要漸層。",
            ],
        ),
    )
)

# ===================================================================== 17
STYLES.append(
    dict(
        id="17-editorial",
        title="siyulio · 17 雜誌專欄",
        namespace="SiyulioEditorial",
        tagline="像一本週末雜誌：高對比襯線、酒紅、首字放大。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f6f1e7", "#191513"),
                "surface": ("#fffdf8", "#221d1a"),
                "line": ("#ddd3c0", "#3b332d"),
                "ink": ("#1d1714", "#f1e9dc"),
                "ink-muted": ("#5f554c", "#bcae9d"),
                "brand": ("#7b1e2c", "#da7380"),
                "brand-text": ("#7b1e2c", "#e88a96"),
                "brand-soft": ("#f1dcd9", "#3a2124"),
                "on-brand": ("#fffdf8", "#191513"),
                "accent": ("#2f5d50", "#7fb8a6"),
                "accent-soft": ("#dbe8e2", "#1f302b"),
                "on-accent": ("#ffffff", "#191513"),
                "focus": ("#7b1e2c", "#e88a96"),
            },
            {
                "brand": "Claret: primary button, drop caps, section rules.",
                "accent": "Bottle green: status tags and one pull-quote per page.",
            },
        ),
        families=fam(
            '"Fraunces", ' + NOTO_SERIF,
            NOTO_SANS,
            '"Inter", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,800;1,9..144,600&family=Inter:wght@500;600&family=Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500&display=swap",
        typegroups=scale(d=(72, 76), dw=600, ls_d="-0.02em", lead=(22, 34)),
        radius=(0, 0, 0),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=600,
            head_ls="-0.02em",
            label_upper=True,
            label_ls="0.14em",
            label_w=600,
            hero_size="68px",
            hero_lh="1.04",
            em_style="italic",
            tag_radius="sm",
            card_border="bg",
            card_hover="border-color: var(--line);",
            card_pad="0",
            media_bg="brand-soft",
            media_ink="brand-text",
            logo_w=800,
            nav_current="color: var(--brand-text); text-decoration: none; font-style: italic;",
        ),
        extra_css="""
.sy-header { border-bottom: 3px double var(--ink); }
.sy-hero { border-top: 1px solid var(--ink); }
.sy-hero p:not(.sy-kicker)::first-letter { font-family: var(--font-display); float: left; font-size: 64px; line-height: 52px; padding: 4px 8px 0 0; color: var(--brand-text); font-weight: 800; }
.sy-card { background: transparent; box-shadow: none; }
.sy-card .sy-media { border-radius: 0; }
.sy-card h3 { font-style: italic; }
.sy-timeline time { font-family: var(--font-display); font-style: italic; font-size: 16px; letter-spacing: 0; }
""",
        cover=dict(
            arrangement="slab",
            pattern="rules",
            blocks=["brand", "ink", "line", "accent"],
            ptoken="ink-muted",
            pitch=16,
            count=7,
            stroke=1,
            em=0.5,
            name_w=600,
            name_ls="-0.03em",
            name_extra="font-style: italic;",
            corner="none",
            why="column rules running under the blocks, the ruled page of a magazine spread",
            pattern_over=False,
        ),
        copy=dict(
            kicker="專欄 · 第 01 期",
            hero="一個製造業企劃，<em>怎麼讓 AI 每天自己上班</em>。",
            lead="這裡寫下我在工廠與辦公室之間，用 AI 做出來的系統、踩過的坑、還有後來想通的事。每一篇都是實作過才寫。",
            cta1="讀最新一篇",
            cta2="訂閱",
        ),
        readme=dict(
            intro="**雜誌專欄** 把網站做成一份有編輯感的刊物：高對比襯線、酒紅、首字放大、雙線分隔。重點是長文和觀點，適合想以寫作經營個人品牌的人。",
            fit="你打算持續寫文章、案例拆解、心得；讀者是會讀完一篇長文的人：主管、同業、媒體。",
            voice=[
                "有敘事：先場景，再問題，再做法。",
                "標題像雜誌標：一個問題或一個反差。",
                "段落短，一段一個想法。",
                "結尾留一句自己的判斷。",
            ],
            examples=[
                "一個製造業企劃，怎麼讓 AI 每天自己上班。",
                "那天早上七點半，報表第一次自己出現在手機裡。",
            ],
            color="米紙 `bg` 加酒紅 `brand`。酒紅在淺色主題可直接當文字（對比夠），深色主題換成玫瑰色 `brand-text`。`accent` 瓶綠只用在狀態與引言。",
            type="Fraunces（可變光學尺寸的襯線）做標題，強調字用斜體；中文落到 Noto Serif TC。內文 Noto Sans TC，標籤 Inter 全大寫、字距 0.14em。",
            layout="零圓角、無陰影，用 1px 細線與雙線分欄。卡片沒有框，只有圖、斜體標題、說明。首段首字放大。",
            imagery="紀實攝影：黑白或低飽和，有景深；插圖用單色版畫風。圖說用小字斜體。",
            signature=[
                "首字放大（drop cap）。",
                "Header 下方的雙線。",
                "斜體的作品名與日期。",
            ],
            dont=[
                "不要圓角卡片與陰影。",
                "不要一頁超過兩種強調色。",
                "不要用 Fraunces 排長段中文。",
            ],
        ),
    )
)

# ===================================================================== 18
STYLES.append(
    dict(
        id="18-one-bit",
        title="siyulio · 18 一位元",
        namespace="SiyulioOneBit",
        tagline="黑白兩色、像素字、老 Mac 視窗：把網站當成一台小電腦。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#ffffff", "#000000"),
                "surface": ("#ffffff", "#000000"),
                "line": ("#000000", "#ffffff"),
                "ink": ("#000000", "#ffffff"),
                "ink-muted": ("#444444", "#bbbbbb"),
                "brand": ("#000000", "#ffffff"),
                "brand-text": ("#000000", "#ffffff"),
                "brand-soft": ("#e6e6e6", "#262626"),
                "on-brand": ("#ffffff", "#000000"),
                "accent": ("#0000cc", "#8ab4ff"),
                "accent-soft": ("#dde0ff", "#1a1f40"),
                "on-accent": ("#ffffff", "#000000"),
                "focus": ("#0000cc", "#8ab4ff"),
            },
            {
                "brand": "Pure ink as a fill: primary button, title bars, cover blocks. The system is two colours plus one link blue.",
                "accent": "Hyperlink blue: links and the status dot, nothing else.",
            },
        ),
        families=fam(
            '"Pixelify Sans", ' + NOTO_SANS,
            NOTO_SANS,
            '"VT323", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Pixelify+Sans:wght@400;600;700&family=VT323&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(56, 60), dw=700, ls_d="0", label=(16, 18), lw=400),
        radius=(0, 0, 0),
        bw=2,
        shadows=shadows(
            "4px 4px 0 #000000",
            "4px 4px 0 #ffffff",
            "2px 2px 0 #000000",
            "2px 2px 0 #ffffff",
        ),
        knobs=dict(
            head_w=700,
            head_ls="0",
            label_upper=True,
            label_ls="0.04em",
            label_w=400,
            hero_size="54px",
            hero_lh="1.1",
            tag_radius="sm",
            btn_border="ink",
            btn_hover="background: var(--ink); color: var(--bg);",
            card_border="ink",
            card_hover="transform: translate(-2px,-2px);",
            media_bg="brand-soft",
            media_ink="ink",
            nav_font="label",
            nav_upper=True,
            nav_current="color: var(--on-brand); background: var(--brand); padding: 0 6px;",
            em_extra="color: var(--accent); text-decoration: underline; text-underline-offset: 6px;",
        ),
        extra_css="""
.sy-tag { font-size: 16px; }
.sy-nav a { font-size: 18px; }
.sy-header { background-image: repeating-linear-gradient(0deg, var(--ink) 0 1px, transparent 1px 4px); }
.sy-header .sy-logo, .sy-header .sy-nav { background: var(--surface); padding: 0 8px; }
.sy-card { padding-top: 0; }
.sy-card::before { content: "■ project"; display: block; margin: 0 calc(-1 * var(--space-5)); padding: 2px var(--space-3); background: var(--brand); color: var(--on-brand); font-family: var(--font-label); font-size: 16px; }
.sy-card .sy-media { border-radius: 0; border: 2px solid var(--ink); background-image: radial-gradient(var(--ink) 1px, transparent 1px); background-size: 4px 4px; }
.sy-card .sy-media span { background: var(--surface); padding: 0 8px; }
.sy-timeline time { font-size: 18px; }
""",
        cover=dict(
            arrangement="stagger",
            pattern="checker",
            blocks=["ink", "ink-muted", "line", "accent"],
            ptoken="bg",
            pitch=8,
            em=0.62,
            name_w=700,
            name_ls="0",
            corner="none",
            why="a 1-bit dither checker punched into the window block, the only grey a 1-bit screen can make",
        ),
        copy=dict(
            kicker="> JASON_LIN.EXE",
            hero="我做的東西都很小，<em>但每天都在跑</em>。",
            cta1="開啟作品",
            cta2="寄信",
        ),
        readme=dict(
            intro="**一位元** 借用 1984 年 Macintosh 的 1-bit 螢幕：只有黑與白，灰色靠點陣做，再加一個超連結藍。像素字、視窗標題列、硬陰影。它有玩心、好記，強調「我自己動手做小工具」。",
            fit="你想展示很多小工具、實驗、自己寫的腳本；讀者是工程師、創客、喜歡有個性網站的人。",
            voice=[
                "像系統訊息：短、帶一點幽默。",
                "可以用 `>`、`.EXE`、檔名當標籤。",
                "說明仍然要寫清楚做到什麼。",
                "幽默一頁最多一處。",
            ],
            examples=[
                "我做的東西都很小，但每天都在跑。",
                "> morning_brief.py — 07:30 自動執行。",
            ],
            color="只有 `ink` 與 `bg` 兩色，灰階用 `brand-soft` 或點陣背景。`accent` 超連結藍只給連結與狀態點。深色主題黑白對調。",
            type="Pixelify Sans 做英文標題與 logo，VT323 做標籤與導覽（16px 起跳才清楚），中文一律 Noto Sans TC，不做像素中文。",
            layout="零圓角、2px 黑框、4px 硬陰影。作品卡頂端是黑色視窗標題列，示意塊用 4px 點陣。Header 用掃描線背景。",
            imagery="作品截圖轉成 1-bit 抖色（dither）；圖示用 16×16 像素圖。不要彩色照片。",
            signature=[
                "作品卡頂端的黑色視窗標題列。",
                "點陣抖色灰。",
                "按鈕 hover 黑白反轉。",
            ],
            dont=[
                "不要加第三種顏色。",
                "不要把中文做成像素字。",
                "不要圓角與模糊陰影。",
            ],
        ),
    )
)
