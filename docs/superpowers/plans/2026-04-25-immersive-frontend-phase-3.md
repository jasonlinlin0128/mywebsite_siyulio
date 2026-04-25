# Immersive Frontend — Phase 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 Phase 1 + 2 建好的 motion runtime 與首頁推到「分類頁 + 文章頁」全站統一視覺：每個分類頁拿到自己的 `CategoryHero`（scroll-driven cinematic timeline 把 sectionThemes.sceneObjects 編隊），每篇文章拿到 `ArticleHero`（section-themed canvas 60vh 封面 + sticky TOC 高亮當前段落），popover 預覽自動跳過 hero 直接秀內文。frontmatter 支援 `cover:` / `accent:` / `hero-style:` 三個可選欄位讓作者覆寫預設行為。

**Architecture:**
- 新組件 `ArticleHero.tsx` + `CategoryHero.tsx` 進 `quartz/components/`，分別取代 `defaultContentPageLayout.beforeBody` 中的 `ArticleTitle + ContentMeta` 與 `defaultListPageLayout.beforeBody` 中的 `BrandIntro + ArticleTitle`。`BrandIntro` / `ArticleTitle` / `ContentMeta` 三檔留在 repo（§15.3 可刪但 Phase 4 才決定），其中 `ArticleTitle` 還會被 `hero-style: none` fallback 路徑用到。
- Phase 2 預留的 `sectionCanvas.inline.ts` 三個 dormant renderer（`geometric-lines` / `particle-flow` / `steam-curves`）由 Phase 3 填上實作，`ArticleHero` 透過 `window.__sectionCanvas.render(host, config)` 呼叫對應 section 的 canvas 視覺（資料來源是 Phase 1 已擴充的 `sectionThemes.motionConfig` 欄位）。
- `CategoryHero` 走另一條路：保留既有 `sectionThemes.sceneObjects` HTML 物件清單，搭配新 `categoryScene.inline.ts` 用 GSAP ScrollTrigger 做「物件飄入 → 重新編隊 → 散開淡出」的 scroll-driven timeline。新 inline script 是 Phase 2 8 支之外的第 9 支，照樣由 `MotionRuntime` 透過 `concatenateResources` 接進 `afterDOMLoaded`。
- Sticky TOC 不新增組件，直接複用 Phase 1+2 之前已存在的 `Component.TableOfContents()`，把它放進 `defaultContentPageLayout.right: [DesktopOnly(...)]`，加新 SCSS partial `_toc-sticky.scss` 處理 `position: sticky` + 當前段落高亮；對應的 `.active` class 由 `toc.inline.ts` 在既有 IntersectionObserver 上補一條規則設定。
- Popover × ArticleHero 碰撞：Phase 1 已寫好 `_popover-immersive.scss`（dormant；CSS 隱藏 `.article-hero` / `.scroll-progress` / `.breadcrumbs`），Phase 3 一旦 `ArticleHero` 實際 render，CSS 規則自動匹配生效；外加新 `popoverScroll.inline.ts` 用 `MutationObserver` 觀察 `.popover-inner` 出現後 `requestAnimationFrame` scroll 到第一個 `<p>/h2/h3/pre/ul/ol`，避免 popover 開出來看到一段空白。
- `quartz.layout.ts` 按 spec §15.2 改寫成 frontmatter-aware：`hero-style: "none"` 的頁面走「Breadcrumbs + ArticleTitle」極簡 fallback；其他頁面走「Breadcrumbs + ArticleHero」。`right: []` 從空的改成 `[Component.DesktopOnly(Component.TableOfContents())]`。`defaultListPageLayout.beforeBody` 的 `BrandIntro` 換成 `CategoryHero`（`ArticleTitle` 一起拿掉因為 CategoryHero 已含 H1）。

**Tech Stack:** Quartz 4.5.2 (Preact SSR + TSX + SCSS), GSAP 3.12.7 + ScrollTrigger（Phase 1 vendored, Phase 2 已動態載入），純 Canvas 2D（`sectionCanvas` 三個 renderer），TypeScript。沿用 Phase 1 + 2 的 `window.__motion` / `window.__nav` / `window.__gsapLoader` / `window.__sectionCanvas` 全域介面。

**Spec reference:** [2026-04-24-immersive-frontend-design.md](../specs/2026-04-24-immersive-frontend-design.md) §3.2（section accent 色票）、§4.1（三層架構）、§4.4（motionConfig）、§5.2（CategoryHero 版型）、§5.3（ArticleHero 版型）、§6.3（popover × hero）、§7（canvas 策略）、§8（a11y / 降級）、§10 Phase 3、§15（layout diff）。

**Phase 1 + 2 前置依賴（必須先 ship）：**
- Phase 1：`MotionRuntime` 已掛、`window.__motion` / `window.__nav` / `window.__gsapLoader` 可用、`_motion-tokens.scss` 與 `_popover-immersive.scss` 已 wire、vendored GSAP + ScrollTrigger 在 `static/vendor/`。
- Phase 2：`HomeHeroApple` 已 render、`focalCanvas.inline.ts` + `sectionCanvas.inline.ts`（dormant）已進 bundle、`window.__sectionCanvas.render` API 已暴露、`lenis.inline.ts` + Search × Lenis 整合已上線、`CustomHead` Google Fonts preload 已切換、`heroCinematic.inline.ts` GSAP timeline + stats count-up 已運作、Matter.js / `_home-apple.scss` 重命名 / Featured 3-col grid 等清理已完成。Phase 2 的 `sectionThemes.motionConfig` + `sectionThemes.sceneObjects` 兩個欄位完整保留供 Phase 3 取用。
- 若上述任一未滿足，先回頭補 Phase 1 / 2。

**Commit convention (per user CLAUDE.md):** Conventional Commits + trailing `Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>`（**不**使用預設 Claude 簽名）。Phase 3 預期 10 個 commit（每 Task 一個，外加必要的 review fix），每個 commit 後 `npx quartz build` 必須能成功。

---

## File Structure

### New files

| Path | 職責 |
|-----|------|
| `quartz/components/ArticleHero.tsx` | 文章頁 hero 60vh：Breadcrumbs 已在 layout 之外；hero 內含 SectionBadge + h1（72px）+ meta（date · 閱讀時間）+ section-themed canvas 容器；讀 frontmatter `cover` / `accent` / `hero-style` |
| `quartz/components/CategoryHero.tsx` | 分類頁 hero 75vh：取代 `BrandIntro`，含 eyebrow + h1（96px）+ description + scroll-driven 物件 stage（沿用 `sectionThemes.sceneObjects`） |
| `quartz/components/SectionBadge.tsx` | 文章頁 hero 內的 section 歸屬小標（spec §4.1 Layer 3），可重用元件 |
| `quartz/components/scripts/categoryScene.inline.ts` | CategoryHero 物件 scroll-driven cinematic timeline（GSAP ScrollTrigger，`__gsapLoader.loadGsap()`），sceneObjects 飄入 → 重新編隊 → 散開淡出 |
| `quartz/components/scripts/popoverScroll.inline.ts` | spec §6.3 Phase 3：MutationObserver 觀察 `.popover-inner` DOM 插入，rAF 後 scrollTop 到第一個 `<p>/h2/h3/pre/ul/ol` 元素 |
| `quartz/styles/_article-hero.scss` | ArticleHero 樣式（`.article-hero`, `.article-hero__copy`, `.article-hero__title`, `.article-hero__meta`, `.article-hero__canvas`, `.section-badge`, hero-style 變體） |
| `quartz/styles/_category-hero.scss` | CategoryHero 樣式（`.category-hero`, `.category-hero__copy`, `.category-hero__stage`, `.category-scene-object`，含 `--accent` 與 reduced-motion fallback） |
| `quartz/styles/_toc-sticky.scss` | TOC sticky positioning + `.toc-content a.active` 當前段落高亮樣式（spec §5.3 v3） |
| `quartz/docs/superpowers/baselines/2026-04-25-phase3-verification.md` | Phase 3 手動 regression + feature 驗證紀錄（自動部分先填、人類 fill manual） |
| `quartz/docs/superpowers/baselines/2026-04-25-lighthouse-after-phase3.md` | Phase 3 完成後 Lighthouse 分數對照 Phase 1 / Phase 2 baseline |

### Modified files

| Path | 改動 |
|-----|------|
| `quartz/components/scripts/sectionCanvas.inline.ts` | 三個 dormant renderer（`renderGeometricLines` / `renderParticleFlow` / `renderSteamCurves`）填上實作；`render(host, config)` 主函數實際開始 rAF + dpr scale + visibilitychange + FPS rolling-avg 降級 + cleanup。`window.__sectionCanvas.render` 不變（API 兼容） |
| `quartz/components/scripts/toc.inline.ts` | 既有 IntersectionObserver 補一條規則：當某個 `<section>` 進入 viewport 時對 `.toc-content a[data-for="{id}"]` 加 `.active` class（同時移除其他 `.active`），不影響原本 `.in-view` class 行為 |
| `quartz/components/styles/toc.scss` | 不動本身（upstream Quartz 檔），改在 `_toc-sticky.scss` 加額外規則 `@use` 進來 |
| `quartz/components/MotionRuntime.tsx` | `concatenateResources` 加 2 支：`categoryScene` + `popoverScroll`；JSDoc 載入順序更新從 8 → 10 |
| `quartz/components/index.ts` | export `ArticleHero` + `CategoryHero` + `SectionBadge` |
| `quartz/styles/custom.scss` | `@use "./_article-hero.scss"` + `@use "./_category-hero.scss"` + `@use "./_toc-sticky.scss"` |
| `quartz.layout.ts` | spec §15.2 v3 改寫：`defaultContentPageLayout.beforeBody` 加 frontmatter-aware ConditionalRender（`hero-style: "none"` 走 ArticleTitle fallback、其他走 ArticleHero）、`right: []` → `[DesktopOnly(TableOfContents())]`；`defaultListPageLayout.beforeBody` 從 `[BrandIntro, ArticleTitle]` 改成 `[Breadcrumbs, CategoryHero]` |

### Files NOT deleted (per spec §15.3)

| Path | 理由 |
|-----|-----|
| `quartz/components/BrandIntro.tsx` | 功能已併入 `CategoryHero`，不再進 layout，但檔案保留；Phase 4 audit 後再決定刪除 |
| `quartz/components/scripts/sectionScene.inline.ts` | `BrandIntro` 的 driver；layout 不再用 `BrandIntro` 代表此 script 也不再實際綁到 DOM；保留待 Phase 4 一併清 |
| `quartz/components/ArticleTitle.tsx` | `hero-style: "none"` fallback 路徑要用到；**不刪** |
| `quartz/components/ContentMeta.tsx` | 功能併入 `ArticleHero`，layout 不再用，但 Phase 4 才刪 |

---

## Task 1: SCSS partials skeleton — `_article-hero.scss` + `_category-hero.scss` + `_toc-sticky.scss`

**Files:**
- Create: `quartz/styles/_article-hero.scss`
- Create: `quartz/styles/_category-hero.scss`
- Create: `quartz/styles/_toc-sticky.scss`
- Modify: `quartz/styles/custom.scss`（三個 `@use`，**尚不刪舊規則**）

**這一步 feature flag 關**：新樣式檔先進，但 `quartz.layout.ts` 還沒改、組件未 export → 沒有對應 DOM，CSS 規則匹配為空，零 side effect。沿用 Phase 2 Task 1 的「先佈樣式骨架」模式。

- [ ] **Step 1: 寫 `_article-hero.scss`（BEM + frontmatter 變體支援）**

Create `quartz/styles/_article-hero.scss`:

