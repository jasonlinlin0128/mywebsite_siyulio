# -*- coding: utf-8 -*-
"""Styles 19-24 (appended to styles.STYLES at import time)."""

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


def R(intro, fit, voice, examples, color, type_, layout, imagery, signature, dont):
    return dict(
        intro=intro,
        fit=fit,
        voice=voice,
        examples=examples,
        color=color,
        type=type_,
        layout=layout,
        imagery=imagery,
        signature=signature,
        dont=dont,
    )


# ===================================================================== 19
STYLES.append(
    dict(
        id="19-platform",
        title="siyulio · 19 月台時刻",
        namespace="SiyulioPlatform",
        tagline="車站月台的語言：深藍站牌、白色粗字、琥珀色到站燈。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f1f3f7", "#0d1426"),
                "surface": ("#ffffff", "#152040"),
                "line": ("#cdd4e2", "#2a3866"),
                "ink": ("#0f1a33", "#eef1f8"),
                "ink-muted": ("#4a5570", "#aab4cc"),
                "brand": ("#1b3a8c", "#3a63d8"),
                "brand-text": ("#1b3a8c", "#9db6ff"),
                "brand-soft": ("#dce4f7", "#1d2c5c"),
                "on-brand": ("#ffffff", "#ffffff"),
                "accent": ("#f2a900", "#ffbe2e"),
                "accent-soft": ("#fdeec4", "#3a3016"),
                "on-accent": ("#0f1a33", "#0d1426"),
                "focus": ("#1b3a8c", "#ffbe2e"),
            },
            {
                "brand": "Station-sign navy: primary button, header bar, cover sign panel. White text on it.",
                "accent": "Departure-board amber: status, times, current page. Text on it is navy.",
            },
        ),
        families=fam(
            '"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", system-ui, sans-serif',
            NOTO_SANS,
            '"Barlow Condensed", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Barlow+Condensed:wght@500;600;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(d=(60, 68), dw=900, ls_d="0", label=(14, 18), lw=600),
        radius=(4, 6, 10),
        bw=1,
        shadows=shadows("0 1px 0 #cdd4e2", "0 1px 0 #2a3866"),
        knobs=dict(
            head_w=900,
            head_ls="0.02em",
            label_upper=True,
            label_ls="0.1em",
            label_w=600,
            hero_size="58px",
            hero_lh="1.15",
            header_bg="brand",
            logo_w=900,
            nav_current="color: var(--on-accent); background: var(--accent); padding: 4px 10px; border-radius: 4px;",
            media_bg="brand",
            media_ink="on-brand",
            card_hover="border-color: var(--brand);",
            em_extra="background: var(--accent-soft); color: var(--ink); padding: 0 6px; border-radius: 4px;",
        ),
        extra_css="""
.sy-header .sy-logo, .sy-header .sy-nav a { color: var(--on-brand); }
.sy-header .sy-logo b { color: var(--accent); }
.sy-header .sy-nav a[aria-current] { color: var(--on-accent); }
.sy-timeline time { font-size: 20px; font-weight: 700; color: var(--ink); background: var(--accent-soft); padding: 0 8px; border-radius: 4px; justify-self: start; height: 26px; line-height: 26px; }
.sy-card .sy-media span::after { content: " →"; color: var(--accent); }
""",
        cover=dict(
            arrangement="bands",
            pattern="rules",
            blocks=["brand", "ink", "accent", "line"],
            ptoken="on-brand",
            pitch=16,
            count=3,
            stroke=2,
            em=0.58,
            name_w=900,
            name_ls="0.01em",
            corner="none",
            why="white rules across the navy sign band, the lines that divide a timetable into rows",
        ),
        copy=dict(
            kicker="NEXT · JASON LIN",
            hero="每一個系統都像一班車：<em>準時到站</em>，才算數。",
            cta1="查看作品",
            cta2="聯絡我",
        ),
        readme=R(
            "**月台時刻** 借用台灣車站的指標系統：深藍站牌、白色粗黑體、琥珀色的到站燈。它說的是「可靠、準時、看得懂」，像每天都在跑的排程。",
            "你強調穩定運作與排程自動化（晨報、排程、24 小時 agent）；讀者是想找一個可靠的人的主管與合作夥伴。",
            [
                "像站務廣播：先地點、再時間、再動作。",
                "時間用 24 小時制：07:30。",
                "一句一件事。",
            ],
            [
                "每一個系統都像一班車：準時到站，才算數。",
                "07:30 晨報到站，已連續運行。",
            ],
            "`brand` 站牌藍做 Header 底與主要按鈕，字一律白。`accent` 琥珀只給時間、狀態、目前頁面，上面的字用深藍。",
            "中文全用 Noto Sans TC Black 做標題，像站名；英數標籤用 Barlow Condensed 大寫。",
            "Header 是整條藍色站牌；時間軸日期是琥珀色小牌；圓角小（4/6/10）。",
            "月台、時刻表、號誌照片；圖示用指標系統的實心箭頭。",
            ["藍色站牌 Header。", "琥珀色時間牌。", "作品卡名稱後的到站箭頭。"],
            ["不要用細字。", "不要把琥珀當大面積底色。", "不要復古懷舊濾鏡。"],
        ),
    )
)

