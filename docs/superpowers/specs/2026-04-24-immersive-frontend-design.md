# www.siyulio.com 沉浸式前端重設計

- **日期**：2026-04-24
- **版本**：v3（二次 `superpowers:code-reviewer` review 後再修：2 BLOCKER + 4 SERIOUS + 4 MINOR）
- **作者**：Jason Lin（與 Claude Opus 4.7 共同設計）
- **狀態**：Design approved，待寫實作 plan
- **目標專案**：`quartz/`（Quartz 4.5.2 + Preact SSR + markdown）
- **目標網址**：https://www.siyulio.com

---

## 0. 版本變動摘要

### v3（最新）— 修 v2 review 找出的 2 BLOCKER + 4 SERIOUS + 4 MINOR

- **§9.3 `loadGsap()` 補齊 race condition 防禦**：檢查 `window.gsap` AND `window.ScrollTrigger`、timeout 機制、prenav 中斷時 reset `loadPromise`、錯誤時允許 retry
- **§15 layout diff 改成真正可貼上的 TypeScript**（`page.fileData.frontmatter?.["hero-style"]` + `Component.` namespace + `(page) => boolean` signature）
- **§6.2 新增 navigation-generation token**（防止快速切頁的舊 async handler 在新頁疊加動畫）
- **§3.1 字體 preload 機制定案**：選 preload stylesheet (`as="style"`) 作為第一步，Phase 4 audit 再決定升級到 self-host woff2
- **§6.3 popover scroll 改用 MutationObserver**（不改 Quartz upstream `popover.inline.ts`，免去升級 Quartz 時 re-apply patch）
- **§16 新增 SCSS 清理小節**（`custom.scss` 的 ~167 行 `.home-landing__*` 規則 Phase 2 必須同步刪除/改名）
- **§9.6 移除「tree-shake Lenis」假設**，改誠實承認全量載入
- **§9.2 補上 Matter.js 移除帶來的 ~25KB gzipped bundle 縮小**（淨變動其實是 bundle 變小）
- **§5.3 寫明 TOC active class 規範**（`.active` on `<a>` matching intersecting `<section>` id）
- **§10 Phase 2 補上 commit 紀律建議**（Matter.js 移除 / HomeHeroApple / Lenis 各一個 commit，方便 bisect）

### v2（前一版）— 修 v1 review 的 4 BLOCKER + 9 SERIOUS + 3 MINOR

- **效能預算整條重寫**（v1 假設 per-route bundle split，Quartz 架構做不到 → 改為 hybrid 遞送：Lenis 走 Quartz pipeline、GSAP 走 static vendored asset + dynamic script tag injection）
- **文章頁 layout 補上明確的 `quartz.layout.ts` diff**（§15）
- **首頁改造補上舊區塊 → 新區塊對照表**（§16）
- **Pillars 砍掉 pin**（避免 scroll-jacking，只留 staggered reveal）
- **StickyTOC 拿掉新組件**（直接複用 `Component.TableOfContents` + sticky CSS）
- **a11y 大幅擴充**：focus-after-SPA、canvas `aria-hidden`、light mode accent 變體、對比度表、鍵盤導航
- **SPA 初始化順序明確寫死**（prenav → kill → nav → `document.fonts.ready` → init Lenis → init ScrollTrigger → `refresh()`）
- **Popover × ArticleHero 碰撞**補明方案（popover CSS 隱藏 hero 區塊）
- **Phase 1 不再加 Lenis**（避免默默破壞現有 popover/TOC/search），Lenis 延到 Phase 2 跟 Matter.js 移除一起做
- **時程改以 dev-days 標示**，另註明「2–3 小時/天 → 實際日曆時間 × 3」
- **hero-style 新增 `none` 選項**
- **OG image / RSS 影響補上評估**

---

## 1. 目標與動機

把 siyulio.com 的前端從「標準 Obsidian-Quartz 筆記站」升級為「Apple 產品頁風格的沉浸式內容站」，但**不改變 Obsidian markdown 寫作流程**，也不更換部署基礎設施。

- **風格錨點**：Apple 產品頁（iPhone / MacBook 類型），staged reveal，不做 scroll-jacking
- **範圍**：全站（首頁 / 3 個分類頁 / 所有文章頁 / 404 / about / tag 頁）
- **約束**：
  - 留在 Quartz 4（不遷移到 Next.js / Astro）
  - 部署不變（Cloudflare Workers + `wrangler.jsonc`）
  - Obsidian wikilinks / backlinks / graph / search / popover 全部維持 work
  - 不要求每篇文章手動配封面圖

---

## 2. 關鍵決策記錄

| 決策點 | 選擇 | 備選方案 |
|-------|------|---------|
| 風格參考 | Apple 產品頁（iPhone / MacBook 類型 → staged reveal） | Vision Pro 派 / Apple Newsroom 派 |
| 改造範圍 | C - 全站（含文章頁） | 僅首頁 / 首頁+分類頁 |
| 技術棧 | A - 留在 Quartz 4 擴充 | 改用 Next.js / Astro |
| 動畫庫 | A - GSAP + ScrollTrigger + Lenis | Motion One / 純 CSS+IntersectionObserver |
| GSAP 遞送方式 | **Vendored static asset + dynamic script injection**（v2 新增） | npm bundle / 3rd-party CDN |
| 文章頁封面策略 | B - Section-themed 動態視覺（可選 `cover:` override） | 每篇手配 / AI 生圖 / 純文字 hero |
| Hero 個性 | C - 首頁極簡、分類/文章頁保留個性物件 | 全站極簡 / 全站有物件 |

---

## 3. 設計語言（Design Tokens）

### 3.1 字體（延用現有）

- **Display**：Outfit
  - Hero：80–128px（依 viewport 彈性）
  - Section h2：48–64px
  - Eyebrow：14px 大寫 + letter-spacing 0.15em
- **Body**：Noto Sans TC
- **Code**：JetBrains Mono

**Font preload 機制（v3 定案）**：

v2 說要「preload 一個 woff2」但 Google Fonts woff2 URL 含 hash 版本號，硬寫會過期。v3 定案：**Phase 2 先做 stylesheet preload**（低風險、零維護），LCP 若未達標再 Phase 4 升級到 self-host woff2。

```html
<!-- 在 Head.tsx 自訂變體注入（Phase 2） -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style"
      href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&family=Noto+Sans+TC:wght@400;500&display=swap">
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;800&family=Noto+Sans+TC:wght@400;500&display=swap">
```

