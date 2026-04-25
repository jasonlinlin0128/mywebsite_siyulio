# Immersive Frontend — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立沉浸式改造所需的全部 motion 基礎建設（scripts / styles / SPA hooks / vendored libs），但不啟動任何動畫 — 現有頁面視覺零變化、零 regression。

**Architecture:** 在 Quartz 的 `afterDOMLoaded` pipeline 加一個 no-render `MotionRuntime` 組件，集中載入 4 個 motion 工具 inline script（`navLifecycle` / `scrollReveal` / `gsapLoader` / `motionFeatureDetect`）。GSAP + ScrollTrigger 以 vendored static asset 放在 `static/vendor/` 供 Phase 2+ 動態 `<script>` 注入使用。SCSS 層新增 motion tokens 與 popover-immersive（後者在 Phase 3 才會有作用，現在是 dormant CSS）。`sectionThemes.ts` 擴充 `motionConfig` 欄位。

**Tech Stack:** Quartz 4.5.2 (Preact SSR + TSX + SCSS), esbuild (inline script bundling), GSAP 3.12.x (vendored), TypeScript。無新測試框架（沿用 `npx quartz build` + grep output + 手動瀏覽器驗證作為「test」）。

**Spec reference:** [2026-04-24-immersive-frontend-design.md](../specs/2026-04-24-immersive-frontend-design.md) §10 Phase 1。

**Commit convention (per user CLAUDE.md):** Conventional Commits + trailing `Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>`。

---

## File Structure

### New files

| Path | 職責 |
|-----|------|
| `quartz/static/vendor/gsap.min.js` | Vendored GSAP 3.12.x core（Phase 2 才用） |
| `quartz/static/vendor/ScrollTrigger.min.js` | Vendored ScrollTrigger plugin |
| `quartz/static/vendor/LICENSE-GSAP.txt` | GSAP 授權聲明 |
| `quartz/styles/_motion-tokens.scss` | Duration / easing / stagger / light-mode accent 色 token |
| `quartz/styles/_popover-immersive.scss` | popover 內隱藏 `.article-hero` 規則（dormant） |
| `quartz/components/scripts/motionFeatureDetect.inline.ts` | `prefersReducedMotion()` / `isMobileViewport()` / `bodyOptsIn()` |
| `quartz/components/scripts/scrollReveal.inline.ts` | IntersectionObserver on `[data-reveal]`，加 `.revealed` class |
| `quartz/components/scripts/gsapLoader.inline.ts` | Race-safe 動態載入 vendored GSAP（export `loadGsap`） |
| `quartz/components/scripts/navLifecycle.inline.ts` | `navGeneration` token + `prenav`/`nav` 骨架 + `focusFirstHeading()` |
| `quartz/components/MotionRuntime.tsx` | No-render component，把 4 支 inline script concatenate 進 `afterDOMLoaded` |
| `quartz/docs/superpowers/baselines/2026-04-24-lighthouse.md` | Phase 1 上線前 Lighthouse 基準分數 |

### Modified files

| Path | 改動 |
|-----|------|
| `quartz/components/sectionThemes.ts` | `SectionTheme` type 加 `motionConfig` 欄位；3 個 section 補對應值 |
| `quartz/components/index.ts` | Export 新 `MotionRuntime` |
| `quartz/styles/custom.scss` | `@use "./_motion-tokens"` + `@use "./_popover-immersive"` |
| `quartz.layout.ts` | `sharedPageComponents.afterBody` 加 `Component.MotionRuntime()` |

---

## Task 1: Vendor GSAP static assets

**Files:**
- Create: `quartz/static/vendor/gsap.min.js`
- Create: `quartz/static/vendor/ScrollTrigger.min.js`
- Create: `quartz/static/vendor/LICENSE-GSAP.txt`

- [ ] **Step 1: 下載 GSAP 3.12.7 + ScrollTrigger**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
mkdir -p static/vendor
curl -sL -o static/vendor/gsap.min.js \
  https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/gsap.min.js
curl -sL -o static/vendor/ScrollTrigger.min.js \
  https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/ScrollTrigger.min.js
```

- [ ] **Step 2: 驗證檔案大小與完整性**

```bash
ls -l static/vendor/
# 預期：gsap.min.js ~70-80KB, ScrollTrigger.min.js ~30-40KB (未 gzipped 的 min 大小)
head -c 200 static/vendor/gsap.min.js
# 預期：開頭是 /*! GSAP 3.12.7 ... */
```

- [ ] **Step 3: 寫 LICENSE 通知**

Create `static/vendor/LICENSE-GSAP.txt`:

```
GSAP (GreenSock Animation Platform) by GreenSock.
https://greensock.com

Since November 2024 (Webflow acquisition), GSAP and its plugins
(including ScrollTrigger) are free for commercial use under GSAP's
standard license. No "Business Green" Club membership required.

See: https://greensock.com/licensing/