```scss
// ArticleHero 樣式（spec §5.3）
// hero-style 變體：themed（預設）、minimal（純 title + meta，無 canvas）
// frontmatter cover / accent 由 ArticleHero.tsx 透過 inline style 注入

@use "./_motion-tokens";

.article-hero {
  position: relative;
  box-sizing: border-box;
  min-height: 60vh;
  display: grid;
  grid-template-rows: 1fr auto;
  align-items: end;
  padding: clamp(2rem, 4vw, 4rem) clamp(1.5rem, 4vw, 3rem) clamp(2rem, 4vw, 4rem);
  margin-bottom: clamp(2rem, 4vw, 3rem);
  border-radius: 28px;
  overflow: hidden;
  isolation: isolate;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--article-hero-accent, var(--dark)) 18%, transparent) 0%,
    transparent 100%
  );

  // section accent CSS var：ArticleHero TSX 會 inline-style 設此值
  --article-hero-accent: var(--section-accent-manufacturing);

  &[data-section-theme="ai-notes"] { --article-hero-accent: var(--section-accent-ai-notes); }
  &[data-section-theme="coffee"]   { --article-hero-accent: var(--section-accent-coffee); }
  &[data-section-theme="about"]    { --article-hero-accent: rgba(160, 160, 160, 0.6); }

  @media all and (max-width: 767px) {
    min-height: 40vh;
    border-radius: 22px;
    padding: 1.6rem 1.2rem;
    margin-bottom: 1.5rem;
  }
}

// canvas 容器：絕對定位塞滿 hero，文字蓋在上面
.article-hero__canvas-host {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;

  canvas {
    width: 100%;
    height: 100%;
    display: block;
    opacity: 0.85;
  }
}

// frontmatter cover 圖：取代 canvas
.article-hero__cover {
  position: absolute;
  inset: 0;
  z-index: 0;
  background-size: cover;
  background-position: center;
  pointer-events: none;

  &::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
      0deg,
      color-mix(in srgb, var(--article-hero-accent) 40%, transparent) 0%,
      transparent 60%
    );
  }
}

.article-hero__copy {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 0.85rem;
  max-width: 44rem;
  justify-self: end;  // spec §5.3：「右下角覆文字」
  text-align: left;
  align-self: end;

  @media all and (max-width: 767px) {
    justify-self: stretch;
    gap: 0.7rem;
  }
}

.article-hero__title {
  margin: 0;
  font-family: var(--headerFont), "Outfit", sans-serif;
  font-weight: 800;
  // 72px display target；CJK 密度比照 Phase 2 home hero 的 64px：72px / 1.4 ≈ 51px CJK
  // 但文章頁標題比首頁長，用較寬的 clamp 區間並留 line-height 1.25 給 CJK 換行
  font-size: clamp(1.7rem, 3.4vw, 3.2rem);
  line-height: 1.25;
  letter-spacing: -0.01em;
}

.article-hero__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.85rem;
  opacity: 0.78;

  time { font-feature-settings: "tnum" 1; }
  .article-hero__reading-time::before { content: "·"; margin-right: 0.6rem; opacity: 0.6; }
}

// hero-style: "minimal" — 沒 canvas、沒 gradient，純 title + meta
.article-hero[data-hero-style="minimal"] {
  min-height: auto;
  background: none;
  padding: 1.2rem 0 0.8rem;
  border-radius: 0;
  margin-bottom: 1rem;

  .article-hero__canvas-host,
  .article-hero__cover { display: none; }

  .article-hero__copy { justify-self: stretch; }

  .article-hero__title {
    font-size: clamp(1.4rem, 2.4vw, 2rem);
  }
}

// SectionBadge — 小型 section 歸屬標籤
.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--article-hero-accent) 50%, transparent);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--article-hero-accent);
  background: color-mix(in srgb, var(--article-hero-accent) 8%, transparent);
  transition: background var(--motion-duration-fast) var(--motion-easing);

  &:hover {
    background: color-mix(in srgb, var(--article-hero-accent) 16%, transparent);
  }
}

// reduced-motion：去掉 gradient 動畫；canvas script 自身會只畫第一幀
@media (prefers-reduced-motion: reduce) {
  .article-hero { transition: none; }
}

// forced-colors / prefers-contrast — spec §8.6
@media (forced-colors: active) {
  .article-hero__canvas-host,
  .article-hero__cover { display: none; }
}
```

- [ ] **Step 2: 寫 `_category-hero.scss`**

Create `quartz/styles/_category-hero.scss`:

```scss
// CategoryHero 樣式（spec §5.2）
// 取代 BrandIntro。布局：左側 copy / 右側 scene stage（單欄 mobile）
// 場景物件由 sectionThemes.sceneObjects 走 SSR，inline.ts 用 GSAP scroll-scrub 編隊

@use "./_motion-tokens";

.category-hero {
  position: relative;
  box-sizing: border-box;
  min-height: 75vh;
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(280px, 1fr);
  gap: clamp(1.5rem, 3vw, 2.8rem);
  align-items: center;
  padding: clamp(2.5rem, 5vw, 5rem) clamp(1.5rem, 4vw, 3rem) clamp(3rem, 6vw, 6rem);
  overflow: hidden;
  isolation: isolate;

  --category-hero-accent: var(--section-accent-manufacturing);
  &[data-section-theme="ai-notes"] { --category-hero-accent: var(--section-accent-ai-notes); }
  &[data-section-theme="coffee"]   { --category-hero-accent: var(--section-accent-coffee); }
  &[data-section-theme="about"]    { --category-hero-accent: rgba(160, 160, 160, 0.6); }

  @media all and (max-width: 767px) {
    grid-template-columns: 1fr;
    min-height: auto;
    padding: 3rem 1.2rem;
    gap: 1.6rem;
  }
}

.category-hero__copy {
  display: grid;
  gap: 1rem;
  max-width: 36rem;
  align-content: center;
}

.category-hero__eyebrow {
  margin: 0;
  font-size: 0.85rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.75;
  color: var(--category-hero-accent);
}

.category-hero__title {
  margin: 0;
  font-family: var(--headerFont), "Outfit", sans-serif;
  font-weight: 800;
  // 96px target；CJK ~64px。比 ArticleHero 大但比 HomeHeroApple 略小
  font-size: clamp(2rem, 4.5vw, 4.5rem);
  line-height: 1.18;
  letter-spacing: -0.012em;
}

.category-hero__copy-text {
  margin: 0;
  font-size: clamp(1rem, 1.1vw, 1.15rem);
  line-height: 1.65;
  opacity: 0.82;
}

// scene stage — 物件 absolute 在這個容器內定位
.category-hero__stage {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 320px;
  aspect-ratio: 5 / 4;
  max-height: min(60vh, 520px);

  @media all and (max-width: 767px) {
    aspect-ratio: 16 / 10;
    max-height: 32vh;
    order: -1;
  }
}

// scene 物件 — sectionThemes.sceneObjects.variant 對應不同 visual class
.category-scene-object {
  position: absolute;
  width: var(--size, 80px);
  aspect-ratio: 1;
  left: var(--x, 50%);
  top: var(--y, 50%);
  transform: translate(-50%, -50%) rotate(var(--rotate, 0deg));
  border-radius: 50%;
  background: radial-gradient(
    circle at 35% 30%,
    color-mix(in srgb, var(--category-hero-accent) 80%, white) 0%,
    color-mix(in srgb, var(--category-hero-accent) 30%, transparent) 70%
  );
  opacity: 0.6;
  pointer-events: none;
  // categoryScene.inline.ts 會用 GSAP 在 scroll progress 0%-100% 之間
  // 動 transform 的 translate / rotate / opacity；CSS 提供 SSR 起手位置

  // 物件 variant 微調（取代舊 BrandIntro 的 brand-object--*）
  // sectionThemes 共有 12 種 variant：module / ring / node / beam / pill /
  // pulse / spark / bean / orbit / core / satellite / trace（code-reviewer
  // B2 抓到 v1 草案只覆蓋 6 種；補齊全部）
  &[data-variant="module"]    { border-radius: 8px; aspect-ratio: 1.2 / 1; }
  &[data-variant="ring"]      { background: none; border: 2px solid var(--category-hero-accent); opacity: 0.5; }
  &[data-variant="node"]      { border-radius: 50%; transform-origin: center; }
  &[data-variant="beam"]      { border-radius: 6px; height: 4px; aspect-ratio: auto; width: var(--size); background: linear-gradient(90deg, transparent, var(--category-hero-accent), transparent); opacity: 0.7; }
  &[data-variant="pill"]      { border-radius: 999px; aspect-ratio: 2 / 1; }
  &[data-variant="pulse"]     { background: radial-gradient(circle, var(--category-hero-accent) 0%, transparent 70%); }
  &[data-variant="spark"]     { border-radius: 2px; transform-origin: center; opacity: 0.7; }
  &[data-variant="bean"]      { border-radius: 30% 70% 70% 30% / 60% 60% 40% 40%; }
  &[data-variant="orbit"]     { background: none; border: 1px solid color-mix(in srgb, var(--category-hero-accent) 50%, transparent); opacity: 0.4; }
  &[data-variant="core"]      { border-radius: 50%; opacity: 0.85; }
  &[data-variant="satellite"] { border-radius: 50%; opacity: 0.5; }
  &[data-variant="trace"]     { background: none; border-top: 1px dashed color-mix(in srgb, var(--category-hero-accent) 40%, transparent); height: 2px; aspect-ratio: auto; width: var(--size); opacity: 0.45; }
}

// reduced-motion：物件保持 SSR 位置不動畫，但仍可見
@media (prefers-reduced-motion: reduce) {
  .category-scene-object { transition: none; }
}

@media (forced-colors: active) {
  .category-hero__stage { display: none; }
}
```

- [ ] **Step 3: 寫 `_toc-sticky.scss`（spec §5.3 v3 active class 規範）**

Create `quartz/styles/_toc-sticky.scss`:

```scss
// Sticky TableOfContents（spec §5.3）
// 不改 upstream Quartz toc.scss，加 layered overrides 做兩件事：
//   1. position: sticky 讓 TOC 在文章頁右側跟著捲動
//   2. .toc-content a.active 用當前 section accent 高亮
// active class 由 toc.inline.ts 的 IntersectionObserver 設定（Task 7）

.right.sidebar .toc {
  position: sticky;
  top: clamp(1rem, 4vh, 7.5rem);
  max-height: calc(100vh - 9rem);
  overflow-y: auto;
  // 隱藏 scrollbar 但保持可滾（Apple 風）
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;

  &:hover {
    scrollbar-color: rgba(255, 247, 234, 0.18) transparent;
  }
}

// section accent 跟隨頁面 — 從 ArticleHero 的 data-section-theme inherit
// （這個 var 在 _article-hero.scss 已定義）
// Quartz renderPage.tsx 實際輸出 `<div class="right sidebar">`（兩個獨立 class，
// 空白分隔），所以 selector 用 `.right.sidebar`（兩個 class 同元素）；用
// `.right-sidebar` 會匹配不到任何元素 — code-reviewer B1 抓到的 bug。
.right.sidebar {
  --toc-active-color: var(--article-hero-accent, var(--dark));
}

// code-reviewer S3：specificity 拉高一階（雙 .active）避免依賴 toc.scss /
// _toc-sticky.scss 的 @use 順序。雙 class 是合法 CSS，瀏覽器處理為
// `<a class="active">` 同時擁有兩個 .active class 也匹配，所以實際選同一
// 個元素，但特異性比單 .active 高一階。
.toc-content a.active.active {
  color: var(--toc-active-color);
  font-weight: 600;
  transition: color var(--motion-duration-fast) var(--motion-easing);
}

// in-view 是 Quartz 既有 class（toc.inline.ts 設）— 用比 active 更弱的視覺
// 兩者都生效時 active 優先（CSS specificity 一樣，後寫覆蓋前寫，OK 因為 toc.scss 先 @use）
.toc-content a.in-view:not(.active) {
  opacity: 0.85;
}

@media (prefers-reduced-motion: reduce) {
  .toc-content a.active { transition: none; }
}
```