**兩階段策略**：
- **Phase 2 (stylesheet preload)**：URL 穩定、零維護、LCP 改善 ~200-400ms
- **Phase 4 audit 後若 LCP 仍 > 2.5s**：升級到 self-host woff2（下載 Outfit 700/800 + Noto Sans TC 400 的 woff2 放到 `static/vendor/fonts/`，改 `@font-face` 指向本地）— 多 ~150KB 靜態資源但 LCP 再減 200-500ms

### 3.2 色票

延用 `quartz.config.ts` 的暖金黑基底，**新增 section accent（有明暗兩套）**：

```
基礎（既有）
  dark mode:  light=#12100d → dark=#fff7ea
  light mode: light=#fff7ea → dark=#12100d

Section accents（v2 修正：新增明暗兩套）
                          Dark mode (暗底)       Light mode (亮底)
  manufacturing-ai        #c8a96b (8.45:1) ✓     #7a5a20 (6.82:1) ✓
  ai-notes                #7b8cc7 (5.80:1) ✓     #3a4d8a (7.45:1) ✓
  coffee                  #a47148 (4.55:1) ✓↑    #5c3a1c (8.10:1) ✓

所有值皆符合 WCAG AA 4.5:1（暗底 coffee 4.55:1 只比臨界值高 0.05 → 實作時
微調到 5:1 以上留緩衝）
```

**對比度實測**（vs 各自 base 色）：

| accent | dark mode 對比 | light mode 對比 | AA pass | AAA pass |
|-------|--------------|---------------|---------|---------|
| gold `#c8a96b` / `#7a5a20` | 8.45:1 | 6.82:1 | ✓ | ✓ 大字 |
| indigo `#7b8cc7` / `#3a4d8a` | 5.80:1 | 7.45:1 | ✓ | light ✓ |
| brown `#a47148` / `#5c3a1c` | 4.55:1* | 8.10:1 | marginal / ✓ | light ✓ |

*實作時將暗底 brown 微調到 ≥ 5:1。

### 3.3 留白 & 節奏

- **Hero 高度**：`100vh`（首頁）/ `75vh`（分類頁）/ `60vh`（文章頁）
- **Section 間距**：`160px`（desktop）/ `96px`（mobile）
- **文字最大寬**：`680px`（閱讀區）/ `1080px`（展示區）

### 3.4 Motion tokens

```scss
$motion-duration-fast:  0.4s;
$motion-duration-base:  0.6s;
$motion-duration-slow:  1.2s;
$motion-easing:         cubic-bezier(0.22, 1, 0.36, 1);  // Apple 標準
$motion-stagger:        80ms;
$motion-reveal-offset:  12%;
```

### 3.5 Motion 鐵律

1. 只動 `transform` + `opacity`，絕不動 `width/height/margin`（避免 reflow）
2. 單一動畫時長介於 0.4s–1.2s
3. Easing 一律使用 Apple 標準 `cubic-bezier(0.22, 1, 0.36, 1)`

---

## 4. 元件架構

### 4.1 三層結構

```
Layer 1｜Hero Components（SSR TSX）
├─ HomeHeroApple.tsx      首頁：純字 + 單一 focal animated visual
├─ CategoryHero.tsx        分類頁：保留個性物件 + scroll timeline
└─ ArticleHero.tsx         文章頁：section-themed 動態封面

Layer 2｜Motion Utilities（inline client scripts）
├─ lenis.inline.ts         Lenis smooth scroll（opt-in via body data attr）
├─ scrollReveal.inline.ts  IntersectionObserver reveal（全站輕量）
├─ heroCinematic.inline.ts GSAP ScrollTrigger 時間軸（動態 load GSAP）
├─ sectionCanvas.inline.ts Canvas 繪製（vanilla，無第三方依賴）
└─ gsapLoader.inline.ts    動態注入 `<script>` 載入 vendored GSAP + ScrollTrigger

Layer 3｜Support Components
├─ ScrollProgress.tsx      文章頁頂部細線進度條（vanilla JS，<1KB）
└─ SectionBadge.tsx        section 歸屬小標

複用現有（v2 修正：不新增 StickyTOC）
└─ Component.TableOfContents  加到 defaultContentPageLayout.right
                              + 新 SCSS `position: sticky` + 當前段落高亮
```

### 4.2 資料流（無侵入擴充）

**所有新 frontmatter 欄位全部可選，不補也會自動 fallback**。

| 欄位 | 用途 | 預設行為 |
|-----|------|---------|
| `cover:` | 手動指定封面圖（URL 或相對路徑） | 無 → 走 section-themed 動態封面 |
| `accent:` | 手動指定主題色 hex | 無 → 按 slug prefix 推斷 section |
| `hero-style:` | `none` / `minimal` / `themed` / `cinematic` | 依頁面類型自動推斷（詳見 §4.3） |

### 4.3 `hero-style` 自動推斷規則（v2 明確化）

```
slug === "index"                     → cinematic（首頁）
slug 屬於分類首頁（xxx/index）        → cinematic（分類頁）
slug 為一般文章                       → themed（section-themed 動態封面）
slug 屬於 tags/*                     → minimal（精簡 hero）
frontmatter `hero-style: none`       → 完全不渲染 hero
```

**`hero-style: none`**：對短篇、about 子頁有用，整個 hero 區塊不出現。

### 4.4 `sectionThemes.ts` 擴充

```ts
motionConfig: {
  canvasRenderer: 'geometric-lines' | 'particle-flow' | 'steam-curves',
  objectSet: string[],
  glowColor: string,        // dark mode
  glowColorLight: string,   // light mode (v2 新增)
  particleDensity: number,
}
```

---

## 5. 各頁版型

### 5.1 首頁 `/`（純 Apple 極簡，**無 pin**）

**v2 修正**：原本 Three Pillars 是「各 100vh scroll-pinned」→ 改為「各 100vh 但不 pin，靠 staggered reveal 進場」。原因：pin 三個 section 需要使用者滾 ~300vh 才能過完這個區塊，在 blog landing 上會變成實質 scroll-jacking。

```
[SiteHeaderNav]
[Hero 100vh]
  eyebrow: JASON LIN / AI FIELD NOTES
  h1 (128px): 把企業裡真的用得上的 AI，整理成可以開始的做法。
  focal visual: 單一 canvas（暖金漸層光暈 + 緩動粒子，隨 scroll 呼吸）
  [ 先看製造業 AI → ] [ 再看 AI 新知 → ]

[Stats Strip ~60vh]
  count-up 動畫：已發布 N 篇 / 主軸內容 / 最近更新

[Three Pillars 各 100vh, 「staggered reveal」不 pin]
  製造業 AI / AI 新知 / 手沖咖啡
  進場：卡片從 scale(0.94) opacity(0) → 1.0 opacity(1)，stagger 80ms
  scroll 自然通過，不卡住

[Featured Articles]
  第一篇：大卡片橫跨兩欄，圖片 scale(1.1 → 1.0) 進場
  其他三篇：stagger 淡入

[Recent Updates list]
[Footer]
```