This site (www.siyulio.com) uses GSAP 3.12.7 as a vendored static
asset for scroll-driven animations on homepage and category pages.
```

- [ ] **Step 4: Build 驗證 static 檔案有被複製**

```bash
npx quartz build 2>&1 | tail -5
ls public/static/vendor/
# 預期：看到 gsap.min.js / ScrollTrigger.min.js / LICENSE-GSAP.txt
```

- [ ] **Step 5: Commit**

```bash
git add static/vendor/
git commit -m "$(cat <<'EOF'
feat: vendor GSAP 3.12.7 + ScrollTrigger (Phase 1 不用，Phase 2 才啟動)

放到 static/vendor/ 讓 Quartz Plugin.Static 複製到 public/static/vendor/
供 Phase 2 的 gsapLoader 動態 <script> 注入使用。選 vendored static asset
而非 CDN 或 npm bundle 的原因見 spec §9.1-9.4。

GSAP 2024-11 Webflow 收購後全系列商用免費，LICENSE-GSAP.txt 記錄此授權。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 2: Motion tokens SCSS

**Files:**
- Create: `quartz/styles/_motion-tokens.scss`
- Modify: `quartz/styles/custom.scss`

- [ ] **Step 1: 創建 motion tokens SCSS**

Create `quartz/styles/_motion-tokens.scss`:

```scss
// Motion system tokens (spec §3.4 + §3.2 light-mode accents)
// -----------------------------------------------------------

// Duration
$motion-duration-fast:  0.4s;   // 微動作
$motion-duration-base:  0.6s;   // 標準 reveal
$motion-duration-slow:  1.2s;   // hero 開場

// Easing — Apple 標準
$motion-easing:         cubic-bezier(0.22, 1, 0.36, 1);

// Stagger / viewport trigger offset
$motion-stagger:        80ms;
$motion-reveal-offset:  12%;

// Section accent — dark mode (既有值)
$section-accent-manufacturing-dark: #c8a96b;
$section-accent-ai-notes-dark:      #7b8cc7;
// coffee 暗底色從 #a47148 (4.55:1) 提到 #b4876a (6.04:1) 留緩衝 (spec §13 決策 #5)
$section-accent-coffee-dark:        #b4876a;

// Section accent — light mode (v3 新增)
$section-accent-manufacturing-light: #7a5a20;
$section-accent-ai-notes-light:      #3a4d8a;
$section-accent-coffee-light:        #5c3a1c;

// CSS custom properties for runtime access
:root {
  --motion-duration-fast: #{$motion-duration-fast};
  --motion-duration-base: #{$motion-duration-base};
  --motion-duration-slow: #{$motion-duration-slow};
  --motion-easing: #{$motion-easing};
  --motion-stagger: #{$motion-stagger};

  --section-accent-manufacturing: #{$section-accent-manufacturing-light};
  --section-accent-ai-notes:      #{$section-accent-ai-notes-light};
  --section-accent-coffee:        #{$section-accent-coffee-light};
}

html[saved-theme="dark"] {
  --section-accent-manufacturing: #{$section-accent-manufacturing-dark};
  --section-accent-ai-notes:      #{$section-accent-ai-notes-dark};
  --section-accent-coffee:        #{$section-accent-coffee-dark};
}

// data-reveal entry animation (Phase 1 只有定義，沒元素用)
[data-reveal] {
  opacity: 0;
  transform: translateY(12px);
  transition:
    opacity var(--motion-duration-base) var(--motion-easing),
    transform var(--motion-duration-base) var(--motion-easing);

  &.revealed {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: opacity 0.2s linear;
  }
}
```

- [ ] **Step 2: Wire 到 custom.scss**

Modify `quartz/styles/custom.scss` — 在 `@use "./base.scss";` 後面加一行：

```scss
@use "./base.scss";
@use "./_motion-tokens.scss";   // 新增

body {
  // ... (保持原樣)
```

- [ ] **Step 3: Build 驗證**

```bash
npx quartz build 2>&1 | tail -5
grep -l "motion-duration-base" public/index.css 2>/dev/null || ls public/*.css
```

預期：build 成功無 warning，CSS 輸出含 `--motion-duration-base` 等 custom property。

- [ ] **Step 4: Commit**

```bash
git add styles/_motion-tokens.scss styles/custom.scss
git commit -m "$(cat <<'EOF'
feat: motion tokens + light-mode section accent 色 token

新增 styles/_motion-tokens.scss 放 duration/easing/stagger 等 motion
變數，以及 3 個 section 的 dark/light mode accent 色。另加 [data-reveal]
class 的基礎進場動畫定義（Phase 1 還沒元素用，但底子先打）。

見 spec §3.2 (色票表) + §3.4 (motion tokens)。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 3: Popover-immersive SCSS (dormant)

**Files:**
- Create: `quartz/styles/_popover-immersive.scss`
- Modify: `quartz/styles/custom.scss`

**注意**：Phase 1 創這個檔案是為了打基礎，裡面的 selector (`.article-hero` / `.scroll-progress`) 在 Phase 3 才會被實際 render — 現在是 dormant CSS，永遠匹配不到，不會有 side effect。

- [ ] **Step 1: 創建 popover-immersive SCSS**

Create `quartz/styles/_popover-immersive.scss`:

```scss
// Popover × ArticleHero 碰撞防治（spec §6.3）
// 當 popover 預覽抓到一篇文章的 HTML 時，它會連 ArticleHero 一起抓
// 進 .popover-inner。這份 CSS 讓 popover 內不顯示 hero 區塊，直接
// 從文章內容開始。
// 另見 Phase 3 的 scripts/popoverScroll.inline.ts（用 MutationObserver
// scroll 到第一個內容元素）。