- [ ] **Step 4: Wire 三個 partial 進 `custom.scss`**

Modify `quartz/styles/custom.scss` — 在現有 `@use "./_home-apple.scss";` 後面加三行：

```scss
@use "./base.scss";
@use "./_motion-tokens.scss";
@use "./_popover-immersive.scss";
@use "./_lenis.scss";
@use "./_home-apple.scss";
@use "./_article-hero.scss";    // Phase 3 新增
@use "./_category-hero.scss";   // Phase 3 新增
@use "./_toc-sticky.scss";      // Phase 3 新增
```

- [ ] **Step 5: Build 驗證**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
npx quartz build 2>&1 | tail -5
```

預期：build 成功無 warning。

```bash
grep -oE "article-hero|category-hero|category-scene-object|section-badge|toc-content a.active" public/index.css | sort -u
# 預期：5 個 selector 都出現
```

首頁 / 分類頁 / 文章頁視覺**完全不變**（沒有對應 DOM）。

- [ ] **Step 6: Commit**

```bash
git add quartz/styles/_article-hero.scss \
  quartz/styles/_category-hero.scss \
  quartz/styles/_toc-sticky.scss \
  quartz/styles/custom.scss

git commit -m "$(cat <<'EOF'
feat: Phase 3 SCSS partials skeleton (ArticleHero / CategoryHero / Sticky TOC)

依 spec §5.2 / §5.3 / §15 預先建立三個樣式檔，讓 Task 3-9 的 TSX 組件
可以直接用對應 BEM class，不需要再回頭加 CSS：

- _article-hero.scss：60vh hero、section accent 漸層、cover 圖支援、
  hero-style="minimal" 變體、forced-colors fallback
- _category-hero.scss：75vh hero、左 copy / 右 scene stage 雙欄、6 個
  variant 物件（ring / bean / orbit / core / beam / pulse）SSR 起手樣式
- _toc-sticky.scss：position: sticky + .toc-content a.active 高亮（spec
  §5.3 v3 規範），覆寫 Quartz upstream toc.scss 不動原檔

此 commit 對外視覺零變化（組件未 export、layout 未改 → CSS 匹配為空）。
Task 3-9 對應 layout / TSX 改動才會讓樣式真的生效。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 2: `sectionCanvas.inline.ts` — 三個真實 renderer 實作

**Files:**
- Modify: `quartz/components/scripts/sectionCanvas.inline.ts`

**這一步把 Phase 2 的 dormant API stub 升級為實際可繪製**：`render(host, config)` 從回傳 no-op cleanup 改成實際 attach `<canvas>` 到 host、開 `requestAnimationFrame` 迴圈、配合 visibilitychange 暫停 / FPS rolling-avg 降級 / dpr scale / cleanup 釋放。三個 renderer 函數體（`renderGeometricLines` / `renderParticleFlow` / `renderSteamCurves`）填上實作。**API surface 不動** — `window.__sectionCanvas.render(host, config)` 簽章與回傳形狀（`() => void` cleanup）保持兼容，呼叫方（Task 3 的 `ArticleHero`）不需先動。

此 commit 後 `[data-home-hero-focal]` 還是只給首頁 focalCanvas，`__sectionCanvas` 仍然沒有實際呼叫者（Task 3 才接），但腳本實作已就位。

- [ ] **Step 1: 替換 `sectionCanvas.inline.ts` 為實作版**

Replace `quartz/components/scripts/sectionCanvas.inline.ts` with:

```ts
// Section-themed canvas renderer (spec §7 + §4.4)
// Phase 3 實作版：替換 Phase 2 的 dormant stub。API 簽章不變。
//
// 由 ArticleHero（Task 3）在 `nav` 事件呼叫：
//   const cleanup = window.__sectionCanvas.render(host, {
//     renderer: 'geometric-lines',
//     glowColor: 'rgba(200,169,107,0.24)',
//     particleDensity: 30,
//   })
// 在 prenav / cleanup 階段呼叫回傳的 cleanup() 釋放 rAF / canvas / listener。

export type SectionCanvasRenderer = "geometric-lines" | "particle-flow" | "steam-curves"

export interface SectionCanvasConfig {
  renderer: SectionCanvasRenderer
  glowColor: string
  particleDensity: number
}

declare const window: Window & {
  __sectionCanvas?: {
    render: (host: HTMLElement, config: SectionCanvasConfig) => () => void
  }
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
}

interface RendererFn {
  (ctx: CanvasRenderingContext2D, w: number, h: number, t: number, config: SectionCanvasConfig): void
}

// ── 1. geometric-lines（manufacturing-ai 主題）──────────────────────────────
//   等距斜線 + 緩慢平移；glowColor 控制線條顏色 alpha 與 glow
function renderGeometricLines(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  config: SectionCanvasConfig,
): void {
  ctx.clearRect(0, 0, w, h)

  const spacing = Math.max(48, w / Math.max(8, config.particleDensity))
  const drift = (t * 0.012) % spacing
  ctx.strokeStyle = config.glowColor
  ctx.lineWidth = 1
  ctx.lineCap = "round"

  // 對角線（左上 → 右下）
  for (let i = -h; i < w + h; i += spacing) {
    ctx.beginPath()
    ctx.moveTo(i + drift, 0)
    ctx.lineTo(i + drift + h, h)
    ctx.stroke()
  }

  // 中心 glow（Apple 風主視覺光暈）
  const cx = w * 0.7
  const cy = h * 0.5
  const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * 0.4)
  grad.addColorStop(0, config.glowColor)
  grad.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, w, h)
}

// ── 2. particle-flow（ai-notes 主題）────────────────────────────────────────
//   緩動粒子場 + 偶發光點，配 glowColor 漸層
const PARTICLE_STATE_KEY = "__pflow"
type ParticleState = {
  particles: Array<{ x: number; y: number; vx: number; vy: number; r: number; alpha: number }>
  initialized: boolean
}

function renderParticleFlow(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  _t: number,
  config: SectionCanvasConfig,
): void {
  // canvas element-level state（避免每幀重新分配）
  const canvas = ctx.canvas as HTMLCanvasElement & { [PARTICLE_STATE_KEY]?: ParticleState }
  let state = canvas[PARTICLE_STATE_KEY]
  if (!state || !state.initialized) {
    const count = config.particleDensity
    state = {
      initialized: true,
      particles: Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: 1 + Math.random() * 2,
        alpha: 0.3 + Math.random() * 0.4,
      })),
    }
    canvas[PARTICLE_STATE_KEY] = state
  }

  ctx.clearRect(0, 0, w, h)

  // 背景漸層
  const grad = ctx.createLinearGradient(0, 0, w, h)
  grad.addColorStop(0, config.glowColor)
  grad.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, w, h)

  // 粒子
  for (const p of state.particles) {
    p.x += p.vx
    p.y += p.vy
    if (p.x < 0 || p.x > w) p.vx *= -1
    if (p.y < 0 || p.y > h) p.vy *= -1
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(255, 247, 234, ${p.alpha})`
    ctx.fill()
  }
}

// ── 3. steam-curves（coffee 主題）──────────────────────────────────────────
//   多條正弦曲線交錯往上飄，模擬蒸氣
function renderSteamCurves(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  config: SectionCanvasConfig,
): void {
  ctx.clearRect(0, 0, w, h)

  // 背景暖色光暈
  const cx = w * 0.5
  const cy = h * 0.7
  const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * 0.5)
  grad.addColorStop(0, config.glowColor)
  grad.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, w, h)

  // 蒸氣曲線：N 條 sin wave，每條的相位 + 振幅不同
  const curveCount = Math.max(3, Math.floor(config.particleDensity / 8))
  ctx.strokeStyle = config.glowColor
  ctx.lineWidth = 1.5

  for (let i = 0; i < curveCount; i++) {
    const phase = (t * 0.0006) + i * 0.7
    const xCenter = w * (0.2 + (i / curveCount) * 0.6)
    const amplitude = 18 + i * 6

    ctx.beginPath()
    for (let y = h; y > 0; y -= 4) {
      const progress = (h - y) / h
      const x = xCenter + Math.sin(progress * Math.PI * 2 + phase) * amplitude * progress
      if (y === h) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.globalAlpha = 0.6 - i * 0.1
    ctx.stroke()
  }
  ctx.globalAlpha = 1
}

const renderers: Record<SectionCanvasRenderer, RendererFn> = {
  "geometric-lines": renderGeometricLines,
  "particle-flow": renderParticleFlow,
  "steam-curves": renderSteamCurves,
}

// ── 主渲染函數 ─────────────────────────────────────────────────────────────
function render(host: HTMLElement, config: SectionCanvasConfig): () => void {
  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  const mobile = window.__motion?.isMobileViewport?.() ?? false

  // 找/建 canvas
  let canvas = host.querySelector<HTMLCanvasElement>(":scope > canvas")
  if (!canvas) {
    canvas = document.createElement("canvas")
    canvas.setAttribute("aria-hidden", "true")
    canvas.setAttribute("role", "presentation")
    host.appendChild(canvas)
  }
  const ctx = canvas.getContext("2d")
  if (!ctx) return () => {}

  const dpr = mobile ? Math.min(window.devicePixelRatio || 1, 1.5) : window.devicePixelRatio || 1
  let w = 0
  let h = 0
  let resizeObs: ResizeObserver | null = null
  let rafId = 0
  let timeoutId = 0
  let lastFrame = 0
  let frameTimes: number[] = []
  let lowPowerMode = false
  let onVisibilityChange: (() => void) | null = null

  function resize() {
    const rect = host.getBoundingClientRect()
    w = Math.max(1, rect.width)
    h = Math.max(1, rect.height)
    canvas!.width = Math.floor(w * dpr)
    canvas!.height = Math.floor(h * dpr)
    canvas!.style.width = `${w}px`
    canvas!.style.height = `${h}px`
    ctx!.scale(dpr, dpr)
    // particle-flow 的快取 state 失效（resize 後座標範圍變了）
    delete (canvas as any)[PARTICLE_STATE_KEY]
  }
  resize()

  const renderer = renderers[config.renderer]

  function loop(t: number) {
    if (document.hidden) {
      rafId = requestAnimationFrame(loop)
      return
    }

    // FPS rolling avg（spec §7：30-frame avg > 22ms 切 low-power）
    if (lastFrame > 0) {
      const dt = t - lastFrame
      frameTimes.push(dt)
      if (frameTimes.length > 30) frameTimes.shift()
      if (frameTimes.length === 30) {
        const avg = frameTimes.reduce((a, b) => a + b, 0) / 30
        // One-way switch: no hysteresis back to high-power. Prevents flapping at threshold.
        if (avg > 22 && !lowPowerMode) lowPowerMode = true
      }
    }
    lastFrame = t

    renderer(ctx!, w, h, t, config)

    if (lowPowerMode) {
      timeoutId = window.setTimeout(() => {
        timeoutId = 0
        rafId = requestAnimationFrame(loop)
      }, 33)
    } else {
      rafId = requestAnimationFrame(loop)
    }
  }

  // Reduced-motion：只畫第一幀，不啟 loop
  if (reduced) {
    renderer(ctx, w, h, 0, config)
  } else {
    renderer(ctx, w, h, 0, config)
    lastFrame = performance.now()
    rafId = requestAnimationFrame(loop)
  }

  resizeObs = new ResizeObserver(() => resize())
  resizeObs.observe(host)

  return () => {
    cancelAnimationFrame(rafId)
    rafId = 0
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = 0
    }
    resizeObs?.disconnect()
    resizeObs = null
    if (onVisibilityChange) {
      document.removeEventListener("visibilitychange", onVisibilityChange)
      onVisibilityChange = null
    }
    frameTimes = []
    lowPowerMode = false
    lastFrame = 0
    delete (canvas as any)[PARTICLE_STATE_KEY]
  }
}