**LCP 候選**：H1 的 128px 大字（text-based LCP）。需搭配 §3.1 的字體 preload。

### 5.2 分類頁 `/manufacturing-ai/` `/ai-notes/` `/coffee/`

```
[SiteHeaderNav]
[Breadcrumbs]
[CategoryHero 75vh]
  eyebrow: SECTION / MANUFACTURING AI
  h1 (96px): 製造業 AI 筆記
  description
  scene (3-5 物件, scroll-driven timeline 不 pin):
    0-30%:   物件飄入
    30-70%:  物件重新編隊
    70-100%: 物件散開淡出

[Article Grid 2-col]
  stagger 80ms 淡入

[Related Sections]
[Footer]
```

**v2 說明**：`CategoryHero` 會**取代**現有 `defaultListPageLayout` 的 `BrandIntro` + `ArticleTitle`（見 §15）。

**LCP 候選**：CategoryHero 的 H1。

**Section 專屬物件組**：

- `manufacturing-ai`：齒輪 / 流程圖 / 報表
- `ai-notes`：終端機 / 鍵盤 / 書籤
- `coffee`：咖啡豆 / 濾杯 / 蒸氣

### 5.3 文章頁（所有 `.md`）

```
[ScrollProgress 1px top bar]
[SiteHeaderNav]
[Breadcrumbs]
[ArticleHero 60vh] (v2 明確：完整取代 ArticleTitle + ContentMeta)
  漸層背景（section accent）
  Canvas 圖案：
    manufacturing-ai → 等距幾何線條
    ai-notes        → 粒子流
    coffee          → 漸層光斑 + 蒸氣曲線
  右下角覆文字：
    [SectionBadge]
    h1 (72px)
    meta: date · N min read

[3-col layout via quartz.layout.ts]
  left: []  (保留空白側欄，手機隱藏)
  center: 內文 680px max，段落 IntersectionObserver 淡入
  right: [
    DesktopOnly(
      TableOfContents (既有組件，加 sticky CSS + active section 高亮)
    )
  ]

[TagList]
[RecentNotes「繼續閱讀」]
[Footer]
```

**v2 關鍵修正**：

1. **不新增 StickyTOC** — 直接在 `quartz.layout.ts` 把 `Component.TableOfContents()` 放進 `right: []`，加新 SCSS 讓它 `position: sticky; top: 120px` + 當前段落高亮。**Active class 規範**（v3 明確）：延伸既有 `toc.inline.ts` 的 IntersectionObserver，當某個 `<section>` 進入 viewport 時，對對應的 `.toc-content a[data-for="{sectionId}"]` 加上 `.active` class（移除其他 `.active`）。CSS 側用 `.toc-content a.active { color: var(--section-accent); font-weight: 600; }`。
2. **LCP 候選**：ArticleHero 的 H1。Canvas 為 `aria-hidden="true"` + `role="presentation"`（見 §8）。
3. **Popover 行為**：彈出的預覽需**隱藏 ArticleHero**（見 §6.3）。

### 5.4 其他頁

- **`/about/`**：當特殊文章頁，可設 `hero-style: minimal` 或 `cover:` 放 portrait
- **404**：Apple 風錯誤頁（大字「404」+ 淡光暈 + 回首頁按鈕）
- **`/tags/xxx/`**：`hero-style: minimal`（精簡 hero，無物件）

---

## 6. Quartz SPA 整合（v2 大幅擴充）

### 6.1 SPA 事件 API（已驗證）

- `nav` event：每次 SPA 導航**後**觸發（初次載入也會，見 `spa.inline.ts:129, 191`）
- `prenav` event：SPA 導航**前**觸發（`spa.inline.ts:81`）
- `window.addCleanup(fn)`：註冊清理函式（`spa.inline.ts:38-44`）

### 6.2 初始化順序（v3 加入 navigation-generation token）

**v3 問題**：v2 寫的 `async` nav handler 有 race — 快速切頁時舊 handler 的 `await document.fonts.ready` 回來時會在**新頁** DOM 上繼續裝 Lenis/ScrollTrigger，造成疊加或錯置。

**v3 修法**：加 `navGeneration` token，每個 async step 後檢查 token 是否還是自己當初 capture 的版本；若已被新 nav 取代則 abort。

```ts
// 模組層級狀態（由 Quartz inline-script IIFE 包住，全站共用一份）
let navGeneration = 0
let lenisInstance: any = null
let rafId = 0
let observers: IntersectionObserver[] = []

document.addEventListener('prenav', () => {
  // 1. 版本號 +1：所有正在跑的舊 handler 都會在下一次 check 時 abort
  navGeneration++
  // 2. 砍掉所有 animation instance
  const gsap = (window as any).gsap
  gsap?.ScrollTrigger?.getAll?.().forEach((t: any) => t.kill())
  lenisInstance?.destroy()
  lenisInstance = null
  observers.forEach(o => o.disconnect())
  observers = []
  cancelAnimationFrame(rafId)
})

document.addEventListener('nav', async () => {
  const myGen = navGeneration  // 在進 async 之前 capture

  // 3. 等字體載好（避免 ScrollTrigger 讀到錯誤 layout 高度）
  await document.fonts.ready
  if (myGen !== navGeneration) return  // 舊 handler，abort

  // 4. 初始化順序：Lenis → GSAP → ScrollTrigger refresh
  if (bodyOptsIn('lenis') && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    setupLenis()
  }
  if (myGen !== navGeneration) return

  if (needsGsap()) {
    await loadGsap()
    if (myGen !== navGeneration) return
    setupScrollTriggers()
    ;(window as any).gsap.ScrollTrigger.refresh()
  }

  setupRevealObservers()
  setupCanvasScene()

  // 5. SPA 導航後 focus 管理（a11y）
  focusFirstHeading()
})
```

**token 檢查點的位置原則**：每個 `await` 之後、以及每個「會產生 side effect」的 setup 之前都要檢查一次。這避免：
- 舊頁還在載 GSAP 時使用者切到新頁 → 舊 handler 的 `await loadGsap()` 回來時不會再 `setupScrollTriggers()` 裝到新頁 DOM 上
- 字體載好時使用者已經切頁 → 舊 handler 的 `setupLenis()` 不會執行

### 6.3 Popover × ArticleHero 碰撞（v3 改用 MutationObserver，不動 upstream）

現有 `enablePopovers: true` 會抓目標頁 HTML 塞進 popover 裡。如果 ArticleHero 60vh 在最上面，popover 預覽會**只秀到 hero，不秀內文** → 很大的 UX 退步。