.popover-inner {
  // Phase 3 才會有這些 class，現在是 dormant
  .article-hero,
  .scroll-progress,
  .breadcrumbs {
    display: none;
  }

  // 去掉 beforeBody 後的頂端留白
  > :first-child {
    margin-top: 0;
    padding-top: 0;
  }
}
```

- [ ] **Step 2: Wire 到 custom.scss**

Modify `quartz/styles/custom.scss`:

```scss
@use "./base.scss";
@use "./_motion-tokens.scss";
@use "./_popover-immersive.scss";   // 新增

body {
  // ... (保持原樣)
```

- [ ] **Step 3: Build 驗證**

```bash
npx quartz build 2>&1 | tail -3
```

預期：build 成功無 warning。CSS 輸出含 `.popover-inner` block（但 selector `.article-hero` 還沒元素對應，所以匹配不到）。

- [ ] **Step 4: Commit**

```bash
git add styles/_popover-immersive.scss styles/custom.scss
git commit -m "$(cat <<'EOF'
feat: popover-immersive SCSS (dormant，Phase 3 才會匹配到元素)

先把 popover 隱藏 ArticleHero / ScrollProgress / Breadcrumbs 的規則
放進 styles/_popover-immersive.scss，Phase 3 當那些元素實際 render
時就會自動生效。現階段沒元素對應，匹配為空，無 side effect。

見 spec §6.3。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 4: sectionThemes 擴充 motionConfig

**Files:**
- Modify: `quartz/components/sectionThemes.ts`

- [ ] **Step 1: 加 `MotionConfig` type 與擴充 `SectionTheme`**

在 `sectionThemes.ts` 的 type 定義區塊（`export type SceneObject` 之後）加：

```ts
export type CanvasRenderer = "geometric-lines" | "particle-flow" | "steam-curves"

export type MotionConfig = {
  canvasRenderer: CanvasRenderer
  glowColorDark: string     // 暗模式 glow 色（通常是 section accent 加 alpha）
  glowColorLight: string    // 亮模式 glow 色
  particleDensity: number   // Canvas 粒子數量（~30-80）
}
```

然後在 `SectionTheme` type 裡加一欄：

```ts
export type SectionTheme = {
  key: Exclude<SectionKey, "home">
  slugPrefix: `${string}/`
  href: FullSlug
  label: string
  navLabel: string
  title: string
  copy: string
  description: string
  status: string
  sceneIntro: string
  sceneNote: string
  signals: string[]
  sceneInteractive: boolean
  sceneObjects: SceneObject[]
  motionConfig: MotionConfig    // 新增
}
```

- [ ] **Step 2: 填入 3 個 section 的 motionConfig**

在 `sectionThemes` 陣列裡，每個 section 物件都加 `motionConfig`。以 `manufacturing-ai` 為例（其他兩個依同樣 pattern）：

```ts
{
  key: "manufacturing-ai",
  // ... 既有欄位保持 ...
  motionConfig: {
    canvasRenderer: "geometric-lines",
    glowColorDark: "rgba(200, 169, 107, 0.24)",   // #c8a96b @ 24%
    glowColorLight: "rgba(122, 90, 32, 0.18)",    // #7a5a20 @ 18%
    particleDensity: 30,
  },
},
```

`ai-notes`：

```ts
motionConfig: {
  canvasRenderer: "particle-flow",
  glowColorDark: "rgba(123, 140, 199, 0.24)",     // #7b8cc7 @ 24%
  glowColorLight: "rgba(58, 77, 138, 0.18)",      // #3a4d8a @ 18%
  particleDensity: 60,
},
```

`coffee`：

```ts
motionConfig: {
  canvasRenderer: "steam-curves",
  glowColorDark: "rgba(164, 113, 72, 0.26)",      // #a47148 @ 26%
  glowColorLight: "rgba(92, 58, 28, 0.18)",       // #5c3a1c @ 18%
  particleDensity: 20,
},
```

- [ ] **Step 3: TypeScript 編譯驗證**

```bash
npx quartz build 2>&1 | tail -5
```

預期：build 成功。若 TS error 會在 build 初期就 fail。

- [ ] **Step 4: Commit**

```bash
git add quartz/components/sectionThemes.ts
git commit -m "$(cat <<'EOF'
feat: sectionThemes 擴充 MotionConfig 欄位

每個 section 加上：
- canvasRenderer: Phase 3 的 ArticleHero canvas 類型
- glowColorDark / glowColorLight: 明暗兩套 glow 色（配合 §3.2 對比度）
- particleDensity: Canvas 粒子/元素密度

Phase 1 這些值還沒被任何組件讀 — 打底給 Phase 2 (CategoryHero)
與 Phase 3 (ArticleHero) 使用。

見 spec §4.4 + §3.2。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 5: motionFeatureDetect inline script

**Files:**
- Create: `quartz/components/scripts/motionFeatureDetect.inline.ts`

- [ ] **Step 1: 寫 motionFeatureDetect**

Create `quartz/components/scripts/motionFeatureDetect.inline.ts`:

```ts
// Motion feature detection utility (spec §8.1 / §8.2)
// 全部 motion-related inline script 共用的降級判斷。

export function prefersReducedMotion(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
}

export function isMobileViewport(): boolean {
  // 跟 Quartz base.scss 定義的手機斷點一致（< 768px）
  return window.matchMedia("(max-width: 767px)").matches
}

export function isCoarsePointer(): boolean {
  return window.matchMedia("(pointer: coarse)").matches
}

/**
 * 檢查 <body> 是否有指定 opt-in flag（例如 data-motion-lenis）
 * 讓 Phase 2+ 可以按頁面選擇性啟動 Lenis 等重量級動畫
 */
export function bodyOptsIn(flag: string): boolean {
  return document.body.dataset[flag] !== undefined
}

// Attach to window so 其他 inline script 可以不 import 直接用
declare global {
  interface Window {
    __motion: {
      prefersReducedMotion: typeof prefersReducedMotion
      isMobileViewport: typeof isMobileViewport
      isCoarsePointer: typeof isCoarsePointer
      bodyOptsIn: typeof bodyOptsIn
    }
  }
}

window.__motion = {
  prefersReducedMotion,
  isMobileViewport,
  isCoarsePointer,
  bodyOptsIn,
}
```

- [ ] **Step 2: 驗證 TypeScript 編譯 OK**

**暫時先別 build** — 這支 script 還沒被任何 component 引用，esbuild 不會碰它。Task 9 (MotionRuntime) 才會把它接進來。

現在只要確認檔案 syntax 沒問題即可：

```bash
# 用 tsc 快速 syntax check (不輸出檔案)
npx tsc --noEmit --target es2020 --module esnext \
  quartz/components/scripts/motionFeatureDetect.inline.ts 2>&1 || \
  echo "syntax error above"
```

預期：無錯誤輸出。

- [ ] **Step 3: Commit**

```bash
git add quartz/components/scripts/motionFeatureDetect.inline.ts
git commit -m "$(cat <<'EOF'
feat: motionFeatureDetect inline script

全站 motion 降級判斷的單一來源：prefersReducedMotion / isMobileViewport /
isCoarsePointer / bodyOptsIn(flag)。掛到 window.__motion 讓其他 inline
script 不用 import 直接用。

Phase 1 還沒 wire，Task 9 的 MotionRuntime 組件會統一把這支跟其他 3 支
motion script concatenate 進 afterDOMLoaded。

見 spec §8.1-8.2。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 6: scrollReveal inline script

**Files:**
- Create: `quartz/components/scripts/scrollReveal.inline.ts`

- [ ] **Step 1: 寫 scrollReveal**

Create `quartz/components/scripts/scrollReveal.inline.ts`:

```ts
// Lightweight reveal observer（spec §4.1 Layer 2）
// 任何元素加 [data-reveal] 就會在進入 viewport 時得到 .revealed class，
// 配合 _motion-tokens.scss 的 CSS transition 產生淡入效果。
// 不用 GSAP，純 IntersectionObserver，~1KB gzipped。

let currentObserver: IntersectionObserver | null = null

function setupReveal() {
  // 先 disconnect 上一次的（SPA 導航時）
  currentObserver?.disconnect()

  const reduced = window.__motion?.prefersReducedMotion() ?? false
  const targets = document.querySelectorAll<HTMLElement>("[data-reveal]")

  // reduced-motion 或沒目標：直接標 revealed，不啟動 observer
  if (reduced || targets.length === 0) {
    targets.forEach((el) => el.classList.add("revealed"))
    currentObserver = null
    return
  }

  currentObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed")
          // 一次性：淡入後不再 observe
          currentObserver?.unobserve(entry.target)
        }
      })
    },
    {
      rootMargin: "0px 0px -12% 0px",   // 對應 $motion-reveal-offset
      threshold: 0.01,
    },
  )

  targets.forEach((el) => currentObserver!.observe(el))
}

document.addEventListener("nav", setupReveal)

window.addEventListener("beforeunload", () => {
  currentObserver?.disconnect()
  currentObserver = null
})
```

- [ ] **Step 2: Syntax check**

```bash
npx tsc --noEmit --target es2020 --module esnext \
  quartz/components/scripts/scrollReveal.inline.ts 2>&1 | head -5
```

預期：無錯誤（或只有 `window.__motion` 在單檔 check 時找不到 — 合理，因為 `__motion` 是 runtime 注入到 window 的）。如果 TS 嚴格抱怨 `window.__motion`，加一行：

```ts
declare const window: Window & { __motion?: { prefersReducedMotion: () => boolean } }
```

放在檔頭。

- [ ] **Step 3: Commit**

```bash
git add quartz/components/scripts/scrollReveal.inline.ts
git commit -m "$(cat <<'EOF'
feat: scrollReveal inline script

IntersectionObserver on [data-reveal]，進入 viewport 後加 .revealed class。
配合 _motion-tokens.scss 的 transition 完成淡入 + translateY。
reduced-motion 下直接 flag revealed，不啟動 observer。

SPA 導航時會先 disconnect 舊 observer，避免疊加（nav handler 重新 setup）。

見 spec §4.1 (Layer 2) + §8.1。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 7: gsapLoader inline script（race-safe）

**Files:**
- Create: `quartz/components/scripts/gsapLoader.inline.ts`

**這是 spec §9.3 的完整實作**，Phase 1 先放檔不啟動；Phase 2 的 `heroCinematic.inline.ts` 會 `loadGsap()` 才真正下載。

- [ ] **Step 1: 寫 gsapLoader**

Create `quartz/components/scripts/gsapLoader.inline.ts`:

```ts
// GSAP dynamic loader (spec §9.3)
// Phase 1: 檔案就位不啟動
// Phase 2+: HomeHeroApple / CategoryHero 的 nav handler 會呼叫 loadGsap()

declare global {
  interface Window {
    gsap?: any
    ScrollTrigger?: any
    __gsapLoader?: {
      loadGsap: () => Promise<void>
      bothLoaded: () => boolean
    }
  }
}

let loadPromise: Promise<void> | null = null

function bothLoaded(): boolean {
  return !!(window.gsap && window.ScrollTrigger)
}

export function loadGsap(): Promise<void> {
  // (1) 雙檢查：gsap AND ScrollTrigger 都要在
  if (bothLoaded()) return Promise.resolve()
  if (loadPromise) return loadPromise

  loadPromise = new Promise<void>((resolve, reject) => {
    // (2) 10 秒 timeout
    const timeoutId = window.setTimeout(() => {
      loadPromise = null
      reject(new Error("GSAP load timeout (10s)"))
    }, 10000)

    const loadScript = (src: string) =>
      new Promise<void>((res, rej) => {
        const s = document.createElement("script")
        s.src = src
        s.onload = () => res()
        s.onerror = () => rej(new Error(`Failed to load ${src}`))
        document.head.appendChild(s)
      })

    loadScript("/static/vendor/gsap.min.js")
      .then(() => loadScript("/static/vendor/ScrollTrigger.min.js"))
      .then(() => {
        clearTimeout(timeoutId)
        window.gsap.registerPlugin(window.ScrollTrigger)
        resolve()
      })
      .catch((err) => {
        clearTimeout(timeoutId)
        loadPromise = null   // (3) 允許 retry
        reject(err)
      })
  })

  return loadPromise
}

// (4) prenav 中斷時：若兩個 global 還沒齊，reset loader
document.addEventListener("prenav", () => {
  if (!bothLoaded()) {
    loadPromise = null
  }
})

// 掛到 window 讓其他 inline script 不用 import
window.__gsapLoader = { loadGsap, bothLoaded }
```

- [ ] **Step 2: Syntax check**

```bash
npx tsc --noEmit --target es2020 --module esnext \
  quartz/components/scripts/gsapLoader.inline.ts 2>&1 | head -5
```

- [ ] **Step 3: Commit**

```bash
git add quartz/components/scripts/gsapLoader.inline.ts
git commit -m "$(cat <<'EOF'
feat: gsapLoader inline script (race-safe 動態載入器)

spec §9.3 完整實作：
- 雙 global 檢查 (gsap AND ScrollTrigger)
- 10 秒 timeout 避免 script 被中途移除永遠 hang
- prenav 中斷時 reset loadPromise 允許下次 retry
- catch 錯誤時 reset loader，caller 可判斷降級路徑

Phase 1 只有定義 window.__gsapLoader.loadGsap()，沒有呼叫。
Phase 2 的 heroCinematic.inline.ts 會在 hero-cinematic 頁面觸發。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 8: navLifecycle inline script（SPA 骨架）

**Files:**
- Create: `quartz/components/scripts/navLifecycle.inline.ts`

**這是 spec §6.2 的實作**，但 Phase 1 只掛骨架（`navGeneration` token + `fonts.ready` + `focusFirstHeading`），不掛任何實際動畫 setup — 那些在 Phase 2+ 加。

- [ ] **Step 1: 寫 navLifecycle**

Create `quartz/components/scripts/navLifecycle.inline.ts`:

```ts
// SPA navigation lifecycle skeleton (spec §6.2)
// Phase 1: navGeneration token + fonts.ready + focusFirstHeading
// Phase 2+: 各 hero script 自己 addEventListener('nav', handler) 並
//          capture navGeneration 做 stale-handler 防禦。

declare global {
  interface Window {
    __nav?: {
      generation: number
      currentGen: () => number
    }
  }
}

let navGeneration = 0

// prenav: 版本號 +1，告訴所有 stale handlers 「你們的 myGen 已過期」
document.addEventListener("prenav", () => {
  navGeneration++
})

// nav: Phase 1 只做 (1) 等字體、(2) focus 管理
// Phase 2+ 的 animation setup 用自己的 nav listener，capture navGeneration 做檢查
document.addEventListener("nav", async () => {
  const myGen = navGeneration

  // (1) 等字體，避免後面組件 setup 時 layout 高度錯誤
  try {
    await document.fonts.ready
  } catch {
    // 字體載入失敗不該 block focus management
  }
  if (myGen !== navGeneration) return   // stale，abort

  // (2) SPA 導航後 focus 管理（spec §6.4）
  focusFirstHeading()
})

function focusFirstHeading() {
  const h1 = document.querySelector<HTMLElement>("main h1, article h1")
  if (h1) {
    h1.setAttribute("tabindex", "-1")
    h1.focus({ preventScroll: true })
  }
}

// 掛到 window，讓 Phase 2+ 的 inline script capture navGeneration
window.__nav = {
  get generation() {
    return navGeneration
  },
  currentGen: () => navGeneration,
}
```

- [ ] **Step 2: Syntax check**

```bash
npx tsc --noEmit --target es2020 --module esnext \
  quartz/components/scripts/navLifecycle.inline.ts 2>&1 | head -5
```

- [ ] **Step 3: Commit**

```bash
git add quartz/components/scripts/navLifecycle.inline.ts
git commit -m "$(cat <<'EOF'
feat: navLifecycle inline script (SPA 骨架 + navGeneration token)

spec §6.2 的 Phase 1 骨架：
- prenav 觸發時 navGeneration++
- nav 觸發時 await document.fonts.ready 後做 focusFirstHeading()
- navGeneration 暴露到 window.__nav，讓 Phase 2+ 的 hero script 在
  自己的 async nav handler 裡 capture 做 stale-handler 防禦

Phase 1 只處理 focus + 字體等待，還沒接任何動畫 setup（那些要等
Phase 2 的 Lenis / Phase 3 的 ArticleHero Canvas 上線才加）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 9: MotionRuntime component

**Files:**
- Create: `quartz/components/MotionRuntime.tsx`
- Modify: `quartz/components/index.ts`

這是個 **no-render** 組件，唯一作用是把 4 支 motion inline script 透過 `afterDOMLoaded` 機制丟進 Quartz 的 `postscript.js`。

- [ ] **Step 1: 參考現有 no-render pattern**

快速看一下 Quartz 是怎麼讓 component 貢獻 afterDOMLoaded 但不 render：

```bash
grep -l "return null" quartz/components/*.tsx | head -3
```

（`TableOfContents.tsx` 第 29-31 行就是 `if (!fileData.toc) return null`，是正常的 conditional return，證明返回 `null` 可行。）

- [ ] **Step 2: 寫 MotionRuntime**

Create `quartz/components/MotionRuntime.tsx`:

```tsx
import { QuartzComponent, QuartzComponentConstructor } from "./types"
import { concatenateResources } from "../util/resources"

// @ts-ignore
import motionFeatureDetectScript from "./scripts/motionFeatureDetect.inline"
// @ts-ignore
import navLifecycleScript from "./scripts/navLifecycle.inline"
// @ts-ignore
import scrollRevealScript from "./scripts/scrollReveal.inline"
// @ts-ignore
import gsapLoaderScript from "./scripts/gsapLoader.inline"

/**
 * MotionRuntime 是個 no-render 組件。掛到 sharedPageComponents.afterBody
 * 讓 4 支 motion inline script 被全站載入（在 Quartz 的單一 postscript.js 裡）。
 *
 * 載入順序（重要）：
 *   1. motionFeatureDetect — 定義 window.__motion 給其他 script 用
 *   2. navLifecycle — 定義 window.__nav + prenav/nav handler 骨架
 *   3. scrollReveal — 依賴 window.__motion.prefersReducedMotion
 *   4. gsapLoader — 獨立，但放最後方便 debug
 *
 * 見 spec §4.1 (Layer 2 inline scripts)。
 */
const MotionRuntime: QuartzComponent = () => null

MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  scrollRevealScript,
  gsapLoaderScript,
)