window.__sectionCanvas = { render }
```

- [ ] **Step 2: Build 驗證 + bundle marker check**

```bash
npx quartz build 2>&1 | tail -5
grep -oE "geometric-lines|particle-flow|steam-curves|__sectionCanvas" public/postscript.js | sort -u
# 預期：4 個關鍵字都在
```

桌機開首頁 console：

```js
typeof window.__sectionCanvas?.render
// 預期："function"
// 不要實際 call — Task 3 才有適合的 host element
```

- [ ] **Step 3: Commit**

```bash
git add quartz/components/scripts/sectionCanvas.inline.ts
git commit -m "$(cat <<'EOF'
feat: sectionCanvas 三個 renderer 實作（geometric-lines / particle-flow / steam-curves）

把 Phase 2 預留的 dormant stub 升級為實際 canvas 繪製。API 簽章不變
（window.__sectionCanvas.render(host, config) → cleanup fn），呼叫方
不用先動。

三個 renderer：
- geometric-lines (manufacturing-ai)：等距斜線緩慢平移 + 中心暖金 glow
- particle-flow (ai-notes)：緩動粒子場 + 線性漸層底
- steam-curves (coffee)：多條 sin 蒸氣曲線 + 暖底光暈

主渲染函數 render() 完整實作：
- canvas 自動 attach 到 host（aria-hidden + role=presentation）
- dpr scale（mobile cap 1.5）+ ResizeObserver
- visibilitychange guard via document.hidden in loop
- 30-frame rolling-avg FPS 降級（>22ms → setTimeout 30fps，one-way）
- prefers-reduced-motion 只畫第一幀
- cleanup 釋放 rAF / timeout / observer / 粒子快取

Task 3 的 ArticleHero 會在 nav handler 呼叫 render()，傳入 sectionThemes
.motionConfig 的 renderer + glowColor + particleDensity。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 3: `ArticleHero.tsx` 組件

**Files:**
- Create: `quartz/components/ArticleHero.tsx`
- Modify: `quartz/components/index.ts`

**這一步建組件骨架**，但 `quartz.layout.ts` 還沒掛它（Task 9）→ build 後 `[data-section-hero-canvas]` 還找不到節點，`window.__sectionCanvas.render` 仍無人呼叫，現有頁面行為不變。

`ArticleHero` 透過 `afterDOMLoaded` 串接一支小 inline script（不另起 file，直接 inline 寫在組件內 const 字串）來呼叫 `window.__sectionCanvas.render`，並依 `frontmatter` 的 `cover` / `accent` / `hero-style` 改變 render 行為。

- [ ] **Step 1: 寫 `SectionBadge.tsx`（小型 reusable badge）**

Create `quartz/components/SectionBadge.tsx`:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { getSectionThemeForSlug } from "./sectionThemes"

/**
 * SectionBadge — section 歸屬小標（spec §4.1 Layer 3）
 * 用在 ArticleHero 內的 hero 角落，連回該 section 入口。
 * 若 slug 對應不到任何 section（例如 about 子頁），回傳 null。
 */
export default (() => {
  const SectionBadge: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const theme = getSectionThemeForSlug(slug)
    if (!theme) return null

    return (
      <a
        class="section-badge"
        href={resolveRelative(slug, theme.href)}
        data-section-theme={theme.key}
      >
        {theme.label}
      </a>
    )
  }

  return SectionBadge
}) satisfies QuartzComponentConstructor
```

- [ ] **Step 2: 寫 `ArticleHero.tsx`（含 inline script for sectionCanvas wiring）**

Create `quartz/components/ArticleHero.tsx`:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { Date as DateComp, getDate } from "./Date"
import readingTime from "reading-time"
import { i18n } from "../i18n"
import { getSectionThemeForSlug } from "./sectionThemes"
import SectionBadge from "./SectionBadge"

/**
 * ArticleHero — 文章頁 60vh hero（spec §5.3）
 * 完整取代既有 ArticleTitle + ContentMeta（在 quartz.layout.ts 的 v3 版本中）。
 *
 * Frontmatter 支援：
 *   cover:        URL 或相對路徑 → 取代 canvas 用 <img> 背景
 *   accent:       hex / rgb 字串 → 透過 inline-style 覆蓋 --article-hero-accent
 *   hero-style:   "themed"（預設） | "minimal" | "none"
 *                 "none" 已在 layout 端轉走 ArticleTitle fallback path，這裡不會收到
 *
 * Canvas 啟動：透過 afterDOMLoaded 注入小段 inline JS，由 nav 事件呼叫
 *   window.__sectionCanvas.render(host, config)，prenav 時呼叫 cleanup。
 */

// code-reviewer S5：navGeneration token defense — 雖然 setup 是 sync，仍
// 對 cleanup ↔ render 之間 prenav 競賽做防禦性檢查。
// code-reviewer S7：glow 跟著 dark/light theme 切換重繪 — 監聽 saved-theme
// 屬性變化（Quartz Darkmode 改 documentElement[saved-theme]），重新呼叫
// __sectionCanvas.render 並先清舊 instance。
const inlineScript = \`
(function(){
  let cleanup = null
  let myGen = 0
  function currentGen() { return window.__nav?.currentGen?.() ?? 0 }
  function pickGlow(host) {
    const dark = document.documentElement.getAttribute('saved-theme') !== 'light'
    return dark
      ? (host.dataset.glowColorDark ?? host.dataset.glowColor ?? 'rgba(255,255,255,0.18)')
      : (host.dataset.glowColorLight ?? host.dataset.glowColor ?? 'rgba(0,0,0,0.18)')
  }
  function setup() {
    cleanup?.()
    cleanup = null
    myGen = currentGen()
    const host = document.querySelector('[data-section-hero-canvas]')
    if (!host) return
    if (!window.__sectionCanvas) return
    if (myGen !== currentGen()) return  // stale nav abort
    const renderer = host.dataset.canvasRenderer
    const density = Number(host.dataset.particleDensity ?? '30')
    if (!renderer) return
    cleanup = window.__sectionCanvas.render(host, {
      renderer,
      glowColor: pickGlow(host),
      particleDensity: Number.isFinite(density) ? density : 30,
    })
  }
  function teardown() {
    cleanup?.()
    cleanup = null
  }
  // theme switch：documentElement[saved-theme] 變化時重 render 拿新 glow
  let themeMo = null
  function watchTheme() {
    themeMo?.disconnect()
    themeMo = new MutationObserver(() => {
      if (cleanup) setup()  // 重 render 用新 glow
    })
    themeMo.observe(document.documentElement, { attributes: true, attributeFilter: ['saved-theme'] })
  }
  document.addEventListener('nav', () => { setup(); watchTheme(); })
  document.addEventListener('prenav', () => { teardown(); themeMo?.disconnect(); themeMo = null })
  window.addEventListener('beforeunload', teardown)
})();
\`

// code-reviewer M2 + M3：accent / cover frontmatter 是 user-controlled string
// 進 inline style 有 CSS injection 風險（self-host 單作者風險低，但加防禦
// 不貴）。accent 只允許 hex / rgb / rgba / 命名色字元，cover 用 encodeURI
// 並包雙引號。
function sanitizeAccent(value: string): string {
  // 允許：a-z A-Z 0-9 # ( ) , . 空白 % -
  return value.replace(/[^a-zA-Z0-9#(),.\s%-]/g, "").trim().slice(0, 64)
}

function sanitizeCoverUrl(value: string): string {
  // encodeURI 把 "); evil('  之類的 inject 字元編碼掉
  return encodeURI(value.trim()).slice(0, 512)
}

// code-reviewer S6 + S10：auto-minimal 推斷規則（spec §4.3 / §5.4）
//   slug 屬於 tags/* → minimal
//   slug 屬於 about/* → minimal
//   其他 → themed
//   frontmatter hero-style: "minimal" 顯式指定 → minimal
// "none" 在 layout 端攔截走 ArticleTitle fallback，這裡不會收到。
function inferHeroStyle(slug: string, frontmatterValue: string | undefined): "themed" | "minimal" {
  if (frontmatterValue === "minimal") return "minimal"
  if (slug.startsWith("tags/")) return "minimal"
  if (slug === "about" || slug.startsWith("about/")) return "minimal"
  return "themed"
}

export default (() => {
  const Badge = SectionBadge()

  function ArticleHero(props: QuartzComponentProps) {
    const { fileData, cfg } = props
    const slug = fileData.slug ?? "index"
    const title = fileData.frontmatter?.title ?? ""
    const fm = fileData.frontmatter as Record<string, unknown> | undefined
    const coverRaw = typeof fm?.cover === "string" ? fm.cover : undefined
    const accentRaw = typeof fm?.accent === "string" ? fm.accent : undefined
    const heroStyleRaw = typeof fm?.["hero-style"] === "string" ? (fm["hero-style"] as string) : undefined

    const heroStyle = inferHeroStyle(slug, heroStyleRaw)
    const cover = coverRaw ? sanitizeCoverUrl(coverRaw) : undefined
    const accent = accentRaw ? sanitizeAccent(accentRaw) : undefined

    const theme = getSectionThemeForSlug(slug)
    const themeKey = theme?.key ?? "about"
    const motionCfg = theme?.motionConfig

    // 兩個 glow 變體都帶到 dataset，inline script 的 watchTheme 在
    // saved-theme 切換時重 render 用對應顏色（code-reviewer S7）
    const glowDark = motionCfg?.glowColorDark ?? "rgba(255, 247, 234, 0.18)"
    const glowLight = motionCfg?.glowColorLight ?? "rgba(18, 16, 13, 0.18)"
    const renderer = motionCfg?.canvasRenderer ?? "geometric-lines"
    const density = motionCfg?.particleDensity ?? 30

    // accent 覆寫：frontmatter 提供且通過 sanitization 才用
    const accentStyle = accent ? `--article-hero-accent: ${accent};` : ""

    // meta：date + reading time
    const text = fileData.text ?? ""
    const minutes = text ? Math.ceil(readingTime(text).minutes) : 0
    const readingLabel =
      minutes > 0 ? i18n(cfg.locale).components.contentMeta.readingTime({ minutes }) : ""

    // SectionBadge 對沒對應 section 的 slug（如 about 子頁）回傳 null，
    // 預先 evaluate 避免 grid 留空 gap（code-reviewer M5）
    const badgeNode = Badge(props)

    return (
      <header
        class="article-hero"
        data-section-theme={themeKey}
        data-hero-style={heroStyle}
        style={accentStyle}
      >
        {heroStyle === "themed" && cover && (
          <div class="article-hero__cover" style={`background-image: url("${cover}");`} />
        )}
        {heroStyle === "themed" && !cover && (
          <div
            class="article-hero__canvas-host"
            data-section-hero-canvas="true"
            data-canvas-renderer={renderer}
            data-glow-color-dark={glowDark}
            data-glow-color-light={glowLight}
            data-particle-density={String(density)}
            aria-hidden="true"
          />
        )}
        <div class="article-hero__copy">
          {badgeNode}
          <h1 class="article-hero__title">{title}</h1>
          {(fileData.dates || readingLabel) && (
            <p class="article-hero__meta">
              {fileData.dates && <DateComp date={getDate(cfg, fileData)!} locale={cfg.locale} />}
              {readingLabel && <span class="article-hero__reading-time">{readingLabel}</span>}
            </p>
          )}
        </div>
      </header>
    )
  }

  ArticleHero.afterDOMLoaded = inlineScript

  return (() => ArticleHero) satisfies QuartzComponentConstructor
})()
```

