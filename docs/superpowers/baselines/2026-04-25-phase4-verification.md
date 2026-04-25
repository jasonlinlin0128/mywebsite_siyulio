# Phase 4 + 整套 Phase 1-4 ship-ready 驗證

日期：2026-04-25
Phase 4 HEAD：`44a1588` (feat: 404 重做 + about portrait — Tasks 3+4)
測試環境：(人類執行時填入：Chrome version, OS)

## 自動檢查（Phase 4 specific）

| 檢查 | 結果 |
|---|---|
| `npx quartz build` 無 warning | ✓ |
| `public/postscript.js` 含 `--scroll-progress` | ✓ |
| `public/index.css` 含 `.scroll-progress` / `--scroll-progress` | ✓ |
| `public/index.html` 含 `<div class="scroll-progress"` | ✓ |
| `public/404.html` 含 `.not-found__code`（404 重做） | ✓ |
| `public/index.css` 含 `data-has-cover`（about portrait 變體 selector） | ✓ |
| 12 支 motion script 都進 bundle | ✓ |

## Bundle size diff vs Phase 3 baseline

| 指標 | Phase 3 (post) | Phase 4 (post) | diff |
|-----|---------------|---------------|------|
| postscript.js raw | 66,359 B | 67,393 B | +1,034 B (+1.6%) |
| postscript.js gzip | 21,666 B | 21,879 B | +213 B (+1.0%) |
| index.css raw | 90,696 B | 94,483 B | +3,787 B (+4.2%) |
| index.css gzip | 16,975 B | 17,494 B | +519 B (+3.1%) |

Phase 4 增量極小（兩個 inline script + 4 個 SCSS partial 都很輕量）。

## 手動逐項驗證 — Phase 4 新功能

| # | 項目 | 路徑 | 結果 | 備註 |
|---|-----|------|------|------|
| 1 | ScrollProgress 1px top bar | 任一頁 | ✓/✗ | scroll 時跟著前進，三色漸層 |
| 2 | ScrollProgress 對 reduced-motion 行為 | 任一頁 + DevTools emulation | ✓/✗ | 無 width transition (突跳)，仍正常顯示 |
| 3 | 文章段落 reveal | 任一文章 + scroll | ✓/✗ | p / h2 / h3 等段落淡入 (translateY 6px) |
| 4 | 段落 reveal reduced-motion | 任一文章 + emulation | ✓/✗ | 直接顯示，無 translateY，0.15s linear 短淡 |
| 5 | 404 頁 Apple 風 | `/non-existent-page` | ✓/✗ | 大字 404 三色漸層 + 兩顆 CTA + 暖光暈 |
| 6 | 404 forced-colors fallback | DevTools forced-colors emulation | ✓/✗ | 大字回到 CanvasText 純色 |
| 7 | About portrait（cover frontmatter） | `/about` 並設 `cover:` | ✓/✗ | 圓形 portrait card 跟文字並列 |
| 8 | About 沒 cover → minimal | `/about` 無 cover | ✓/✗ | 純 title + meta，無 hero |

## 整套 Phase 1-4 全項驗證（spec §10 全 phase 驗收）

| spec 項目 | 出處 | 結果 |
|---|---|---|
| Lighthouse Performance ≥ 90 (首頁) | §9.6 / §10 Phase 4 | ?? (Lighthouse 跑分人類填) |
| Lighthouse Performance ≥ 95 (文章頁) | §9.6 / §10 Phase 4 | ?? |
| Lighthouse Accessibility ≥ 95 (全頁) | §9.6 / §10 Phase 4 | ?? |
| 全站零 console error | §10 Phase 4 | ✓/✗ (人類驗) |
| 無 SPA 動畫疊加 / 消失 | §10 Phase 4 | `(window.ScrollTrigger?.getAll?.() ?? []).length` 紀錄；點 CTA 來回測 |
| 鍵盤導航流暢（tab 順序、focus ring） | §8.5 / §10 Phase 4 | ✓/✗ (Tab 全頁、確認 outline 可見) |
| iOS Safari 上 Lenis 沒慣性爆衝 | §10 Phase 4 | ✓/✗ (Phase 2 §8.2 已 mobile gate Lenis off → 不該觸發) |
| popover 預覽不秀 hero | §6.3 / §10 Phase 3 | ✓/✗ |
| Sticky TOC + active 高亮 | §5.3 / §10 Phase 3 | ✓/✗ |
| ArticleHero 三主題 canvas | §7 / §10 Phase 3 | ✓/✗ |
| 首頁 HomeHeroApple GSAP 進場 | §5.1 / §10 Phase 2 | ✓/✗ (reduced-motion off 才看到) |
| Lenis × Search modal 整合 | §6.5 / §10 Phase 2 | ✓/✗ (按 / 開 search，背景不滾) |

## Cross-browser checklist（spec §10 Phase 4）

各瀏覽器都跑 `/`、`/manufacturing-ai/`、任一文章、`/404` 共 4 頁：

| 瀏覽器 | / | /manufacturing-ai/ | 文章 | 404 |
|---|---|---|---|---|
| Chrome（latest） | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
| Edge（latest） | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
| Firefox（latest） | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
| Safari（latest） | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
| iOS Safari | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |
| Android Chrome | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ |

## prefers-contrast / forced-colors 逐頁（spec §8.6）

DevTools Rendering → Emulate `prefers-contrast: more` 與 `forced-colors: active`：

| 頁面 | prefers-contrast | forced-colors |
|---|---|---|
| 首頁 | ✓/✗ | ✓/✗ |
| 分類頁 | ✓/✗ (canvas / glow 應更亮 × 2) | ✓/✗ (canvas / glow 隱藏) |
| 文章頁 | ✓/✗ | ✓/✗ (canvas-host / cover 隱藏) |
| 404 | ✓/✗ | ✓/✗ (大字 fallback CanvasText) |

## Phase 1-4 整套 ship-ready signoff

簽核欄位（人類最後填）：

- [ ] 所有自動檢查 ✓
- [ ] 所有手動 Phase 4 新功能 ✓
- [ ] spec §10 全 phase 驗收 ✓
- [ ] Cross-browser 6 環境 ✓
- [ ] prefers-contrast / forced-colors 4 頁 ✓
- [ ] Lighthouse 跑分達標
- [ ] axe-core 無 critical issue
- [ ] PR review 完成

→ Phase 1-4 ship。可 merge 到 v4 → main → 部署。