**v3 修法**：兩層 — CSS 隱藏 hero + **新 inline script** 用 MutationObserver 觀察 popover 出現，滾到第一個有意義的內容。**不改** upstream `quartz/components/scripts/popover.inline.ts`（避免未來 Quartz 升級要 re-apply patch）。

**CSS（`quartz/styles/_popover-immersive.scss`，Phase 1 就位，Phase 3 才生效）**：

```scss
.popover-inner {
  .article-hero,
  .scroll-progress,
  .breadcrumbs {
    display: none;  // popover 預覽只秀文章內容
  }
  // 去掉 beforeBody 後的頂端留白
  > :first-child {
    margin-top: 0;
    padding-top: 0;
  }
}
```

**新 inline script（`popoverScroll.inline.ts`）**：

```ts
// 不改 upstream popover.inline.ts，用 MutationObserver 觀察 popover 出現
let mo: MutationObserver | null = null

function setupPopoverScroll() {
  mo?.disconnect()
  mo = new MutationObserver((mutations) => {
    for (const m of mutations) {
      for (const node of Array.from(m.addedNodes)) {
        if (node instanceof HTMLElement && node.classList.contains('popover-inner')) {
          // popover DOM 剛插入，下一 frame 再 scroll（等 layout 完成）
          requestAnimationFrame(() => {
            const firstContent = node.querySelector('p, h2, h3, pre, ul, ol') as HTMLElement
            if (firstContent) {
              const offset = firstContent.offsetTop - 20
              if (offset > 0) node.scrollTop = offset
            }
          })
        }
      }
    }
  })
  mo.observe(document.body, { childList: true, subtree: true })
}

document.addEventListener('nav', setupPopoverScroll)
window.addEventListener('beforeunload', () => mo?.disconnect())
```

**為何用 MutationObserver 而不直接改 popover.inline.ts**：
- Quartz 是 npm / fork 管理，upstream 檔改動等於維護 patch
- MutationObserver 成本極低（只在 `<body>` 觀察 childList）
- 未來 popover HTML 結構若改，只要 `.popover-inner` class 還在就能工作

### 6.4 SPA 導航後 focus 管理（v2 新增）

`spa.inline.ts` 目前只做 scroll + title 廣播，不管 focus。新設計加 reveal 動畫後，tab 使用者可能卡在一個還沒動畫完的區塊。

**解法**：`nav` event 結尾呼叫：

```ts
function focusFirstHeading() {
  const h1 = document.querySelector('main h1, article h1') as HTMLElement
  if (h1) {
    h1.setAttribute('tabindex', '-1')
    h1.focus({ preventScroll: true })
  }
}
```

### 6.5 Search Modal × Lenis（v2 新增）

Search modal 開啟時需暫停 Lenis（避免 modal 底下內容繼續 smooth scroll）：

```ts
// 擴充 search.inline.ts 開啟 modal 時
window.lenis?.stop()
// 關閉時
window.lenis?.start()
```

---

## 7. Canvas 動態視覺策略

每個 section 的 canvas hero：

- `requestAnimationFrame` 驅動
- 畫面尺寸 = viewport × `devicePixelRatio`
- 隱藏 tab 時暫停（`visibilitychange` listener）
- **FPS 降級**（v2 修正）：維護一個 30-frame 滾動平均 `performance.now()` 差，若平均 > 22ms（約 45 FPS）則自動切到 `setTimeout` 30 FPS 模式。單一 frame spike 不觸發降級（避免 GC 誤判）。
- 卸載時必呼叫 `cancelAnimationFrame`
- 每個 section 視覺 < 100 lines canvas code，**不用 Three.js / WebGL**
- **`aria-hidden="true"` + `role="presentation"`**（§8）

---

## 8. 無障礙與降級（v2 大幅擴充）

### 8.1 `prefers-reduced-motion`

```js
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Lenis 不啟動（恢復原生 scroll）
  // GSAP scrub 改即時切換（不做平滑）
  // Canvas hero 只畫第一幀，不啟動 rAF
  // Reveal 改為直接 opacity: 1，取消 translateY
  // 保留：0.2s 極短淡入
}
```

### 8.2 手機版（< 768px）

```
停用：
  - Lenis
  - ScrollTrigger 所有 pin（已在 §5 改為全站無 pin，此條冗餘但保留）
  - Sticky TOC（右欄整個隱藏）
減半：
  - Hero canvas 解析度
  - Stats count-up（直接顯示最終值）
保留：
  - Section-themed hero 封面（靜態第一幀）
  - 段落 reveal
  - ScrollProgress 進度條
```

### 8.3 Canvas / 圖形元素（v2 新增）

- **所有 canvas hero**：必加 `aria-hidden="true"` + `role="presentation"`
- **裝飾性 SVG / 物件**（CategoryHero 的飄浮物件）：同上
- **Section themed gradient 背景**：純 CSS，天然不被 screen reader 讀到，不需特別處理

### 8.4 SPA 導航後 focus 管理（見 §6.4）

### 8.5 鍵盤導航

- **Sticky TOC**：沿用既有 `Component.TableOfContents` 的 `<a href="#">` 結構，天然可 tab
- **ScrollProgress**：純裝飾，`aria-hidden="true"`
- **Hero 按鈕**：保留既有 `<a>` 結構，不用 `<div onclick>`
- **Pillars 卡片**：整張卡片是 `<a>`，可 tab，focus ring 自訂但不移除

### 8.6 `prefers-contrast` / `forced-colors`

- **`@media (prefers-contrast: more)`**：移除半透明玻璃效果、glow 光暈亮度 × 2
- **`@media (forced-colors: active)`**：Canvas hero 完全隱藏（`forced-color-adjust: none` 會讓 canvas 糊掉）

### 8.7 色票對比度（見 §3.2）

三個 section accent 在明暗雙模式皆符合 WCAG AA。暗底 brown 微調到 ≥ 5:1。

### 8.8 瀏覽器支援

- **完整體驗**：Chrome / Edge / Firefox / Safari 最新兩版
- **降級體驗**：舊版瀏覽器 → 無 GSAP 不啟動動畫（`if (!window.gsap) return`）+ IntersectionObserver 失敗時元素直接顯示（feature detection）
- **拒絕支援**：IE 11

---

## 9. 效能預算（v2 重寫，符合 Quartz 單 bundle 架構現實）

### 9.1 Quartz 打包架構（reviewer 驗證）

- Quartz 將**所有** `*.inline.ts` bundle 成單一個 `postscript.js`，**全站共用、無 per-route split**
- 無法做 "文章頁 bundle < 20KB / 首頁 < 100KB" 的切割（v1 錯誤假設已移除）
- 唯一能做 per-page 遞送差異的機制：**動態注入 `<script>` tag**（本 spec 採用）

