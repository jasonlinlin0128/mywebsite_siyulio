# Immersive Frontend — Phase 4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 全站完成度收尾 — 加上 Apple 風的 ScrollProgress 細節、文章段落 IntersectionObserver 漸入、404 重做、about 頁 portrait 支援，最後跑一次 audit / Lighthouse / cross-browser checklist 把 spec §10 Phase 4 的驗收項目掃完。Phase 4 ship 後 = spec §10 終態「可上線」。

**Architecture:**
- 新增 1 個輕量組件 `ScrollProgress.tsx`（純 div + inline script 用 scroll handler 更新 CSS var 寬度，no GSAP），透過 `sharedPageComponents.afterBody` 全站全頁掛上 1px 頂部進度條。
- 新增 1 支 inline script `paragraphReveal.inline.ts`：在文章內容區自動找 `<article p>` / `<article h2>` / `<article h3>` 等元素加 `[data-reveal]` 屬性，沿用 Phase 1 已建立的 `scrollReveal.inline.ts` IntersectionObserver 機制（不重新發明），段落滑入 viewport 時 fade-in + translateY → 0。
- 重做 Quartz 預設 404：建一個自訂 `NotFound.tsx`（取代 upstream `quartz/components/pages/404.tsx`）並加 `_404.scss` partial，Apple 風大字「404」+ 暖光暈 + 回首頁/聯絡我兩顆 CTA。
- About 頁 portrait：在 `_article-hero.scss` 加 `data-section-theme="about"` + `data-has-cover` 變體規則，用 `cover:` frontmatter 的 portrait 圖片裁成圓形 / 60vh 高的 portrait card；不另起組件，全靠 CSS。
- 既有 SPA focus management（Phase 1 navLifecycle.inline.ts 的 `focusFirstHeading()`）與 Search × Lenis（Phase 2 Task 7）已上線，Phase 4 只做驗證；無新 code。
- Audit 部分：寫 Lighthouse 最終跑分模板 + axe-core 命令說明 + cross-browser 手動 checklist；`prefers-contrast` / `forced-colors` 既有 SCSS 規則（Phase 3 已加 forced-colors fallback）需手動逐頁驗證，不寫新 code。

**Tech Stack:** Quartz 4.5.2 (Preact SSR + TSX + SCSS), TypeScript。沿用 Phase 1-3 全套 motion runtime。Phase 4 不加新 npm 依賴、不動 GSAP / Lenis / 任何 inline script 之外的部分。

**Spec reference:** [2026-04-24-immersive-frontend-design.md](../specs/2026-04-24-immersive-frontend-design.md) §5.3（ScrollProgress）、§5.4（404 + about portrait）、§6.4（SPA focus）、§6.5（Search × Lenis）、§8.5（鍵盤導航）、§8.6（prefers-contrast / forced-colors）、§10 Phase 4、§12（OG image deferred）。

**Phase 1 + 2 + 3 前置依賴（必須先 ship）：** 全部完成。`MotionRuntime` 已掛 10 支 inline script、`HomeHeroApple` / `ArticleHero` / `CategoryHero` 都進 layout、TOC sticky / popoverScroll / 三個 sectionCanvas renderer 都已生效。Phase 4 從 `feature/immersive-phase-3` HEAD 接續開新 branch。

**Commit convention:** Conventional Commits + trailing `Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>`。Phase 4 預期 5 個 commit + 1 baseline doc commit = 6 個 commit。每個 commit 後 `npx quartz build` 必須 clean。

---

## File Structure

### New files