# ===================================================================== 20
STYLES.append(
    dict(
        id="20-topo",
        title="siyulio · 20 等高線",
        namespace="SiyulioTopo",
        tagline="地形圖的配色：沙色紙、橄欖綠、赭色等高線。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f2eee2", "#171a14"),
                "surface": ("#faf8f1", "#20241c"),
                "line": ("#d8d0b8", "#3a4032"),
                "ink": ("#23261d", "#ecead9"),
                "ink-muted": ("#5a5b4c", "#b3b19c"),
                "brand": ("#4d5f2f", "#98ad6a"),
                "brand-text": ("#4d5f2f", "#b2c788"),
                "brand-soft": ("#e1e5cc", "#2c3420"),
                "on-brand": ("#faf8f1", "#171a14"),
                "accent": ("#a2531f", "#e08b52"),
                "accent-soft": ("#f1dcc8", "#3d2818"),
                "on-accent": ("#ffffff", "#171a14"),
                "focus": ("#a2531f", "#e08b52"),
            },
            {
                "brand": "Olive survey green: primary button, map areas, cover terrain.",
                "accent": "Ochre contour: status, elevation numbers, one highlight per view.",
            },
        ),
        families=fam(
            '"Spectral", ' + NOTO_SERIF, NOTO_SANS, '"DM Mono", ui-monospace, monospace'
        ),
        gfonts=GF
        + "Spectral:ital,wght@0,500;0,700;1,500&family=DM+Mono:wght@400;500&family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500&display=swap",
        typegroups=scale(d=(60, 66), dw=700, ls_d="-0.01em"),
        radius=(4, 8, 14),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=700,
            label_upper=False,
            label_ls="0.02em",
            hero_size="56px",
            em_style="italic",
            em_extra="color: var(--accent);",
            media_bg="brand-soft",
            media_ink="brand-text",
            card_hover="border-color: var(--accent);",
        ),
        extra_css="""
.sy-card .sy-media { background-image: repeating-radial-gradient(circle at 70% 60%, transparent 0 10px, var(--line) 10px 11px); }
.sy-card .sy-media span { background: var(--brand-soft); padding: 0 8px; }
.sy-timeline time::after { content: " m"; color: var(--ink-muted); }
.sy-hero .sy-kicker::before { content: "▲ "; color: var(--accent); }
""",
        cover=dict(
            arrangement="bleed",
            pattern="quarter",
            blocks=["brand", "accent", "line", "ink"],
            ptoken="brand-soft",
            pitch=32,
            em=0.55,
            name_w=700,
            name_ls="-0.02em",
            name_extra="font-style: italic;",
            corner="radius-lg",
            why="quarter-arcs stepping across the terrain block like contour lines on a survey sheet",
        ),
        copy=dict(
            kicker="現在位置 · Jason Lin",
            hero="一步一步把地形畫清楚，<em>路就會出現</em>。",
            cta1="看路線",
            cta2="聯絡我",
        ),
        readme=R(
            "**等高線** 取自地形圖：沙色紙、橄欖綠、赭色線條、帶單位的數字。它說的是「我先把現況測清楚，再規劃路線」，適合以盤點、規劃、導入見長的人。",
            "你的強項是盤點現況、畫架構、規劃導入路徑；讀者是需要有人幫忙看清全貌的主管。",
            [
                "像勘查紀錄：先現況，再判讀，再建議。",
                "數字帶單位。",
                "不誇大，不用口號。",
            ],
            [
                "一步一步把地形畫清楚，路就會出現。",
                "盤點 81 個機會點，挑出前 5 個先做。",
            ],
            "`brand` 橄欖綠做按鈕與地形塊；`accent` 赭色只給數字、等高線、強調字。",
            "Spectral 襯線做標題（強調字斜體），中文 Noto Serif TC；內文 Noto Sans TC；數字標籤 DM Mono。",
            "中等圓角（4/8/14），無陰影；作品卡示意塊畫同心等高線。",
            "空拍、地圖、手繪草圖；圖示用 1.5px 細線。",
            ["示意塊的同心等高線。", "kicker 前的三角點符號。", "斜體赭色強調字。"],
            [
                "不要冒險、登頂的勵志語氣。",
                "不要真實地圖截圖當裝飾。",
                "不要綠色大面積鋪底。",
            ],
        ),
    )
)