- [ ] **Step 3: Export `ArticleHero` + `SectionBadge` 進 `quartz/components/index.ts`**

Modify `quartz/components/index.ts`：
- Import 區加 `import ArticleHero from "./ArticleHero"` + `import SectionBadge from "./SectionBadge"`（放在現有 `ArticleTitle` 之後）
- Export `{ ... }` 區加 `ArticleHero,` + `SectionBadge,`（同樣放在 `ArticleTitle,` 之後）

- [ ] **Step 4: Build 驗證**

```bash
npx quartz build 2>&1 | tail -5
# 預期：build 成功無 TS error
grep -oE "data-section-hero-canvas|article-hero__title|section-badge" public/postscript.js public/index.css | sort -u
# 預期：在 css 至少有 .article-hero__title / .section-badge；postscript 有 data-section-hero-canvas
# (組件實際 render 在 layout 改後才會印到 index.html，先確認 bundle 內容)
```

- [ ] **Step 5: Commit**

```bash
git add quartz/components/ArticleHero.tsx \
  quartz/components/SectionBadge.tsx \
  quartz/components/index.ts

git commit -m "$(cat <<'EOF'
feat: ArticleHero + SectionBadge 組件骨架（未進 layout）

ArticleHero（spec §5.3）：60vh hero 含 SectionBadge + h1（72px target）+
meta（date + reading time）+ section-themed canvas 容器。frontmatter 支援：
- cover: URL → 取代 canvas 用背景圖
- accent: 顏色字串 → inline style 覆蓋 --article-hero-accent
- hero-style: "minimal" → 走無 canvas 純 title+meta 變體
- hero-style: "none" 由 layout 端攔截走 ArticleTitle fallback，不會到此

afterDOMLoaded 注入小段 inline JS，nav handler 呼叫 window.__sectionCanvas
.render() 啟動 Task 2 的 renderer；prenav / beforeunload 呼 cleanup。
canvas config 從 sectionThemes.motionConfig（Phase 1 已擴充）取。

SectionBadge：可重用的 section 歸屬小標，連回該 section 入口；
slug 找不到對應 section 時回 null。

兩個組件 export 進 index.ts。layout 還沒接 → 視覺零變化。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 4: `CategoryHero.tsx` 組件

**Files:**
- Create: `quartz/components/CategoryHero.tsx`
- Modify: `quartz/components/index.ts`

**這一步建第二個新組件，仍未進 layout**：CategoryHero 的 scene 物件 SSR 出來但靜態（沒 GSAP timeline）。Task 5 才會加 `categoryScene.inline.ts` 動態驅動。先確認 SSR 輸出正確、CSS 規則匹配、a11y 屬性齊。

- [ ] **Step 1: 寫 `CategoryHero.tsx`**

Create `quartz/components/CategoryHero.tsx`:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug } from "../util/path"
import { getSectionThemeForSlug } from "./sectionThemes"

/**
 * CategoryHero — 分類頁 75vh hero（spec §5.2）
 * 取代 BrandIntro。內容主要從 sectionThemes 取，scene 物件由
 * categoryScene.inline.ts（Task 5）用 GSAP ScrollTrigger 動畫。
 */
export default (() => {
  const CategoryHero: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const theme = getSectionThemeForSlug(slug)

    if (!theme) return null

    return (
      <header class="category-hero" data-section-theme={theme.key}>
        <div class="category-hero__copy">
          <p class="category-hero__eyebrow">{theme.label}</p>
          <h1 class="category-hero__title">{theme.title}</h1>
          <p class="category-hero__copy-text">{theme.copy}</p>
        </div>
        <div
          class="category-hero__stage"
          data-category-scene="true"
          aria-hidden="true"
          role="presentation"
        >
          {theme.sceneObjects.map((object, index) => (
            <span
              class="category-scene-object"
              data-variant={object.variant}
              data-index={index}
              data-origin-x={object.x}
              data-origin-y={object.y}
              data-depth={object.depth}
              style={`--x: ${object.x}%; --y: ${object.y}%; --size: ${object.size}px; --rotate: ${object.rotate}deg;`}
            />
          ))}
        </div>
      </header>
    )
  }

  return CategoryHero
}) satisfies QuartzComponentConstructor
```

**註（重要）**：CategoryHero **不使用** `data-hero-cinematic` 屬性。Phase 2 的 `heroCinematic.inline.ts` 用 `document.querySelector("[data-hero-cinematic]")` 抓 host，若 CategoryHero 也設此屬性會被 heroCinematic 誤抓並對整個 hero 套 `gsap.to({opacity:0.35, y:-40})` scrub（spec §5.1 home hero exit 行為，**不**該套到分類頁）。Task 5 的 `categoryScene.inline.ts` 改用 `.category-hero` class 直接作 host selector，徹底避開此衝突。

- [ ] **Step 2: Export `CategoryHero` 進 `index.ts`**

Modify `quartz/components/index.ts` — Import 區加 `import CategoryHero from "./CategoryHero"`（放在 `BrandIntro` import 之後），Export 區加 `CategoryHero,`（放在 `BrandIntro,` 之後）。

- [ ] **Step 3: Build 驗證**

```bash
npx quartz build 2>&1 | tail -5
grep -oE "category-hero__title|category-scene-object|data-category-scene" public/index.css public/postscript.js 2>&1 | sort -u
# 預期：CSS 含 .category-hero__title / .category-scene-object；bundle 含 data-category-scene
```

- [ ] **Step 4: Commit**

```bash
git add quartz/components/CategoryHero.tsx quartz/components/index.ts
git commit -m "$(cat <<'EOF'
feat: CategoryHero 組件骨架（未進 layout，scene 暫無動畫）

CategoryHero（spec §5.2）：75vh hero，左 copy / 右 scene stage：
- copy：eyebrow (section.label) + h1 (section.title) + copy-text (section.copy)
- stage：根據 sectionThemes.sceneObjects 印 6-8 個 .category-scene-object
  span，每個帶 data-variant / data-index / data-origin-x/y / data-depth +
  --x/--y/--size/--rotate CSS var 起手樣式

**不**重用 data-hero-cinematic 屬性 — Phase 2 heroCinematic.inline.ts 用
querySelector("[data-hero-cinematic]") 抓 host，若這裡也設此屬性會被誤
抓並對整個 hero 套 home hero 的 fade-out scrub（spec §5.1 行為）。Task 5
的 categoryScene.inline.ts 改用 .category-hero class selector 直接找。

CSS aria-hidden + role=presentation 在 stage 上（spec §8.3）。

Layout 還沒接 → 分類頁仍看到 BrandIntro，視覺零變化。Task 5 補上 GSAP
scroll-driven timeline 後，Task 9 才正式 swap layout。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 5: `categoryScene.inline.ts` — GSAP scroll-driven cinematic timeline

**Files:**
- Create: `quartz/components/scripts/categoryScene.inline.ts`
- Modify: `quartz/components/MotionRuntime.tsx`

**這支 script 是 Phase 2 8 支之外的第 9 支**。負責 CategoryHero 的 scroll-driven timeline：
- 0-30% scroll progress：物件從各自起點偏移（飄入）
- 30-70%：重新編隊（depth 系數差異化動）
- 70-100%：散開 + 淡出

走 Phase 1 的 `window.__gsapLoader.loadGsap()` 動態載 GSAP + ScrollTrigger，配合 §6.2 navGeneration token 做 stale-handler 防禦，配合 spec §8.2 mobile + §8.1 reduced-motion 不載 GSAP（保持 SSR 靜態起手位置）。

- [ ] **Step 1: 寫 `categoryScene.inline.ts`**

Create `quartz/components/scripts/categoryScene.inline.ts`:

```ts
// CategoryHero scroll-driven cinematic timeline (spec §5.2 + §6.2 + §8.1 + §8.2)
//
// 0-30%   scroll progress：物件從原點偏移（飄入感）
// 30-70%  ：重新編隊，depth 越大移動越多
// 70-100% ：物件散開 + 淡出（hero 離開 viewport 前）
//
// reduced-motion / mobile 不載 GSAP → 物件保持 SSR 靜態 CSS var 位置不動

declare const window: Window & {
  gsap?: any
  ScrollTrigger?: any
  __gsapLoader?: { loadGsap: () => Promise<void> }
  __nav?: { currentGen: () => number }
  __lenis?: {
    on?: (event: string, fn: (...args: any[]) => void) => void
    off?: (event: string, fn: (...args: any[]) => void) => void
    raf?: (time: number) => void
    isActive?: () => boolean
  }
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
}

let scrollTriggers: any[] = []
let lenisScrollHandler: ((...args: any[]) => void) | null = null

function teardown() {
  for (const t of scrollTriggers) {
    try { t.kill?.() } catch { /* no-op */ }
  }
  scrollTriggers = []
  // code-reviewer S8：解除 Lenis × ScrollTrigger sync listener
  if (lenisScrollHandler && window.__lenis?.off) {
    try { window.__lenis.off("scroll", lenisScrollHandler) } catch { /* no-op */ }
  }
  lenisScrollHandler = null
}

async function setupCategoryScene() {
  teardown()

  // 用 .category-hero class 直接抓 host — 不重用 data-hero-cinematic
  // 屬性以避免跟 Phase 2 heroCinematic.inline.ts 的 querySelector 撞車
  // （那支會對 host 套 home-hero 的 fade-out scrub）
  const host = document.querySelector<HTMLElement>(".category-hero")
  if (!host) return

  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  if (reduced) return  // SSR 靜態位置足夠

  const mobileGate = window.__motion?.isMobileViewport?.() ?? false
  if (mobileGate) return  // spec §8.2

  if (!window.__gsapLoader) {
    console.warn("[categoryScene] window.__gsapLoader missing — skipping")
    return
  }

  const myGen = window.__nav?.currentGen?.() ?? 0
  const staleNav = () => myGen !== (window.__nav?.currentGen?.() ?? 0)

  try {
    await window.__gsapLoader.loadGsap()
    if (staleNav()) return
    await document.fonts.ready
    if (staleNav()) return
  } catch (err) {
    console.warn("[categoryScene] GSAP load failed, scene stays static", err)
    return
  }

  const gsap = window.gsap
  const ScrollTrigger = window.ScrollTrigger
  if (!gsap || !ScrollTrigger) return

  // code-reviewer S8：Lenis smooth scroll 跑自己的 RAF loop，scroll 位置
  // 跟 native window.scrollY 不同步，scrub timeline 會感覺黏滯。
  // 解法：把 Lenis 的 scroll event 餵給 ScrollTrigger.update。
  if (window.__lenis?.on) {
    lenisScrollHandler = () => ScrollTrigger.update()
    try { window.__lenis.on("scroll", lenisScrollHandler) } catch { /* no-op */ }
  }

  const objects = host.querySelectorAll<HTMLElement>(".category-scene-object")
  if (objects.length === 0) return

  // 為每個物件建立 scroll-scrub timeline；重新編隊位置 = 隨機偏移依 depth scale
  objects.forEach((el) => {
    const depth = Number(el.dataset.depth ?? "1")
    const idx = Number(el.dataset.index ?? "0")
    // 用 idx 做偽隨機，保證 SSR / hydrate 一致
    const seed = (idx * 37 + 11) % 100
    const dx1 = (seed - 50) * depth * 0.6   // 飄入終點 X 偏移（px）
    const dy1 = ((seed * 7) % 100 - 50) * depth * 0.4   // 飄入終點 Y 偏移
    const dx2 = -dx1 * 0.7                  // 散開階段反向
    const dy2 = dy1 * -1.2

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: host,
        start: "top top",
        end: "bottom top",
        scrub: 0.6,
      },
    })

    tl.fromTo(
      el,
      { xPercent: 0, yPercent: 0, opacity: 0.6, rotation: 0 },
      { xPercent: dx1, yPercent: dy1, opacity: 0.85, rotation: 4 * depth, ease: "none" },
      0,
    )
      .to(el, { xPercent: dx1 * 0.4, yPercent: dy1 * 0.4, rotation: -2 * depth, ease: "none" }, 0.3)
      .to(el, { xPercent: dx2, yPercent: dy2, opacity: 0, ease: "none" }, 0.7)

    scrollTriggers.push(tl.scrollTrigger)
  })

  ScrollTrigger.refresh()
}

