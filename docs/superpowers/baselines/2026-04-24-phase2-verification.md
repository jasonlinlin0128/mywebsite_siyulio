# Phase 2 完成驗證清單

- **日期**：2026-04-24
- **Branch**：`feature/immersive-phase-2`
- **HEAD SHA**：`6da989b56350b0fdaa973bc913b922dd60095245`
- **自動化檢查執行者**：Claude Code（Opus 4.7 1M ctx）
- **手動驗證執行者**：`???`（待填：姓名 / 環境）
- **手動驗證日期**：`???`
- **瀏覽器 / OS**：`???`（建議：Chrome 最新版，macOS / Windows 11）

> 本文件分兩類檢查：
> - **AUTOMATED**：`npx quartz build` 後以 grep / stat 實測，本次已填入實測結果
> - **MANUAL**：需要人類跑瀏覽器、Device Mode、DevTools 才能確認，以 `[ ]` checkbox + `???` placeholder 留白

---

## 1. Phase 2 commit 總覽（fc70250..HEAD）

Phase 2 共 14 個 commit（包含 plan 文件與 follow-up）：

```
6da989b refactor(heroCinematic): 追蹤 timeline 以 teardown 清 + 顯式 __gsapLoader check
94da543 feat: heroCinematic inline script — GSAP 時間軸 + ScrollTrigger
cf273da feat: CustomHead 加 Google Fonts preload（spec §3.1 定案階段一）
cd386e6 feat: Search modal 開啟時 stop Lenis、關閉時 start（spec §6.5）
da64fd8 refactor(lenis): 清掉 dead bodyOptsIn type field + 修正 scss 誤導註解
18e6873 feat: Lenis smooth scroll 全站啟動（mobile / reduced-motion opt-out）
0d883b8 chore: 移除 Matter.js 依賴、heroScene.inline.ts、static/scene 資產
ee23348 chore: Task 4 follow-up — .gitignore + plan stripper v3 backport
d7a1c7b refactor: 刪除 custom.scss 中所有 .home-landing__* / .home-hero-scene / .hero-object 規則
0df0e3e docs(plan): backport Task 3 code-review fixes (C1+I1+I2+I3)
4dc3028 fix(HomeLanding): 過濾 about 避免 Three Pillars 塞 4 卡 + drop dead imports
7f7b8ba feat: HomeLanding 依 §16 對照表重寫（Matter hero 廢止、Apple hero 上線）
17d88ea fix(focalCanvas): PerformanceObserver + fallback 生命週期完善 + 移除死 hueShift
d9e9f48 feat: focalCanvas + sectionCanvas inline scripts 進 MotionRuntime
731146e refactor: HomeHeroApple 去掉 role="presentation"（保留 aria-hidden）
c6864ca feat: HomeHeroApple 組件骨架 + _home-apple.scss 新樣式（未 wire）
1101766 docs: Phase 2 implementation plan (immersive frontend)
```

---

## 2. 自動化檢查結果（AUTOMATED，本次已執行）

> 命令依據：Task 10 Step 12 template，改用 `npx quartz build` 後針對 `public/` 輸出跑檢查。

### 2.1 Bundle markers（postscript.js 必須含這 11 個 token）

| Token | 期望 | 實測 |
|-------|------|------|
| `__motion` | present | ✅ |
| `__nav` | present | ✅ |
| `__gsapLoader` | present | ✅ |
| `__sectionCanvas` | present | ✅ |
| `__lenis` | present | ✅ |
| `data-reveal` | present | ✅ |
| `data-home-hero-focal` | present | ✅ |
| `data-hero-cinematic` | present | ✅ |
| `Lenis` | present | ✅ |
| `heroCinematic` | present | ✅ |
| `power3.out`（GSAP easing） | present | ✅ |

**結論**：全部 8 個 inline script（motionFeatureDetect / navLifecycle / scrollReveal / focalCanvas / sectionCanvas / lenis / gsapLoader / heroCinematic）都有出現在 bundle 裡。

### 2.2 Matter.js 殘留檢查（必須 0 處）

| 檢查 | 期望 | 實測 |
|------|------|------|
| `matter-js \| Engine.create \| Bodies.circle` in postscript.js | 0 match | ✅ 0 |
| `matter-js` in `package.json` | 0 match | ✅ 0 |
| `matter-js` in `package-lock.json` | 0 match | ✅ 0 |