| Path | 職責 |
|-----|------|
| `quartz/components/ScrollProgress.tsx` | 1px 頂部進度條，CSS var `--scroll-progress` 0-1 由 inline script 更新 |
| `quartz/components/scripts/scrollProgress.inline.ts` | scroll listener (`{passive:true}`) 算 progress 寫 CSS var；reduced-motion 不啟動（spec §8.1 段落只用「短淡入」，這條完全不顯示） |
| `quartz/components/scripts/paragraphReveal.inline.ts` | 進文章頁時對 `article p, article h2, article h3, article ul, article ol, article pre` auto-add `data-reveal` 屬性，讓 Phase 1 scrollReveal 自動 IO 接手 |
| `quartz/components/NotFound.tsx` | 自訂 404 頁（Apple 風大字 + 光暈 + CTA） |
| `quartz/styles/_scroll-progress.scss` | `.scroll-progress` 樣式（fixed top、accent 漸層） |
| `quartz/styles/_404.scss` | 404 頁面樣式 |
| `quartz/styles/_paragraph-reveal.scss` | `article [data-reveal]` 進場 transition + reduced-motion fallback（覆寫 _motion-tokens 的全域 `[data-reveal]` 規則，給文章段落專用） |
| `quartz/styles/_about-portrait.scss` | About 頁 portrait 變體（`.article-hero[data-section-theme="about"][data-has-cover]`） |
| `quartz/docs/superpowers/baselines/2026-04-25-phase4-verification.md` | Phase 4 + 整套 Phase 1-4 ship-ready checklist |
| `quartz/docs/superpowers/baselines/2026-04-25-lighthouse-final.md` | Phase 4 完成後 Lighthouse / axe-core / WebPageTest 對照模板 |

### Modified files

| Path | 改動 |
|-----|------|
| `quartz/components/MotionRuntime.tsx` | `concatenateResources` 加 2 支：`scrollProgress` + `paragraphReveal`（11、12 支），JSDoc 更新 |
| `quartz/components/index.ts` | export `ScrollProgress` + `NotFound`（取代 upstream `pages/404.tsx`） |
| `quartz.layout.ts` | `sharedPageComponents.afterBody` 第一個 push `Component.ScrollProgress()`（要在 MotionRuntime 之前？不，afterBody 順序不影響 render；但 ScrollProgress fixed positioned 不依賴順序）。實作中放 `MotionRuntime` 之後 |
| `quartz/styles/custom.scss` | 4 個新 partial 進 `@use` |
| `quartz/components/ArticleHero.tsx` | inline JSX 加 `data-has-cover` 屬性（讓 about portrait 變體 SCSS 可選擇） |

### Files NOT deleted (deferred to potential Phase 5 cleanup)

- `quartz/components/BrandIntro.tsx`：Phase 3 後不再 used，但保留檔（spec §15.3）
- `quartz/components/scripts/sectionScene.inline.ts`：BrandIntro 的 driver；layout 不再用 BrandIntro 代表此 script 不會綁到 DOM
- `quartz/components/ContentMeta.tsx`：功能併入 ArticleHero，layout 不用，保留檔
- 三個都不在 layout、`postscript.js` bundle 也沒影響（Quartz 只 bundle layout 用到的組件的 css/js），保留無 cost

---

## Task 1: `ScrollProgress.tsx` + inline script + SCSS + wire layout

**Files:**
- Create: `quartz/components/ScrollProgress.tsx`
- Create: `quartz/components/scripts/scrollProgress.inline.ts`
- Create: `quartz/styles/_scroll-progress.scss`
- Modify: `quartz/styles/custom.scss`（`@use`）
- Modify: `quartz/components/index.ts`
- Modify: `quartz/components/MotionRuntime.tsx`（11 支）
- Modify: `quartz.layout.ts`（`sharedPageComponents.afterBody` 加 ScrollProgress）

**ScrollProgress 設計**：1px 高 fixed top bar，寬度 = `var(--scroll-progress)` × 100%（CSS var 0-1）。inline script 監聽 `scroll` 事件 (passive)，計算 `scrollY / (documentHeight - viewportHeight)` 寫到 `document.documentElement.style.setProperty('--scroll-progress', ratio)`。spec §8.5 ScrollProgress aria-hidden（純裝飾）。reduced-motion 不停用（純 visual feedback、無動畫；只是寬度跟著捲）。

- [ ] **Step 1: 寫 `ScrollProgress.tsx`**

```tsx
import { QuartzComponent, QuartzComponentConstructor } from "./types"

/**
 * ScrollProgress — 1px 頂部進度條（spec §5.3）
 * Width 由 CSS var --scroll-progress（0-1）控制，inline script 寫入。
 * aria-hidden 因為純 visual feedback。
 */
const ScrollProgress: QuartzComponent = () => {
  return <div class="scroll-progress" aria-hidden="true" />
}

export default (() => ScrollProgress) satisfies QuartzComponentConstructor
```