### 9.2 遞送策略（v2 重寫）

| 資源 | 遞送方式 | 每頁載入？ | 大小（gzipped） |
|-----|---------|----------|---------------|
| Lenis（smooth scroll） | npm → Quartz inline bundle | 全站（但 opt-in 啟動） | ~5 KB |
| ScrollReveal observer | inline bundle | 全站 | ~1 KB |
| Canvas renderers | inline bundle | 全站（runtime 只跑當頁需要的） | ~3 KB |
| ScrollProgress | inline bundle | 全站 | ~0.5 KB |
| **GSAP core** | **static/vendor/gsap.min.js** | **只在 hero-style=cinematic 頁面**（首頁/分類頁） | **~32 KB** |
| **ScrollTrigger** | **static/vendor/ScrollTrigger.min.js** | **同上** | **~14 KB** |

**總 `postscript.js` 增量預估**：`~5 + 1 + 3 + 0.5 = ~10 KB gzipped` 加在現有 `postscript.js` 上，全站頁面都載這份。

**首頁 + 分類頁額外**：`gsap.min.js` (32KB) + `ScrollTrigger.min.js` (14KB) = 46KB，透過 `<script>` 動態注入，瀏覽器快取（Cloudflare Workers 預設快取 1 年）。

**文章頁**：只付 `postscript.js` 增量（~10KB），**不載 GSAP**。

### 9.3 GSAP 動態載入實作（v3 補齊 race condition 防禦）

**v2 兩個 race bug**：
1. `window.gsap` 存在但 `window.ScrollTrigger` 還沒存在時（`s1.onload` 設完但 `s2.onload` 未完），下一頁早 return → `ReferenceError`
2. prenav 中斷時 `<script>` 被移除 → `onload` 永遠不 fire → `loadPromise` 永遠 pending → 下次 await 直接 hang

**v3 修法**：雙 global 檢查 + prenav reset + 10 秒 timeout + 錯誤允許 retry。

```ts
// quartz/components/scripts/gsapLoader.inline.ts
let loadPromise: Promise<void> | null = null

function bothLoaded(): boolean {
  const w = window as any
  return !!(w.gsap && w.ScrollTrigger)
}

export function loadGsap(): Promise<void> {
  // (1) 雙檢查：gsap AND ScrollTrigger 都要在
  if (bothLoaded()) return Promise.resolve()
  if (loadPromise) return loadPromise

  loadPromise = new Promise<void>((resolve, reject) => {
    // (2) 10 秒 timeout — 避免 script 被中途移除造成永遠 hang
    const timeoutId = window.setTimeout(() => {
      loadPromise = null  // 允許下次 call 重試
      reject(new Error('GSAP load timeout (10s)'))
    }, 10000)

    const loadScript = (src: string) =>
      new Promise<void>((res, rej) => {
        const s = document.createElement('script')
        s.src = src
        s.onload = () => res()
        s.onerror = () => rej(new Error(`Failed to load ${src}`))
        document.head.appendChild(s)
      })

    loadScript('/static/vendor/gsap.min.js')
      .then(() => loadScript('/static/vendor/ScrollTrigger.min.js'))
      .then(() => {
        clearTimeout(timeoutId)
        const w = window as any
        w.gsap.registerPlugin(w.ScrollTrigger)
        resolve()
      })
      .catch((err) => {
        clearTimeout(timeoutId)
        loadPromise = null  // (3) 錯誤時 reset，允許下次 retry
        reject(err)
      })
  })

  return loadPromise
}

// (4) prenav 中斷時：若 gsap 或 ScrollTrigger 還不齊，reset loader
document.addEventListener('prenav', () => {
  if (!bothLoaded()) {
    loadPromise = null
  }
})
```

**`HomeHeroApple` / `CategoryHero` 的 `afterDOMLoaded` 呼叫（搭配 §6.2 的 nav-gen token）**：

```ts
document.addEventListener('nav', async () => {
  if (!document.querySelector('[data-hero-cinematic]')) return
  const myGen = navGeneration  // 見 §6.2
  try {
    await loadGsap()
    if (myGen !== navGeneration) return  // 舊 handler，abort
    await document.fonts.ready
    if (myGen !== navGeneration) return
    initTimeline()
  } catch (err) {
    console.warn('GSAP load failed, hero degraded to static', err)
    // 降級路徑：hero 保持第一幀，文字仍可讀
  }
})
```

**總防禦層級**：
- Promise-level：timeout 10s → reject
- Error 處理：reject 後 reset loader，下次 call 能 retry
- 狀態檢查：每次 early-return 要 AND 檢查兩個 global
- Race 防禦：prenav 中斷時主動 reset
- 降級路徑：catch 錯誤不讓頁面白屏，hero 退為靜態

### 9.4 Vendored asset 準備

從 `https://github.com/greensock/GSAP/releases` 下載 GSAP 3.12.x 的 `gsap.min.js` + `ScrollTrigger.min.js`，放到：

```
quartz/static/vendor/gsap.min.js          (~32KB gzipped)
quartz/static/vendor/ScrollTrigger.min.js (~14KB gzipped)
quartz/static/vendor/LICENSE-GSAP         (標準 MIT for tools / Webflow license notice)
```

**授權確認**：2024-11 GreenSock 被 Webflow 收購後，GSAP 全系列（含 ScrollTrigger）對商業用途免費，本站自用符合授權。

### 9.5 LCP 策略

- **LCP 候選**：
  - 首頁：`<h1>` 128px 大字
  - 分類頁：CategoryHero `<h1>` 96px
  - 文章頁：ArticleHero `<h1>` 72px
- **字體 preload**（v3 定案）：preload Google Fonts **stylesheet**（`as="style"`），詳見 §3.1。Phase 4 audit LCP 若仍未達標再升級到 self-host woff2
- **Canvas 延後 init 機制**：
  ```ts
  if ('PerformanceObserver' in window) {
    new PerformanceObserver((list) => {
      if (list.getEntries().some(e => e.entryType === 'largest-contentful-paint')) {
        initCanvasScene()
      }
    }).observe({ type: 'largest-contentful-paint', buffered: true })
  } else {
    setTimeout(initCanvasScene, 350)  // 保底 fallback
  }
  ```

### 9.6 目標指標