### 2.3 舊 class 殘留檢查（Phase 1 遺留必須全清）

| 舊 class | 期望 | 實測（`custom.scss` + `public/index.css`） |
|----------|------|------|
| `home-landing__` | 0 match | ✅ 0 |
| `home-hero-scene` | 0 match | ✅ 0 |
| `hero-object` | 0 match | ✅ 0 |

### 2.4 新 BEM class 進 bundle（public/index.css）

| Class prefix | 期望 | 實測 |
|--------------|------|------|
| `home-hero__` | present | ✅ |
| `home-pillars` | present | ✅ |
| `home-stats-strip` | present | ✅ |
| `home-featured` | present | ✅ |
| `home-recent` | present | ✅ |
| `lenis-smooth` | present | ✅ |
| `lenis-stopped` | present | ✅ |

### 2.5 首頁 `public/index.html` DOM markers

| Selector / attribute | 期望 | 實測 |
|----------------------|------|------|
| `data-hero-cinematic="true"` | 1 處 | ✅ 1 |
| `data-home-hero-focal="true"` | 1 處 | ✅ 1 |
| `data-count-to="[0-9]+"` | ≥1 處 | ✅ 1 處（value=`8`） |
| `class="home-pillars__card"` | **3 張**（過濾 about） | ✅ **3** |
| `class="home-featured__card"` | ≥1 處 | ✅ 4 處 |

### 2.6 Google Fonts preload（CustomHead / spec §3.1）

| 檢查 | 期望 | 實測 |
|------|------|------|
| `<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?...">` | present on `public/index.html` | ✅ 含 `Outfit`、`Noto Sans TC`、`JetBrains Mono`、`display=swap` |

### 2.7 Bundle sizes（vs Phase 1 baseline）

| 資源 | Phase 1（raw） | Phase 2（raw） | Diff | Phase 2（gzip） |
|------|----------------|----------------|------|------------------|
| `postscript.js` | 126,964 B (~124 KB) | **60,794 B (~59 KB)** | **−66,170 B (−52%)** | **20,042 B (~19.6 KB)** |
| `index.css` | ~89 KB（Phase 1 note） | **82,649 B (~80.7 KB)** | ~−8 KB | **15,550 B (~15.2 KB)** |

**結論**：Matter.js 移除（~25 KB 省）+ inline scripts 共用 feature-detect 邏輯 + 死樣式清理，postscript.js 降了一半以上。Spec §9.6 原估 Phase 2 postscript ~117 KB（−10 KB），**實測超出預期**（−66 KB），因為 Lenis / GSAP 都走 CDN runtime 載入而非 bundle。

### 2.8 整合點 marker（postscript.js）

| Marker | 期望 | 實測 |
|--------|------|------|
| `ScrollTrigger` | present（heroCinematic 用） | ✅ |
| `lenis` | present | ✅ |
| `.stop()` / `.start()` | present（Search × Lenis 整合） | ✅ |

---

## 3. 手動驗證清單（MANUAL — 待下游人類執行）

> 執行方式：`npx quartz build --serve` → 開 `http://localhost:8080` → 按清單逐項驗證 → 把 `???` 改成實測結果、勾 `[ ]`。

### 3.1 首頁新視覺驗證（桌機 1440×900 或以上）

- [ ] **Hero（HomeHeroApple）**：大標題「讓 AI 在你的流程裡，變成能用的資產。」是否 cinematic fade-in？是否看到背景 focal canvas 粒子？
  - 觀察：`???`
- [ ] **Stats strip**：數字從 0 count-up 到目標值（`data-count-to="8"`）？
  - 觀察：`???`
- [ ] **Pillars（3 張卡）**：卡片是否 stagger reveal（一張接一張淡入）？內容：`製造業 AI` / `AI 筆記` / `咖啡筆記`（**絕不能出現 `about`**）？
  - 觀察：`???`
- [ ] **Featured**：4 張精選卡片排版是否正確、有 hover 效果？
  - 觀察：`???`
- [ ] **Recent**：最新文章列表是否顯示、時間排序正確？
  - 觀察：`???`

### 3.2 SPA 導航驗證

- [ ] 點首頁 hero CTA「瀏覽文章」→ 跳到 `/manufacturing-ai/`，URL 有變、不是 full reload
  - `window.__nav.generation` 從 0 → 1（DevTools Console）：`???`