- [ ] **Step 2: 寫 `scrollProgress.inline.ts`**

```ts
// ScrollProgress (spec §5.3)
// 1px top bar 寬度跟 scroll 進度，document.documentElement style 寫
// CSS var --scroll-progress (0-1)。passive listener，extremely cheap。

let scrollHandler: (() => void) | null = null

function setup() {
  teardown()
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight
    const ratio = max <= 0 ? 0 : Math.min(1, Math.max(0, window.scrollY / max))
    document.documentElement.style.setProperty("--scroll-progress", String(ratio))
  }
  update()
  scrollHandler = update
  window.addEventListener("scroll", scrollHandler, { passive: true })
  // resize 時 documentHeight 變了也要重算
  window.addEventListener("resize", scrollHandler, { passive: true })
}

function teardown() {
  if (scrollHandler) {
    window.removeEventListener("scroll", scrollHandler)
    window.removeEventListener("resize", scrollHandler)
    scrollHandler = null
  }
}

document.addEventListener("nav", setup)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

- [ ] **Step 3: 寫 `_scroll-progress.scss`**

```scss
// ScrollProgress 1px top bar (spec §5.3)
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: calc(100% * var(--scroll-progress, 0));
  height: 2px;
  background: linear-gradient(
    90deg,
    color-mix(in srgb, var(--section-accent-manufacturing) 80%, transparent) 0%,
    color-mix(in srgb, var(--section-accent-ai-notes) 60%, transparent) 50%,
    color-mix(in srgb, var(--section-accent-coffee) 60%, transparent) 100%
  );
  z-index: 9999;
  pointer-events: none;
  transition: width 80ms linear;
  // forced-colors / prefers-contrast：保留為實線（spec §8.6）
  @media (forced-colors: active) {
    background: CanvasText;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-progress { transition: none; }
}
```

- [ ] **Step 4: Wire 進 `custom.scss` + `index.ts` + `MotionRuntime.tsx` + `quartz.layout.ts`**

`custom.scss` 加 `@use "./_scroll-progress.scss";` 在最後。

`index.ts` 加 `import ScrollProgress from "./ScrollProgress"` + export。

`MotionRuntime.tsx` 加 `// @ts-ignore` import + `scrollProgressScript` 進 `concatenateResources` 最後一個位置（11 支）；JSDoc 更新。

`quartz.layout.ts` 在 `sharedPageComponents.afterBody` push `Component.ScrollProgress()`（第一個位置）：

```ts
afterBody: [
  Component.ScrollProgress(),  // Phase 4 — 1px top progress bar
  Component.MotionRuntime(),
  Component.ConditionalRender({ ... RecentNotes ... }),
],
```

- [ ] **Step 5: Build + Commit**

```bash
npx quartz build 2>&1 | tail -3
grep -oE "scroll-progress|--scroll-progress" public/index.html public/index.css public/postscript.js | sort -u
# 預期：scroll-progress class + CSS var 都在
```

```bash
git add quartz/components/ScrollProgress.tsx \
  quartz/components/scripts/scrollProgress.inline.ts \
  quartz/styles/_scroll-progress.scss \
  quartz/styles/custom.scss \
  quartz/components/index.ts \
  quartz/components/MotionRuntime.tsx \
  quartz.layout.ts

git commit -m "$(cat <<'EOF'
feat: ScrollProgress 1px 頂部進度條（spec §5.3）

ScrollProgress 組件 + inline script + SCSS + layout wire：
- 純 div + CSS var --scroll-progress (0-1) 控制 width
- passive scroll + resize listener 寫 documentElement style var
- nav/prenav lifecycle 接 setup/teardown
- aria-hidden（spec §8.5 純 visual feedback）
- forced-colors fallback 用 CanvasText（spec §8.6）
- reduced-motion 取消 width transition（避免 width 動畫被讀為 motion）

Section accent 漸層用 manufacturing-ai → ai-notes → coffee 三色，避
單一 section 配色限制。

11 支 motion script in MotionRuntime；scrollProgress 是最輕量的（純
scroll handler，無 rAF，無 GSAP）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 2: 段落 reveal — `paragraphReveal.inline.ts` + SCSS

**Files:**
- Create: `quartz/components/scripts/paragraphReveal.inline.ts`
- Create: `quartz/styles/_paragraph-reveal.scss`
- Modify: `quartz/styles/custom.scss`（`@use`）
- Modify: `quartz/components/MotionRuntime.tsx`（12 支）

**設計**：Quartz article body 的元素是 markdown 渲染出來的 `<p> / <h2> / <h3> / <pre> / <ul> / <ol>`，沒有 `[data-reveal]` 屬性。Phase 4 加一支 inline script 在 `nav` 事件對 `article p, article h2, article h3, article pre, article ul, article ol` 自動加 `data-reveal=""` 屬性，這樣 Phase 1 既有的 `scrollReveal.inline.ts` IntersectionObserver 就會自動處理進場 fade。`_paragraph-reveal.scss` 給文章內元素覆寫 transition timing，比 Phase 1 全域 `[data-reveal]` 更輕（duration 短一點，translateY 6px 而非 12px）。

- [ ] **Step 1: 寫 `paragraphReveal.inline.ts`**

```ts
// 文章段落 reveal (spec §10 Phase 4)
// 對 article 內的 block 元素自動加 [data-reveal]，讓 Phase 1 scrollReveal
// IntersectionObserver 接手做 fade-in。reduced-motion 由 scrollReveal 內部
// 處理（直接 .revealed，無動畫），這裡不另外 gate。

