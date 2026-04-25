# Phase 1-4 Lighthouse + axe-core final audit

日期：2026-04-25
Final HEAD：`44a1588`
Chrome 版本：(填入)
Lighthouse 版本：(填入)

## Lighthouse Desktop 三頁面跑分

跑分順序：reload → wait full load → Lighthouse → Desktop preset → Performance + Accessibility + Best Practices + SEO + PWA(skip)。

### 首頁 `/`

| 指標 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | spec §9.6 目標 | Pass? |
|-----|--------|--------|--------|--------|--------------|-------|
| Performance | ?? | ?? | ?? | ?? | ≥ 90 | ?? |
| Accessibility | ?? | ?? | ?? | ?? | ≥ 95 | ?? |
| Best Practices | ?? | ?? | ?? | ?? | — | — |
| SEO | ?? | ?? | ?? | ?? | — | — |
| LCP (ms) | ?? | ?? | ?? | ?? | < 2500 | ?? |
| CLS | ?? | ?? | ?? | ?? | < 0.1 | ?? |
| INP (ms) | ?? | ?? | ?? | ?? | < 200 | ?? |
| TBT (ms) | ?? | ?? | ?? | ?? | — | — |
| Speed Index (ms) | ?? | ?? | ?? | ?? | — | — |

### 分類頁 `/manufacturing-ai/`

(同上格式，Phase 4 column 填值)

### 文章頁 `/manufacturing-ai/<挑一篇>/`

| 指標 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | spec §9.6 目標 | Pass? |
|-----|--------|--------|--------|--------|--------------|-------|
| Performance | ?? | ?? | ?? | ?? | ≥ 95 | ?? |
| Accessibility | ?? | ?? | ?? | ?? | ≥ 95 | ?? |
| 其他 | ?? | ?? | ?? | ?? | — | — |

### 404 頁 `/404.html`

| 指標 | Phase 4 |
|-----|--------|
| Performance | ?? |
| Accessibility | ?? |

## Bundle size 全 phase 對照

| 指標 | Phase 1 baseline | Phase 2 (post) | Phase 3 (post) | Phase 4 (post) | 全 phase Δ |
|-----|---------------|--------------|--------------|--------------|----------|
| postscript.js raw | 126,964 B (Matter.js) | 60,794 B | 66,359 B | 67,393 B | **−59,571 B / −47%** |
| postscript.js gzip | ~38 KB est. | ~20 KB | 21,666 B | 21,879 B | **−16 KB est. / −42%** |
| index.css raw | 約 80 KB est. | 82,649 B | 90,696 B | 94,483 B | +14 KB est. (新 BEM 樣式) |
| index.css gzip | ~14 KB est. | ~15 KB | 16,975 B | 17,494 B | +3.5 KB est. |

**淨變動極佳**：postscript.js 反而縮小 47%（Matter.js 移除得分佔很大比例），CSS 增量在預算內。

## axe-core CLI（人類執行）

```bash
# install
npm i -g @axe-core/cli

# run against built site (need dev server running on :8080)
axe http://localhost:8080/ --tags wcag2a,wcag2aa --save axe-report.json

# 重點頁面
axe http://localhost:8080/manufacturing-ai/ --tags wcag2a,wcag2aa
axe http://localhost:8080/manufacturing-ai/<挑一篇>/ --tags wcag2a,wcag2aa
axe http://localhost:8080/404.html --tags wcag2a,wcag2aa
```

預期：critical / serious 為 0；moderate / minor 紀錄但可接受。

| 頁面 | Critical | Serious | Moderate | Minor |
|---|---|---|---|---|
| / | ?? | ?? | ?? | ?? |
| /manufacturing-ai/ | ?? | ?? | ?? | ?? |
| /文章/ | ?? | ?? | ?? | ?? |
| /404.html | ?? | ?? | ?? | ?? |

## WebPageTest URL

跑線：Cable / Chrome / Dulles VA：
- 首頁：(URL)
- 分類頁：(URL)
- 文章頁：(URL)

| 指標 | / | /manufacturing-ai/ | /文章/ |
|---|---|---|---|
| First Byte | ?? | ?? | ?? |
| Start Render | ?? | ?? | ?? |
| Speed Index | ?? | ?? | ?? |
| Largest Contentful Paint | ?? | ?? | ?? |
| Total Bytes | ?? | ?? | ?? |
| Requests | ?? | ?? | ?? |

## 已知遺留 / 退步項目

(人類填入觀察到的 known issues)

## 建議下一步

- 若 LCP 未達 2.5s：spec §3.1 Phase 4 升級到 self-host woff2
- 若 axe-core critical 非 0：先修 critical，moderate 排到 Phase 5
- 若 WebPageTest 顯示某資源拖累：考慮 critical CSS inline / preload
- (可選) Phase 5：清掉 Phase 3 §15.3 保留檔（BrandIntro / sectionScene / ContentMeta）
