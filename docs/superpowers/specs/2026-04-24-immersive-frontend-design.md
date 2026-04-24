# www.siyulio.com 沉浸式前端重設計

- **日期**：2026-04-24
- **作者**：Jason Lin（與 Claude Opus 4.7 共同設計）
- **狀態**：Design approved，待寫實作 plan
- **目標專案**：`quartz/`（Quartz 4 + Preact SSR + markdown）
- **目標網址**：https://www.siyulio.com

---

## 1. 目標與動機

把 siyulio.com 的前端從「標準 Obsidian-Quartz 筆記站」升級為「Apple 產品頁風格的沉浸式內容站」，但**不改變 Obsidian markdown 寫作流程**，也不更換部署基礎設施。

- **風格錨點**：Apple 產品頁（iPhone / MacBook 類型），staged reveal，不做 scroll-jacking
- **範圍**：全站（首頁 / 3 個分類頁 / 所有文章頁 / 404 / about / tag 頁）
- **約束**：
  - 留在 Quartz 4（不遷移到 Next.js / Astro）
  - 部署不變（Cloudflare Workers + `wrangler.jsonc`）
  - Obsidian wikilinks / backlinks / graph / search 全部維持 work
  - 不要求每篇文章手動配封面圖

---

## 2. 關鍵決策記錄

| 決策點 | 選擇 | 備選方案 |
|-------|------|---------|
| 風格參考 | Apple 產品頁（iPhone / MacBook 類型 → staged reveal） | Vision Pro 派 / Apple Newsroom 派 |
| 改造範圍 | C - 全站（含文章頁） | 僅首頁 / 首頁+分類頁 |
| 技術棧 | A - 留在 Quartz 4 擴充 | 改用 Next.js / Astro |
| 動畫庫 | A - GSAP + ScrollTrigger + Lenis | Motion One / 純 CSS+IntersectionObserver |
| 文章頁封面策略 | B - Section-themed 動態視覺（可選 `cover:` override） | 每篇手配 / AI 生圖 / 純文字 hero |
| Hero 個性 | C - 首頁極簡、分類/文章頁保留個性物件 | 全站極簡 / 全站有物件 |

---

## 3. 設計語言（Design Tokens）

### 3.1 字體（延用現有）

- **Display**：Outfit
  - Hero：80–128px（依 viewport 彈性）
  - Section h2：48–64px
  - Eyebrow：14px 大寫 + letter-spacing 0.15em（Apple 標誌性小標）
- **Body**：Noto Sans TC（內文）
- **Code**：JetBrains Mono

### 3.2 色票

延用 `quartz.config.ts` 的暖金黑基底，**新增 section accent 與 motion tokens**：

```
基礎（既有）
  background:  #12100d → #fff7ea（暗模式 / 亮模式）
  gold primary: #c8a96b
  gold tertiary: #f3d79a
  highlight: rgba(200, 169, 107, 0.14)

新增 section accent（實作前會出小樣確認）
  manufacturing-ai:  暖金 #c8a96b（延用既有）
  ai-notes:          靛藍 #7b8cc7（候選）
  coffee:            深棕 #a47148（候選）

新增 glow tokens（每 section 對應一組）
  <section>-glow:    accent 色 with 24% alpha
  <section>-blur:    accent 色 with 8% alpha, blur 60px
```

### 3.3 留白 & 節奏

- **Hero 高度**：`100vh`（首頁）/ `75vh`（分類頁）/ `60vh`（文章頁）
- **Section 間距**：`160px`（desktop）/ `96px`（mobile）
- **文字最大寬**：`680px`（閱讀區）/ `1080px`（展示區）

### 3.4 Motion tokens

```scss
$motion-duration-fast:  0.4s;   // 微動作
$motion-duration-base:  0.6s;   // 標準 reveal
$motion-duration-slow:  1.2s;   // hero 開場
$motion-easing:         cubic-bezier(0.22, 1, 0.36, 1);  // Apple 標準
$motion-stagger:        80ms;   // 同組元素時間差
$motion-reveal-offset:  12%;    // viewport 進入觸發點
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
├─ lenis.inline.ts         全站 smooth scroll 初始化
├─ scrollReveal.inline.ts  IntersectionObserver reveal（文章頁用）
├─ heroCinematic.inline.ts GSAP ScrollTrigger 時間軸（首頁/分類 hero）
└─ sectionCanvas.inline.ts Canvas 繪製 section-themed 動態視覺

Layer 3｜Support Components
├─ ScrollProgress.tsx      文章頁頂部細線進度條
├─ StickyTOC.tsx           文章頁右側浮動目錄（desktop only）
└─ SectionBadge.tsx        section 歸屬小標
```