const SELECTORS = "article p, article h2, article h3, article h4, article pre, article ul, article ol, article blockquote, article figure"

let added: HTMLElement[] = []

function setup() {
  teardown()
  const els = document.querySelectorAll<HTMLElement>(SELECTORS)
  els.forEach((el) => {
    if (el.hasAttribute("data-reveal")) return  // 已有 (Phase 3 ArticleHero 內有也跳過)
    el.setAttribute("data-reveal", "")
    added.push(el)
  })
  // scrollReveal.inline.ts 自己會在 nav 事件 query 全頁 [data-reveal]，所以
  // 順序很重要：paragraphReveal 必須在 scrollReveal 之前跑（在 MotionRuntime
  // concatenate 順序中放 scrollReveal 之前）— 但 concatenate 全部跑完才開始
  // 觸發 nav listener，所以實際上是「同一 nav event tick 內」順序執行。
}

function teardown() {
  for (const el of added) {
    el.removeAttribute("data-reveal")
  }
  added = []
}

document.addEventListener("nav", setup)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

**重要**：MotionRuntime 載入順序中 `paragraphReveal` 必須在 `scrollReveal` **之前**。原 scrollReveal 在 motionFeatureDetect / navLifecycle 之後第 3 支，paragraphReveal 要插到 #3 之前 → 變第 3 支，scrollReveal 變第 4 支。重新編號其他 script。

實際上更簡單：paragraphReveal 自己在 `nav` listener handler 裡先跑（同步 query + setAttribute），同 nav 事件 dispatch 順序中只要 paragraphReveal 的 listener 在 scrollReveal 之前 register 就行。`document.addEventListener` 多個 listener 按 register 順序觸發。所以 MotionRuntime 內 `paragraphReveal` 放 `scrollReveal` **之前** 就 OK。

- [ ] **Step 2: 寫 `_paragraph-reveal.scss`**

```scss
// 文章段落 reveal — 比 Phase 1 全域 [data-reveal] 更輕（spec §10 Phase 4）
// Phase 1 _motion-tokens.scss 全域 [data-reveal]：opacity 0→1 + translateY 12px → 0，
// 這裡覆寫文章內 [data-reveal] 用更短時間 + 更小位移（避閱讀時被 motion 干擾）

article [data-reveal] {
  opacity: 0;
  transform: translateY(6px);
  transition:
    opacity var(--motion-duration-fast) var(--motion-easing),
    transform var(--motion-duration-fast) var(--motion-easing);

  &.revealed {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  article [data-reveal] {
    opacity: 1;
    transform: none;
    transition: opacity 0.15s linear;
  }
}
```

- [ ] **Step 3: Wire + Build + Commit**

