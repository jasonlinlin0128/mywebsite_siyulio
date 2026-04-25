# Phase 1 完成後效能基準線

- **日期**：2026-04-24
- **Commit**：`a189945`（Phase 1 最後一個 commit，Task 10 wire MotionRuntime）
- **Branch**：`feature-immersive-phase-1`
- **測試環境**：localhost:8080（`npx quartz build --serve`）
- **瀏覽器**：HeadlessChrome 147 (Playwright)，viewport 1440×900
- **工具**：Web Performance API（`PerformanceObserver` for LCP/CLS，`PerformanceNavigationTiming` for FCP/TTFB）

> ⚠️ 這是 **local dev** 數字，不是 production。Production（Cloudflare Workers）會有更高 TTFB 但 FCP/LCP 應差不多甚至更好。基準線的用途是 **偵測 Phase 2 導入 Lenis/GSAP/canvas 後的 regression**，不是拿來跟 Lighthouse 評分比對。

## 3 頁測量

### 首頁 `/`（完整 cold load）

| 指標 | 值 | 備註 |
|-----|---|------|
| TTFB | 4 ms | localhost 近乎零延遲 |
| FCP | 448 ms | |
| **LCP** | **448 ms** | LCP 元素：`<h1>`（128px 大標），**符合 spec §9.5 候選** |
| CLS | 0 | 無版面位移 |
| Load event | 550 ms | |
| **Total transfer** | **246 KB** | |
| ├ script | 124 KB | |
| ├ CSS | 89 KB | |
| └ other | 33 KB | |
| postscript.js（raw） | **126,964 bytes (~124 KB)** | 全站單一 bundle |
| Script count | 3 | prescript.js、copy-tex.min.js、postscript.js |

### 分類頁 `/manufacturing-ai/`（從首頁 SPA 跳轉後 full reload）

| 指標 | 值 |
|-----|---|
| TTFB | 13 ms |
| FCP | 156 ms |
| **LCP** | **156 ms**（element: `<h2>`）|
| CLS | 0 |
| Load event | 142 ms |
| Total transfer | 0 KB（全部從 cache，dev server 允許快取 static assets）|

### 文章頁 `/manufacturing-ai/在傳統製造業導入 AI...`

| 指標 | 值 |
|-----|---|
| TTFB | 6 ms |
| FCP | 368 ms |
| **LCP** | **368 ms**（element: `<h1>`）|
| CLS | 0 |
| Load event | 327 ms |
| Resource count | 23 |
| Total transfer | 0 KB（cache）|

## 關鍵 baseline 數字（Phase 2 要對照的）

```
postscript.js (raw):       126,964 bytes
postscript.js (gzipped):   ~35-45 KB estimated
LCP (home):                448 ms (H1)
LCP (article):             368 ms (H1)
CLS (all pages):           0
```

## Phase 2 期望變化

從 spec §9.6 的期望：

| 指標 | Phase 1 基準 | Phase 2 目標 | 手段 |
|-----|------------|------------|------|
| LCP (home) | 448 ms | **保持或變快** | 字體 preload、Matter.js 移除 |
| postscript.js raw | 126,964 B | **~117 KB**（-10KB）| Matter.js 移除 ~25KB，加 Lenis ~15KB 實淨 -10KB |
| CLS | 0 | **保持 0** | Hero 用 `min-height: 100vh` 預佔 |
| 新增資源（cinematic 頁）| 0 | +46 KB gzipped | Vendored GSAP + ScrollTrigger 動態載入 |
| 新增資源（文章頁）| 0 | 0（GSAP 不載） | 只載 Lenis + IntersectionObserver |

## 功能驗證（Task 11 的 8 項，Playwright 實測）

| # | 項目 | 結果 |
|---|------|------|
| 1 | 桌機版 render | ✅ 1440×900 下 hero + FIELD SYSTEM 排列正常 |
| 2 | `window.__motion` / `__nav` / `__gsapLoader` | ✅ 全部 defined，keys 正確 |
| 3 | Console errors | ✅ 0 error，0 warning |
| 4 | Matter.js hero 物件 render | ✅ 7 個物件有正確 px 座標 |
| 5 | data-reveal 機制 | ✅ JS inject element → nav event → `.revealed` class + CSS transition 跑 |
| 6 | Wikilink popover | ✅ Hover 後 popover 出現 + 抓目標 HTML |
| 7 | SPA navigation | ✅ 點 link 後 URL 變 + navGen 從 0 → 1（prenav 正確觸發）|
| 8 | SPA 導航後 motion API 存活 | ✅ `__motion` / `__gsapLoader` 仍 defined |

**不適用**（本站 layout 沒裝）：TOC、Search modal、Darkmode toggle。

## 已知既有問題（非 Phase 1 造成）

- **Matter.js hero 滑鼠互動失效**：`.home-hero-scene` 有 `pointer-events: none` 擋住 `pointermove`，從 commit `355ed5f`（2026-04-12）就這樣，Phase 1 沒碰這塊。物件 render 正確但不跟滑鼠反應。**Phase 2 會把整個 Matter.js hero 換成 canvas focal visual，屆時自然解決**。
- **Popover 內 `.breadcrumbs` selector 未匹配**：我的 `_popover-immersive.scss` 寫 `.breadcrumbs`，實際 class 是 `breadcrumb-container`。Phase 1 dormant，不影響；Phase 3 實作 ArticleHero 時順便改。
- **可能還有死 wikilink**：`/ai-notes/如何建立自己的常用指令庫` 存在，但之前清過的 wikilinks 指向別處。不是 Phase 1 問題，可另單獨處理。