- [ ] 瀏覽器 **上一頁（back）** → 回首頁，動畫重新觸發？data-reveal 元素重新 inject？
  - 觀察：`???`
- [ ] `ScrollTrigger.getAll().length` 在首頁 → 文章頁 → 回首頁的三次觀察值（不該每次暴漲，應該 teardown 清掉）：
  - 首頁初次：`???`
  - 離首頁後：`???`
  - 回首頁：`???`

### 3.3 Dark / Light 切換

- [ ] 切 dark → light → dark，hero / pillars / featured / recent 配色都跟著切？
  - 觀察：`???`
- [ ] Focal canvas 粒子顏色是否也跟著切（spec §7.2 tokenized color）？
  - 觀察：`???`

### 3.4 Popover 仍正常

- [ ] Hover 任一 wikilink（例如首頁 recent 的文章連結），popover 是否正常浮出、抓到目標內文預覽？
  - 觀察：`???`

### 3.5 TOC 高亮

- [ ] 進一篇文章，滾動時右側 TOC 是否正確高亮當前 section？
  - 觀察：`???`

### 3.6 Search × Lenis 整合（spec §6.5，桌機）

- [ ] 按 `/` 或 `Ctrl+K` 開 search modal：背景 body **不能**跟著 scroll（Lenis 應 `stop()`）
  - 觀察：`???`
- [ ] 關閉 modal：body 恢復可捲（Lenis 應 `start()`），捲起來仍是 smooth 慣性
  - 觀察：`???`

### 3.7 Mobile 降級（Chrome Device Mode → iPhone 14 Pro）

- [ ] GSAP **沒載**（Network 裡沒 `gsap.min.js`）：`???`
- [ ] Stats 是靜態值（沒 count-up 動畫）：`???`
- [ ] `window.__lenis` is `undefined`：`???`
- [ ] Focal canvas 降級成 **靜態粒子**（不動）：`???`

### 3.8 Reduced-motion 降級（DevTools → Rendering → prefers-reduced-motion: reduce）

- [ ] GSAP **沒載**：`???`
- [ ] Focal canvas 只渲 **第一幀**後停：`???`
- [ ] `data-reveal` 元素立刻帶 `.revealed`（不等 IntersectionObserver）：`???`

### 3.9 Console 潔淨度

- [ ] 首頁 / 分類頁 / 文章頁，DevTools Console **0 error、0 warning**
  - 首頁：`???`
  - 分類頁：`???`
  - 文章頁：`???`

### 3.10 Bundle 淨變動 vs Phase 1 baseline

- [x] postscript.js raw：126,964 → **60,794** B（**−66,170 B / −52%**），優於 spec §9.6 目標（−10 KB）
- [x] postscript.js gzip：Phase 1 估 35–45 KB → **20,042 B (~19.6 KB)**
- [x] index.css raw：~89 KB → **82,649 B**（Matter.js + 舊 home-landing class 清理）
- [ ] 人工確認 Network tab：首頁 cold load 沒有 Matter.js CDN、沒有 `heroScene.inline.js` 請求

---

## 4. 結論 / Blockers / Regression

（由手動驗證者填寫）

- **整體結論**：`???`（PASS / PASS with minor / BLOCKED）
- **阻擋上線的 blocker**：`???`
- **可延後的 regression / known issue**：`???`
- **Phase 3 要接手的尾巴**：`???`

---

## 附錄 A：如何重跑自動化檢查

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
rm -rf public/
npx quartz build

# Bundle markers
grep -oE "__motion|__nav|__gsapLoader|__sectionCanvas|__lenis|data-reveal|data-home-hero-focal|data-hero-cinematic|Lenis|heroCinematic|power3.out" public/postscript.js | sort -u

# Matter.js absence
grep -oE "matter-js|Engine\.create|Bodies\.circle" public/postscript.js
grep -c "matter-js" package.json package-lock.json

# Pillar count must be 3
grep -oE 'class="home-pillars__card"' public/index.html | wc -l

# Bundle sizes
ls -l public/postscript.js public/index.css
gzip -c public/postscript.js | wc -c
gzip -c public/index.css | wc -c
```

## 附錄 B：Phase 1 baseline 參考

完整 Phase 1 數字見 `docs/superpowers/baselines/2026-04-24-perf-baseline.md`（本 repo 實際檔名）。