document.addEventListener("nav", setupCategoryScene)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

- [ ] **Step 2: Wire 進 `MotionRuntime.tsx`**

Modify `quartz/components/MotionRuntime.tsx`：

Import 區加（放在 `heroCinematicScript` 之後）：

```tsx
// @ts-ignore
import categorySceneScript from "./scripts/categoryScene.inline"
```

`concatenateResources(...)` 加 `categorySceneScript,`（放在 `heroCinematicScript` 之後）。Phase 3 後 9 支：

```tsx
MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  scrollRevealScript,
  focalCanvasScript,
  sectionCanvasScript,
  lenisScript,
  gsapLoaderScript,
  heroCinematicScript,
  categorySceneScript,   // Phase 3 新增（spec §5.2 scroll-cinematic）
)
```

JSDoc 載入順序更新到 9 條目。

- [ ] **Step 3: Build 驗證 + bundle marker**

```bash
npx quartz build 2>&1 | tail -3
grep -oE "data-hero-cinematic|categoryScene|data-category-scene" public/postscript.js | sort -u
# 預期：data-hero-cinematic + data-category-scene 出現
```

- [ ] **Step 4: Commit**

```bash
git add quartz/components/scripts/categoryScene.inline.ts \
  quartz/components/MotionRuntime.tsx

git commit -m "$(cat <<'EOF'
feat: categoryScene inline script — CategoryHero scroll-driven timeline

spec §5.2 物件編隊三段式 timeline：
- 0-30% scroll：飄入終點偏移（depth-scaled）
- 30-70%     ：重新編隊位置
- 70-100%    ：散開 + 淡出

每個 .category-scene-object 建一個 scrub: 0.6 ScrollTrigger，timeline
從 SSR 靜態位置（CSS var --x/--y）開始，xPercent / yPercent / rotation /
opacity 走 fromTo + to，依 data-depth 與 data-index 偽隨機計算終點偏移
（idx 確保 SSR / hydrate 一致）。

降級：
- prefers-reduced-motion → 不載 GSAP，物件留 SSR 起手位置（spec §8.1）
- mobile (< 768px) → 不載 GSAP（spec §8.2）
- __gsapLoader 缺席 → console.warn 並 return

navGeneration token 做 stale nav 防禦（每個 await 後檢查）。

第 9 支 inline script 進 MotionRuntime，依賴 gsapLoader 所以放它後面。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 6: `popoverScroll.inline.ts` — popover 預覽自動 scroll 過 hero

**Files:**
- Create: `quartz/components/scripts/popoverScroll.inline.ts`
- Modify: `quartz/components/MotionRuntime.tsx`

**spec §6.3 v3 實作**：Phase 1 已寫好 `_popover-immersive.scss`（dormant，CSS 隱藏 `.article-hero` / `.scroll-progress` / `.breadcrumbs`），Phase 3 等 ArticleHero 真正 render（Task 9）就會自動匹配生效。但 popover scroll 還需要主動把 popover 內容滾到第一個內文段落，避免 popover 開出來看到一段空白。

第 10 支 inline script。`MutationObserver` 觀察 `body` 的 childList，看到 `.popover-inner` 插入時 rAF 後找第一個 `<p>/h2/h3/pre/ul/ol`，scrollTop 過去。

- [ ] **Step 1: 寫 `popoverScroll.inline.ts`**

Create `quartz/components/scripts/popoverScroll.inline.ts`:

```ts
// Popover 預覽自動 scroll 過 hero（spec §6.3 Phase 3）
// 配 _popover-immersive.scss（Phase 1 已就位，display:none 隱藏 article-hero
// / scroll-progress / breadcrumbs）。本 script 主動把 popover 內容滾到第
// 一個有意義的元素，避免 popover 開出來看到一段空白。
//
// 實作方式：MutationObserver 觀察 body 的 childList，看到 .popover-inner
// 插入後 requestAnimationFrame（等 layout 完）找第一個 p/h2/h3/pre/ul/ol，
// 用 scrollTop 移過去。
//
// 為什麼不直接改 popover.inline.ts：那是 Quartz upstream 檔，動了未來
// 升級會痛。MutationObserver 對 body childList 成本極低。

let mo: MutationObserver | null = null

function setupPopoverScroll() {
  mo?.disconnect()
  mo = new MutationObserver((mutations) => {
    for (const m of mutations) {
      for (const node of Array.from(m.addedNodes)) {
        if (!(node instanceof HTMLElement)) continue
        // popover.inline.ts upstream 把 popover-inner 包在 popover 容器裡，
        // 但插入順序取決於版本。同時檢查 node 自己是 .popover-inner 與
        // node 內含 .popover-inner，二擇一覆蓋兩種插法。
        const inner =
          node.classList.contains("popover-inner")
            ? node
            : node.querySelector?.<HTMLElement>(".popover-inner")
        if (!inner) continue

        requestAnimationFrame(() => {
          const firstContent = inner.querySelector<HTMLElement>(
            "p, h2, h3, pre, ul, ol",
          )
          if (!firstContent) return
          const offset = firstContent.offsetTop - 20
          if (offset > 0) inner.scrollTop = offset
        })
      }
    }
  })
  mo.observe(document.body, { childList: true, subtree: true })
}

function teardown() {
  mo?.disconnect()
  mo = null
}

document.addEventListener("nav", setupPopoverScroll)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

- [ ] **Step 2: Wire 進 `MotionRuntime.tsx`**

Modify `quartz/components/MotionRuntime.tsx` — import 加（放在 `categorySceneScript` 之後）：

```tsx
// @ts-ignore
import popoverScrollScript from "./scripts/popoverScroll.inline"
```

`concatenateResources(...)` 加 `popoverScrollScript,`（最後一個）。Phase 3 後 10 支：

```tsx
MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  scrollRevealScript,
  focalCanvasScript,
  sectionCanvasScript,
  lenisScript,
  gsapLoaderScript,
  heroCinematicScript,
  categorySceneScript,
  popoverScrollScript,   // Phase 3 新增（spec §6.3 popover × hero 防碰撞）
)
```

JSDoc 載入順序更新到 10 條目。

- [ ] **Step 3: Build + bundle marker**

```bash
npx quartz build 2>&1 | tail -3
grep -oE "popover-inner|popoverScroll" public/postscript.js | sort -u
# 預期：popover-inner 字串出現
```

- [ ] **Step 4: Commit**

```bash
git add quartz/components/scripts/popoverScroll.inline.ts \
  quartz/components/MotionRuntime.tsx

git commit -m "$(cat <<'EOF'
feat: popoverScroll inline script — popover 預覽自動跳過 hero（spec §6.3）

配 _popover-immersive.scss（Phase 1 已就位 dormant，Phase 3 ArticleHero
進 layout 後 CSS 自動匹配），本 script 主動把 popover 內容滾到第一個
有意義的元素（p/h2/h3/pre/ul/ol），避免 popover 開出來只看到隱藏 hero
留下的空白頂端。

實作走 MutationObserver 觀察 body childList，看到 .popover-inner 插入
後 rAF 一幀（等 layout）才 scrollTop。為什麼不直接改 upstream popover
.inline.ts：避免未來 Quartz 升級需 re-apply patch（spec §6.3 v3 決策）。

第 10 支 inline script 進 MotionRuntime（順序：motion/nav/reveal/focal/
section/lenis/gsap/heroCinematic/categoryScene/popoverScroll）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 7: TOC sticky + active-class CSS（已在 Task 1 寫進 `_toc-sticky.scss`，這 Task 補 toc.inline.ts 的 active observer）

**Files:**
- Modify: `quartz/components/scripts/toc.inline.ts`

**spec §5.3 v3**：當某個 `<section>` 進入 viewport 時，對對應的 `.toc-content a[data-for="{sectionId}"]` 加 `.active` class（同時移除其他 a 的 `.active`）。Quartz upstream `toc.inline.ts` 既有 IntersectionObserver 已會做 `.in-view` class，Task 7 補一條最頂部 entry 才得 `.active` 的規則 — 不影響原 `.in-view` 行為。

策略：保留 upstream observer 不動，加第二個輕量 observer 專管 `.active`，rootMargin 收緊到 viewport 上半部，只認最早進來的那個 section。

- [ ] **Step 1: 修改 `toc.inline.ts` 補 active observer**

Read 現有 `quartz/components/scripts/toc.inline.ts` 確認結構（44 行小檔），然後 modify：

替換整檔內容為：

```ts
// 原 in-view observer（upstream，spec §5.3 v3 不動）保留
const inViewObserver = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    const slug = entry.target.id
    const tocEntryElements = document.querySelectorAll(`a[data-for="${slug}"]`)
    const windowHeight = entry.rootBounds?.height
    if (windowHeight && tocEntryElements.length > 0) {
      if (entry.boundingClientRect.y < windowHeight) {
        tocEntryElements.forEach((tocEntryElement) => tocEntryElement.classList.add("in-view"))
      } else {
        tocEntryElements.forEach((tocEntryElement) => tocEntryElement.classList.remove("in-view"))
      }
    }
  }
})

// 新 active observer（Phase 3 新增，spec §5.3 v3）
// code-reviewer S1：IntersectionObserver entries 參數只含「狀態變化」的 entry，
// 不是「目前所有 intersecting」。所以維護一個 module-scope Set<id> 記
// 「目前正 intersect 的所有 heading id」，callback 內依 entry.isIntersecting
// add/remove，最後從 set 撈出 boundingClientRect.top 最小（最頂）那個當 active。
let lastActiveSlug: string | null = null
const intersectingHeadings = new Set<string>()

function pickTopmostActiveHeading() {
  let topmost: { id: string; top: number } | null = null
  intersectingHeadings.forEach((id) => {
    const el = document.getElementById(id)
    if (!el) return
    const top = el.getBoundingClientRect().top
    if (topmost === null || top < topmost.top) {
      topmost = { id, top }
    }
  })
  if (topmost === null) return null
  return (topmost as { id: string; top: number }).id
}

