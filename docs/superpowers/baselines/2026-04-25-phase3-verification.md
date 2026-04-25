# Phase 3 手動驗證紀錄

日期：2026-04-25
Phase 3 HEAD：`406d3d9` (feat: TOC active-section observer + quartz.layout.ts §15 v3 rewrite)
測試環境：（人類執行時填入：Chrome version, OS）

## 自動檢查（automated by `npx quartz build`）

| 檢查 | 結果 |
|---|---|
| build 成功無 warning | ✓ |
| `public/postscript.js` 含 12 個關鍵字（10 支 motion script 全 + section markers） | ✓ |
| └ 含 `__motion` / `__nav` / `__gsapLoader` / `__sectionCanvas` / `__lenis` | ✓ |
| └ 含 `data-reveal` / `data-home-hero-focal` / `data-hero-cinematic` / `data-section-hero-canvas` | ✓ |
| └ 含 `popover-inner` / `categoryScene` / `category-hero` | ✓ |
| `public/index.css` 含 `.article-hero` / `.category-hero` / `.section-badge` / `.category-scene-object` / `.toc-content a.active` | ✓ |
| `public/index.html`（首頁）含 `<section class="home-hero">` | ✓ |
| `public/manufacturing-ai/index.html`（分類頁）含 `<header class="category-hero">` | ✓ |
| 任一文章頁含 `<header class="article-hero">` | ✓ |

## Bundle size diff vs Phase 2 baseline

| 指標 | Phase 2 (post) | Phase 3 (post) | diff |
|-----|---------------|---------------|------|
| postscript.js raw | 60,794 B | 66,359 B | +5,565 B (+9.2%) |
| postscript.js gzip | ~20 KB | 21,666 B | +1.6 KB |
| index.css raw | 82,649 B | 90,696 B | +8,047 B (+9.7%) |
| index.css gzip | ~15 KB | 16,975 B | +1.7 KB |

新增 motion scripts (categoryScene + popoverScroll) ≈ +5.5KB raw / +1.6KB gz；
新 SCSS partials (article-hero + category-hero + toc-sticky) ≈ +8KB raw / +1.7KB gz。
總 bundle 增量在 spec §9.6 預算內。

## 手動逐頁驗證（執行人填寫）

| # | 項目 | 路徑 | 結果 | 備註 |
|---|-----|------|------|------|
| 1 | 首頁 HomeHeroApple 不變 | `/` | ✓/✗ | Phase 2 上線，這 Phase 應不變 |
| 2 | 分類頁 CategoryHero | `/manufacturing-ai/` | ✓/✗ | eyebrow + h1 + copy + 右側 stage |
| 3 | CategoryHero scroll 動畫 | 同上 + 滾動 | ✓/✗ | reduced-motion off 才會跑 |
| 4 | 文章頁 ArticleHero themed | 任一文章 | ✓/✗ | 60vh + section accent |
| 5 | manufacturing-ai canvas | 一篇 | ✓/✗ | geometric-lines 等距斜線 |
| 6 | ai-notes canvas | 一篇 | ✓/✗ | particle-flow 粒子場 |
| 7 | coffee canvas | 一篇 | ✓/✗ | steam-curves 蒸氣曲線 |
| 8 | Sticky TOC + active class | 文章頁右側 | ✓/✗ | 滾動時 a 變 section accent |
| 9 | cover frontmatter | 設 `cover:` 的測試文章 | ✓/✗ | 用 URL 當背景，無 canvas |
| 10 | accent frontmatter | 設 `accent:` 的測試文章 | ✓/✗ | 邊框 + badge + TOC 都用該色 |
| 11 | hero-style: none fallback | 設此 frontmatter 的文章 | ✓/✗ | 沒 ArticleHero，純 ArticleTitle |
| 12 | tags/* 自動 minimal | 任一 tag 頁 | ✓/✗ | 純 title + meta 無 canvas |
| 13 | about/* 自動 minimal | `/about/` | ✓/✗ | 純 title + meta 無 canvas |
| 14 | popover scroll 過 hero | hover wikilink | ✓/✗ | popover 內容直接從 `<p>` 開始 |
| 15 | SPA 動畫不疊加 | 點 CTA + 返回 | ✓/✗ | `(window.ScrollTrigger?.getAll?.() ?? []).length` 紀錄 |
| 16 | reduced-motion 降級 | DevTools Rendering emulation | ✓/✗ | 物件靜止、canvas 第一幀、無 GSAP |
| 17 | mobile 降級 | DevTools Device iPhone | ✓/✗ | 單欄、CategoryHero 物件靜態、無 GSAP、無 Sticky TOC |
| 18 | dark/light 主題切換 | 點主題按鈕 | ✓/✗ | canvas glow 跟著切（saved-theme MutationObserver） |
| 19 | console 0 error | 所有頁面 | ✓/✗ | 無紅 / 無黃警告 |

## 已知 Phase 3 限制

1. **`accent` / `cover` frontmatter XSS sanitization**：accent 限定 hex/rgb 字元、cover 用 encodeURI；單一作者自有網域風險低，但跨來源內容不要直接導入此欄位。
2. **TOC sticky 在短文章上**：min-height 沒設給 `.right.sidebar`，極短文章（少於一個 viewport）的 TOC 會 fallback 到 static — spec §5.3 沒禁止，可接受。
3. **CategoryHero 物件動畫只在 reduced-motion off + desktop 出現**：mobile / reduced 路徑物件保持 SSR CSS var 靜態位置（spec §8.1 + §8.2）。

## 測試文章清理

Phase 3 ship 前把 `content/_phase3-test-*.md` 刪掉或移到 `content/_drafts/`。