### 4.2 資料流（無侵入擴充）

既有 frontmatter 不變，**可選擴充**：

| 欄位 | 用途 | 預設行為 |
|-----|------|---------|
| `cover:` | 手動指定封面圖 | 無 → 走 section-themed 動態封面 |
| `accent:` | 手動指定主題色 | 無 → 按 slug prefix 推斷 section |
| `hero-style:` | `minimal` \| `cinematic` | 預設 `cinematic`（分類/文章）/ `minimal`（首頁） |

`sectionThemes.ts` 擴充新增 `motionConfig`：

```ts
motionConfig: {
  canvasRenderer: 'geometric-lines' | 'particle-flow' | 'steam-curves',
  objectSet: string[],          // 分類頁 hero 物件清單
  glowColor: string,
  particleDensity: number,
}
```

---

## 5. 各頁版型

### 5.1 首頁 `/`（純 Apple 極簡）

```
[SiteHeaderNav]
[Hero 100vh]
  eyebrow: JASON LIN / AI FIELD NOTES
  h1 (128px): 把企業裡真的用得上的 AI，整理成可以開始的做法。
  focal visual: 單一 canvas（暖金漸層光暈 + 緩動粒子，隨 scroll 呼吸）
  [ 先看製造業 AI → ] [ 再看 AI 新知 → ]

[Stats Strip 100vh]
  count-up 動畫：已發布 N 篇 / 主軸內容 / 最近更新

[Three Pillars 各 100vh, scroll-pinned]
  製造業 AI → 卡片從 scale(0.9) 放大到 1.0，描述淡入
  AI 新知    → 同上，換 accent
  手沖咖啡   → 同上

[Featured Articles]
  第一篇：大卡片橫跨兩欄，scroll 進場圖片從 scale(1.1) 縮到 1.0
  其他三篇：小卡片依序淡入

[Recent Updates list]
  每項 stagger 80ms

[Footer]
```

**關鍵轉變**：砍掉現有 7 個飄浮小物件（咖啡豆/筆電/手機/耳機/馬克杯），換成 **1 個 canvas focal visual**。

### 5.2 分類頁 `/manufacturing-ai/` `/ai-notes/` `/coffee/`（保留個性物件）

```
[Breadcrumbs]
[Hero 75vh]
  eyebrow: SECTION / MANUFACTURING AI
  h1 (96px): 製造業 AI 筆記
  description: ...
  scene (3-5 物件, scroll-driven timeline):
    0-30%:   物件飄入
    30-70%:  物件重新編隊
    70-100%: 物件散開淡出

[Article Grid 2-col]
  每張卡片獨立淡入（stagger 80ms）

[Related Sections]
  延伸閱讀另外兩個分類

[Footer]
```

**Section 專屬物件組**：

- `manufacturing-ai`：齒輪 / 流程圖 / 報表
- `ai-notes`：終端機 / 鍵盤 / 書籤
- `coffee`：咖啡豆 / 濾杯 / 蒸氣

### 5.3 文章頁（所有 `.md`）

```
[Progress Bar 1px, top]
[SiteHeaderNav]
[Breadcrumbs]
[Hero 60vh, section-themed 動態封面]
  漸層背景（section accent）
  Canvas 圖案：
    manufacturing-ai → 等距幾何線條（30 條, sin wave）
    ai-notes        → 粒子流（~60 particles, Perlin noise）
    coffee          → 漸層光斑 + 2 條蒸氣曲線（bezier）
  右下角覆文字：
    [section badge]
    h1 (72px)
    meta: date · N min read

[3-col layout]
  左：空白側欄
  中：內文 680px max，段落 IntersectionObserver 淡入 + translateY 8px
  右：Sticky TOC（desktop only），當前段落高亮

[TagList]
[RecentNotes「繼續閱讀」（已存在）]
[Footer]
```