const activeObserver = new IntersectionObserver(
  (entries) => {
    // 更新 set
    for (const entry of entries) {
      const id = entry.target.id
      if (entry.isIntersecting) intersectingHeadings.add(id)
      else intersectingHeadings.delete(id)
    }
    // 重新計算頂端 heading
    const slug = pickTopmostActiveHeading()
    if (slug === lastActiveSlug) return
    lastActiveSlug = slug
    document
      .querySelectorAll(".toc-content a.active")
      .forEach((a) => a.classList.remove("active"))
    if (slug) {
      document
        .querySelectorAll(`a[data-for="${slug}"]`)
        .forEach((a) => a.classList.add("active"))
    }
  },
  {
    rootMargin: "-10% 0px -75% 0px",
    threshold: 0,
  },
)

function toggleToc(this: HTMLElement) {
  this.classList.toggle("collapsed")
  this.setAttribute(
    "aria-expanded",
    this.getAttribute("aria-expanded") === "true" ? "false" : "true",
  )
  const content = this.nextElementSibling as HTMLElement | undefined
  if (!content) return
  content.classList.toggle("collapsed")
}

function setupToc() {
  for (const toc of document.getElementsByClassName("toc")) {
    const button = toc.querySelector(".toc-header")
    const content = toc.querySelector(".toc-content")
    if (!button || !content) return
    button.addEventListener("click", toggleToc)
    window.addCleanup(() => button.removeEventListener("click", toggleToc))
  }
}

document.addEventListener("nav", () => {
  setupToc()

  inViewObserver.disconnect()
  activeObserver.disconnect()
  lastActiveSlug = null
  intersectingHeadings.clear()
  const headers = document.querySelectorAll("h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]")
  headers.forEach((header) => {
    inViewObserver.observe(header)
    activeObserver.observe(header)
  })
})
```

**註**：兩個 observer 共享同一組 headers，但用不同 rootMargin / threshold 算各自的 class。`-10% 0px -75% 0px` 意思是 root（viewport）的有效偵測區是「離頂 10% 到離底 75% 的中間區」— 這樣只有當 header 進到 viewport 上方 15% 區域內才算 active，避免兩個 sections 同時 active 的閃爍。

- [ ] **Step 2: Build + 簡單驗證**

```bash
npx quartz build 2>&1 | tail -3
grep -c "activeObserver\|lastActiveSlug" public/postscript.js
# 預期：> 0（也可能被 minify 掉，沒關係，`active` class 規則本身一定要在 css）
grep -oE "toc-content a.active|toc-content a.in-view" public/index.css | sort -u
# 預期：兩條規則都在
```

- [ ] **Step 3: Commit**

```bash
git add quartz/components/scripts/toc.inline.ts
git commit -m "$(cat <<'EOF'
feat: toc.inline.ts 補 active-section observer（spec §5.3 v3）

保留 upstream in-view observer 不動，加第二個 IntersectionObserver 用
更收緊的 rootMargin (-10% 0px -75% 0px) 只認 viewport 上半部最早進來
的 section，對該 .toc-content a[data-for="{id}"] 加 .active class（同
時清掉其他）。

active 與 in-view 是兩個 CSS class（不同視覺強度），由 _toc-sticky.scss
分別寫規則。Quartz upstream toc.scss 不動。

降級：reduced-motion 路徑不影響 IntersectionObserver（純 class 變化、
無動畫），所以無需 motion gate。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 8: `quartz.layout.ts` 按 spec §15 v3 改寫 + frontmatter-aware ConditionalRender

**Files:**
- Modify: `quartz.layout.ts`

**這是 Phase 3 視覺翻轉的點**：layout 改完 build 後分類頁立刻變成 `CategoryHero` 樣式、所有文章頁都有 `ArticleHero`、文章頁右欄出現 sticky TOC、popover 預覽自動 scroll 過 hero。

- [ ] **Step 1: 替換 `quartz.layout.ts` 為 §15 v3 版**

Replace `quartz.layout.ts` with:

```ts
import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// helpers — frontmatter-aware ConditionalRender 條件
// 用 any 跟既有 layout 既有風格一致（QuartzComponentProps 從
// "./quartz/components/types" 來，但 ConditionalRender 的 condition
// signature 已 infer，運行時無 type 風險）
const isNonIndex = (page: any) => page.fileData.slug !== "index"
const heroStyleNone = (page: any) =>
  page.fileData.frontmatter?.["hero-style"] === "none"

export const sharedPageComponents: SharedLayout = {
  head: Component.CustomHead(),
  header: [Component.SiteHeaderNav()],
  afterBody: [
    Component.MotionRuntime(),   // 全站 motion 基礎建設 (Phase 1+2+3)
    Component.ConditionalRender({
      component: Component.RecentNotes({
        title: "繼續閱讀",
        limit: 3,
        showTags: false,
        filter: (file) => !!file.slug && file.slug !== "index" && !file.slug.endsWith("/index"),
      }),
      condition: (page) => {
        const slug = page.fileData.slug ?? ""
        return slug !== "index" && !slug.endsWith("/index")
      },
    }),
  ],
  footer: Component.Footer({
    links: {
      Home: "/",
      製造業AI: "/manufacturing-ai/",
      AI新知: "/ai-notes/",
      手沖咖啡: "/coffee/",
      個人經歷: "/about/",
    },
  }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    // 首頁：HomeLanding（Phase 2 內部含 HomeHeroApple）
    Component.ConditionalRender({
      component: Component.HomeLanding(),
      condition: (page) => page.fileData.slug === "index",
    }),
    // 非首頁且 hero-style !== "none"：Breadcrumbs + ArticleHero（Phase 3 新組件）
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => isNonIndex(page) && !heroStyleNone(page),
    }),
    Component.ConditionalRender({
      component: Component.ArticleHero(),
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
    Component.DesktopOnly(Component.TableOfContents()),
  ],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.CategoryHero(),   // Phase 3 取代原本的 BrandIntro + ArticleTitle
  ],
  left: [],
  right: [],
}
```

**重點對照 v3 spec**（spec §15.2）：
- `head: CustomHead()` ✓（Phase 2）
- `defaultContentPageLayout.beforeBody`：5 個 ConditionalRender 順序如上
- `defaultContentPageLayout.right`：`[DesktopOnly(TableOfContents())]` ✓
- `defaultListPageLayout.beforeBody`：`[Breadcrumbs, CategoryHero]`（取代舊 `[BrandIntro, ArticleTitle]`）

`ContentMeta` 從 layout 完全消失（功能併入 ArticleHero），組件檔本身留著（§15.3）。

- [ ] **Step 2: Build + 跑全部頁面類型驗證**

```bash
npx quartz build 2>&1 | tail -10
# 預期：build 成功

# 各頁面類型輸出檢查
grep -c 'class="article-hero"' public/manufacturing-ai/index.html 2>/dev/null
# 預期：0（manufacturing-ai/index 是分類首頁，走 defaultListPageLayout → 不應有 article-hero）

grep -c 'class="category-hero"' public/manufacturing-ai/index.html 2>/dev/null
# 預期：1

# 隨便挑一篇文章看 ArticleHero 出現
ls public/manufacturing-ai/*.html 2>/dev/null | head -1 | xargs grep -c 'class="article-hero"' 2>/dev/null
# 預期：1（ArticleHero render）

# 文章頁有 TOC sticky 容器
ls public/manufacturing-ai/*.html 2>/dev/null | head -1 | xargs grep -c 'class.*toc' 2>/dev/null
# 預期：> 0
```

- [ ] **Step 3: 啟動 dev server 手動逐頁掃**

```bash
npx quartz build --serve 2>&1 &
sleep 3
```

開瀏覽器跑這 5 個情境，每個都 console 0 error：

| 路徑 | 預期 hero |
|---|---|
| `/` | HomeHeroApple（Phase 2） |
| `/manufacturing-ai/` | CategoryHero（製造業 AI 主題、scene 物件、scroll 時看物件編隊） |
| `/ai-notes/` | CategoryHero（AI 主題） |
| `/coffee/` | CategoryHero（咖啡主題） |
| 任一文章 | ArticleHero（60vh、section accent、SectionBadge、h1、date · reading time） |

- [ ] **Step 4: Commit**

```bash
git add quartz.layout.ts
git commit -m "$(cat <<'EOF'
feat: quartz.layout.ts 按 spec §15 v3 改寫（ArticleHero / CategoryHero / Sticky TOC）

defaultContentPageLayout：
- beforeBody 改 frontmatter-aware ConditionalRender：
  * slug === "index" → HomeLanding（不變）
  * 非首頁 && hero-style !== "none" → Breadcrumbs + ArticleHero
  * 非首頁 && hero-style === "none" → Breadcrumbs + ArticleTitle (fallback)
  * 非首頁不論 → TagList
- right: [DesktopOnly(TableOfContents())] — Sticky TOC 透過
  _toc-sticky.scss + toc.inline.ts 補的 active observer 上線

defaultListPageLayout：
- beforeBody 從 [BrandIntro, ArticleTitle] 改成 [Breadcrumbs, CategoryHero]
  CategoryHero 內部含 eyebrow + h1 + copy + scene stage（spec §5.2）

ContentMeta 從 layout 完全消失（功能併入 ArticleHero）。BrandIntro /
ContentMeta 兩檔留在 repo（§15.3 可刪但 Phase 4 才決定）。ArticleTitle
仍會被 hero-style: "none" fallback 路徑用到 → 不刪。

Phase 3 視覺翻轉點：本 commit 後分類頁與文章頁全面採新 hero 樣式。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 9: 手動 regression + feature 驗證（含 popover scroll、TOC active、hero-style: none、cover/accent frontmatter）

**Files:**
- Create: `quartz/docs/superpowers/baselines/2026-04-25-phase3-verification.md`

**這是 Phase 3 的手動驗證**。Phase 2 沒驗動畫版（reduced-motion 環境限制），Phase 3 也一樣，需要手動關 reduced-motion 才看得見 GSAP 相關。但 frontmatter 行為（cover / accent / hero-style）需要實作測試文章來驗證 — 此 task 包含建測試文章 + 手動掃。

- [ ] **Step 1: 建 3 篇測試文章**

Create 3 test markdown files under `content/`：

`content/_phase3-test-cover.md`：
```markdown
---
title: Phase 3 cover 測試
cover: /static/icon.png
date: 2026-04-25
draft: true
description: 測試 frontmatter cover 圖片是否取代 canvas
---

# 第一段內文

這是 cover 圖片測試文章。打開後 ArticleHero 應該用 `/static/icon.png` 當背景圖。

## 第二段標題

驗證 sticky TOC + active class 跟著切換。
```

`content/_phase3-test-accent.md`：
```markdown
---
title: Phase 3 accent 測試
accent: "#ff5e3a"
date: 2026-04-25
draft: true
---

# 內文段落 1