# ===================================================================== 21
STYLES.append(
    dict(
        id="21-kraft",
        title="siyulio · 21 牛皮紙箱",
        namespace="SiyulioKraft",
        tagline="出貨箱的質感：牛皮紙、黑色模板字、紅色出貨章。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#d9c09a", "#1e1912"),
                "surface": ("#e8d4b2", "#2a2319"),
                "line": ("#b39669", "#4a3e2c"),
                "ink": ("#1d1812", "#efe3cd"),
                "ink-muted": ("#4a3e2e", "#c2b399"),
                "brand": ("#1d1812", "#efe3cd"),
                "brand-text": ("#1d1812", "#efe3cd"),
                "brand-soft": ("#ccb084", "#3a3022"),
                "on-brand": ("#e8d4b2", "#1e1912"),
                "accent": ("#b3261e", "#ff6b5e"),
                "accent-soft": ("#e5b9a0", "#4a2420"),
                "on-accent": ("#ffffff", "#1e1912"),
                "focus": ("#b3261e", "#ff6b5e"),
            },
            {
                "brand": "Stencil black: primary button, shipping marks, cover blocks.",
                "accent": "Stamp red: the shipping stamp, status, one mark per view.",
            },
        ),
        families=fam(
            '"Stardos Stencil", ' + NOTO_SANS,
            NOTO_SANS,
            '"Courier Prime", ui-monospace, monospace',
        ),
        gfonts=GF
        + "Stardos+Stencil:wght@400;700&family=Courier+Prime:wght@400;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(d=(64, 68), dw=700, ls_d="0.01em"),
        radius=(0, 2, 4),
        bw=2,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=700,
            head_ls="0.02em",
            head_upper=True,
            label_upper=True,
            label_ls="0.08em",
            label_w=700,
            hero_size="60px",
            btn_border="ink",
            btn_font="label",
            btn_upper=True,
            card_border="ink",
            card_hover="transform: rotate(-0.5deg);",
            media_bg="brand-soft",
            media_ink="ink",
            logo_upper=True,
            nav_font="label",
            nav_upper=True,
            nav_current="color: var(--accent); text-decoration: none; border: 2px solid var(--accent); padding: 2px 8px;",
            em_extra="color: var(--accent);",
        ),
        extra_css="""
.sy-hero { position: relative; }
.sy-hero::after { content: "SHIPPED"; position: absolute; right: 32px; top: 32px; font-family: var(--font-label); font-weight: 700; font-size: 20px; letter-spacing: 0.1em; color: var(--accent); border: 3px solid var(--accent); padding: 4px 12px; transform: rotate(-8deg); }
.sy-card .sy-media { border-radius: 0; border: 2px dashed var(--ink-muted); }
.sy-tag { border: 1px solid var(--ink); }
.sy-timeline time::before { content: "#"; }
""",
        cover=dict(
            arrangement="slab",
            pattern="chevrons",
            blocks=["ink", "accent", "brand-soft", "line"],
            ptoken="bg",
            pitch=24,
            em=0.62,
            name_w=700,
            name_ls="0.02em",
            name_extra="text-transform: uppercase;",
            corner="none",
            why="'this way up' chevrons stencilled on the carton, the mark every shipped box carries",
        ),
        copy=dict(
            kicker="FROM: JASON LIN",
            hero="做好了就出貨，<em>不在倉庫裡放著</em>。",
            cta1="開箱看看",
            cta2="寄信給我",
        ),
        readme=R(
            "**牛皮紙箱** 用出貨箱的語言：牛皮紙底、黑色模板字、紅色「已出貨」章。它強調「交付」，每個作品都是一箱真的送出去的東西。",
            "你想強調交付與落地（已上線、已有人在用）；讀者是在意結果的主管與客戶。",
            [
                "短、實在：做了什麼、送給誰、何時上線。",
                "可以用出貨單格式：FROM、TO、#編號。",
                "不說「打造」「賦能」。",
            ],
            ["做好了就出貨，不在倉庫裡放著。", "#112 晨報系統 → 每天 07:30 送達。"],
            "牛皮紙 `bg` 加黑色 `brand`；`accent` 印章紅只給出貨章、狀態與一處強調。",
            "Stardos Stencil 模板字做英文標題（全大寫），中文落到 Noto Sans TC；標籤用 Courier Prime 打字機字。",
            "零圓角、2px 黑框；示意塊用虛線框像待貼標籤；Hero 右上角斜蓋一枚紅章。",
            "紙箱、標籤、膠帶、工作桌的實物照片；圖示用模板字風格。",
            ["Hero 右上角的 SHIPPED 紅章。", "虛線標籤框。", "#編號日期。"],
            ["不要做舊、髒污材質貼圖。", "不要一頁蓋兩個章。", "不要中文模板字。"],
        ),
    )
)