**文章頁原則**：不做 scroll-jacking，純閱讀體驗。

### 5.4 其他頁

- **`/about/`**：當特殊文章頁，可選擴充 `cover:` 放 portrait
- **404**：Apple 風錯誤頁（大字「404」+ 淡光暈 + 回首頁按鈕）
- **`/tags/xxx/`**：簡化版分類頁（有 eyebrow + h1，無物件 hero）

---

## 6. Quartz SPA 整合（關鍵技術點）

`enableSPA: true` 表示頁面切換不會全頁重載。動畫生命週期必須掛在 Quartz SPA hooks：

```ts
// 每個 inline script 的標準結構
export default (() => {
  // 初始化（每次 SPA 導航後會呼叫）
  function init() {
    // 銷毀上一頁的 instance
    cleanup()
    // 重新 init
    setupLenis()
    setupScrollTriggers()
    setupObservers()
  }

  function cleanup() {
    ScrollTrigger.getAll().forEach(t => t.kill())
    observer?.disconnect()
    lenisInstance?.destroy()
    cancelAnimationFrame(rafId)
  }

  document.addEventListener('nav', init)       // Quartz SPA hook
  window.addCleanup(cleanup)                   // 頁面離開前清理
})()
```

**這是 Quartz 沉浸式站點最容易踩的雷**，沒處理好會導致 SPA 導航後動畫消失 / 疊加 / 記憶體洩漏。

---

## 7. Canvas 動態視覺策略

每個 section 的 canvas hero：

- `requestAnimationFrame` 驅動
- 畫面尺寸 = viewport × `devicePixelRatio`
- 隱藏 tab 時暫停（`visibilitychange` listener）
- 目標 60 FPS，若 `performance.now()` 差 > 32ms 自動掉到 30 FPS
- 卸載時必呼叫 `cancelAnimationFrame`
- 每個 section 視覺 < 100 lines canvas code，不用 Three.js / WebGL

---

## 8. 無障礙與降級

### 8.1 `prefers-reduced-motion`

```js
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Lenis 停用（恢復原生 scroll）
  // GSAP scrub 改即時切換（不做平滑）
  // Canvas hero 只畫第一幀，不啟動 rAF
  // Reveal 改為直接 opacity: 1，取消 translateY
  // 保留：0.2s 極短淡入
}
```

### 8.2 手機版（< 768px）

```
停用：
  - Lenis（iOS Safari 原生 scroll 體驗更好）
  - ScrollTrigger pin
  - Sticky TOC
減半：
  - Hero canvas 解析度
  - Stats count-up（直接顯示最終值）
保留：
  - Section-themed hero 封面（靜態）
  - 段落 reveal
  - 進度條
```

### 8.3 瀏覽器支援

- **完整體驗**：Chrome / Edge / Firefox / Safari 最新兩版
- **降級體驗**：舊版瀏覽器 → 所有元素直接顯示（feature detection）
- **拒絕支援**：IE 11

---

## 9. 效能預算

| 指標 | 目標 | 手段 |
|-----|------|------|
| LCP（首頁） | < 2.5s | Hero 字體 preload、canvas 延後到 LCP 後 init |
| INP | < 200ms | 動畫庫 defer load、main thread 不跑 rAF 重任務 |
| CLS | < 0.1 | Hero 高度用 `min-height: 100vh` 預佔 |
| JS bundle（文章頁） | < 20 KB gzipped | 文章頁不載 GSAP |
| JS bundle（首頁） | < 100 KB gzipped | GSAP + ScrollTrigger + Lenis tree-shake |
| Canvas FPS | ≥ 30 | FPS 自動降級機制 |
| Lighthouse Performance | ≥ 90（首頁）/ ≥ 95（文章頁） | — |
| Lighthouse Accessibility | ≥ 95 | — |

**載入策略切分**：

| 頁面類型 | 載入內容 |
|--------|---------|
| 首頁 `/` | Lenis + GSAP + ScrollTrigger + Canvas (~90KB gzipped) |
| 分類頁 `/xxx/` | Lenis + GSAP + ScrollTrigger + Canvas (~90KB gzipped) |
| 文章頁 | Lenis + IntersectionObserver (~15KB gzipped) |

---

## 10. 實作階段（Milestones）