export default (() => MotionRuntime) satisfies QuartzComponentConstructor
```

- [ ] **Step 3: Export 到 index.ts**

Modify `quartz/components/index.ts` — 在 imports 區加：

```ts
import MotionRuntime from "./MotionRuntime"
```

然後在 `export {` 區加 `MotionRuntime,`（保持字母順序或跟隨既有慣例）：

```ts
export {
  // ... 其他 exports ...
  HomeLanding,
  MotionRuntime,   // 新增
}
```

- [ ] **Step 4: Build 驗證**

```bash
npx quartz build 2>&1 | tail -10
```

預期：build 成功。此時 `MotionRuntime` 還沒被 layout 用，但 TS 要能編譯通過。

- [ ] **Step 5: Commit**

```bash
git add quartz/components/MotionRuntime.tsx quartz/components/index.ts
git commit -m "$(cat <<'EOF'
feat: MotionRuntime no-render 組件

把 4 支 motion inline script (motionFeatureDetect / navLifecycle /
scrollReveal / gsapLoader) 透過 concatenateResources 一起掛到
afterDOMLoaded，等 Task 10 把組件掛到 sharedPageComponents.afterBody
就會在全站生效。

載入順序有意義：
  1. motionFeatureDetect 先註冊 window.__motion
  2. navLifecycle 接 SPA event + 暴露 window.__nav
  3. scrollReveal 依賴前兩者
  4. gsapLoader 獨立，但放最後

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 10: Wire MotionRuntime into shared layout

**Files:**
- Modify: `quartz.layout.ts`

- [ ] **Step 1: 加進 sharedPageComponents.afterBody**

Modify `quartz.layout.ts` — 在 `sharedPageComponents` 的 `afterBody` 陣列開頭加 `Component.MotionRuntime()`：

```ts
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [Component.SiteHeaderNav()],
  afterBody: [
    Component.MotionRuntime(),   // 新增：全站 motion 基礎建設 (Phase 1)
    Component.ConditionalRender({
      component: Component.RecentNotes({
        // ... 既有設定保留 ...
      }),
      condition: (page) => {
        // ... 既有 condition 保留 ...
      },
    }),
  ],
  footer: Component.Footer({
    // ... 既有保留 ...
  }),
}
```

- [ ] **Step 2: Build 驗證 postscript.js 增量**

```bash
# 先記錄 build 前 postscript.js 大小
ls -l public/postscript.js 2>/dev/null | awk '{print "BEFORE:", $5, "bytes"}'

npx quartz build 2>&1 | tail -3

ls -l public/postscript.js | awk '{print "AFTER:", $5, "bytes"}'
# 預期：增加 5-15 KB（未 gzip 的 raw size；gzipped 後 ~5-10KB）
```

- [ ] **Step 3: 驗證 script 內容有被 bundle 進去**

```bash
grep -o "__motion\|__nav\|__gsapLoader\|data-reveal" public/postscript.js | sort -u
# 預期：看到 4 個字串至少出現一次
```

- [ ] **Step 4: 本地啟動 dev server 手動驗證**

```bash
npx quartz build --serve 2>&1 | tee .quartz-serve-phase1.log &
sleep 3
```

打開瀏覽器到 `http://localhost:8080`，開 DevTools Console，執行：

```js
window.__motion  // 預期：{prefersReducedMotion, isMobileViewport, ...}
window.__nav     // 預期：{generation, currentGen}
window.__gsapLoader  // 預期：{loadGsap, bothLoaded}
```

三個都應該是 defined。

停 dev server：

```bash
# 找到 node process 停掉（或直接 Ctrl+C 如果在前景）
```

- [ ] **Step 5: Commit**

```bash
git add quartz.layout.ts
git commit -m "$(cat <<'EOF'
feat: wire MotionRuntime 進 sharedPageComponents.afterBody

Phase 1 最後一步 — 現在全站每頁都會載入 4 支 motion inline script
(motionFeatureDetect / navLifecycle / scrollReveal / gsapLoader)，
但還沒觸發任何實際動畫。現有功能零變化。

postscript.js 增量：~5-10KB gzipped。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 11: 零 regression 手動驗證

**Files:** 無（純驗證 task）

**這是 Phase 1 的關鍵驗收：確認加了 motion 基礎建設後，現有功能全部照舊。**

- [ ] **Step 1: 啟動 dev server**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
npx quartz build --serve 2>&1 | tee .quartz-serve-phase1.log &
sleep 3
```

- [ ] **Step 2: 瀏覽器開 http://localhost:8080，執行 6 項檢查**

依序檢查下列 6 項，每項 **pass 或 fail 都記錄** 到這個 checklist：

| # | 項目 | 怎麼檢查 | 預期 |
|---|-----|---------|------|
| 1 | 首頁 Matter.js hero | 打開 `/`，滑鼠移過 7 個飄浮物件 | 物件跟滑鼠互動 (沒壞) |
| 2 | Wikilink popover | 開任一篇有 wikilink 的文章（`manufacturing-ai/在傳統製造業...`），hover wikilink | popover 跳出顯示目標頁預覽 |
| 3 | TOC | 開任一篇有 `## 標題` 的文章，往下滾 | TOC 項目跟著高亮 (既有行為) |
| 4 | Search | 按鍵盤 `/` 或點搜尋圖示 | search modal 跳出 |
| 5 | SPA 導航 | 點任一分類頁連結 | URL 換但頁面不全頁 reload（看 network tab） |
| 6 | Dark mode 切換 | 按右上角太陽/月亮圖示 | 顏色切換，motion tokens 裡的 accent 也跟著切（雖然還沒有元素用它） |

- [ ] **Step 3: 瀏覽器 Console 檢查 motion API 可用**

```js
window.__motion.prefersReducedMotion()  // 應回傳 boolean
window.__motion.isMobileViewport()      // 應回傳 boolean
window.__nav.currentGen()                // 應回傳 number (0 或更大)
window.__gsapLoader.bothLoaded()         // 應回傳 false (Phase 1 還沒載 GSAP)
```

- [ ] **Step 4: data-reveal 手動測試**

在 Console 執行：

```js
const el = document.createElement('div')
el.setAttribute('data-reveal', '')
el.textContent = 'TEST reveal'
el.style.cssText = 'position:fixed; top:50%; left:50%; background:red; padding:20px; z-index:9999;'
document.body.appendChild(el)
setTimeout(() => {
  console.log('Has .revealed?', el.classList.contains('revealed'))
  // 預期：true (因為 fixed 元素本來就在 viewport 內，IntersectionObserver 會立刻觸發)
  el.remove()
}, 500)
```

預期 console log: `Has .revealed? true`

- [ ] **Step 5: 關閉 dev server 並 commit 驗證紀錄**

先停 dev server。然後創建 `quartz/docs/superpowers/baselines/2026-04-24-phase1-verification.md`：

```markdown
# Phase 1 零 regression 驗證紀錄

日期：YYYY-MM-DD
Commit：<最後一個 commit hash>

| # | 項目 | 結果 |
|---|-----|------|
| 1 | Matter.js hero 互動 | ✓/✗ |
| 2 | Wikilink popover | ✓/✗ |
| 3 | TOC 高亮 | ✓/✗ |
| 4 | Search modal | ✓/✗ |
| 5 | SPA 導航 | ✓/✗ |
| 6 | Dark mode 切換 | ✓/✗ |
| 7 | window.__motion / __nav / __gsapLoader 可用 | ✓/✗ |
| 8 | data-reveal 加上會得到 .revealed | ✓/✗ |

備註：（任何觀察到的小異常都寫這裡）
```

填完後：

```bash
git add docs/superpowers/baselines/2026-04-24-phase1-verification.md
git commit -m "$(cat <<'EOF'
docs: Phase 1 零 regression 驗證紀錄

手動驗證 8 項：Matter.js hero / popover / TOC / search / SPA nav /
dark mode / motion global API / data-reveal。全部通過。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 12: Lighthouse baseline

**Files:**
- Create: `quartz/docs/superpowers/baselines/2026-04-24-lighthouse.md`

**這是為 Phase 2 的效能比較打基準線。**

- [ ] **Step 1: 啟動 dev server**

```bash
npx quartz build --serve 2>&1 &
sleep 3
```

- [ ] **Step 2: 跑 Lighthouse（Chrome DevTools 版）**

開 Chrome 到 `http://localhost:8080/`，F12 → Lighthouse tab → 選 Desktop + Performance/Accessibility/Best Practices/SEO → Analyze page load

記錄分數。接著換到 `/manufacturing-ai/`、挑一篇文章（例如 `/manufacturing-ai/企業內部推-AI-時，最常見的-5-種阻力`）各跑一次。

- [ ] **Step 3: 寫基準線文件**

Create `quartz/docs/superpowers/baselines/2026-04-24-lighthouse.md`:

```markdown
# Phase 1 完成後 Lighthouse 基準分數

日期：YYYY-MM-DD (Phase 1 剛上線)
Commit：<最後一個 commit hash>
Chrome 版本：<F12 → About 查>
Lighthouse 版本：<F12 Lighthouse panel 左下角>

## 首頁 `/`

| 指標 | 分數 | LCP (ms) | CLS | INP (ms) |
|-----|------|---------|-----|---------|
| Performance | ??  | ??      | ??  | ??      |
| Accessibility | ?? | - | - | - |
| Best Practices | ?? | - | - | - |
| SEO | ?? | - | - | - |

## 分類頁 `/manufacturing-ai/`

(同上表格)

## 文章頁（挑一篇有 wikilink 的）

(同上表格)

---

**Phase 2 目標**（見 spec §9.6）：
- LCP 不退步（盡量變好）
- Performance ≥ 90
- Accessibility ≥ 95
- postscript.js gzipped 淨變動 -10KB (砍 Matter.js 後)
```

- [ ] **Step 4: 停 dev server，commit**

```bash
git add docs/superpowers/baselines/2026-04-24-lighthouse.md
git commit -m "$(cat <<'EOF'
docs: Phase 1 Lighthouse 基準線

記錄 Phase 1 完成、Phase 2 尚未開始時的首頁 / 分類頁 / 文章頁的
Lighthouse 分數。Phase 2 後會做對照檢查 LCP / Performance 不退步。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Phase 1 完成標準（驗收）

完成所有 12 個 Task 後，check 下列全數滿足才算 Phase 1 ship：

- [ ] `npx quartz build` 無 warning / error
- [ ] `public/static/vendor/gsap.min.js` 與 `ScrollTrigger.min.js` 就位
- [ ] `public/postscript.js` 含 `__motion` / `__nav` / `__gsapLoader` / `data-reveal` 字串
- [ ] 瀏覽器 Console `window.__motion` / `window.__nav` / `window.__gsapLoader` 三個 API 都存在
- [ ] 零 regression 驗證 8 項全通過（Task 11）
- [ ] Lighthouse 基準線已記錄（Task 12）
- [ ] Git log 顯示 11 個 Phase 1 commits（Task 1-9 + Task 10 + Task 11 + Task 12）

**如果任一項失敗**：不要進 Phase 2，先修到過。Phase 1 的定位是「非侵入地基」，這層破了後面全部不穩。

---

## 接下來

Phase 1 ship 後，寫 Phase 2 的 plan（砍 Matter.js + HomeHeroApple + Lenis + focal canvas）。**不要現在就寫 Phase 2 plan** — Phase 2 很吃 Phase 1 實際產出的 API 形狀，先讓 Phase 1 跑一輪真實的，Phase 2 plan 會更準。

Phase 2 plan 寫完前請回到本 repo 的 brainstorming / plan 流程：
- Phase 2 plan 位置：`docs/superpowers/plans/YYYY-MM-DD-immersive-frontend-phase-2.md`
- 以 spec §10 Phase 2 交付清單為起點
- 實作前再跑一次 code-reviewer 看 Phase 1 留下的技術債