# ===================================================================== 22
STYLES.append(
    dict(
        id="22-porcelain",
        title="siyulio · 22 青花",
        namespace="SiyulioPorcelain",
        tagline="青花瓷的兩色：白釉底、鈷藍、細緻的襯線。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#f7f8fa", "#0e1424"),
                "surface": ("#ffffff", "#141c33"),
                "line": ("#d5dbe8", "#2a3557"),
                "ink": ("#14203f", "#e9edf6"),
                "ink-muted": ("#4c5674", "#a8b1c9"),
                "brand": ("#1f3d99", "#6f8fe6"),
                "brand-text": ("#1f3d99", "#a3b8f2"),
                "brand-soft": ("#e1e7f6", "#1c2850"),
                "on-brand": ("#ffffff", "#0e1424"),
                "accent": ("#8a6a2f", "#d1ad6a"),
                "accent-soft": ("#f1e8d4", "#33291a"),
                "on-accent": ("#ffffff", "#0e1424"),
                "focus": ("#1f3d99", "#a3b8f2"),
            },
            {
                "brand": "Cobalt: primary button, pattern, cover blocks. Everything else is glaze white.",
                "accent": "Old-gold rim: status and one small mark per view.",
            },
        ),
        families=fam(
            '"Cormorant Garamond", ' + NOTO_SERIF,
            NOTO_SANS,
            '"Cormorant Garamond", ' + NOTO_SERIF,
        ),
        gfonts=GF
        + "Cormorant+Garamond:ital,wght@0,500;0,700;1,500&family=Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500&display=swap",
        typegroups=scale(d=(64, 70), dw=700, ls_d="0", label=(14, 18), lw=700),
        radius=(2, 6, 999),
        bw=1,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=700,
            head_ls="0.01em",
            label_upper=True,
            label_ls="0.16em",
            label_w=700,
            hero_size="58px",
            hero_lh="1.15",
            em_style="normal",
            tag_radius="pill",
            btn_hover="background: var(--brand-soft); color: var(--ink);",
            media_bg="brand-soft",
            media_ink="brand-text",
            card_hover="border-color: var(--brand);",
        ),
        extra_css="""
.sy-btn { border-radius: 999px; }
.sy-btn-primary:hover { background: var(--brand); color: var(--on-brand); filter: brightness(1.1); }
.sy-card { border-radius: 12px; }
.sy-card .sy-media { border-radius: 8px; background-image: radial-gradient(circle at 50% 50%, transparent 0 22px, var(--brand) 22px 23px, transparent 23px 30px, var(--brand) 30px 31px, transparent 31px); background-size: 72px 72px; }
.sy-card .sy-media span { background: var(--brand-soft); padding: 0 10px; }
.sy-header { border-bottom: 1px solid var(--line); box-shadow: 0 3px 0 -2px var(--brand); }
""",
        cover=dict(
            arrangement="columns",
            pattern="discs",
            blocks=["brand", "ink", "line", "accent"],
            ptoken="surface",
            pitch=36,
            disc=10,
            em=0.5,
            name_w=700,
            name_ls="0.01em",
            corner="none",
            why="white glaze discs left in the cobalt column, the reserved dots of a blue-and-white bowl",
        ),
        copy=dict(
            kicker="JASON LIN · 林佳賢",
            hero="工具要像器皿：<em>天天用，才有溫度</em>。",
            cta1="看作品",
            cta2="聯絡我",
        ),
        readme=R(
            "**青花** 只用兩色：白釉與鈷藍，加一點舊金。細緻襯線與圓潤膠囊按鈕，安靜、有質感，偏東方但不刻意。",
            "你希望網站看起來沉穩、有品味、偏顧問或講師形象；讀者是重視質感與信任的決策者。",
            [
                "溫和、精準，不用驚嘆號。",
                "用器物、手作的比喻要克制，一頁最多一處。",
                "多寫「怎麼用」少寫「多厲害」。",
            ],
            [
                "工具要像器皿：天天用，才有溫度。",
                "這套報表系統，同事每天早上都會打開。",
            ],
            "白 `bg` 與鈷藍 `brand` 為主，`accent` 舊金只當小點綴；深色主題是夜藍釉。",
            "Cormorant Garamond 做英文標題與標籤（大寫、字距 0.16em），中文 Noto Serif TC；內文 Noto Sans TC。",
            "膠囊按鈕、12px 圓角卡片；示意塊是鈷藍同心圓紋；Header 下方一條細藍線。",
            "白底器物、手部工作照（不露臉）、淺色自然光。圖示 1px 細線。",
            ["同心圓紋示意塊。", "膠囊按鈕。", "大寫寬字距的英文標籤。"],
            ["不要龍紋、仿古圖騰。", "不要第三種主色。", "不要粗重陰影。"],
        ),
    )
)