每個 phase 結束都能獨立上線，不會有「做一半很醜」的中間態。

### Phase 1｜地基：Motion 基礎設施（~3 天）

**交付**：
- `scripts/lenis.inline.ts`
- `scripts/scrollReveal.inline.ts`
- `sectionThemes.ts` 擴充 `motionConfig`
- `styles/_motion-tokens.scss`
- Quartz SPA hook cleanup / re-init
- `prefers-reduced-motion` + 手機 feature detection

**驗收**：
- 現有頁面零 regression
- scroll 有 smooth 慣性感
- 任何元素加 `data-reveal` 就自動淡入

### Phase 2｜首頁改造（~5–7 天）

**交付**：
- `HomeHeroApple.tsx`
- `scripts/heroCinematic.inline.ts`
- `scripts/sectionCanvas.inline.ts`
- `HomeLanding.tsx` 重寫（砍 7 個飄浮物件）
- Pillars section GSAP pin + staged reveal
- Stats count-up
- `styles/_home-apple.scss`

**驗收**：
- 首頁 LCP < 2.5s、bundle < 100KB gzipped
- 手機版降級正常
- Reduced motion 測試通過

### Phase 3｜分類頁 + 文章頁 hero（~5 天）

**交付**：
- `CategoryHero.tsx`
- `ArticleHero.tsx`
- 3 組 section 專屬 canvas 視覺
- `quartz.layout.ts` 擴充
- `cover:` frontmatter 支援

**驗收**：
- 每個分類頁獨立個性
- 所有文章頁都有 hero（零 frontmatter 工作量）
- Wikilinks / backlinks / search 全部仍 work

### Phase 4｜文章頁細節 + 全站拋光（~3–4 天）

**交付**：
- `ScrollProgress.tsx`
- `StickyTOC.tsx`
- 段落 reveal
- 404 頁重做
- About 頁 portrait 支援
- Lighthouse / axe-core audit
- Cross-browser 測試

**驗收**：
- Lighthouse ≥ 90 / 95
- 全站零 console error、無 SPA 動畫疊加

---

## 11. 風險與緩解

| 風險 | 可能性 | 衝擊 | 緩解 |
|-----|-------|------|------|
| Quartz SPA 導航導致動畫疊加 / 消失 | 中 | 高 | Phase 1 先驗證 SPA hooks 接法，做 debug demo 頁 |
| GSAP + Lenis 在 Quartz esbuild 打包有問題 | 低 | 中 | 先做 POC，必要時改用 CDN import |
| Canvas 視覺在低階手機掉幀 | 中 | 中 | FPS 自動降級 + 手機版直接靜態 |
| 砍掉飄浮物件後失去個性 | 中 | 低 | 物件保留在分類頁；不好看隨時切回 |
| 暖金主色 + 新 section accent 打架 | 中 | 中 | Phase 1 先出小樣測色 |

---

## 12. 暫緩 / 已知問題

- **死 wikilink**：`prompts/如何建立自己的常用指令庫` 這條連結對應的內容檔案不存在（在 `manufacturing-ai/在傳統製造業導入 AI...md`、`ai-notes/` 相關檔案可能也有類似情況）。本次設計不處理，單開 issue 清理內容。
- **Sitemap / RSS**：現有 `Plugin.ContentIndex` 已產出，本次不動。
- **Comments / 評論系統**：非本次範圍。

---

## 13. 實作時仍待敲定的小決策

以下 4 項在實作時才決定，避免現在卡住：

1. **Stats strip 三個數字**：現「文章數 / 主軸 / 最近更新」，Phase 2 可能改
2. **首頁 focal visual 具體視覺**：Phase 2 出 2–3 個小樣讓 Jason 挑
3. **Lenis `lerp` 係數**：0.1（標準） / 0.08（更黏） / 關掉
4. **Section accent 實際色值**：Phase 1 先出色票確認

---

## 14. 非目標（Out of Scope）

- 不改 Obsidian 寫作流程
- 不改部署架構（維持 Cloudflare Workers）
- 不改 Quartz 4 → 其他框架
- 不做評論系統 / CMS / 動態內容
- 不做 i18n（目前只有中文 zh-TW）
- 不做 PWA / Service Worker
- 不強制每篇文章補 frontmatter（`cover:` 等全部可選）