| 指標 | 目標 | 手段 |
|-----|------|------|
| LCP（所有頁） | < 2.5s | 字體 preload、canvas 延後到 LCP 後 |
| INP | < 200ms | GSAP 動態載入、canvas rAF 節流 |
| CLS | < 0.1 | Hero 高度用 `min-height` 預佔 |
| `postscript.js` 增量 | ≤ 15 KB gzipped | 只 import 會用的 Lenis API（不期望 tree-shake） |
| `postscript.js` **淨變動**（v3 新增） | **-10 KB**（縮小） | 移除 Matter.js ~25KB − 新增 ~15KB |
| 首次載入 cinematic 頁（含 GSAP） | 額外 ≤ 50 KB gzipped | vendored + CDN edge cache |
| Canvas 平均 FPS | ≥ 45（30-frame avg） | rolling avg 降級 |
| Lighthouse Performance | ≥ 90（首頁）/ ≥ 95（文章頁） | 上面所有手段合計 |
| Lighthouse Accessibility | ≥ 95 | §8 全部做好 |

---

## 10. 實作階段（Milestones）v2 重劃

**v2 修正**：
- 單位改為 **dev-day**（一個完整工作天 ≈ 6 小時有效時間）
- 「每天 2–3 小時」要把 dev-day × ~3 算日曆時間
- Phase 1 **不加 Lenis**（避免默默破壞 popover / TOC / search），改做純基礎建設
- Lenis 延到 Phase 2，跟 Matter.js 移除一起做，避免互相打架

### Phase 1｜地基：非侵入式基礎建設（~4 dev-days → 2 週日曆）

**交付**：
- `scripts/scrollReveal.inline.ts`（IntersectionObserver utility）
- `scripts/gsapLoader.inline.ts`（動態 load GSAP，不自動執行）
- `sectionThemes.ts` 擴充 `motionConfig`（含 light mode glow 色）
- `styles/_motion-tokens.scss`
- `styles/_popover-immersive.scss`（popover hide article-hero）
- SPA `prenav`/`nav` hook 骨架（含 `navGeneration` token + `document.fonts.ready` + focus management，尚未掛任何動畫，見 §6.2）
- `prefers-reduced-motion` + mobile feature detection 工具函式
- Light mode accent 色 token 加入
- `static/vendor/gsap.min.js` + `ScrollTrigger.min.js` 放到 repo（檔案就位，還沒用）

**驗收**：
- 現有頁面**零 regression**（popover、TOC、search、Matter.js hero 全部照舊）
- 加 `data-reveal` 屬性的元素會淡入
- Build 無 warning
- Lighthouse 數字不退

**可上線嗎？** 是，完全非侵入。

### Phase 2｜首頁改造 + Lenis 導入（~7 dev-days → 3.5 週日曆）

**v3 commit 紀律建議**：Phase 2 同時動三件事（Matter.js 移除 / HomeHeroApple / Lenis 導入），若出 bug 不方便 bisect。建議**拆成 4–5 個 commit**，每個都能跑：

1. `feat: 新增 HomeHeroApple 組件骨架，feature flag 關`（Matter.js 還在）
2. `feat: 新增 focal canvas + sectionCanvas 繪製器，feature flag 關`
3. `feat: HomeLanding 按 §16 對照表重寫（含 SCSS 遷移）`（Matter.js 這時砍）
4. `feat: 加入 Lenis smooth scroll + 配 §6.5 search stop/start 介面`
5. `feat: GSAP 動態載入 + heroCinematic 時間軸 + Head.tsx 字體 preload`

每個 commit 完都能 `npm run build` 成功、基本功能正常。出 bug 可 `git bisect`。

**交付**：
- **砍掉 Matter.js hero**（現有 `heroScene.inline.ts` 的 7 個飄浮物件）
- `HomeHeroApple.tsx`（純字 + 單一 focal canvas）
- `scripts/heroCinematic.inline.ts`（GSAP timeline，動態 load GSAP）
- `scripts/sectionCanvas.inline.ts`（canvas 繪製，vanilla）
- `HomeLanding.tsx` 按 §16 對照表重寫（含 SCSS 遷移 §16.2）
- Pillars section 靠 IntersectionObserver staggered reveal（無 pin）
- Stats count-up
- Lenis 首次啟動（搭配 Matter.js 移除，沒有互相打架風險）
- 自訂 `Head.tsx` 變體加字體 stylesheet preload（§3.1）
- `styles/_home-apple.scss` + `custom.scss` 清理 (§16.2)

**驗收**：
- 首頁 LCP < 2.5s
- 首頁新增載入（含 GSAP）≤ 50 KB gzipped
- 手機版降級正常（canvas 解析度減半、無 GSAP）
- Reduced motion 測試通過
- Lenis 沒破壞 popover / TOC / search / SPA nav（依 §6 整合）
- Lighthouse Performance ≥ 90
- Popover 預覽在首頁連結上秀內文（§6.3 CSS 生效）

**可上線嗎？** 是，首頁獨立完工。

### Phase 3｜分類頁 + 文章頁 hero（~5 dev-days → 2.5 週日曆）

**交付**：
- `CategoryHero.tsx`（scroll-driven timeline，複用 GSAP loader）
- `ArticleHero.tsx`（section-themed canvas 封面）
- 3 組 section 專屬 canvas 視覺（齒輪/粒子/蒸氣）
- `quartz.layout.ts` 按 §15 改 layout
- `cover:` / `accent:` / `hero-style:` frontmatter 支援
- `hero-style: none` 行為
- `styles/toc.scss` 擴充（`position: sticky` + active section 高亮 + §5.3 的 `.toc-content a.active` 規則）
- Sticky TOC 在 `right: []` 就位
- Popover 預覽 CSS rule 生效（§6.3 的 `_popover-immersive.scss`）
- **新 `scripts/popoverScroll.inline.ts`**（§6.3，MutationObserver scroll 到第一個內容元素）

**驗收**：
- 每個分類頁獨立個性
- 所有文章頁都有 hero（零 frontmatter 工作量）
- Wikilinks / backlinks / search / popover / graph 全部仍 work
- `hero-style: none` 測試：某篇文章設 `none` 後 hero 消失
- Popover 預覽在文章連結上秀內文（不秀 hero）
- 手機版右欄 TOC 隱藏

**可上線嗎？** 是，全站視覺一致。

### Phase 4｜文章頁細節 + 全站拋光（~4 dev-days → 2 週日曆）

**交付**：
- `ScrollProgress.tsx`
- 段落 reveal（IntersectionObserver 輕量版）
- 404 頁重做
- About 頁 portrait 支援
- SPA focus management 上線（見 §6.4）
- Search × Lenis 整合（§6.5）
- OG image：**暫不啟用**，但留下介面讓未來可用新 hero 當素材（§12）
- Lighthouse / axe-core / WebPageTest audit
- Cross-browser 測試（Chrome/Edge/Firefox/Safari + iOS Safari + Android Chrome）
- `prefers-contrast` / `forced-colors` 測試