```bash
# Modify custom.scss 加 @use "./_paragraph-reveal.scss";
# Modify MotionRuntime.tsx 加 paragraphRevealScript（在 scrollRevealScript 之前）
# 12 支 in concatenateResources

npx quartz build 2>&1 | tail -3
grep -oE 'data-reveal' public/manufacturing-ai/*.html | head -5
# 預期：build 出來的 HTML 還沒 data-reveal（這是 client-side 加的），但
# postscript.js 應該有 SELECTORS 字串
grep -oE 'article p, article h2|article p,article h2' public/postscript.js | head -1
```

```bash
git add quartz/components/scripts/paragraphReveal.inline.ts \
  quartz/styles/_paragraph-reveal.scss \
  quartz/styles/custom.scss \
  quartz/components/MotionRuntime.tsx

git commit -m "$(cat <<'EOF'
feat: 段落 reveal — paragraphReveal inline script + 文章專用 transition

spec §10 Phase 4 段落 reveal 交付：
- paragraphReveal.inline.ts: nav 事件對 article 內的 p/h2/h3/h4/pre/ul/ol/
  blockquote/figure 自動加 [data-reveal] 屬性
- 沿用 Phase 1 已建立的 scrollReveal IntersectionObserver 機制，不重新發明
- _paragraph-reveal.scss: 文章內 [data-reveal] 覆寫全域規則，duration 縮短
  到 fast、translateY 從 12px 降到 6px（避閱讀時 motion 干擾）
- reduced-motion 走 0.15s linear 淡入（spec §8.1 「保留 0.2s 極短淡入」）

MotionRuntime concatenate 順序：paragraphReveal 放 scrollReveal 之前，確保
listener register 順序正確（document.addEventListener 按 register 順序觸發
listener）。12 支 motion script。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 3: 404 頁重做（Apple 風）

**Files:**
- Create: `quartz/components/NotFound.tsx`（取代 upstream `quartz/components/pages/404.tsx` 透過 layout）
- Create: `quartz/styles/_404.scss`
- Modify: `quartz/styles/custom.scss`（`@use`）
- Modify: `quartz/components/index.ts`（export NotFound）

**設計**：Quartz upstream `pages/404.tsx` 是 contentPage 機制，會 render 預設 layout。Phase 4 自訂的 NotFound 走 spec §5.4「Apple 風錯誤頁（大字「404」+ 淡光暈 + 回首頁按鈕）」。

實作策略：upstream Quartz 的 `pages/404.tsx` 可以用 `quartz.config.ts` 或 layout override。先看是否能在 `quartz.layout.ts` 對 `slug === "404"` 條件 render 自訂組件。實作期由 implementer 確認 upstream 機制。Phase 4 plan 預留：若 layout override 不行，退而使用 SCSS 在現有 `.content` 加變體覆寫。

- [ ] **Step 1: 寫 `NotFound.tsx`**

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative, FullSlug } from "../util/path"

/**
 * NotFound — Apple 風 404 頁（spec §5.4）
 * 大字「404」+ 淡光暈 + 回首頁 / 看分類 兩顆 CTA
 */
export default (() => {
  const NotFound: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ("404" as FullSlug)
    return (
      <section class="not-found" data-section-theme="home">
        <div class="not-found__glow" aria-hidden="true" />
        <div class="not-found__copy">
          <p class="not-found__eyebrow">PAGE NOT FOUND</p>
          <h1 class="not-found__code">404</h1>
          <p class="not-found__lead">這個頁面已經不存在，或從來不曾存在。</p>
          <div class="not-found__actions">
            <a class="not-found__cta not-found__cta--primary" href={resolveRelative(slug, "" as FullSlug)}>
              回首頁
            </a>
            <a class="not-found__cta" href={resolveRelative(slug, "manufacturing-ai/index" as FullSlug)}>
              看製造業 AI
            </a>
          </div>
        </div>
      </section>
    )
  }
  return NotFound
}) satisfies QuartzComponentConstructor
```

- [ ] **Step 2: 寫 `_404.scss`**