# ===================================================================== 23
STYLES.append(
    dict(
        id="23-highway",
        title="siyulio · 23 公路指標",
        namespace="SiyulioHighway",
        tagline="高速公路綠牌：白字、箭頭、出口編號，告訴人往哪走。",
        themes=LIGHT_DARK,
        colors=colors(
            {
                "bg": ("#eef2ef", "#0c1a14"),
                "surface": ("#ffffff", "#13261d"),
                "line": ("#c6d3cb", "#2a4437"),
                "ink": ("#0f1f17", "#edf3ef"),
                "ink-muted": ("#45574d", "#a9bbb1"),
                "brand": ("#00693e", "#167a4c"),
                "brand-text": ("#00693e", "#7fd3a8"),
                "brand-soft": ("#d3e8dc", "#183828"),
                "on-brand": ("#ffffff", "#ffffff"),
                "accent": ("#ffcd00", "#ffd633"),
                "accent-soft": ("#fff2b8", "#3a3312"),
                "on-accent": ("#0f1f17", "#0c1a14"),
                "focus": ("#0f1f17", "#ffd633"),
            },
            {
                "brand": "Guide-sign green: primary button, sign panels, cover. White text with a white keyline.",
                "accent": "Exit-tab yellow: exit numbers, status, current page.",
            },
        ),
        families=fam(
            '"Overpass", ' + NOTO_SANS,
            '"Overpass", ' + NOTO_SANS,
            '"Overpass", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "Overpass:wght@400;600;800;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap",
        typegroups=scale(d=(62, 68), dw=800, ls_d="0", lw=800),
        radius=(4, 8, 12),
        bw=2,
        shadows=shadows("none", "none"),
        knobs=dict(
            head_w=800,
            head_ls="0",
            label_upper=True,
            label_ls="0.04em",
            label_w=800,
            hero_size="58px",
            hero_bg="brand",
            media_bg="brand",
            media_ink="on-brand",
            card_hover="border-color: var(--brand);",
            nav_current="color: var(--on-accent); background: var(--accent); padding: 2px 10px; border-radius: 4px;",
        ),
        extra_css="""
.sy-hero { margin: var(--space-4); border-radius: 12px; box-shadow: inset 0 0 0 4px var(--brand), inset 0 0 0 6px var(--on-brand); }
.sy-hero h1, .sy-hero p { color: var(--on-brand); }
.sy-hero .sy-kicker { color: var(--on-accent); background: var(--accent); justify-self: start; padding: 2px 10px; border-radius: 4px; font-weight: 800; }
.sy-hero h1 em { color: var(--accent); }
.sy-hero .sy-btn-primary { background: var(--on-brand); color: var(--brand-text); border-color: var(--on-brand); }
.sy-hero .sy-btn:not(.sy-btn-primary) { background: transparent; color: var(--on-brand); border-color: var(--on-brand); }
.sy-card .sy-media { box-shadow: inset 0 0 0 3px var(--brand), inset 0 0 0 5px var(--on-brand); }
.sy-card .sy-media span::before { content: "↑ "; }
.sy-timeline time { background: var(--accent); color: var(--on-accent); padding: 0 8px; border-radius: 4px; justify-self: start; height: 24px; font-weight: 800; }
""",
        cover=dict(
            arrangement="grid",
            pattern="chevrons",
            blocks=["brand", "accent", "line", "ink"],
            ptoken="on-brand",
            pitch=32,
            em=0.55,
            name_w=900,
            name_ls="0",
            corner="none",
            why="white arrow chevrons on the guide-sign green, pointing the way forward",
        ),
        copy=dict(
            kicker="出口 01 · Jason Lin",
            hero="不知道 AI 從哪裡開始？<em>我幫你指路</em>。",
            cta1="往作品集",
            cta2="聯絡我",
        ),
        readme=R(
            "**公路指標** 借用高速公路綠色指示牌：白字、白色內框、黃色出口編號、箭頭。它的任務是「告訴人往哪走」，適合把自己定位成導入顧問或引路人。",
            "你想幫別人起步（AI 導入顧問、內訓講師）；讀者是想導入 AI 但不知道從哪開始的人。",
            [
                "像指示牌：目的地＋方向＋距離。",
                "給選項不給長篇。",
                "動詞開頭：「往作品集」。",
            ],
            [
                "不知道 AI 從哪裡開始？我幫你指路。",
                "出口 03：自動化報表，約 2 週上路。",
            ],
            "`brand` 公路綠做 Hero 整塊與主要按鈕，字一律白；`accent` 出口黃只給編號、日期、目前頁。",
            "Overpass（以公路字體為原型）全站使用；中文 Noto Sans TC Black。",
            "Hero 是一面綠色指示牌（白色內框、圓角 12）；作品卡示意塊同樣是小綠牌；日期是黃色出口牌。",
            "道路、交流道、空拍路網；圖示用指示牌箭頭。",
            ["Hero 綠牌與白色內框。", "黃色出口編號。", "示意塊的向上箭頭。"],
            ["不要把整頁都塗綠。", "不要用紅色。", "不要細字與斜體。"],
        ),
    )
)

# ===================================================================== 24
STYLES.append(
    dict(
        id="24-chalkboard",
        title="siyulio · 24 黑板課",
        namespace="SiyulioChalk",
        tagline="教室黑板：墨綠板面、粉筆白、黃色粉筆重點。",
        themes=DARK_LIGHT,
        colors=dark_first(
            {
                "bg": ("#1f3a32", "#f4f3ee"),
                "surface": ("#264539", "#ffffff"),
                "line": ("#3e5f52", "#d8d6cc"),
                "ink": ("#f1f1e8", "#1d2a25"),
                "ink-muted": ("#bccbc2", "#4f5a55"),
                "brand": ("#f2d35b", "#1f3a32"),
                "brand-text": ("#f2d35b", "#1f5a46"),
                "brand-soft": ("#3a4d36", "#e6eee8"),
                "on-brand": ("#1f3a32", "#ffffff"),
                "accent": ("#f29ca3", "#b3364a"),
                "accent-soft": ("#4a3c3f", "#f6dde1"),
                "on-accent": ("#1f3a32", "#ffffff"),
                "focus": ("#f2d35b", "#b3364a"),
            },
            {
                "brand": "Yellow chalk: key points, primary button, underlines. On the light (whiteboard) theme it becomes board green.",
                "accent": "Pink chalk: status and the one 'remember this' mark.",
            },
        ),
        families=fam(
            '"LXGW WenKai TC", ' + NOTO_SANS,
            NOTO_SANS,
            '"LXGW WenKai TC", ' + NOTO_SANS,
        ),
        gfonts=GF
        + "LXGW+WenKai+TC:wght@400;700&family=Noto+Sans+TC:wght@400;500;700&display=swap",
        typegroups=scale(d=(60, 70), dw=700, ls_d="0", lw=400, label=(14, 20)),
        radius=(4, 8, 12),
        bw=1,
        shadows=shadows_df("none", "none"),
        knobs=dict(
            head_w=700,
            head_ls="0",
            label_upper=False,
            label_ls="0.02em",
            label_w=400,
            hero_size="58px",
            hero_lh="1.2",
            em_extra="text-decoration: underline wavy var(--brand); text-underline-offset: 10px; color: var(--ink);",
            media_bg="bg",
            media_ink="brand-text",
            card_hover="border-color: var(--brand);",
            nav_current="color: var(--brand-text); text-decoration: underline wavy; text-underline-offset: 6px;",
        ),
        extra_css="""
.sy-card .sy-media { border: 2px dashed var(--line); }
.sy-card .sy-media span { font-size: 44px; }
.sy-hero .sy-kicker { font-size: 18px; }
.sy-tag { font-family: var(--font-sans); }
.sy-timeline time { font-size: 18px; }
.sy-btn-primary { font-family: var(--font-display); font-size: 17px; }
""",
        cover=dict(
            arrangement="stagger",
            pattern="dots",
            blocks=["brand", "accent", "line", "ink"],
            ptoken="bg",
            pitch=20,
            dot=2,
            em=0.55,
            name_w=700,
            name_ls="0",
            corner="radius-md",
            why="chalk-dust dots tapped onto the yellow block, the marks a teacher leaves counting points",
        ),
        copy=dict(
            kicker="今天的課 · Jason Lin",
            hero="AI 其實沒那麼難，<em>我們一步一步來</em>。",
            cta1="看教材與作品",
            cta2="邀請我分享",
        ),
        readme=R(
            "**黑板課** 是教室的黑板：墨綠板面、粉筆白字、黃色粉筆畫重點、手寫感的楷體。它說的是「我會教你」，適合把內訓與分享放在網站前面的人。",
            "你常做內訓、分享、教同事用 AI；讀者是想學、想邀請講者的人。",
            [
                "像上課：先說今天學什麼，再一步一步。",
                "用「我們」。",
                "重點一頁一個，用黃色粉筆標。",
            ],
            ["AI 其實沒那麼難，我們一步一步來。", "今天的重點：讓報表自己跑出來。"],
            "深色黑板是主題；`brand` 黃粉筆做重點、按鈕、波浪底線；`accent` 粉紅粉筆只給狀態。淺色主題是白板，黃色換成板綠。",
            "LXGW WenKai TC（霞鶩文楷）做標題與標籤，像手寫板書；內文 Noto Sans TC 保持好讀。",
            "中等圓角；示意塊用虛線框像板上畫的格子；強調字用波浪底線。",
            "上課、白板、手繪流程圖照片；圖示用手繪感的粗線。",
            ["黃色波浪底線。", "楷體板書標題。", "虛線框示意塊。"],
            ["不要粉筆塵模糊貼圖。", "不要卡通學生插圖。", "不要整段都用楷體。"],
        ),
    )
)