**驗收**：
- Lighthouse Performance ≥ 90 (首頁) / ≥ 95 (文章頁)
- Lighthouse Accessibility ≥ 95
- 全站零 console error、無 SPA 動畫疊加 / 消失
- 鍵盤導航流暢（tab 順序正確、focus ring 可見）
- iOS Safari 上 Lenis 沒有慣性爆衝

**可上線嗎？** 是，完成態。

### 總時程

- **Dev-days**：4 + 7 + 5 + 4 = **20 dev-days**
- **每天 2–3 小時**：**~10 週日曆（2.5 個月）**
- **全職**：4 週
- **Phase 1 + Phase 2（最有感改動）先上線**：~5.5 週日曆

---

## 11. 風險與緩解（v2 擴充）

| 風險 | 可能性 | 衝擊 | 緩解 |
|-----|-------|------|------|
| Quartz SPA 導航導致動畫疊加 / 消失 | 中 | 高 | §6.2 的 `prenav`/`nav` 順序寫死；Phase 1 做 debug demo 頁驗證 |
| GSAP vendored asset 大小超預期 | 低 | 中 | 下載後秤重；不行改用更輕的子集 `@gsap/shockingly` → `@gsap/basic` |
| Popover 預覽秀錯內容（秀到 hero） | 高（v1 漏網） | 高 | §6.3 CSS 隱藏 + Phase 3 實測 |
| Lenis 破壞 iOS Safari 慣性 | 中 | 中 | 手機版停用 Lenis（§8.2） |
| Lenis 破壞 popover / search modal | 中 | 高 | §6.5 stop/start 介面；Phase 2 導入時逐項驗證 |
| SPA nav 後 ScrollTrigger 讀到錯誤 layout 高度（字體未載入） | 中 | 中 | §6.2 `await document.fonts.ready` 明確寫死 |
| Canvas 視覺在低階手機掉幀 | 中 | 中 | Rolling-avg FPS 降級（§7）+ 手機直接靜態 |
| 砍 Matter.js hero 後使用者覺得失去個性 | 中 | 低 | 物件保留在分類頁；不好看可還原 |
| 暖金主色 + 新 section accent 打架 | 中 | 中 | Phase 1 先出色票小樣 |
| 明亮模式 accent 對比度失敗 | 低（v2 已實測） | 中 | §3.2 已列明暗兩套，WCAG AA 驗證通過 |
| GSAP ESM tree-shake 假設錯誤 | — | — | **v2 已放棄**，改用 vendored static asset |
| Per-route bundle split 假設錯誤 | — | — | **v2 已放棄**，改用動態 `<script>` 注入 |
| 文章頁 Sticky TOC 在手機壞 | 低 | 低 | `DesktopOnly` wrapper 直接隱藏 |
| SPA 導航後 tab focus 卡在舊位置 | 中 | 中 | §6.4 `focusFirstHeading()` |

---

## 12. 暫緩 / 已知問題（v2 擴充）

- **死 wikilink**：已於 commit `66bb0a7` 清理 6 條（3 個 `../prompts/` + 1 `../work-notes/` + 1 `../obsidian-notes/` + 1 目標不存在）。
- **Sitemap / RSS**：現有 `Plugin.ContentIndex` 繼續用，本次不動。但 RSS 讀 `description` 欄位，新 ArticleHero 不影響（RSS 本來就不含 hero HTML）。若要讓 RSS 讀者看到更多上下文，可在 Phase 3 後鼓勵作者寫 frontmatter `description`。
- **Comments / 評論系統**：非本次範圍。
- **OG image**：本次暫不啟用 `Plugin.CustomOgImages`，但新 ArticleHero canvas 正好是未來重啟 OG 時的理想素材源（SSR canvas → PNG 可用 `@vercel/og` 或 `satori`）。設計層預留此可能。

---

## 13. 實作時仍待敲定的小決策

1. **Stats strip 三個數字**：現「文章數 / 主軸 / 最近更新」，Phase 2 可能改
2. **首頁 focal visual 具體視覺**：Phase 2 出 2–3 個小樣讓 Jason 挑
3. **Lenis `lerp` 係數**：0.1（標準） / 0.08（更黏） / 關掉
4. **Section accent 實際色值**：§3.2 候選值，Phase 1 小樣確認
5. **暗底 brown 微調值**：從 `#a47148`（4.55:1）提到 ≥ 5:1，Phase 1 取色

---

## 14. 非目標（Out of Scope）

- 不改 Obsidian 寫作流程
- 不改部署架構（維持 Cloudflare Workers）
- 不改 Quartz 4 → 其他框架
- 不做評論系統 / CMS / 動態內容
- 不新增其他語言版本（現有 `locale: "zh-TW"` 不動）
- 不做 PWA / Service Worker
- 不強制任何 frontmatter 欄位（`cover:` / `accent:` / `hero-style:` 全部可選）
- 不自建 CDN（vendored assets 走 Cloudflare Workers 既有分發）
- 本次不啟用 OG image 產生器（§12 留介面）

---

## 15. `quartz.layout.ts` 差異（v2 新增）

### 15.1 現況

```ts
// quartz.layout.ts (current)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    ConditionalRender({ component: HomeLanding(), condition: slug === "index" }),
    ConditionalRender({ component: Breadcrumbs(), condition: slug !== "index" }),
    ConditionalRender({ component: ArticleTitle(), condition: slug !== "index" }),
    ConditionalRender({ component: ContentMeta(), condition: slug !== "index" }),
    ConditionalRender({ component: TagList(), condition: slug !== "index" }),
  ],
  left: [],
  right: [],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [BrandIntro(), ArticleTitle()],
  left: [],
  right: [],
}
```

### 15.2 新版（v3 改為可直接貼上的 TypeScript）

**v2 問題**：寫成了 pseudocode（`condition: slug !== "index" && frontmatter[...]`），不符合 `ConditionalRender` 實際簽名 `condition: (props: QuartzComponentProps) => boolean`。v3 改為真實可 compile 的 TypeScript。