```scss
// 404 頁面 Apple 風（spec §5.4）
.not-found {
  position: relative;
  box-sizing: border-box;
  min-height: calc(100vh - 12rem);
  display: grid;
  place-items: center;
  padding: clamp(2rem, 5vw, 5rem);
  isolation: isolate;
  overflow: hidden;
  text-align: center;
}

.not-found__glow {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: radial-gradient(
    circle at 50% 40%,
    rgba(200, 169, 107, 0.18) 0%,
    transparent 60%
  );
  pointer-events: none;
}

.not-found__copy {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 1rem;
  max-width: 36rem;
  justify-items: center;
}

.not-found__eyebrow {
  margin: 0;
  font-size: 0.85rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.7;
}

.not-found__code {
  margin: 0;
  font-family: var(--headerFont), "Outfit", sans-serif;
  font-size: clamp(6rem, 18vw, 14rem);
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.04em;
  background: linear-gradient(
    135deg,
    var(--section-accent-manufacturing) 0%,
    var(--section-accent-ai-notes) 50%,
    var(--section-accent-coffee) 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

.not-found__lead {
  margin: 0;
  font-size: clamp(1rem, 1.2vw, 1.15rem);
  opacity: 0.78;
  line-height: 1.65;
}

.not-found__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 1rem;
  justify-content: center;
}

.not-found__cta {
  display: inline-flex;
  align-items: center;
  padding: 0.7rem 1.4rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 247, 234, 0.26);
  font-weight: 600;
  text-decoration: none;
  color: var(--dark);
  background: transparent;
  transition: background 0.4s cubic-bezier(0.22, 1, 0.36, 1);

  &:hover { background: rgba(255, 247, 234, 0.08); }

  &--primary {
    background: var(--dark);
    color: var(--light);
    border-color: var(--dark);

    &:hover { background: rgba(18, 16, 13, 0.88); }
  }
}

@media (forced-colors: active) {
  .not-found__glow,
  .not-found__code {
    background: none;
    -webkit-text-fill-color: CanvasText;
    color: CanvasText;
  }
}
```

- [ ] **Step 3: Wire + Build**

加 `@use "./_404.scss";` 進 `custom.scss`。Export NotFound 進 `index.ts`。

研究 Quartz 的 404 機制 — `quartz/components/pages/404.tsx` 既有 export 是 `NotFound`，可能直接 override 或透過 `quartz.config.ts.configuration.notFound` 之類。實作期 implementer 自行確認最小入侵點。預設假設：把 upstream `pages/404.tsx` 改成 import 我們的 `Component.NotFound()` JSX，或在 layout 加 ConditionalRender 對 `slug === "404"`。

最務實的方式是修改 `quartz/components/pages/404.tsx` 直接用我們的 NotFound JSX（單一檔修改，不影響其他）：

```tsx
// quartz/components/pages/404.tsx — Phase 4 改造
import NotFound from "../NotFound"
import { QuartzComponentConstructor } from "../types"

export default ((opts) => NotFound()) satisfies QuartzComponentConstructor
```

或更乾淨的方式：在 `quartz.layout.ts` 加 ConditionalRender，但 spec 沒明示。實作期決定。

- [ ] **Step 4: Test 404**

啟動 dev server，瀏覽 `/non-existent-page` → 應看到 Apple 風 404，大字 + 兩顆 CTA。

- [ ] **Step 5: Commit**

```bash
git add quartz/components/NotFound.tsx \
  quartz/styles/_404.scss \
  quartz/styles/custom.scss \
  quartz/components/index.ts \
  quartz/components/pages/404.tsx

git commit -m "$(cat <<'EOF'
feat: 404 頁重做（Apple 風大字 + 暖光暈 + CTA）

spec §5.4 「Apple 風錯誤頁（大字「404」+ 淡光暈 + 回首頁按鈕）」實作：
- NotFound.tsx: 純字 JSX，eyebrow + 大字 404 + lead + 兩顆 CTA
- _404.scss: 大字用 manufacturing → ai-notes → coffee section accent 漸層
  text-fill-color: transparent；center radial glow；按鈕沿用 home-hero CTA
  風格保持一致
- forced-colors fallback (spec §8.6)

upstream pages/404.tsx 改為 re-export 我們的 NotFound（最小入侵）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 4: About portrait 支援

**Files:**
- Create: `quartz/styles/_about-portrait.scss`
- Modify: `quartz/styles/custom.scss`（`@use`）
- Modify: `quartz/components/ArticleHero.tsx`（加 `data-has-cover` attribute）

**設計**：about 頁 frontmatter 設 `cover: ./portrait.jpg` 時，hero 用「portrait card」變體 — 圓形 / 60vh 高 / 跟文字並列而非絕對定位背景。spec §5.4 「`cover:` 放 portrait」明示但無細節，Phase 4 用 CSS-only 變體處理（不改 ArticleHero TSX 的核心結構）。

- [ ] **Step 1: ArticleHero.tsx 加 `data-has-cover` 屬性**

修改 `ArticleHero.tsx` 的 `<header>` 標籤加 `data-has-cover`：

```tsx
<header
  class="article-hero"
  data-section-theme={themeKey}
  data-hero-style={heroStyle}
  data-has-cover={heroStyle === "themed" && cover ? "true" : undefined}
  style={accentStyle}
