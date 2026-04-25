# Phase 2 完成後 Lighthouse 跑分

- **日期**：`???`（填 Lighthouse 實跑日）
- **Branch**：`feature/immersive-phase-2`
- **HEAD SHA**：`6da989b56350b0fdaa973bc913b922dd60095245`
- **Chrome 版本**：`???`（DevTools → About Chrome）
- **Lighthouse 版本**：`???`（DevTools → Lighthouse panel 標頭）
- **測試環境**：`npx quartz build --serve` → `http://localhost:8080`
- **裝置模擬**：Desktop，Throttling = "Simulated Slow 4G, 4x CPU slowdown" 或 "No throttling"（請勾一個並寫在下方 Notes）
- **執行者**：`???`

> Phase 1 baseline 出自 `docs/superpowers/baselines/2026-04-24-perf-baseline.md`（本 repo 實際檔名為 `-perf-baseline.md`，非 `-lighthouse.md`）。
> Phase 1 量測工具是 **Web Performance API via Playwright**（非 Lighthouse），所以 FCP / LCP 可以直接對照，但 Lighthouse 的 Performance score / TBT / SI 沒有 Phase 1 數字。

---

## 1. 首頁 `/`

### 1.1 Core Web Vitals + Lighthouse scores

| 指標 | Phase 1 baseline | Phase 2 實測 | Diff | 備註 |
|------|------------------|----------------|------|------|
| **Performance score** | n/a（Phase 1 用 PerfObserver） | `???` | `???` | |
| **Accessibility** | n/a | `???` | `???` | |
| **Best Practices** | n/a | `???` | `???` | |
| **SEO** | n/a | `???` | `???` | |
| TTFB | 4 ms | `???` | `???` | |
| FCP | 448 ms | `???` | `???` | |
| **LCP** | **448 ms**（H1） | `???` | `???` | LCP 元素：`???` |
| CLS | 0 | `???` | `???` | |
| TBT | n/a | `???` | `???` | |
| Speed Index | n/a | `???` | `???` | |
| Total transfer | 246 KB | `???` | `???` | |
| postscript.js raw | 126,964 B | 60,794 B | **−66,170 B / −52%** | 已由自動化檢查確認 |

### 1.2 Lighthouse Opportunities / Diagnostics（記下重要幾項）

- `???`

---

## 2. 分類頁 `/manufacturing-ai/`

### 2.1 Core Web Vitals + Lighthouse scores

| 指標 | Phase 1 baseline | Phase 2 實測 | Diff | 備註 |
|------|------------------|----------------|------|------|
| **Performance score** | n/a | `???` | `???` | |
| **Accessibility** | n/a | `???` | `???` | |
| **Best Practices** | n/a | `???` | `???` | |
| **SEO** | n/a | `???` | `???` | |
| TTFB | 13 ms | `???` | `???` | |
| FCP | 156 ms | `???` | `???` | |
| **LCP** | **156 ms**（H2） | `???` | `???` | LCP 元素：`???` |
| CLS | 0 | `???` | `???` | |
| TBT | n/a | `???` | `???` | |
| Speed Index | n/a | `???` | `???` | |

### 2.2 Lighthouse Opportunities / Diagnostics

- `???`

---

## 3. 文章頁（挑一篇代表）

**挑選的 URL**：`???`（建議：`/manufacturing-ai/在傳統製造業導入-AI，最先卡住的不是模型/`）

### 3.1 Core Web Vitals + Lighthouse scores

| 指標 | Phase 1 baseline | Phase 2 實測 | Diff | 備註 |
|------|------------------|----------------|------|------|
| **Performance score** | n/a | `???` | `???` | |
| **Accessibility** | n/a | `???` | `???` | |
| **Best Practices** | n/a | `???` | `???` | |
| **SEO** | n/a | `???` | `???` | |
| TTFB | 6 ms | `???` | `???` | |
| FCP | 368 ms | `???` | `???` | |
| **LCP** | **368 ms**（H1） | `???` | `???` | LCP 元素：`???` |
| CLS | 0 | `???` | `???` | |
| TBT | n/a | `???` | `???` | |
| Speed Index | n/a | `???` | `???` | |

### 3.2 Lighthouse Opportunities / Diagnostics

- `???`

---

## 4. Spec §9.6 目標達成狀況

| # | 目標 | 來源 | 狀態 | 備註 |
|---|------|------|------|------|
| 1 | LCP (home) ≤ Phase 1（448 ms）或更快 | spec §9.6 | `?` | `???` |
| 2 | CLS = 0（所有頁面） | spec §9.6 | `?` | `???` |
| 3 | postscript.js raw 比 Phase 1 小（目標 ~117 KB） | spec §9.6 | ✅ | 實測 60,794 B，遠優於目標 |
| 4 | 首頁 cinematic 頁新增資源 ≤ 46 KB gzipped（GSAP+ScrollTrigger dynamic） | spec §9.6 | `?` | 看 Network 的 `gsap.min.js` + `ScrollTrigger.min.js` gzipped 總和：`???` |
| 5 | 文章頁 **不載 GSAP** | spec §9.6 | `?` | Network 觀察：`???` |
| 6 | Lenis bundle（全站） | spec §9.6 | `?` | Network 觀察：`???` |
| 7 | Lighthouse Performance ≥ `???`（請填 spec 目標值，若沒訂就寫實測） | spec §9.6 | `?` | `???` |
| 8 | Accessibility ≥ 95 | spec §9.6 | `?` | `???` |

---

## 5. Notes / 退步項目 / 待追蹤

### 5.1 Throttling 設定

- 使用的 throttling：`???`（Simulated Slow 4G 4x CPU / No throttling / 其他）
- 重跑次數：`???`（建議至少 3 次取中位數）

### 5.2 退步項目（Phase 1 → Phase 2 變差的指標）

- `???`

### 5.3 值得 flag 的 Opportunity

- `???`

### 5.4 Phase 3 要接手

- `???`

---

## 附錄：怎麼跑 Lighthouse

1. `cd "C:/Users/user/Desktop/自有網域PoC/quartz"`
2. `rm -rf public/ && npx quartz build --serve`
3. Chrome 開新分頁無痕模式 → `http://localhost:8080`
4. F12 → Lighthouse panel → Desktop → 勾 Performance / Accessibility / Best Practices / SEO → Analyze page load
5. 對每個 URL 跑 3 次，取中位數填上表
6. 三個 URL：`/`、`/manufacturing-ai/`、挑一篇 `/manufacturing-ai/*.html`

⚠️ 跑 localhost 記得 **關 DevTools Cache（Disable cache）**，否則 LCP 會異常低。