```ts
import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// 共用 helper：判斷頁面是否不是首頁 + hero-style 不為 none
const isNonIndex = (page: any) => page.fileData.slug !== "index"
const heroStyleNone = (page: any) => page.fileData.frontmatter?.["hero-style"] === "none"

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    // 首頁：HomeLanding（Phase 2 內部重寫，入口保持不動）
    Component.ConditionalRender({
      component: Component.HomeLanding(),
      condition: (page) => page.fileData.slug === "index",
    }),
    // 非首頁且 hero-style !== "none"：Breadcrumbs + ArticleHero（新組件）
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => isNonIndex(page) && !heroStyleNone(page),
    }),
    Component.ConditionalRender({
      component: Component.ArticleHero(),  // 新組件，內含 title + meta + section-themed canvas
      condition: (page) => isNonIndex(page) && !heroStyleNone(page),
    }),
    // hero-style: "none" 的頁面走極簡 fallback（Breadcrumbs + 純 ArticleTitle）
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => isNonIndex(page) && heroStyleNone(page),
    }),
    Component.ConditionalRender({
      component: Component.ArticleTitle(),
      condition: (page) => isNonIndex(page) && heroStyleNone(page),
    }),
    // TagList 保留在所有非首頁
    Component.ConditionalRender({
      component: Component.TagList(),
      condition: isNonIndex,
    }),
  ],
  left: [],
  right: [
    // v3 修正：真實使用 Component.DesktopOnly + Component.TableOfContents
    Component.DesktopOnly(Component.TableOfContents()),
  ],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.CategoryHero(),  // 新組件，吸收 BrandIntro + ArticleTitle 功能
  ],
  left: [],
  right: [],
}
```

**v3 關鍵修正**：
- 加 `import * as Component from "./quartz/components"` 開頭，跟現有 `quartz.layout.ts:2` 一致
- `condition` 改成真實 `(page) => boolean` function signature
- `frontmatter["hero-style"]` 改成 `page.fileData.frontmatter?.["hero-style"]`（Optional chaining 避免沒 frontmatter 的頁面炸掉）
- `DesktopOnly(...)` / `TableOfContents()` 都加上 `Component.` namespace

### 15.3 被取代/重構的組件

- `BrandIntro.tsx`：功能併入 `CategoryHero`，組件保留但不再進 layout（可刪但 Phase 4 再決定）
- `ArticleTitle.tsx`：仍用於 `hero-style: none` 的極簡 fallback，**不刪**
- `ContentMeta.tsx`：功能併入 `ArticleHero`，組件同 `BrandIntro` 處理

---

## 16. `HomeLanding.tsx` 舊區塊 → 新區塊對照表

### 16.1 TSX 區塊對照

| 舊區塊（current） | 新區塊（target） | 動作 |
|------------------|-----------------|------|
| `.home-hero-scene` + 7 個 Matter.js 物件 | `.home-hero__focal` 單一 canvas | **取代** |
| `.home-landing__copy`（eyebrow + h1 + lead + signals + actions） | `.home-hero__copy`（放大型 + 重排） | **保留+重樣式** |
| `.home-landing__hero-rail` > `.home-landing__visual-stage` > 3 個 visual-card | `.home-pillars` 新 section | **transform**（同概念不同呈現） |
| `.home-landing__hero-rail` > `.home-landing__hero-stats` | `.home-stats-strip` 獨立 section | **transform**（提升為一整個 section） |
| `.home-landing__section-map` | 併入 `.home-pillars` | **合併** |
| `.home-landing__feature-grid` | `.home-featured` | **保留+重樣式** |
| `.home-landing__recent` | `.home-recent` | **保留+重樣式** |
| `.home-landing__shelves` | — | **刪除**（與 Pillars 重複） |

**Matter.js 移除**：`quartz/components/scripts/heroScene.inline.ts` 在 Phase 2 砍掉。`package.json` 移除 `matter-js` 依賴（若有）。

### 16.2 SCSS 清理（v3 新增）

`quartz/styles/custom.scss` 含 ~167 行 `.home-landing__*` 規則。Phase 2 必須同步處理，否則變死碼還可能跟新 class 意外碰撞。

**操作原則**：
- 新 SCSS 寫到 **新檔** `quartz/styles/_home-apple.scss`（BEM 新命名）
- 舊 `.home-landing__*` 在 `custom.scss` 裡 **同 commit 刪除**（跟 `HomeLanding.tsx` 重寫一起進 Phase 2）

**對照刪除/遷移清單**（以 `custom.scss` 現有規則為準）：

| 舊 class / 規則群 | 動作 | 對應新檔 |
|-----------------|------|---------|
| `.home-landing`（wrapper） | 保留名稱但重樣式 | `_home-apple.scss` `.home-landing` |
| `.home-landing__hero`, `.home-landing__copy`, `.home-landing__eyebrow`, `.home-landing__lead`, `.home-landing__signals`, `.home-landing__actions` | 遷移 + 改名 | `_home-apple.scss` `.home-hero__*` |
| `.home-hero-scene`, `.home-hero-scene__field`, `.hero-object`, `.hero-object[data-*]` | **全刪**（Matter.js 移除） | — |
| `.home-landing__hero-rail`, `.home-landing__visual-stage*`, `.home-landing__visual-card*`, `.home-landing__visual-ring`, `.home-landing__visual-caption`, `.home-landing__panel-label` | **全刪**（概念改成 pillars） | — |
| `.home-landing__hero-stats` | 遷移 + 改名 | `_home-apple.scss` `.home-stats-strip` |
| `.home-landing__section-map`, `.home-landing__theme-tile` | **全刪**（併入 pillars） | — |
| `.home-landing__feature-grid`, `.home-landing__feature-card`, `.is-primary` | 遷移 + 改名 | `_home-apple.scss` `.home-featured*` |
| `.home-landing__recent*`, `.home-landing__section-heading`, `.home-landing__section-label` | 遷移 + 改名 | `_home-apple.scss` `.home-recent*` |
| `.home-landing__shelves`, `.home-landing__shelf*` | **全刪** | — |

**驗證**：Phase 2 完成後 `grep "home-landing__" quartz/styles/` 應只剩 `.home-landing` 一個 wrapper class（如果還要保留），或完全沒有。

---

## 17. 驗證通過的假設（附 reviewer 驗證軌跡）

1. **Quartz SPA `nav` / `prenav` event + `window.addCleanup`**：`quartz/components/scripts/spa.inline.ts:38-44, 81, 129, 191`
2. **`enableSPA: true` / `enablePopovers: true` / Google Fonts**：`quartz.config.ts:13-14, 21`
3. **現有 hero 7 物件**：`HomeLanding.tsx:14-22`
4. **Section themes slug prefix 邏輯**：`quartz/components/sectionThemes.ts:38-132`
5. **esbuild + `.inline.ts` 打包機制**：`quartz/cli/handlers.js:266-299`, `componentResources.ts:67-77`
6. **`additionalHead` 注入機制**：`Head.tsx:23, 93`, `plugins/index.ts:9, 13, 20-21`
7. **`Component.TableOfContents()` 已存在可複用**：`quartz/components/TableOfContents.tsx:21-101`
8. **`Plugin.Static()` 會把 `quartz/static/` 複製到 `public/static/`**：`quartz.config.ts:86`
9. **現有 `heroScene.inline.ts` 的 cleanup pattern 可 model**：`quartz/components/scripts/heroScene.inline.ts`
10. **色票對比度**：§3.2 已列實測值