ArticleHero 邊框 / SectionBadge / TOC active 顏色應該是橘紅色 (#ff5e3a)。

## 內文段落 2

切換 dark / light 模式都應該保持紅色。
```

`content/_phase3-test-none.md`：
```markdown
---
title: Phase 3 hero-style none 測試
hero-style: none
date: 2026-04-25
draft: true
---

# 內文段落 1

這篇 ArticleHero 應該完全不出現，只看到 Breadcrumbs + ArticleTitle (純 h1) + TagList。
```

- [ ] **Step 2: Rebuild + 啟動 dev server**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
npx quartz build 2>&1 | tail -3
npx quartz build --serve &
sleep 3
```

- [ ] **Step 3: 手動逐項驗證（記錄結果到下一步的 markdown）**

| # | 項目 | 路徑 | 怎麼驗 |
|---|-----|------|------|
| 1 | 首頁 HomeHeroApple 不變（Phase 2 上線） | `/` | hero 純字 + focal canvas |
| 2 | 分類首頁 → CategoryHero | `/manufacturing-ai/` | eyebrow / h1 / copy + 右側物件 stage |
| 3 | CategoryHero scroll 時物件動（reduced-motion off） | 同上 + 滾動 | 物件 fade-in / shift / fade-out |
| 4 | 一般文章 → ArticleHero themed | 任一文章 | 60vh hero、section accent、canvas 隨主題 |
| 5 | ArticleHero canvas 跟對 section 主題 | `/manufacturing-ai/...` 一篇 | 看到 geometric-lines |
| 6 | ai-notes 看到 particle-flow | 一篇 | 粒子場 |
| 7 | coffee 看到 steam-curves | 一篇 | 蒸氣曲線 |
| 8 | Sticky TOC | 文章頁右側 | 滾動時 TOC 不動，當前段落 a 變成 section accent + 粗體 |
| 9 | cover frontmatter | `/_phase3-test-cover` | hero 用 icon.png 當背景，無 canvas |
| 10 | accent frontmatter | `/_phase3-test-accent` | hero 邊框 + badge + TOC active 都是 #ff5e3a |
| 11 | hero-style: none | `/_phase3-test-none` | 沒 ArticleHero，純 Breadcrumbs + ArticleTitle |
| 12 | popover 預覽過 hero | 任一頁面 hover wikilink | popover 內容直接從 `<p>` 開始，不見 hero |
| 13 | SPA 導航 hero 不疊加 | 點 CTA + 返回 | console.log(window.ScrollTrigger.getAll().length) 不超過合理值 |
| 14 | reduced-motion 降級 | DevTools Rendering emulation | 物件靜止 SSR 位置、canvas 第一幀、無 GSAP loaded |
| 15 | mobile 降級 | DevTools Device iPhone | 單欄、CategoryHero 物件靜態、無 GSAP、無 Sticky TOC（DesktopOnly） |
| 16 | console 0 error 全程 | 所有頁面 | 無紅 / 無黃警告 |

- [ ] **Step 4: 寫驗證紀錄 + Commit**

Create `quartz/docs/superpowers/baselines/2026-04-25-phase3-verification.md`:

```markdown
# Phase 3 手動驗證紀錄

日期：2026-04-25
Phase 3 HEAD：<最後 commit hash>
測試環境：Chrome <version>, Windows 11

## 自動檢查（automated by `npx quartz build`）

| 檢查 | 結果 |
|---|---|
| build 成功無 warning | ✓/✗ |
| `public/postscript.js` 含 `data-section-hero-canvas` / `data-category-scene` / `popover-inner` | ✓/✗ |
| `public/index.css` 含 `.article-hero` / `.category-hero` / `.toc-content a.active` | ✓/✗ |
| 文章頁 HTML 含 `<header class="article-hero">` | ✓/✗ |
| 分類頁 HTML 含 `<header class="category-hero">` | ✓/✗ |

## 手動逐頁（Step 3 16 項）

| # | 項目 | 結果 | 備註 |
|---|-----|------|------|
| 1 | 首頁 HomeHeroApple 不變 | ✓/✗ | |
| 2 | 分類頁 CategoryHero | ✓/✗ | |
| 3 | CategoryHero scroll 動畫 | ✓/✗ | reduced-motion off 條件 |
| 4 | 文章頁 ArticleHero themed | ✓/✗ | |
| 5 | manufacturing-ai canvas | ✓/✗ | geometric-lines |
| 6 | ai-notes canvas | ✓/✗ | particle-flow |
| 7 | coffee canvas | ✓/✗ | steam-curves |
| 8 | Sticky TOC + active | ✓/✗ | |
| 9 | cover frontmatter | ✓/✗ | |
| 10 | accent frontmatter | ✓/✗ | |
| 11 | hero-style: none fallback | ✓/✗ | |
| 12 | popover scroll 過 hero | ✓/✗ | |
| 13 | SPA 動畫不疊加 | ✓/✗ | `(window.ScrollTrigger?.getAll?.() ?? []).length` 紀錄（reduced-motion / mobile 路徑 ScrollTrigger 會 undefined，optional-chain 處理） |
| 14 | reduced-motion 降級 | ✓/✗ | |
| 15 | mobile 降級 | ✓/✗ | |
| 16 | console 0 error | ✓/✗ | |

## Bundle size diff vs Phase 2 baseline

| 指標 | Phase 2 (post) | Phase 3 (post) | diff |
|-----|---------------|---------------|------|
| postscript.js raw | 60,794 B | ?? | ?? |
| postscript.js gzip | ~20 KB | ?? | ?? |
| index.css raw | 82,649 B | ?? | ?? |
| index.css gzip | ~15 KB | ?? | ?? |

## 備註 / 退步項目

（任何小觀察寫這）

## 測試文章清理

Phase 3 ship 前把 `content/_phase3-test-*.md` 刪掉（或挪到 `content/_drafts/`），避免污染正式內容。
```

- [ ] **Step 5: Commit 驗證紀錄**

```bash
git add docs/superpowers/baselines/2026-04-25-phase3-verification.md
git commit -m "$(cat <<'EOF'
docs: Phase 3 手動驗證紀錄（自動檢查已填、人類待跑 16 項）

Tasks 1-8 完成後的 regression + feature 驗證表。自動部分（grep 檢查
bundle / CSS marker、build 是否乾淨）已在 commit 前實際執行並填入；
手動 16 項（hero swap / canvas / sticky TOC / frontmatter cover/accent/
hero-style:none / popover / SPA / reduced-motion / mobile / console）
留 ✓/✗ 給下游人類執行時填寫。

附三篇測試文章建議刪除步驟（避免污染正式內容）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 10: Phase 3 Lighthouse 對照

**Files:**
- Create: `quartz/docs/superpowers/baselines/2026-04-25-lighthouse-after-phase3.md`

- [ ] **Step 1: 跑 Lighthouse Desktop 三頁面**

```bash
npx quartz build 2>&1 | tail -3
npx quartz build --serve &
sleep 3
```

Chrome DevTools → Lighthouse tab → Desktop + Performance/Accessibility/Best Practices/SEO → 對 3 頁分別跑：
1. `/`（首頁）
2. `/manufacturing-ai/`（分類頁，含 CategoryHero scroll-driven scene）
3. 任一文章（含 ArticleHero canvas + Sticky TOC）

記錄分數、LCP、CLS、INP。

- [ ] **Step 2: 寫 `lighthouse-after-phase3.md`**

Create `quartz/docs/superpowers/baselines/2026-04-25-lighthouse-after-phase3.md`：

```markdown
# Phase 3 完成後 Lighthouse 分數

日期：2026-04-25
Phase 3 HEAD：<最後 commit hash>
Chrome / Lighthouse 版本：<填入>

## 首頁 `/`

| 指標 | Phase 1 | Phase 2 | Phase 3 | diff vs Phase 2 |
|-----|--------|--------|--------|----|
| Performance | ?? | ?? | ?? | ?? |
| Accessibility | ?? | ?? | ?? | ?? |
| Best Practices | ?? | ?? | ?? | ?? |
| SEO | ?? | ?? | ?? | ?? |
| LCP (ms) | ?? | ?? | ?? | ?? |
| CLS | ?? | ?? | ?? | ?? |
| INP (ms) | ?? | ?? | ?? | ?? |

## 分類頁 `/manufacturing-ai/`

(同上格式)

## 文章頁 `/manufacturing-ai/<某篇>/`

(同上格式)

## spec §9.6 目標對照

| 指標 | 目標 | 首頁 | 分類頁 | 文章頁 | Pass? |
|-----|------|----|------|------|-------|
| LCP | < 2.5s | ?? | ?? | ?? | ?? |
| INP | < 200ms | ?? | ?? | ?? | ?? |
| CLS | < 0.1 | ?? | ?? | ?? | ?? |
| Performance ≥ 90（首頁） | 90 | ?? | — | — | ?? |
| Performance ≥ 95（文章頁） | 95 | — | — | ?? | ?? |
| Accessibility ≥ 95 | 95 | ?? | ?? | ?? | ?? |

## 備註

（退步項目、可接受的 trade-off、Phase 4 audit 候選）
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/baselines/2026-04-25-lighthouse-after-phase3.md
git commit -m "$(cat <<'EOF'
docs: Phase 3 Lighthouse 分數對照模板（待人類跑分填入）

對照 Phase 1 baseline + Phase 2 完成後分數，三頁面（首頁 / 分類頁 /
文章頁）跑 Lighthouse Desktop。spec §9.6 目標對照清單留 ?? 給下游
填入實測值。

Phase 3 主要新成本：
- ArticleHero canvas（每篇文章一個 sectionCanvas instance）
- CategoryHero scroll-cinematic（GSAP 動態載入，僅分類首頁）
- Sticky TOC（IntersectionObserver active observer，純 class 變化、
  無動畫，CPU 成本極低）

預期：文章頁 LCP 略升（多了 hero canvas），但 INP / CLS 應持平或更佳。
分類頁 GSAP 載入只發生在 reduced-motion off + desktop，mobile / 降級
路徑分數應跟 Phase 2 相同。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Phase 3 完成標準（驗收）

完成所有 10 個 Task 後，check 下列全數滿足才算 Phase 3 ship：

- [ ] `npx quartz build` 無 warning / error
- [ ] `public/postscript.js` 含 10 支 motion script 全部關鍵字（`__motion` / `__nav` / `__gsapLoader` / `__sectionCanvas` / `__lenis` / `data-reveal` / `data-home-hero-focal` / `data-hero-cinematic` / `data-section-hero-canvas` / `data-category-scene` / `popover-inner`）
- [ ] `public/index.css` 含 Phase 3 三組新 selector：`.article-hero` / `.category-hero` / `.toc-content a.active`
- [ ] 任一分類頁 HTML 含 `<header class="category-hero">`
- [ ] 任一文章頁 HTML 含 `<header class="article-hero">` + `<aside class="right">` 內含 `.toc`
- [ ] 設 `hero-style: none` 的文章 HTML **不**含 `article-hero`，但有 `article-title`
- [ ] 設 `cover: ...` 的文章 HTML 有 `.article-hero__cover` 帶 `background-image`
- [ ] 設 `accent: ...` 的文章 HTML 有 `style="--article-hero-accent: ..."` inline
- [ ] 手動 16 項驗證全通過（Task 9）
- [ ] Lighthouse Phase 3 不退步（Task 10）
- [ ] Git log 顯示 10 個 Phase 3 commit（Task 1-10）

**如任一失敗**：不要進 Phase 4，先修到過。

---

## 接下來（Phase 4 預告）

Phase 3 ship 後進 Phase 4：文章頁細節 + 全站拋光（spec §10 Phase 4），含：

- `ScrollProgress.tsx`（1px 頂部進度條）
- 段落 reveal（IntersectionObserver 輕量版）
- 404 頁重做（Apple 風）
- About 頁 portrait 支援
- SPA focus management 上線（spec §6.4）
- OG image 介面預留（spec §12）
- Lighthouse / axe-core / WebPageTest audit
- Cross-browser 測試（Chrome/Edge/Firefox/Safari + iOS Safari + Android Chrome）
- `prefers-contrast` / `forced-colors` 完整測試
- BrandIntro / ContentMeta / sectionScene.inline.ts 評估是否刪除

**不要現在就寫 Phase 4 plan** — Phase 3 跑過一輪後，Phase 4 audit 出來的具體分數與 cross-browser 結果會大幅影響 plan 內容。Phase 4 plan 位置：`docs/superpowers/plans/YYYY-MM-DD-immersive-frontend-phase-4.md`。

Phase 3 ship 後建議跑一次 `superpowers:code-reviewer` 對照 spec 抓漏網。