>
```

對 about 頁（slug 起頭 about/）frontmatter 設 `cover:` 時 → `data-section-theme="about"` AND `data-has-cover="true"` 同時成立 → about-portrait SCSS 變體匹配。

但等等：`inferHeroStyle()` Phase 3 已把 `about/*` slug 自動推成 `minimal`。`hero-style: minimal` 變體會 `display: none` 兩個 cover 容器。

修法：在 `inferHeroStyle()` 加例外 — 如果 about slug 同時有 `cover:` frontmatter，仍走 themed（讓 portrait 顯示）：

```ts
function inferHeroStyle(
  slug: string,
  frontmatterValue: string | undefined,
  hasCover: boolean,
): "themed" | "minimal" {
  if (frontmatterValue === "minimal") return "minimal"
  if (slug.startsWith("tags/")) return "minimal"
  // about 沒 cover 才走 minimal；有 cover 走 themed 帶 portrait card 變體
  if ((slug === "about" || slug.startsWith("about/")) && !hasCover) return "minimal"
  return "themed"
}
```

呼叫處改成：

```ts
const heroStyle = inferHeroStyle(slug, heroStyleRaw, !!coverRaw)
```

- [ ] **Step 2: 寫 `_about-portrait.scss`**

```scss
// About 頁 portrait 變體（spec §5.4）
// 條件：data-section-theme="about" + data-has-cover="true"
// 把 article-hero__cover 從「絕對定位背景」改成「圓形 portrait card」
// 跟文字並列（不再蓋）

.article-hero[data-section-theme="about"][data-has-cover="true"] {
  grid-template-columns: minmax(0, 1fr) minmax(180px, 280px);
  grid-template-rows: 1fr;
  gap: clamp(1.5rem, 3vw, 2.4rem);
  align-items: center;
  padding: clamp(2rem, 4vw, 4rem) clamp(1.5rem, 4vw, 3rem);

  .article-hero__cover {
    position: relative;
    inset: auto;
    z-index: 1;
    border-radius: 50%;
    aspect-ratio: 1;
    width: 100%;
    height: auto;
    max-height: 320px;
    background-size: cover;
    background-position: center;

    &::after {
      // 軟陰影 / glow
      content: "";
      position: absolute;
      inset: -4px;
      border-radius: 50%;
      background: linear-gradient(
        135deg,
        color-mix(in srgb, var(--article-hero-accent) 30%, transparent) 0%,
        transparent 100%
      );
      z-index: -1;
    }
  }

  .article-hero__copy {
    justify-self: stretch;
  }

  @media all and (max-width: 767px) {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;

    .article-hero__cover {
      max-width: 200px;
      max-height: 200px;
      justify-self: center;
    }
  }
}
```

- [ ] **Step 3: Wire + Build**

加 `@use "./_about-portrait.scss";` 進 `custom.scss`。

- [ ] **Step 4: Test**

建測試文章 `content/_phase4-test-about-portrait.md`：

```markdown
---
title: About 測試
cover: /static/icon.png
draft: true
---

# 內文

驗證 about + cover 走 portrait card 變體。
```

但這是非 about/ slug — 應該不會觸發 about 變體。實際 about 頁建在 `content/about.md`（spec 提及）。如果 repo 已有 `content/about.md` 直接加 `cover:` 進 frontmatter 測。否則建 `content/about.md` 簡單版。

實作期確認 `content/about.md` 是否存在 + 是否願意暫時加 `cover:` 測。

- [ ] **Step 5: Commit**

```bash
git add quartz/components/ArticleHero.tsx \
  quartz/styles/_about-portrait.scss \
  quartz/styles/custom.scss

git commit -m "$(cat <<'EOF'
feat: About 頁 portrait 支援（spec §5.4）

ArticleHero 改 inferHeroStyle 加例外：about/* slug 有 cover frontmatter
時走 themed（顯示 portrait），無 cover 仍走 minimal。

新 _about-portrait.scss 變體：
- data-section-theme="about" + data-has-cover="true" 同時匹配
- grid 改 1fr / 280px 兩欄（文字 + portrait card）
- portrait card 用圓形 + section accent glow，沒 absolute fill 背景
- mobile 變單欄垂直堆疊

ArticleHero TSX 加 data-has-cover 屬性給 SCSS selector 用。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 5: 全 Phase ship-ready 驗證 + Lighthouse final + audit checklist

**Files:**
- Create: `quartz/docs/superpowers/baselines/2026-04-25-phase4-verification.md`
- Create: `quartz/docs/superpowers/baselines/2026-04-25-lighthouse-final.md`

**這 task 不寫 code**，把 spec §10 Phase 4 驗收項目 + cross-browser checklist + audit 命令說明全部彙整成兩份 baseline doc 給人類執行。

- [ ] **Step 1: 寫 `phase4-verification.md`**

包含：
- 自動檢查（grep `scroll-progress` / `not-found__code` / `data-has-cover` / 11 支 motion script bundle）
- 手動 Phase 4 新功能（ScrollProgress / 段落 reveal / 404 / about portrait）
- 手動 spec §10 Phase 4 驗收（Lighthouse / Accessibility / 0 console error / 鍵盤導航 / iOS Safari Lenis）
- Cross-browser checklist（Chrome / Edge / Firefox / Safari + iOS Safari + Android Chrome）
- prefers-contrast / forced-colors 逐頁檢查
- 整套 Phase 1-4 ship-ready signoff

- [ ] **Step 2: 寫 `lighthouse-final.md`**

包含：
- 三頁面 Lighthouse 跑分（首頁 / 分類 / 文章），對照 Phase 1 / 2 / 3 baseline
- spec §9.6 全部目標達成 / 未達成清單
- axe-core CLI 命令（或 Lighthouse 內建 a11y audit 結果）
- WebPageTest URL 與分數
- 退步項目 / 遺留 known issues

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/baselines/2026-04-25-phase4-verification.md \
  docs/superpowers/baselines/2026-04-25-lighthouse-final.md

git commit -m "$(cat <<'EOF'
docs: Phase 4 verification + Lighthouse final + audit checklist

Phase 4 ship-ready signoff 模板（自動部分填入 grep 結果，手動部分留 ?? / ✓✗）：
- phase4-verification.md：4 項新功能（ScrollProgress / 段落 reveal / 404 /
  about portrait）+ spec §10 Phase 4 驗收 + cross-browser checklist +
  forced-colors / prefers-contrast 逐頁
- lighthouse-final.md：三頁 Lighthouse 對照 Phase 1-3 baseline + spec §9.6
  全部目標 + axe-core / WebPageTest 跑分

整套 Phase 1-4（spec §10 全 phase）至此可宣告完成態。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Phase 4 完成標準

- [ ] `npx quartz build` 無 warning
- [ ] `public/postscript.js` 含 `scroll-progress` / `paragraphReveal` 字串（12 支 motion script）
- [ ] `public/index.css` 含 `.scroll-progress` / `.not-found__code` / `.article-hero[data-has-cover]`
- [ ] 跑 `/` 看到 1px top progress bar 跟著 scroll 走
- [ ] 文章頁段落滑入 viewport 時淡入
- [ ] `/non-existent-page` 看到 Apple 風 404
- [ ] About 頁設 cover 後看到 portrait card 變體
- [ ] Lighthouse 三頁面分數達 spec §9.6 目標
- [ ] Cross-browser 全綠 (manual)
- [ ] Git log 顯示 5 個 Phase 4 commit + 1 baseline commit

---

## 完成後

整套 spec §10 Phase 1-4 全完工。下一步：
1. PR 流程（Phase 3 + Phase 4 可合併開一個 PR 也可分開）
2. merge 到 v4 → 可以 push 到 main / 部署
3. 評估是否 Phase 5（清掉 BrandIntro / sectionScene / ContentMeta 等保留檔；可選）
