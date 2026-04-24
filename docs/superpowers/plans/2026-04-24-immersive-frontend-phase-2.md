# Immersive Frontend — Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 首頁從「Matter.js 7 物件 hero + 多塊舊 `.home-landing__*` 組件」改造為「Apple 產品頁風格 hero + focal canvas + Pillars/Stats/Featured/Recent」；同時砍掉 Matter.js、導入 Lenis smooth scroll、接上 GSAP 動態載入。完成後首頁即具備 §5.1 定義的完整視覺。

**Architecture:** 沿用 Phase 1 的 `MotionRuntime` 無 render 組件作為全站 motion runtime 骨幹；Phase 2 往裡再塞 3 支 inline script（`focalCanvas` / `lenis` / `heroCinematic`）。新 `HomeHeroApple.tsx` 是 hero 的 SSR 外殼（純字 + 單一 canvas + CTA），內文區塊（Pillars/Stats/Featured/Recent）直接寫在 `HomeLanding.tsx` 裡重寫後的 JSX。Lenis 全站載入但 opt-in（手機 / reduced-motion / search modal 開時停用）。GSAP 走 Phase 1 已 vendored 的 `gsapLoader.loadGsap()`，只有首頁 / 分類頁會實際下載。Matter.js 依賴、`heroScene.inline.ts` 與 `static/scene/*` 原物件資產在 Phase 2 一次清掉。`custom.scss` 的 ~171 條 `.home-landing__*` / `.home-hero-scene` / `.hero-object` 規則同 commit 遷入新檔 `_home-apple.scss` 或直接刪除，避免留死碼。

**Tech Stack:** Quartz 4.5.2 (Preact SSR + TSX + SCSS), esbuild inline bundler, GSAP 3.12.7 + ScrollTrigger（Phase 1 vendored, 此階段動態 load）, Lenis 1.1.x（npm → inline bundle）, 純 Canvas 2D（focal canvas / 無 Three.js / 無 WebGL）, TypeScript。沿用 Phase 1 已建立的 `window.__motion` / `window.__nav` / `window.__gsapLoader` 全域介面。

**Spec reference:** [2026-04-24-immersive-frontend-design.md](../specs/2026-04-24-immersive-frontend-design.md) §5.1（首頁版型）、§10 Phase 2、§16（舊→新區塊對照）、§6.2（SPA nav-gen token）、§6.5（Search × Lenis）、§3.1（字體 preload）、§9.2–9.3（效能預算 + GSAP 動態載入）、§8.2（手機降級）。

**Phase 1 前置依賴（必須先 ship）：** Phase 1 已完成 12 個 task、`window.__motion` / `window.__nav` / `window.__gsapLoader` 可用、`static/vendor/gsap.min.js` + `ScrollTrigger.min.js` 就位、`_motion-tokens.scss` 與 `_popover-immersive.scss` 已 wire、`MotionRuntime` 已進 `sharedPageComponents.afterBody`、Lighthouse baseline 已記錄。若上述任一未滿足先回頭補 Phase 1。

**Commit convention (per user CLAUDE.md):** Conventional Commits + trailing `Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>`。**Phase 2 以 10 個 commit 完成**，對應 spec §10 的「4-5 commit / 每個都能跑」原則再拆細讓 `git bisect` 粒度更好。

---

## File Structure

### New files

| Path | 職責 |
|-----|------|
| `quartz/components/HomeHeroApple.tsx` | 首頁 hero 外殼（eyebrow + h1 + lead + CTA + 單一 focal canvas 容器） |
| `quartz/components/scripts/focalCanvas.inline.ts` | Hero 單一 canvas 繪製 —  暖金漸層光暈 + 緩動粒子，scroll 驅動呼吸，`requestAnimationFrame` + FPS 降級 |
| `quartz/components/scripts/sectionCanvas.inline.ts` | Phase 3 `ArticleHero` 用的 section-themed canvas 繪製器（`geometric-lines` / `particle-flow` / `steam-curves` 三個 renderer）。Phase 2 僅建立 API 骨架，dormant（無 DOM 對應） |
| `quartz/components/scripts/lenis.inline.ts` | Lenis smooth scroll 啟動器（mobile / reduced-motion / body opt-out 時靜默不啟動），暴露 `window.__lenis` 給 search 用 |
| `quartz/components/scripts/heroCinematic.inline.ts` | 首頁 hero 的 GSAP ScrollTrigger 時間軸 + stats count-up 動畫（動態 load GSAP、配合 §6.2 `navGeneration` token） |
| `quartz/components/CustomHead.tsx` | 擴充 `Component.Head()` 的 Quartz 預設實作，加字體 preload（`as="style"`） |
| `quartz/styles/_home-apple.scss` | 新首頁 BEM 樣式（`.home-hero__*` / `.home-pillars*` / `.home-stats-strip*` / `.home-featured*` / `.home-recent*`） |
| `quartz/styles/_lenis.scss` | Lenis library reset（`html.lenis-smooth` / `html.lenis-stopped` 等），抽獨立檔避免跟 home-apple 混 |
| `quartz/docs/superpowers/baselines/2026-04-24-phase2-verification.md` | Phase 2 手動 regression + feature 驗證紀錄 |
| `quartz/docs/superpowers/baselines/2026-04-24-lighthouse-after-phase2.md` | Phase 2 完成後 Lighthouse 分數（與 Phase 1 baseline 對照） |

### Modified files

| Path | 改動 |
|-----|------|
| `quartz/components/HomeLanding.tsx` | 依 §16 完全重寫內文（import `HomeHeroApple` + 新 Pillars / Stats / Featured / Recent 區塊）；移除 Matter.js `sceneObjects` / `heroSceneScript` import / `afterDOMLoaded` 指派；刪除 `.home-landing__shelves` 區塊（§16 指示刪除） |
| `quartz/components/MotionRuntime.tsx` | `concatenateResources` 增補 3 支新 inline script：`focalCanvas` / `lenis` / `heroCinematic`（載入順序見 Task 2/6/9 註解） |
| `quartz/components/scripts/search.inline.ts` | `showSearch()` / `hideSearch()` 內呼叫 `window.__lenis?.stop()` / `.start()`（§6.5） |
| `quartz/components/index.ts` | `export { CustomHead }` 新增 |
| `quartz/styles/custom.scss` | **刪除** 所有 `.home-landing__*` / `.home-hero-scene*` / `.hero-object*` 規則（~171 行，§16.2）；`@use "./_home-apple.scss"` 加進 head |
| `quartz.config.ts` | `sharedPageComponents.head` 從 `Component.Head()` 改為 `Component.CustomHead()` — 等一下，檢查：Quartz 的 head 是掛在 `quartz.layout.ts` 的 `sharedPageComponents.head`（見 Phase 1 Task 10 改過那檔） |
| `quartz.layout.ts` | `sharedPageComponents.head: Component.Head()` → `Component.CustomHead()` |
| `package.json` | 刪 `matter-js` + `@types/matter-js` 依賴；加 `lenis` 依賴（`npm i lenis` 後 auto-update） |
| `package-lock.json` | `npm i lenis` 後 auto-update |

### Deleted files

| Path | 原因 |
|-----|-----|
| `quartz/components/scripts/heroScene.inline.ts` | Matter.js 物理 hero 廢止（§16 + §10 Phase 2） |
| `quartz/static/scene/coffee-bean-1.png` / `.svg` | Matter.js 物件資產廢止 |
| `quartz/static/scene/coffee-bean-2.png` / `.svg` | 同上 |
| `quartz/static/scene/coffee-bean-3.png` / `.svg` | 同上 |
| `quartz/static/scene/headphones.png` / `.svg` | 同上 |
| `quartz/static/scene/laptop.png` / `.svg` | 同上 |
| `quartz/static/scene/mug.png` / `.svg` | 同上 |
| `quartz/static/scene/phone.png` / `.svg` | 同上（14 個檔案一併刪） |

**注意**：`quartz/components/scripts/sectionScene.inline.ts` 與 `quartz/components/BrandIntro.tsx` **不刪**，留給 Phase 3（`CategoryHero` 取代 `BrandIntro` 時才動）。

---

## Task 1: `HomeHeroApple.tsx` 骨架 + `_home-apple.scss` 新檔

**Files:**
- Create: `quartz/components/HomeHeroApple.tsx`
- Create: `quartz/styles/_home-apple.scss`
- Modify: `quartz/styles/custom.scss`（新 `@use`，**尚不刪舊規則**）
- Modify: `quartz/components/index.ts`

**這一步 feature flag 關**：新組件與樣式先進檔，但 `HomeLanding.tsx` 還沒改、Matter.js 仍正常運作。`npm run build` 後前端視覺與 Phase 1 完全一致；新 SCSS 規則沒對應 DOM 所以匹配為空，無 side effect。

- [ ] **Step 1: 寫 `HomeHeroApple.tsx`（純 SSR 外殼，不含 inline script hook）**

Create `quartz/components/HomeHeroApple.tsx`:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"

/**
 * HomeHeroApple — 首頁 hero 外殼（spec §5.1）
 *
 * 結構：
 *   .home-hero
 *     .home-hero__focal   — 單一 canvas 容器（focalCanvas.inline.ts 會 attach）
 *     .home-hero__copy
 *       .home-hero__eyebrow
 *       h1.home-hero__title     — LCP 候選（128px）
 *       p.home-hero__lead
 *       .home-hero__signals
 *       .home-hero__actions     — 兩顆 CTA
 *
 * 這個組件不自帶 afterDOMLoaded；focal canvas 啟動邏輯走 MotionRuntime
 * 裡的 focalCanvas.inline.ts（Task 2 建立），透過 `[data-home-hero-focal]`
 * 屬性 DOM lookup。heroCinematic（GSAP timeline）走同樣 pattern（Task 9）。
 */
export default (() => {
  function HomeHeroApple({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)

    return (
      <section class="home-hero" data-hero-cinematic="true">
        <div
          class="home-hero__focal"
          data-home-hero-focal="true"
          aria-hidden="true"
          role="presentation"
        >
          <canvas class="home-hero__canvas" />
        </div>
        <div class="home-hero__copy">
          <p class="home-hero__eyebrow">JASON LIN / AI FIELD NOTES</p>
          <h1 class="home-hero__title">把企業裡真的用得上的 AI，整理成可以開始的做法。</h1>
          <p class="home-hero__lead">
            我在傳統製造業做 AI 落地，橫跨軟體開發與 PM，也是認真對待手沖咖啡的人。
            這裡不是 AI 新聞站，而是一個把現場經驗、工具方法與生活感受慢慢寫清楚的地方。
          </p>
          <div class="home-hero__signals">
            <span>製造業 AI 落地</span>
            <span>AI 工具與方法</span>
            <span>手沖咖啡</span>
          </div>
          <div class="home-hero__actions">
            <a
              class="home-hero__cta home-hero__cta--primary"
              href={resolveRelative(slug, "manufacturing-ai/index" as FullSlug)}
            >
              先看製造業 AI
            </a>
            <a
              class="home-hero__cta"
              href={resolveRelative(slug, "ai-notes/index" as FullSlug)}
            >
              再看 AI 新知
            </a>
          </div>
        </div>
      </section>
    )
  }

  return HomeHeroApple
}) satisfies QuartzComponentConstructor
```

- [ ] **Step 2: 寫 `_home-apple.scss`（BEM 新樣式骨架）**

Create `quartz/styles/_home-apple.scss`:

```scss
// Home Apple-style layout (spec §5.1 + §16.2 SCSS 遷移)
// Phase 2 完整樣式。BEM 命名避免跟舊 .home-landing__* 碰撞。
// 暫時配色用 Phase 1 tokens + 既有 --light/--dark CSS var。

@use "./_motion-tokens";

// ── Hero 100vh ───────────────────────────────────────────────────────────────
.home-hero {
  position: relative;
  min-height: 100vh;  // spec §3.3
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 2.4rem;
  align-items: center;
  padding: clamp(3rem, 6vw, 6rem) clamp(1.5rem, 4vw, 3rem);
  overflow: hidden;
  isolation: isolate;  // 讓 canvas 的 mix-blend 不外溢

  // mobile：一欄，canvas 縮到 40vh 背景
  @media all and (max-width: 767px) {
    grid-template-columns: 1fr;
    min-height: auto;
    padding: 4rem 1.2rem;
    gap: 1.8rem;
  }
}

.home-hero__focal {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  max-height: 80vh;

  @media all and (max-width: 767px) {
    aspect-ratio: 16 / 9;
    max-height: 40vh;
    order: -1;  // canvas 放在文字上面
  }
}

.home-hero__canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.home-hero__copy {
  display: grid;
  gap: 1.35rem;
  align-content: center;
  max-width: 38rem;
}

.home-hero__eyebrow {
  margin: 0;
  font-size: 0.875rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.72;
}

.home-hero__title {
  margin: 0;
  font-family: var(--headerFont), "Outfit", sans-serif;
  font-weight: 800;
  font-size: clamp(3rem, 8vw, 8rem);  // 128px 上限
  line-height: 1.02;
  letter-spacing: -0.02em;
}

.home-hero__lead {
  margin: 0;
  font-size: clamp(1rem, 1.2vw, 1.15rem);
  line-height: 1.7;
  opacity: 0.82;
}

.home-hero__signals {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;

  span {
    padding: 0.35rem 0.85rem;
    border: 1px solid rgba(255, 247, 234, 0.16);
    border-radius: 999px;
    font-size: 0.8rem;
    opacity: 0.82;
  }
}

.home-hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: 0.4rem;
}

.home-hero__cta {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid rgba(255, 247, 234, 0.26);
  color: var(--dark);
  background: transparent;
  transition: background var(--motion-duration-fast) var(--motion-easing);

  &:hover { background: rgba(255, 247, 234, 0.08); }

  &--primary {
    background: var(--dark);
    color: var(--light);
    border-color: var(--dark);

    &:hover { background: rgba(18, 16, 13, 0.88); }
  }
}

// ── Stats strip ~60vh ────────────────────────────────────────────────────────
.home-stats-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.5rem;
  padding: clamp(3rem, 6vw, 5rem) clamp(1.5rem, 4vw, 3rem);
  border-top: 1px solid rgba(255, 247, 234, 0.1);
  border-bottom: 1px solid rgba(255, 247, 234, 0.1);

  @media all and (max-width: 767px) {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 2.5rem 1.2rem;
  }
}

.home-stats-strip__item {
  display: grid;
  gap: 0.4rem;
}

.home-stats-strip__label {
  font-size: 0.8rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.7;
}

.home-stats-strip__value {
  font-family: var(--headerFont), "Outfit", sans-serif;
  font-weight: 800;
  font-size: clamp(1.8rem, 3.2vw, 2.8rem);
  letter-spacing: -0.015em;
}

// ── Three Pillars（staggered reveal，無 pin，spec §5.1 v2 修正） ──────────────
.home-pillars {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.4rem;
  padding: clamp(4rem, 8vw, 8rem) clamp(1.5rem, 4vw, 3rem);

  @media all and (max-width: 900px) {
    grid-template-columns: 1fr;
    padding: 3rem 1.2rem;
  }
}

.home-pillars__card {
  display: grid;
  gap: 0.8rem;
  padding: 2rem 1.8rem;
  border-radius: 28px;
  border: 1px solid rgba(255, 247, 234, 0.1);
  background: rgba(255, 247, 234, 0.02);
  text-decoration: none;
  color: inherit;
  transition: transform var(--motion-duration-base) var(--motion-easing),
    border-color var(--motion-duration-fast) var(--motion-easing);

  &:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 247, 234, 0.22);
  }

  p {
    margin: 0;
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.7;
  }

  strong {
    font-family: var(--headerFont), "Outfit", sans-serif;
    font-size: clamp(1.4rem, 2.2vw, 1.8rem);
    font-weight: 700;
  }

  span {
    font-size: 0.95rem;
    opacity: 0.78;
    line-height: 1.6;
  }

  small {
    font-size: 0.75rem;
    opacity: 0.6;
  }
}

// data-reveal stagger — 靠 Phase 1 scrollReveal + _motion-tokens.scss 的基礎動畫
// 這裡只加 stagger delay 覆寫
.home-pillars__card[data-reveal] {
  transition-delay: 0ms;

  &:nth-child(2) { transition-delay: var(--motion-stagger); }
  &:nth-child(3) { transition-delay: calc(var(--motion-stagger) * 2); }
}

// ── Featured（第一篇大卡橫跨兩欄） ────────────────────────────────────────────
.home-featured {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.2rem;
  padding: clamp(3rem, 6vw, 6rem) clamp(1.5rem, 4vw, 3rem) 0;

  @media all and (max-width: 900px) {
    grid-template-columns: 1fr;
    padding: 2.5rem 1.2rem 0;
  }
}

.home-featured__card {
  padding: 1.6rem 1.5rem;
  border-radius: 22px;
  border: 1px solid rgba(255, 247, 234, 0.1);
  background: rgba(255, 247, 234, 0.02);
  text-decoration: none;
  color: inherit;
  display: grid;
  gap: 0.55rem;
  transition: transform var(--motion-duration-base) var(--motion-easing);

  &:hover { transform: translateY(-3px); }

  p {
    margin: 0;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.7;
  }

  h2 {
    margin: 0;
    font-family: var(--headerFont), "Outfit", sans-serif;
    font-weight: 700;
    font-size: clamp(1.2rem, 2vw, 1.7rem);
    line-height: 1.25;
  }

  span {
    font-size: 0.92rem;
    opacity: 0.78;
    line-height: 1.58;
  }

  &--primary {
    grid-column: 1 / -1;
    padding: 2.2rem 2rem;
    background: rgba(255, 247, 234, 0.04);

    h2 { font-size: clamp(1.6rem, 2.8vw, 2.4rem); }
  }
}

// ── Recent updates ──────────────────────────────────────────────────────────
.home-recent {
  display: grid;
  gap: 1.2rem;
  padding: clamp(3rem, 6vw, 5rem) clamp(1.5rem, 4vw, 3rem) clamp(4rem, 8vw, 6rem);

  @media all and (max-width: 900px) {
    padding: 2rem 1.2rem 3rem;
  }
}

.home-recent__heading {
  display: grid;
  gap: 0.65rem;
  margin-bottom: 0.8rem;

  p {
    margin: 0;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.7;
  }

  h2 {
    margin: 0;
    font-family: var(--headerFont), "Outfit", sans-serif;
    font-size: clamp(1.5rem, 2.6vw, 2rem);
    font-weight: 700;
    line-height: 1.25;
  }

  .home-recent__copy {
    margin: 0;
    font-size: 0.95rem;
    opacity: 0.78;
    line-height: 1.65;
  }
}

.home-recent__list {
  display: grid;
  gap: 0.95rem;
}

.home-recent__item {
  display: grid;
  gap: 0.4rem;
  padding: 1.1rem 1.2rem;
  border-radius: 18px;
  border: 1px solid rgba(255, 247, 234, 0.08);
  text-decoration: none;
  color: inherit;
  transition: border-color var(--motion-duration-fast) var(--motion-easing);

  &:hover { border-color: rgba(255, 247, 234, 0.22); }

  .home-recent__meta {
    display: flex;
    gap: 0.8rem;
    font-size: 0.78rem;
    opacity: 0.7;
  }

  strong {
    font-family: var(--headerFont), "Outfit", sans-serif;
    font-size: clamp(1.05rem, 1.6vw, 1.25rem);
    font-weight: 700;
  }

  p {
    margin: 0;
    font-size: 0.9rem;
    opacity: 0.78;
    line-height: 1.6;
  }
}
```

- [ ] **Step 3: Wire 新 scss 進 `custom.scss`（**只加 `@use`，**不**刪舊規則）**

Modify `quartz/styles/custom.scss` — 在 `@use "./_popover-immersive.scss";` 後面加一行：

```scss
@use "./base.scss";
@use "./_motion-tokens.scss";
@use "./_popover-immersive.scss";
@use "./_home-apple.scss";   // 新增（Task 3 後才有 DOM 對應）
```

- [ ] **Step 4: Export `HomeHeroApple` 到 `quartz/components/index.ts`**

Modify `quartz/components/index.ts`：

- 在 imports 區加 `import HomeHeroApple from "./HomeHeroApple"`（放在 `HomeLanding` import 之後以維持字母/主題順序）
- 在 `export { ... }` 區加 `HomeHeroApple,`（放在 `HomeLanding,` 後面）

改完後 export 區域應包含：

```ts
  HomeLanding,
  HomeHeroApple,
  MotionRuntime,
```

- [ ] **Step 5: Build 驗證**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
npx quartz build 2>&1 | tail -10
```

預期：
- Build 成功無 warning / error
- `public/index.css` 產生，含 `.home-hero {` / `.home-pillars` / `.home-stats-strip` 等新 selector（可 `grep home-hero public/index.css` 確認）
- 首頁視覺**完全不變**（因為 `HomeHeroApple` 還沒被任何 layout 引用）

```bash
grep -c "home-hero\|home-pillars\|home-stats-strip" public/index.css
# 預期：> 5
```

- [ ] **Step 6: Commit**

```bash
git add quartz/components/HomeHeroApple.tsx quartz/components/index.ts \
  quartz/styles/_home-apple.scss quartz/styles/custom.scss
git commit -m "$(cat <<'EOF'
feat: HomeHeroApple 組件骨架 + _home-apple.scss 新樣式（未 wire）

依 spec §5.1 新增首頁 hero SSR 外殼：純字 (eyebrow/h1/lead/signals/CTA)
＋單一 .home-hero__focal canvas 容器（content 與 canvas 繪製邏輯分別由
後續 task 的 focalCanvas 與 heroCinematic inline script 填上）。

新 BEM 樣式寫到 _home-apple.scss（含 Hero 100vh / Stats strip / Three Pillars
stagger / Featured grid / Recent list），此 commit 先用 @use 接進來。
舊 .home-landing__* 與 .home-hero-scene 規則**尚未刪除** — Task 3 砍
Matter.js 時才會同 commit 清掉。

此 commit 對外視覺零變化（HomeHeroApple 未進任何 layout / Matter hero 還在）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 2: `focalCanvas.inline.ts` + `sectionCanvas.inline.ts` + wire 進 `MotionRuntime`

**Files:**
- Create: `quartz/components/scripts/focalCanvas.inline.ts`
- Create: `quartz/components/scripts/sectionCanvas.inline.ts`（dormant stub，Phase 3 `ArticleHero` 接）
- Modify: `quartz/components/MotionRuntime.tsx`

**這一步 feature flag 還是關**：`focalCanvas` 會全站載入但 `[data-home-hero-focal]` 目標尚不存在（`HomeHeroApple` 還沒進 layout）→ early-return，零 side effect。`sectionCanvas` 整支都是 API 骨架 + `window.__sectionCanvas.render(...)` 暴露點，Phase 2 沒人呼叫，純 dormant。兩者對應 spec §10 Phase 2 commit 2「focal canvas + sectionCanvas 繪製器，feature flag 關」。

- [ ] **Step 1: 寫 `focalCanvas.inline.ts`**

Create `quartz/components/scripts/focalCanvas.inline.ts`:

```ts
// Hero focal canvas — spec §5.1 / §7
// 單一 canvas，暖金漸層光暈 + 緩動粒子，scroll 驅動呼吸
// 純 Canvas 2D，無第三方依賴。~3KB gzipped。

declare const window: Window & {
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
  __nav?: { currentGen: () => number }
}

interface Particle {
  x: number
  y: number
  r: number
  vx: number
  vy: number
  alpha: number
  hueShift: number
}

// code-reviewer S3：低電量模式下 loop 用 setTimeout 安排下一幀，此時
// rafId 裡存的是 timeout ID。teardown 不能只呼叫 cancelAnimationFrame，
// 還得 clearTimeout — 分開追蹤兩個 ID 最乾淨。
let rafId = 0
let timeoutId = 0
let resizeObs: ResizeObserver | null = null
let scrollListener: (() => void) | null = null

// FPS 降級 rolling avg（spec §7）
let frameTimes: number[] = []
let lowPowerMode = false
let lastFrame = 0

function setupFocalCanvas() {
  teardown()

  const host = document.querySelector<HTMLElement>("[data-home-hero-focal]")
  if (!host) return  // 目標不存在 → early return
  const canvas = host.querySelector<HTMLCanvasElement>(".home-hero__canvas")
  if (!canvas) return
  const ctx = canvas.getContext("2d")
  if (!ctx) return

  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  const mobile = window.__motion?.isMobileViewport?.() ?? false

  const dpr = mobile ? Math.min(window.devicePixelRatio || 1, 1.5) : window.devicePixelRatio || 1
  let w = 0
  let h = 0

  function resize() {
    const rect = host!.getBoundingClientRect()
    w = Math.max(1, rect.width)
    h = Math.max(1, rect.height)
    canvas!.width = Math.floor(w * dpr)
    canvas!.height = Math.floor(h * dpr)
    canvas!.style.width = `${w}px`
    canvas!.style.height = `${h}px`
    ctx!.scale(dpr, dpr)
  }
  resize()

  // spec §5.1: 「暖金漸層光暈 + 緩動粒子」
  const particleCount = mobile ? 18 : 40
  const particles: Particle[] = []
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 1 + Math.random() * 2.2,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      alpha: 0.35 + Math.random() * 0.35,
      hueShift: Math.random() * 20 - 10,
    })
  }

  let scrollProgress = 0   // 0-1，spec §5.1 "隨 scroll 呼吸"
  scrollListener = () => {
    const max = window.innerHeight * 1.2
    scrollProgress = Math.min(1, Math.max(0, window.scrollY / max))
  }
  window.addEventListener("scroll", scrollListener, { passive: true })

  function drawFrame(t: number) {
    // FPS rolling avg 降級（spec §7：30-frame avg > 22ms 則切 low-power）
    if (lastFrame > 0) {
      const dt = t - lastFrame
      frameTimes.push(dt)
      if (frameTimes.length > 30) frameTimes.shift()
      if (frameTimes.length === 30) {
        const avg = frameTimes.reduce((a, b) => a + b, 0) / 30
        if (avg > 22 && !lowPowerMode) {
          lowPowerMode = true
        }
      }
    }
    lastFrame = t

    ctx!.clearRect(0, 0, w, h)

    // 漸層光暈（中心 → 邊緣 fade），暖金色
    const cx = w * (0.52 + 0.04 * Math.sin(t * 0.0006))
    const cy = h * (0.5 + 0.03 * Math.cos(t * 0.0005) + scrollProgress * 0.08)
    const rMax = Math.hypot(w, h) * 0.7
    const grad = ctx!.createRadialGradient(cx, cy, 0, cx, cy, rMax)
    grad.addColorStop(0, `rgba(200, 169, 107, ${0.42 - scrollProgress * 0.2})`)
    grad.addColorStop(0.35, `rgba(200, 169, 107, ${0.2 - scrollProgress * 0.1})`)
    grad.addColorStop(1, "rgba(200, 169, 107, 0)")
    ctx!.fillStyle = grad
    ctx!.fillRect(0, 0, w, h)

    // 粒子
    for (const p of particles) {
      p.x += p.vx
      p.y += p.vy
      if (p.x < 0 || p.x > w) p.vx *= -1
      if (p.y < 0 || p.y > h) p.vy *= -1
      ctx!.beginPath()
      ctx!.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx!.fillStyle = `rgba(255, 247, 234, ${p.alpha * (1 - scrollProgress * 0.4)})`
      ctx!.fill()
    }
  }

  function loop(t: number) {
    if (document.hidden) {
      rafId = requestAnimationFrame(loop)
      return
    }
    drawFrame(t)
    if (lowPowerMode) {
      // 30fps fallback — 用 setTimeout 拖到下一個 ~33ms tick，再重新排 rAF
      timeoutId = window.setTimeout(() => {
        timeoutId = 0
        rafId = requestAnimationFrame(loop)
      }, 33)
    } else {
      rafId = requestAnimationFrame(loop)
    }
  }

  // Reduced-motion：只畫第一幀（spec §8.1）
  if (reduced) {
    drawFrame(0)
    return
  }

  // 先畫第一幀（LCP 之前），再啟動 rAF
  drawFrame(0)

  // spec §9.5: 延後到 LCP 後才啟動 rAF loop
  const startLoop = () => {
    lastFrame = performance.now()
    rafId = requestAnimationFrame(loop)
  }
  if ("PerformanceObserver" in window) {
    try {
      new PerformanceObserver((list) => {
        if (list.getEntries().some((e) => e.entryType === "largest-contentful-paint")) {
          startLoop()
        }
      }).observe({ type: "largest-contentful-paint", buffered: true })
    } catch {
      setTimeout(startLoop, 350)
    }
  } else {
    setTimeout(startLoop, 350)
  }

  // ResizeObserver：容器尺寸改變時重新 layout
  resizeObs = new ResizeObserver(() => resize())
  resizeObs.observe(host)

  // visibilitychange：隱藏 tab 時已在 loop 內 guard，不需額外 listener
}

function teardown() {
  cancelAnimationFrame(rafId)
  rafId = 0
  if (timeoutId) {
    clearTimeout(timeoutId)  // low-power fallback 可能 pending 中
    timeoutId = 0
  }
  resizeObs?.disconnect()
  resizeObs = null
  if (scrollListener) {
    window.removeEventListener("scroll", scrollListener)
    scrollListener = null
  }
  frameTimes = []
  lowPowerMode = false
  lastFrame = 0
}

document.addEventListener("nav", setupFocalCanvas)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

**為何 script 是 safe-no-op 的**：第一行 `document.querySelector("[data-home-hero-focal]")` 若回傳 `null` 就 `return`，整個 setup 不跑，零成本。

- [ ] **Step 2: 寫 `sectionCanvas.inline.ts`（dormant stub）**

Create `quartz/components/scripts/sectionCanvas.inline.ts`:

```ts
// Section-themed canvas renderer (spec §7 / §4.4)
// Phase 2: dormant — 只暴露 API surface，無 DOM target
// Phase 3: ArticleHero 會在 nav 事件呼叫 window.__sectionCanvas.render(el, config)
//         來繪製 geometric-lines / particle-flow / steam-curves 其中一種視覺
//
// 為什麼 Phase 2 就建檔：spec §10 Phase 2 commit 2 要求「focal canvas +
// sectionCanvas 繪製器」同 commit 進 repo，避免 Phase 3 一次要 review 太多
// canvas 邏輯。此 commit 後 window.__sectionCanvas API 已可呼叫（renderer
// 回傳 no-op 處理函數），不破壞任何現有行為。

export type SectionCanvasRenderer = "geometric-lines" | "particle-flow" | "steam-curves"

export interface SectionCanvasConfig {
  renderer: SectionCanvasRenderer
  glowColor: string          // rgba / hex，Phase 3 由 sectionThemes.motionConfig.glowColorDark/Light 傳入
  particleDensity: number
}

declare const window: Window & {
  __sectionCanvas?: {
    render: (host: HTMLElement, config: SectionCanvasConfig) => () => void
  }
}

// Phase 2 dormant stub — 三個 renderer 的具體繪製邏輯在 Phase 3 實作，
// 現階段只保證 API 存在且 cleanup 函數可呼叫。Phase 3 會覆寫這些函數體。
function renderGeometricLines(
  _ctx: CanvasRenderingContext2D,
  _w: number,
  _h: number,
  _config: SectionCanvasConfig,
): void {
  // Phase 3: 等距幾何線條（manufacturing-ai 主題）
}

function renderParticleFlow(
  _ctx: CanvasRenderingContext2D,
  _w: number,
  _h: number,
  _config: SectionCanvasConfig,
): void {
  // Phase 3: 粒子流（ai-notes 主題）
}

function renderSteamCurves(
  _ctx: CanvasRenderingContext2D,
  _w: number,
  _h: number,
  _config: SectionCanvasConfig,
): void {
  // Phase 3: 蒸氣曲線 + 光斑（coffee 主題）
}

const renderers = {
  "geometric-lines": renderGeometricLines,
  "particle-flow": renderParticleFlow,
  "steam-curves": renderSteamCurves,
}

/**
 * Phase 3 API — 呼叫此函數附加 canvas 繪製到指定 host element。
 * 回傳 cleanup 函數讓呼叫方在 prenav / teardown 時反註冊。
 * Phase 2 dormant：回傳的函數可安全呼叫（no-op）。
 */
function render(host: HTMLElement, config: SectionCanvasConfig): () => void {
  // Phase 3 實作大綱（目前不執行）：
  // 1. 找 host 裡的 canvas 或創一個
  // 2. resize to host bounding rect × dpr
  // 3. setInterval 或 rAF 呼叫 renderers[config.renderer]
  // 4. 回傳 cleanup
  void host
  void config
  void renderers
  return () => {
    /* Phase 3 會填 teardown；Phase 2 no-op */
  }
}

window.__sectionCanvas = { render }
```

- [ ] **Step 3: Wire 兩支 script 進 `MotionRuntime.tsx`**

Modify `quartz/components/MotionRuntime.tsx` — 在 imports 區加：

```tsx
// @ts-ignore
import focalCanvasScript from "./scripts/focalCanvas.inline"
// @ts-ignore
import sectionCanvasScript from "./scripts/sectionCanvas.inline"
```

在 `concatenateResources(...)` 呼叫裡加兩個參數（放在 `scrollRevealScript` 之後、`gsapLoaderScript` 之前）：

```tsx
MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  scrollRevealScript,
  focalCanvasScript,     // Phase 2 新增 — 首頁 hero focal canvas (spec §5.1)
  sectionCanvasScript,   // Phase 2 新增 — Phase 3 ArticleHero dormant API (spec §7)
  gsapLoaderScript,
)
```

- [ ] **Step 4: Build 驗證兩支 script 被 bundle，runtime 為 no-op**

```bash
npx quartz build 2>&1 | tail -3
grep -c "home-hero__focal\|data-home-hero-focal\|__sectionCanvas" public/postscript.js
# 預期：> 0（兩支 script 都有進 bundle）
```

啟動 dev server 開 `/`，DevTools Console：

```js
document.querySelector('[data-home-hero-focal]')
// 預期：null（HomeHeroApple 還沒進 layout）

window.__sectionCanvas
// 預期：{render: fn}
window.__sectionCanvas.render(document.body, {renderer: 'geometric-lines', glowColor: '#000', particleDensity: 10})()
// 預期：無 error，回傳 cleanup fn（no-op）
```

確認無 console error / warning。

- [ ] **Step 5: Commit**

```bash
git add quartz/components/scripts/focalCanvas.inline.ts \
  quartz/components/scripts/sectionCanvas.inline.ts \
  quartz/components/MotionRuntime.tsx
git commit -m "$(cat <<'EOF'
feat: focalCanvas + sectionCanvas inline scripts 進 MotionRuntime

focalCanvas（spec §5.1 / §7 / §8.1 / §9.5 首頁 hero focal canvas）：
- 暖金漸層光暈 + 緩動粒子（手機粒子數減半、dpr 降級）
- scroll 驅動「呼吸」感（scrollProgress 影響中心偏移與 alpha）
- FPS rolling-avg 降級（30-frame avg > 22ms → setTimeout 30fps）
- Reduced-motion 時只畫第一幀
- LCP 之後才啟動 rAF loop（PerformanceObserver，保底 setTimeout 350ms）
- prenav 時 teardown（ResizeObserver / scroll listener / rAF）

sectionCanvas（spec §7 / §4.4 dormant API，Phase 3 ArticleHero 接）：
- 暴露 window.__sectionCanvas.render(host, {renderer, glowColor, particleDensity})
- 3 個 renderer 骨架：geometric-lines / particle-flow / steam-curves
- Phase 2 函數體為 no-op，回傳 cleanup 可安全呼叫
- 對應 spec §10 Phase 2 commit 2 要求兩支一起進

兩者加進 MotionRuntime concatenateResources。此 commit 後 postscript.js
已含兩腳本；focalCanvas runtime querySelector 找不到 [data-home-hero-focal]
→ early return 零 side effect；sectionCanvas 全程 dormant。Task 3 swap
入 HomeHeroApple 時 focalCanvas 才會真正啟動。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 3: `HomeLanding.tsx` 按 §16 重寫（feature flag 打開、Matter 廢止）

**Files:**
- Modify: `quartz/components/HomeLanding.tsx`

**這一步正式開 feature flag**：`HomeLanding` 把 JSX 換成 `<HomeHeroApple />` + 新 Pillars/Stats/Featured/Recent；`heroSceneScript` import 與 `afterDOMLoaded` 指派同時刪除。Matter.js 依賴這時仍在 `package.json` 裡，但沒有任何 import，Task 5 統一清。

build 後首頁視覺 **質變**：hero 變成新版、Matter.js 物件完全消失、多了 Three Pillars / Featured / Recent 新版樣式。這是 Phase 2 視覺上第一個「看得出來」的 commit。

- [ ] **Step 1: 重寫 `HomeLanding.tsx`**

Replace `quartz/components/HomeLanding.tsx` content with:

```tsx
import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { formatDate, getDate } from "./Date"
import { getSectionThemeForSlug, sectionThemes } from "./sectionThemes"
import HomeHeroApple from "./HomeHeroApple"

const featuredSlugs = [
  "manufacturing-ai/在傳統製造業導入-AI，最先卡住的不是模型",
  "manufacturing-ai/企業內部推-AI-時，最常見的-5-種阻力",
  "ai-notes/我目前最常用的-AI-工具組合",
  "coffee/泡咖啡這件事，怎麼幫我整理思緒",
] as const

function isRealArticle(page: QuartzPluginData) {
  const slug = page.slug
  return !!slug && slug !== "index" && !slug.endsWith("/index") && !slug.startsWith("tags/")
}

function summarize(page: QuartzPluginData) {
  const fromDescription = page.frontmatter?.description?.trim()
  if (fromDescription) return fromDescription

  const paragraphs =
    page.text
      ?.split(/\n+/)
      .map((line) =>
        line
          .replace(/^#+\s*/, "")
          .replace(/^[-*]\s*/, "")
          .replace(/^\d+\.\s*/, "")
          .replace(/\[\[(.*?)\]\]/g, "$1")
          .replace(/\s+/g, " ")
          .trim(),
      )
      .filter((line) => line.length > 32) ?? []

  const candidate = paragraphs[0] ?? page.description?.trim() ?? page.frontmatter?.title ?? ""
  return candidate.slice(0, 92) + (candidate.length > 92 ? "..." : "")
}

function getDateSafe(page: QuartzPluginData) {
  try {
    return getDate({ defaultDateType: "modified" } as any, page)
  } catch {
    return page.dates?.modified
  }
}

export default (() => {
  const HeroComponent = HomeHeroApple()

  function HomeLanding(props: QuartzComponentProps) {
    const { fileData, allFiles, cfg } = props
    const slug = fileData.slug ?? ("index" as FullSlug)
    const articles = allFiles.filter(isRealArticle)
    const recentArticles = [...articles]
      .sort((a, b) => (getDateSafe(b)?.getTime() ?? 0) - (getDateSafe(a)?.getTime() ?? 0))
      .slice(0, 4)
    const featuredArticles = featuredSlugs
      .map((targetSlug) => articles.find((page) => page.slug === targetSlug))
      .filter((page): page is QuartzPluginData => !!page)
    const mostRecent = recentArticles[0]
    const lastUpdated =
      mostRecent && getDateSafe(mostRecent)
        ? formatDate(getDateSafe(mostRecent)!, cfg.locale)
        : "持續整理中"

    // spec §5.1 v2「Three Pillars」只 render 3 個內容主軸（不含 about）。
    // sectionThemes 含 4 個 entry，需過濾 about 以對齊 _home-apple.scss 的
    // .home-pillars grid-template-columns: repeat(3, ...) 設計。
    const pillarThemes = sectionThemes.filter((t) => t.key !== "about")

    return (
      <div class="home-landing" data-section-theme="home">
        <HeroComponent {...props} />

        <section class="home-stats-strip" data-reveal>
          <div class="home-stats-strip__item">
            <span class="home-stats-strip__label">目前已發布</span>
            <strong class="home-stats-strip__value" data-count-to={articles.length}>
              {articles.length}
            </strong>
          </div>
          <div class="home-stats-strip__item">
            <span class="home-stats-strip__label">主軸內容</span>
            <strong class="home-stats-strip__value">3 個領域</strong>
          </div>
          <div class="home-stats-strip__item">
            <span class="home-stats-strip__label">最近更新</span>
            <strong class="home-stats-strip__value">{lastUpdated}</strong>
          </div>
        </section>

        <section class="home-pillars">
          {pillarThemes.map((section) => (
            <a
              href={resolveRelative(slug, section.href)}
              class="home-pillars__card"
              data-section-theme={section.key}
              data-reveal
            >
              <p>{section.label}</p>
              <strong>{section.navLabel}</strong>
              <span>{section.description}</span>
              <small>{section.status}</small>
            </a>
          ))}
        </section>

        {featuredArticles.length > 0 && (
          <section class="home-featured">
            {featuredArticles.map((page, index) => {
              const theme = getSectionThemeForSlug(page.slug)
              return (
                <a
                  href={resolveRelative(slug, page.slug! as FullSlug)}
                  class={`home-featured__card ${index === 0 ? "home-featured__card--primary" : ""}`}
                  data-section-theme={theme?.key}
                  data-reveal
                >
                  <p>{theme?.label}</p>
                  <h2>{page.frontmatter?.title}</h2>
                  <span>{summarize(page)}</span>
                </a>
              )
            })}
          </section>
        )}

        <section class="home-recent">
          <header class="home-recent__heading">
            <p>START HERE</p>
            <h2>先從代表文章開始，不需要先把整個網站翻完。</h2>
            <p class="home-recent__copy">
              我把最值得先看的內容直接擺在首頁，第一次進來也能快速抓到重點。
            </p>
          </header>
          <div class="home-recent__list">
            {recentArticles.map((page) => {
              const theme = getSectionThemeForSlug(page.slug)
              const date = getDateSafe(page)
              return (
                <a
                  href={resolveRelative(slug, page.slug! as FullSlug)}
                  class="home-recent__item"
                  data-section-theme={theme?.key}
                  data-reveal
                >
                  <div class="home-recent__meta">
                    <span>{theme?.navLabel}</span>
                    {date ? (
                      <time datetime={date.toISOString()}>{formatDate(date, cfg.locale)}</time>
                    ) : (
                      <time />
                    )}
                  </div>
                  <strong>{page.frontmatter?.title}</strong>
                  <p>{summarize(page)}</p>
                </a>
              )
            })}
          </div>
        </section>
      </div>
    )
  }

  return HomeLanding
}) satisfies QuartzComponentConstructor
```

**刪除的項目**（相對 Phase 1 前版本）：
- `import heroSceneScript from "./scripts/heroScene.inline"`
- `const SCENE_EXT = ".png"` + `sceneObjects` 陣列
- `articlesForSection` helper（§16 把 `.home-landing__shelves` 刪除後無人使用）
- 整個 `.home-landing__hero-scene` + `.home-landing__hero-rail` + `.home-landing__section-map` + `.home-landing__shelves` JSX
- `(HomeLanding as QuartzComponent).afterDOMLoaded = heroSceneScript`

**保留 + 重寫**：
- Eyebrow / h1 / lead / signals / actions → 移到 `HomeHeroApple`
- Hero stats → 拉出成 `.home-stats-strip` 獨立 section
- Three sections → 變 `.home-pillars`（取代 `.home-landing__section-map` + `.home-landing__shelves`）
- Feature grid → `.home-featured`
- Recent → `.home-recent`

`data-reveal` 屬性觸發 Phase 1 的 `scrollReveal.inline.ts` 進場動畫（配合 `_motion-tokens.scss` 的 `[data-reveal]` 基礎 CSS）。

- [ ] **Step 2: Build 驗證**

```bash
npx quartz build 2>&1 | tail -10
```

預期：build 成功無 TS / SCSS error。

檢查 `public/postscript.js` 是否還殘留 Matter.js import（理論上應該 import graph 抓不到，但先驗）：

```bash
grep -c "matter-js\|Engine.create\|Bodies.circle" public/postscript.js
# 預期：0（Matter.js 從 postscript.js 裡消失）
```

啟動 dev server：

```bash
npx quartz build --serve 2>&1 &
sleep 3
```

瀏覽器開 `/`：
- 看到新 hero（純字 + 暖金漸層粒子 canvas）
- 看到 Stats strip（3 格）
- 看到 Three Pillars 卡片
- 看到 Featured（第一卡橫跨兩欄）+ Recent list
- 不該再看到 7 個 Matter.js 物件

DevTools Console：
```js
document.querySelector('[data-home-hero-focal]')
// 預期：HTMLElement（focalCanvas 現在有目標了）
document.querySelectorAll('.hero-object').length
// 預期：0
document.querySelector('[data-hero-cinematic]')
// 預期：HTMLElement（為 Task 9 的 heroCinematic 準備）
```

- [ ] **Step 3: Commit**

```bash
git add quartz/components/HomeLanding.tsx
git commit -m "$(cat <<'EOF'
feat: HomeLanding 依 §16 對照表重寫（Matter hero 廢止、Apple hero 上線）

spec §16 執行：
- 新 hero 由 HomeHeroApple 負責（純字 + focal canvas）
- Hero stats rail 拉出成 .home-stats-strip 獨立 section
- .home-landing__section-map 與 .home-landing__shelves 合併為 .home-pillars
- Feature grid 改名 .home-featured、Recent 改名 .home-recent
- 全新 BEM 命名，data-reveal 觸發 Phase 1 scrollReveal 進場

刪除：
- heroSceneScript import 與 afterDOMLoaded 指派
- Matter.js sceneObjects 陣列 + SCENE_EXT 常數
- articlesForSection helper（無人使用）
- .home-landing__hero-scene/.__hero-rail/.__section-map/.__shelves JSX

Matter.js 依賴仍在 package.json（Task 5 才清），但 postscript.js 已
不再 bundle matter-js（無 import graph 進入）。首頁視覺此 commit 後即
是 spec §5.1 目標狀態（除 GSAP 時間軸 / Lenis / 字體 preload 尚未接）。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 4: `custom.scss` 清 `.home-landing__*` / `.home-hero-scene` / `.hero-object` 規則

**Files:**
- Modify: `quartz/styles/custom.scss`

**這一步只刪不加**。Task 3 HTML 已經不再有 `.home-landing__hero` / `.__copy` / `.__eyebrow` / `.__hero-rail` / `.__visual-*` / `.__section-map` / `.__theme-tile` / `.__feature-grid` / `.__feature-card` / `.__recent*` / `.__shelves` / `.__shelf*` / `.home-hero-scene` / `.hero-object`，對應的 SCSS 變成死碼；此 commit 一次清掉。`.home-landing` wrapper 保留（Task 3 JSX 仍用），但其具體樣式也移到 `_home-apple.scss`。

**操作原則（code-reviewer M3）**：block-by-block Edit 容易漏、容易把非目標 rule 一起刪。改用**腳本 atomic 重寫**：寫個一次性 Node.js brace-balance 解析器，讀整份 `custom.scss` 後輸出「沒有任何 `.home-landing*` / `.home-hero-scene*` / `.hero-object*` rule block 的新版本」，人工 review diff 一次後覆蓋原檔。這樣可保證：(a) 不會因片段不唯一而選錯、(b) 不會因 brace count 算錯留下孤兒 `}`、(c) 可在 `@media` 裡的巢狀規則被正確遞迴處理。

- [ ] **Step 1: 基準計數**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
grep -c "home-landing\|home-hero-scene\|hero-object" quartz/styles/custom.scss
# 記錄此數（執行當下應 ~169-171，為刪除前 baseline）
wc -l quartz/styles/custom.scss
# 記錄總行數
```

- [ ] **Step 2: 寫刪除腳本 `.verify/strip-home-landing.mjs`（一次性，不 commit）**

Create `.verify/strip-home-landing.mjs`（`.verify/` 在 Task 4 已加進 `.gitignore`）:

```js
// 一次性 SCSS block stripper v3 —— recursive + selector-list aware + empty-at-rule cleanup。
//
// v1 缺陷：只在頂層 tokenize，@media { ... } 裡面直接 memcpy，media query 裡的
// .home-landing__* 沒被刪；selector list 整塊殺會誤刪同組的無辜 selector。
// v2 解了這兩個問題，但留下兩個瑕疵：
//   (a) @media 裡所有 child 都被殺時，留下空 `@media (...) {}`；
//   (b) selector list 重組成 `.foo{...}`（無空格、}} 擠一起），可讀性差。
// v3 修：
//   (a) at-rule 處理完 body 若 body trim 後是空的，整個 at-rule 丟掉；
//   (b) selector list 若有部分被 filter，用 ",\n" 重組並在 `{` 前補空格，
//       body 前後保留原本的 \n；
//   (c) 最後用 normalize 清掉多重空行。
import fs from "node:fs"

const src = fs.readFileSync("quartz/styles/custom.scss", "utf8")
const PATTERN = /\.home-landing(\b|__)|\.home-hero-scene(\b|__)|\.hero-object(\b|__)/

function processScope(scope) {
  let out = ""
  let i = 0
  const N = scope.length

  function findBalanced(pos) {
    if (scope[pos] !== "{") throw new Error("findBalanced: not at {")
    let depth = 0
    let j = pos
    while (j < N) {
      const ch = scope[j]
      if (ch === "{") depth++
      else if (ch === "}") {
        depth--
        if (depth === 0) return j
      } else if (ch === "/" && scope[j + 1] === "*") {
        j += 2
        while (j < N && !(scope[j] === "*" && scope[j + 1] === "/")) j++
        j++
      } else if (ch === "/" && scope[j + 1] === "/") {
        while (j < N && scope[j] !== "\n") j++
        continue
      } else if (ch === '"' || ch === "'") {
        const quote = ch
        j++
        while (j < N && scope[j] !== quote) {
          if (scope[j] === "\\") j++
          j++
        }
      }
      j++
    }
    throw new Error("unbalanced")
  }

  while (i < N) {
    const segStart = i
    let sawBrace = false
    while (i < N) {
      const ch = scope[i]
      if (ch === "{") { sawBrace = true; break }
      if (ch === ";") { i++; break }
      if (ch === "/" && scope[i + 1] === "*") {
        i += 2
        while (i < N && !(scope[i] === "*" && scope[i + 1] === "/")) i++
        i += 2
        continue
      }
      if (ch === "/" && scope[i + 1] === "/") {
        while (i < N && scope[i] !== "\n") i++
        continue
      }
      if (ch === '"' || ch === "'") {
        const quote = ch
        i++
        while (i < N && scope[i] !== quote) {
          if (scope[i] === "\\") i++
          i++
        }
        i++
        continue
      }
      if (ch === "}") break
      i++
    }

    if (!sawBrace) {
      out += scope.slice(segStart, i)
      if (i < N && scope[i] === "}") break
      continue
    }

    const rawSelector = scope.slice(segStart, i)
    const blockEnd = findBalanced(i)
    const rawBody = scope.slice(i + 1, blockEnd)
    i = blockEnd + 1

    const trimmedSel = rawSelector.trim()

    if (trimmedSel.startsWith("@")) {
      const newBody = processScope(rawBody)
      if (newBody.trim() === "") {
        if (i < N && scope[i] === "\n") i++
        continue
      }
      out += rawSelector + "{" + ensureTrailingNewline(newBody) + "}"
      continue
    }

    const parts = splitSelectorList(rawSelector)
    const kept = parts.filter((p) => !PATTERN.test(p))

    if (kept.length === 0) {
      if (i < N && scope[i] === "\n") i++
      continue
    }

    if (kept.length === parts.length) {
      const newBody = processScope(rawBody)
      out += rawSelector + "{" + newBody + "}"
    } else {
      const leadingMatch = rawSelector.match(/^(\s*)/)
      const leading = leadingMatch ? leadingMatch[1] : ""
      const trimmedParts = kept.map((p) => p.trim())
      const newSelector = leading + trimmedParts.join(",\n" + leading) + " "
      const newBody = processScope(rawBody)
      out += newSelector + "{" + newBody + "}"
    }
  }

  return out
}

function ensureTrailingNewline(s) {
  if (s.length === 0) return s
  const tail = s.slice(-40)
  if (/\n\s*$/.test(tail)) return s
  return s.replace(/[ \t]*$/, "") + "\n"
}

function splitSelectorList(sel) {
  const parts = []
  let depth = 0
  let start = 0
  for (let k = 0; k < sel.length; k++) {
    const ch = sel[k]
    if (ch === "(" || ch === "[") depth++
    else if (ch === ")" || ch === "]") depth--
    else if (ch === "," && depth === 0) {
      parts.push(sel.slice(start, k))
      start = k + 1
    }
  }
  parts.push(sel.slice(start))
  return parts
}

let out = processScope(src)
out = out.replace(/\n{4,}/g, "\n\n\n")
if (!out.endsWith("\n")) out += "\n"

fs.writeFileSync("quartz/styles/custom.scss", out, "utf8")
console.log("done")
```

- [ ] **Step 3: 跑腳本 + 驗證結果**

```bash
node .verify/strip-home-landing.mjs
```

驗證：

```bash
grep -c "home-landing\|home-hero-scene\|hero-object" quartz/styles/custom.scss
# 預期：0
wc -l quartz/styles/custom.scss
# 預期：比 baseline 少 ~250-350 行（刪掉 169 個 class occurrences 分佈於
# 多個 block）
```

若 grep 回傳非 0：看剩下哪一行，通常是 `@media` 內部某個 nested 規則 pattern 沒涵蓋到 — 手動 Edit 刪完，或改 regex 重跑。

- [ ] **Step 4: 刪除 `.home-landing` wrapper 規則（無 `__` 的那個）**

如果 `_home-apple.scss` 已負責 `.home-landing` 樣式（Task 1 Step 2 裡寫過），custom.scss 裡的 `.home-landing { ... }` 也該清掉：

```bash
grep -n "^\.home-landing " quartz/styles/custom.scss
# 若有輸出：用 Edit tool 刪那個 block
```

最終驗證：

```bash
grep -cE "\.home-landing|\.home-hero-scene|\.hero-object" quartz/styles/custom.scss
# 預期：0
```

- [ ] **Step 5: 人工 diff review（原子替換最後一道防線）**

```bash
git diff quartz/styles/custom.scss | head -60
# 檢查：
# - 看起來只有 - 行、沒有意外的 - 非 home-landing rule
# - 檔案尾部 brace count 平衡（所有 @media / 外層 rule 的 `{` 都有對應 `}`）

# 嚴格 brace count 驗證：
grep -o "[{}]" quartz/styles/custom.scss | sort | uniq -c
# 預期：{ 與 } 行數相同
```

- [ ] **Step 6: Build + CSS 驗證**

```bash
npx quartz build 2>&1 | tail -5
grep -c "home-landing__\|home-hero-scene\|hero-object" public/index.css
# 預期：0
grep -c "home-hero\|home-pillars\|home-stats-strip\|home-featured\|home-recent" public/index.css
# 預期：> 10
```

- [ ] **Step 7: 視覺 regression check**

`npx quartz build --serve` → 打開 `/`：
- Hero 區域視覺跟 Task 3 後一致（`_home-apple.scss` 負責）
- Stats / Pillars / Featured / Recent 樣式正確
- Dark / light 切換正常（舊規則已清不會覆蓋新 token）

- [ ] **Step 8: Commit**

```bash
git add quartz/styles/custom.scss
git commit -m "$(cat <<'EOF'
refactor: 刪除 custom.scss 中所有 .home-landing__* / .home-hero-scene / .hero-object 規則

spec §16.2 執行。Task 3 把 HomeLanding HTML 重寫為 BEM 新命名後，舊的
~167 行 .home-landing__ 規則（跨三個區段：基礎樣式 2430-2810、responsive
overrides 3300-3670、Matter scene 3828-3870）全部變死碼 — 此 commit 一次清掉。

驗證：
- grep "home-landing__\|home-hero-scene\|hero-object" custom.scss → 0
- grep 同 selector public/index.css → 0
- 首頁視覺與 Task 3 後完全一致（_home-apple.scss 接手負責）

.home-landing wrapper（無 __）若仍留在 custom.scss 也一併清掉，該 class
的樣式由 _home-apple.scss 維護。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 5: 刪 Matter.js 依賴 + `heroScene.inline.ts` + scene 資產

**Files:**
- Delete: `quartz/components/scripts/heroScene.inline.ts`
- Delete: `quartz/static/scene/*` (14 個檔案 — 7 個 `.png` + 7 個 `.svg`)
- Modify: `package.json`（刪 `matter-js` + `@types/matter-js`）
- Modify: `package-lock.json`（`npm uninstall` 自動更新）

**此 commit 純 cleanup，無程式邏輯變化**。Task 3 後 `heroScene.inline.ts` 已無 import graph；Task 4 後 CSS 也清乾淨；此 commit 把實體檔、資產、npm 依賴都移除。

- [ ] **Step 1: 刪除 `heroScene.inline.ts`（用 `git rm` 一次 stage 刪除）**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
git rm quartz/components/scripts/heroScene.inline.ts
```

驗證無殘餘 import：

```bash
grep -rn "heroScene\|heroSceneScript" quartz/ --include="*.ts" --include="*.tsx" 2>/dev/null
# 預期：無輸出
```

- [ ] **Step 2: 刪除 scene 資產（14 檔，用 `git rm -r`）**

```bash
ls quartz/static/scene/
# 預期看到 7 png + 7 svg（coffee-bean-1/2/3、laptop、phone、headphones、mug）

git rm -r quartz/static/scene/
# code-reviewer M7：用 git rm -r 一次刪檔 + stage 刪除，比 rm + git add -A
# 乾淨（不會意外把 .claude/ / .verify/ 等 untracked 目錄一起抓進來）
```

驗證無其他地方引用這些資產：

```bash
grep -rn "static/scene\|coffee-bean\|/scene/" quartz/ --include="*.ts" --include="*.tsx" --include="*.scss" --include="*.md" 2>/dev/null | head -5
# 預期：無（或只有 sectionThemes.ts 裡的 sceneObjects 欄位 — 檢查後如是 Phase 3 CategoryHero 要用的，保留；如已無用，Phase 3 再處理）
```

**注意**：`quartz/components/sectionThemes.ts` 的 `sceneObjects` 欄位是給 Phase 3 `CategoryHero` 用的**不同**資產系統（sectionScene.inline.ts 驅動），與首頁 hero 資產無關。**不要**清 sectionThemes 裡的 sceneObjects 欄位。

- [ ] **Step 3: 移除 Matter.js npm 依賴**

```bash
npm uninstall matter-js @types/matter-js
```

驗證 `package.json`：

```bash
grep -c "matter-js" package.json
# 預期：0
```

驗證 `package-lock.json`：

```bash
grep -c "\"matter-js\"" package-lock.json
# 預期：0
```

- [ ] **Step 4: Build 驗證一切正常**

```bash
npx quartz build 2>&1 | tail -10
# 預期：build 成功無 warning / error
```

驗證 `public/postscript.js` bundle：

```bash
grep -c "matter-js\|Matter\.\|Engine\.create" public/postscript.js
# 預期：0

ls -l public/postscript.js
# 記錄 AFTER size；跟 Phase 1 baseline 對比應小 ~25KB raw（~7-10KB gzipped）
```

- [ ] **Step 5: 功能驗證**

```bash
npx quartz build --serve 2>&1 &
sleep 3
```

瀏覽器開 `/`、任一分類頁、任一文章頁：
- 首頁 hero 正常（focal canvas + 新版文字）
- 分類頁（`/manufacturing-ai/` 等）的 `BrandIntro` 物件動畫照舊（sectionScene.inline.ts 不動）
- 文章頁正常
- Console 無 404 error（沒有殘留請求舊 `/static/scene/*.png`）

- [ ] **Step 6: Commit**

Step 1-2 已用 `git rm` 把刪檔 stage 好；Step 3 的 `npm uninstall` 已更新 `package.json` / `package-lock.json`，這兩個用一般 `git add`：

```bash
git add package.json package-lock.json
git status
# 預期看到：
#   deleted:    quartz/components/scripts/heroScene.inline.ts
#   deleted:    quartz/static/scene/*.png / *.svg (14 個)
#   modified:   package.json
#   modified:   package-lock.json

git commit -m "$(cat <<'EOF'
chore: 移除 Matter.js 依賴、heroScene.inline.ts、static/scene 資產

Phase 2 前三個 commit 已把 Matter hero 徹底替換為 HomeHeroApple + focal
canvas，此 commit 純 cleanup：
- 刪 quartz/components/scripts/heroScene.inline.ts（無 import graph）
- 刪 quartz/static/scene/*（7 png + 7 svg，Matter 物件貼圖）
- npm uninstall matter-js @types/matter-js

驗證：
- public/postscript.js 不再含 matter-js / Engine.create（bundle 小 ~25KB raw）
- 無 404 資產請求（分類頁的 sectionScene / sectionThemes.sceneObjects 是
  另一套系統，不動）

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 6: Lenis smooth scroll — 安裝、`lenis.inline.ts`、接進 `MotionRuntime`

**Files:**
- Modify: `package.json`（`npm i lenis` 自動加）
- Modify: `package-lock.json`
- Create: `quartz/components/scripts/lenis.inline.ts`
- Modify: `quartz/components/MotionRuntime.tsx`

**Lenis 全站載入但 opt-in**：手機 / reduced-motion 不啟動；search modal 開啟時 `window.__lenis.stop()`（Task 7 會加呼叫點）。

- [ ] **Step 1: 安裝 Lenis**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
npm i lenis
```

驗證：

```bash
grep "\"lenis\"" package.json
# 預期：看到 "lenis": "^x.y.z"
```

- [ ] **Step 2: 寫 `lenis.inline.ts`**

Create `quartz/components/scripts/lenis.inline.ts`:

```ts
// Lenis smooth scroll (spec §5.1 / §6.5 / §8.2 / §9.2)
// 全站載入 bundle，但：
//   - 手機 (< 768px)：不啟動（iOS Safari 慣性相容）
//   - reduced-motion：不啟動（恢復原生 scroll）
//   - body[data-motion-lenis="false"]：明確 opt-out
// window.__lenis 暴露給 search.inline.ts 在 modal 開啟時 stop/start

import Lenis from "lenis"

declare const window: Window & {
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
    bodyOptsIn: (flag: string) => boolean
  }
  __lenis?: {
    stop: () => void
    start: () => void
    isActive: () => boolean
  }
}

let lenis: Lenis | null = null
let rafId = 0

function shouldActivate(): boolean {
  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  const mobile = window.__motion?.isMobileViewport?.() ?? false
  if (reduced || mobile) return false
  // body[data-motion-lenis="false"] 明確 opt-out（保留未來 per-page disable）
  const explicit = document.body.dataset.motionLenis
  if (explicit === "false") return false
  return true
}

function setupLenis() {
  teardown()

  if (!shouldActivate()) {
    window.__lenis = undefined
    return
  }

  lenis = new Lenis({
    lerp: 0.1,           // spec §13 決策 #3：標準 lerp
    smoothWheel: true,
    wheelMultiplier: 1,
    touchMultiplier: 1.5,
  })

  function loop(time: number) {
    lenis?.raf(time)
    rafId = requestAnimationFrame(loop)
  }
  rafId = requestAnimationFrame(loop)

  window.__lenis = {
    stop: () => lenis?.stop(),
    start: () => lenis?.start(),
    isActive: () => !!lenis,
  }
}

function teardown() {
  cancelAnimationFrame(rafId)
  rafId = 0
  lenis?.destroy()
  lenis = null
  window.__lenis = undefined
}

document.addEventListener("nav", setupLenis)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

- [ ] **Step 3: Wire 進 `MotionRuntime.tsx`**

Modify `quartz/components/MotionRuntime.tsx`：

Import 區加：

```tsx
// @ts-ignore
import lenisScript from "./scripts/lenis.inline"
```

`concatenateResources(...)` 加 `lenisScript`（放在 `sectionCanvasScript` 之後、`gsapLoaderScript` 之前）：

```tsx
MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  scrollRevealScript,
  focalCanvasScript,
  sectionCanvasScript,
  lenisScript,         // Phase 2 新增 (spec §6.5)
  gsapLoaderScript,
)
```

- [ ] **Step 4: Build 驗證 bundle 增量 + Lenis CSS**

```bash
npx quartz build 2>&1 | tail -5
grep -c "Lenis\|__lenis" public/postscript.js
# 預期：> 0
ls -l public/postscript.js
# 記錄 size；跟 Task 5 後對比應增加 ~15-20KB raw（~5KB gzipped）
```

- [ ] **Step 4.5: 建立 `_lenis.scss`（reset 樣式抽獨立檔）**

code-reviewer S7：Lenis reset 屬於「library 配套 CSS」，Semantic 上不該塞進 `_home-apple.scss`（那檔是首頁專屬樣式）— 抽獨立檔跟 Phase 1 的 `_motion-tokens.scss` / `_popover-immersive.scss` 一致。

Create `quartz/styles/_lenis.scss`:

```scss
// Lenis smooth scroll reset (spec §6.5)
// 由 lenis.inline.ts 在啟動時把 html.lenis + html.lenis-smooth class 掛上
// （Lenis 1.x 預設 wrapper = document.documentElement 的行為）。
// mobile / reduced-motion / body data opt-out 路徑下 Lenis 不啟動，
// html 不帶這些 class → 以下規則全部不匹配 → 沿用原生 scroll。

html.lenis,
html.lenis body {
  height: auto;
}

html.lenis.lenis-smooth {
  scroll-behavior: auto !important;
}

html.lenis.lenis-smooth [data-lenis-prevent] {
  overscroll-behavior: contain;
}

html.lenis.lenis-stopped {
  overflow: hidden;
}
```

Modify `quartz/styles/custom.scss` — 在現有 `@use "./_home-apple.scss";` **之前**加一行：

```scss
@use "./base.scss";
@use "./_motion-tokens.scss";
@use "./_popover-immersive.scss";
@use "./_lenis.scss";           // 新增（Lenis library reset）
@use "./_home-apple.scss";
```

再 build：

```bash
npx quartz build 2>&1 | tail -3
grep -c "lenis-smooth\|lenis-stopped" public/index.css
# 預期：> 0
```

- [ ] **Step 5: 手動驗證 Lenis 在桌機跑、手機/reduced 停用**

```bash
npx quartz build --serve &
sleep 3
```

Desktop Chrome DevTools Console（桌機視窗 > 768px）：

```js
window.__lenis  // 預期：{stop, start, isActive}
window.__lenis.isActive()  // 預期：true
document.documentElement.classList.contains('lenis')  // 預期：true
```

滾動頁面 — 應明顯感覺平滑（相比原生有 inertia）。

切到 DevTools Device Mode 選 iPhone（< 768px），refresh：

```js
window.__lenis  // 預期：undefined（mobile 不啟動）
document.documentElement.classList.contains('lenis')  // 預期：false
```

DevTools Rendering → Emulate CSS media feature `prefers-reduced-motion: reduce`，refresh：

```js
window.__lenis  // 預期：undefined
```

測試通過。

- [ ] **Step 6: 驗證 popover / TOC / darkmode 沒壞**

手動檢查：
- Wikilink popover 彈出正常
- TOC（文章頁）高亮隨滾動切換
- Darkmode 切換按鈕正常
- Search modal `/` 能開（下一 Task 會整合 Lenis stop/start，此 Task 先確認它能開）

任一失敗：回退此 commit、找 Lenis 跟該系統的碰撞點。

- [ ] **Step 7: Commit**

```bash
git add quartz/components/scripts/lenis.inline.ts quartz/components/MotionRuntime.tsx \
  quartz/styles/_lenis.scss quartz/styles/custom.scss \
  package.json package-lock.json
git commit -m "$(cat <<'EOF'
feat: Lenis smooth scroll 全站啟動（mobile / reduced-motion opt-out）

spec §5.1 / §6.5 / §8.2 / §9.2 實作：
- npm i lenis；走 Quartz 單一 postscript.js bundle (~5KB gzipped 增量)
- 啟動條件：desktop (>= 768px) && !prefers-reduced-motion
           && body[data-motion-lenis] !== "false"
- window.__lenis 暴露 stop/start/isActive 給 Task 7 的 search modal 整合
- prenav 時 destroy + cancelAnimationFrame；beforeunload 同上
- Lenis reset 抽獨立 _lenis.scss（跟 _motion-tokens.scss / _popover-immersive.scss
  並列），avoid library CSS 混進 _home-apple.scss home-page-specific 樣式

驗證：桌機滾動平滑 + popover/TOC/darkmode/search 不壞；mobile/reduced
條件下 window.__lenis undefined、無 smoothing。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 7: Search modal × Lenis 整合（spec §6.5）

**Files:**
- Modify: `quartz/components/scripts/search.inline.ts`

**單點改動**：`showSearch()` 加 `window.__lenis?.stop()`、`hideSearch()` 加 `window.__lenis?.start()`。沒有 Lenis 時 optional chaining 自動跳過，降級路徑乾淨。

- [ ] **Step 1: 找到 `showSearch` / `hideSearch` 函式位置**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
grep -n "^  function hideSearch\|^  function showSearch" quartz/components/scripts/search.inline.ts
# 預期：showSearch ~236, hideSearch ~223（Phase 1 沒改過這支，應該還是原位置）
```

- [ ] **Step 2: 加 Lenis 呼叫**

用 Read tool 讀出 `quartz/components/scripts/search.inline.ts` 的 L220-L245 區段，精準抓到 `hideSearch` / `showSearch` 函式主體。

用 Edit tool 改：

```ts
  function hideSearch() {
    container.classList.remove("active")
```

改為：

```ts
  function hideSearch() {
    container.classList.remove("active")
    ;(window as any).__lenis?.start()
```

同時：

```ts
  function showSearch(searchTypeNew: SearchType) {
```

改為（在進第一行做動前 stop）：

```ts
  function showSearch(searchTypeNew: SearchType) {
    ;(window as any).__lenis?.stop()
```

**為什麼用 `(window as any).__lenis` 而不 declare global**：search.inline.ts 是 Quartz upstream 檔，儘量減少對它的 type surface 改動，maintainer 升級時少衝突。`(window as any)` 一行 cast 即可，accessor 結果是 `undefined` 時 optional chaining 自動安全 no-op。

- [ ] **Step 3: Build + Syntax 驗證**

```bash
npx quartz build 2>&1 | tail -5
# 預期：build 成功無 TS error
```

- [ ] **Step 4: 手動驗證 open/close 正確 stop/start Lenis**

```bash
npx quartz build --serve &
sleep 3
```

桌機視窗開首頁，DevTools Console：

```js
// 預先滾動一段距離
window.scrollTo({top: 800, behavior: 'smooth'})

// 2 秒後
window.__lenis?.isActive()  // true

// 按 / 開 search
// Console:
window.__lenis?.isActive()  // 仍是 true（Lenis instance 還在，只是 stopped）
// 但滾動鍵 / 滑鼠滾輪不會讓底層頁面動了（Lenis 真的被 stop）

// 點 search 背景關閉（或 esc）
// Console:
// Lenis 恢復滾動
```

驗證沒有 console error。

- [ ] **Step 5: Mobile 路徑驗證（Lenis 未啟動時 stop/start 為 no-op）**

DevTools Device Mode iPhone、refresh、開 search：

- Console 不該有 error（`undefined?.stop()` 為安全 no-op）
- Search modal 正常開關

- [ ] **Step 6: Commit**

```bash
git add quartz/components/scripts/search.inline.ts
git commit -m "$(cat <<'EOF'
feat: Search modal 開啟時 stop Lenis、關閉時 start（spec §6.5）

一行 cast 到 window.__lenis 呼叫 stop/start，避免 search modal 背後
smooth scroll 繼續滾動（UX 破壞）。

用 (window as any).__lenis 而非 declare global：search.inline.ts 是
Quartz upstream 檔，減少 type surface 改動以免未來升級衝突。Optional
chaining 讓 Lenis 未啟動的 mobile / reduced-motion 路徑自動安全 no-op。

驗證：
- 桌機：開 search 後滾輪/鍵盤不動頁面；關 search 後恢復
- 手機 / reduced-motion：search 正常開關，無 console error

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 8: `CustomHead.tsx` — 字體 preload 擴充（spec §3.1）

**Files:**
- Create: `quartz/components/CustomHead.tsx`
- Modify: `quartz/components/index.ts`（export `CustomHead`）
- Modify: `quartz.layout.ts`（`head: Component.CustomHead()`）

**策略**：`CustomHead` 是 `Component.Head()` 的 wrapper — 它把 Quartz 預設 `Head` 的所有 meta / stylesheet / OG tag 保留，只額外在 Google Fonts CSS `<link rel="stylesheet">` 之前插入一個 `<link rel="preload" as="style">`（v3 定案的階段一）。Phase 4 audit 若 LCP 仍 > 2.5s 再升級到 self-host woff2。

- [ ] **Step 1: 寫 `CustomHead.tsx`**

Create `quartz/components/CustomHead.tsx`:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import Head from "./Head"
import { googleFontHref } from "../util/theme"

/**
 * CustomHead — 在 Quartz 預設 Head 之外加 Google Fonts stylesheet preload
 * （spec §3.1）。
 *
 * v3 定案：階段一用 stylesheet preload (as="style")，Google Fonts woff2
 * URL 含 hash 所以不能硬寫個別字重；preload stylesheet 讓瀏覽器早一步
 * 把 CSS 抓下來、早一步發現 font-face src，改善 LCP ~200-400ms。Phase 4
 * audit 若仍未達 LCP < 2.5s，升級到 self-host woff2（寫死 @font-face
 * 指向 static/vendor/fonts/）。
 *
 * 實作方式：**Fragment wrapper**（不碰 Preact VNode internals）。
 * 原 Head 組件照常 render，preload <link> 用 Fragment 放在它**前面**—
 * Preact SSR 會把 Fragment 攤平成連續 HTML，outer layout builder 把整包
 * 塞進 <head>，所以 preload link 會出現在其他 head content 之前。
 * 比 VNode 的 props.children spread 法更穩（不依賴 Preact 內部欄位如 __v
 * / $$typeof，Preact 大版更新不會破）。
 */
export default (() => {
  const BaseHead = Head()

  const CustomHead: QuartzComponent = (props: QuartzComponentProps) => {
    const { cfg } = props
    const shouldPreload =
      cfg.theme.cdnCaching && cfg.theme.fontOrigin === "googleFonts"

    return (
      <>
        {shouldPreload && (
          <link rel="preload" as="style" href={googleFontHref(cfg.theme)} />
        )}
        {(BaseHead as any)(props)}
      </>
    )
  }

  return CustomHead
}) satisfies QuartzComponentConstructor
```

**為什麼不額外加 `<link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin>`**：Quartz 的 `Head.tsx` 在 `cdnCaching && fontOrigin === "googleFonts"` 時已 render preconnect（見 `Head.tsx:43-52`）。再加一個會是 duplicate，瀏覽器 dedupe 無害但 HTML validator 會抱怨。

**為什麼不走 VNode mutation**：v1 草案試過 `{ ...baseNode, props: { ...props, children: merged } }`，但 Preact VNode 帶 internal fields（`__v` / `$$typeof` 等）object-spread 是保留的，不過是 Preact 內部 implementation detail；版本更新可能換欄位名。Fragment 法完全走 public API。

- [ ] **Step 2: Export 到 `quartz/components/index.ts`**

Modify `quartz/components/index.ts`：

- Import 區加 `import CustomHead from "./CustomHead"`（放在 `Head` import 後）
- Export 區加 `CustomHead,`（放在 `Head,` 後）

- [ ] **Step 3: 切換 layout 使用 `CustomHead`**

Modify `quartz.layout.ts` L5：

```ts
  head: Component.Head(),
```

改為：

```ts
  head: Component.CustomHead(),
```

- [ ] **Step 4: Build 驗證**

```bash
npx quartz build 2>&1 | tail -5
# 預期：成功
```

驗證 `public/index.html` 含 preload：

```bash
grep -o 'rel="preload"[^>]*' public/index.html | head -3
# 預期：看到 rel="preload" as="style" href="https://fonts.googleapis.com/..."
```

- [ ] **Step 5: 瀏覽器 Network Panel 驗證**

```bash
npx quartz build --serve &
sleep 3
```

Chrome DevTools Network（hard reload / disable cache）：
- Filter: `fonts`
- 預期看到 Google Fonts CSS 被 preload（Priority "High" 或 "Highest"）
- 字體 woff2 載入時機早於沒有 preload 的 baseline

在 Console：

```js
// 檢查 <head> 裡有 preload link
document.head.querySelector('link[rel="preload"][as="style"]')?.href
// 預期：https://fonts.googleapis.com/css2?family=...
```

- [ ] **Step 6: Commit**

```bash
git add quartz/components/CustomHead.tsx quartz/components/index.ts quartz.layout.ts
git commit -m "$(cat <<'EOF'
feat: CustomHead 加 Google Fonts preload（spec §3.1 定案階段一）

不改 Quartz upstream Head.tsx，用 Fragment wrapper 把 <link rel="preload"
as="style"> 放在基底 Head 的 VNode 前面（preconnect 不重複 render — 基底
Head 已經有 preconnect fonts.gstatic.com）。其他 meta / OG tag / 原
stylesheet 全部保留。

為什麼走 Fragment 而非 VNode 的 .props.children spread：後者依賴 Preact
內部欄位（__v / $$typeof），跨版本脆弱；Fragment 法純 public API。

LCP 改善預期 ~200-400ms（spec §3.1 實測估計）。Phase 4 audit 後若仍
未達 LCP < 2.5s，再升級到 self-host woff2。

quartz.layout.ts sharedPageComponents.head 從 Component.Head() 切到
Component.CustomHead()。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 9: `heroCinematic.inline.ts` — GSAP 時間軸接上 focalCanvas

**Files:**
- Create: `quartz/components/scripts/heroCinematic.inline.ts`
- Modify: `quartz/components/MotionRuntime.tsx`

**這是 Phase 2 最後一支主 script**。`[data-hero-cinematic]` 出現時（首頁有）動態 load GSAP + ScrollTrigger（走 Phase 1 的 `window.__gsapLoader.loadGsap()`），然後掛一個 ScrollTrigger timeline 讓 hero copy fade-in、scroll 觸發 canvas 參數脈動、完成後 refresh ScrollTrigger。配合 §6.2 的 `navGeneration` token 做 stale-handler 防禦。

- [ ] **Step 1: 寫 `heroCinematic.inline.ts`**

Create `quartz/components/scripts/heroCinematic.inline.ts`:

```ts
// Hero cinematic timeline (spec §5.1 / §9.3 / §6.2)
// 首頁 hero copy 進場動畫 + scroll 驅動微動作
// 動態 load GSAP，走 Phase 1 window.__gsapLoader
//
// 搭配 §6.2 navGeneration token 做 race defense：
//   - 每個 await 之後 check myGen !== window.__nav.currentGen() → abort
//   - prenav 時被 Phase 1 navLifecycle++ 掉

declare const window: Window & {
  gsap?: any
  ScrollTrigger?: any
  __gsapLoader?: {
    loadGsap: () => Promise<void>
    bothLoaded: () => boolean
  }
  __nav?: {
    currentGen: () => number
  }
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
}

let scrollTriggers: any[] = []

function teardown() {
  for (const t of scrollTriggers) {
    try {
      t.kill?.()
    } catch {
      /* no-op */
    }
  }
  scrollTriggers = []
  // code-reviewer S6：不在 teardown 呼 ScrollTrigger.refresh()。
  // prenav 後頁面馬上要卸掉，refresh 會讓 ST 重算所有 Phase 3+ 的 trigger
  // layout，純白費功。新頁的 nav handler 自己會 refresh。
}

async function setupHeroCinematic() {
  teardown()

  const host = document.querySelector<HTMLElement>("[data-hero-cinematic]")
  if (!host) return  // 不是 cinematic 頁 → 不載 GSAP

  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  if (reduced) return  // spec §8.1：reduced-motion 不啟動 GSAP

  // code-reviewer spec gap：spec §10 Phase 2 驗收寫「手機版無 GSAP」，
  // plan v1 漏掉這條（只擋 reduced）。GSAP + ScrollTrigger ~46KB gzipped
  // 在手機上是純浪費（hero copy 文字直接顯示照樣好看、stats count-up 手機
  // 本來就靜態顯示），這裡擋掉讓手機只付 focalCanvas 的成本。
  const mobileGate = window.__motion?.isMobileViewport?.() ?? false
  if (mobileGate) return

  const myGen = window.__nav?.currentGen?.() ?? 0
  const staleNav = () => myGen !== (window.__nav?.currentGen?.() ?? 0)

  try {
    await window.__gsapLoader!.loadGsap()
    if (staleNav()) return

    await document.fonts.ready
    if (staleNav()) return
  } catch (err) {
    console.warn("[heroCinematic] GSAP load failed, hero degraded to static", err)
    return
  }

  const gsap = window.gsap
  const ScrollTrigger = window.ScrollTrigger
  if (!gsap || !ScrollTrigger) return

  // GSAP ease 說明（code-reviewer B3）：
  //   spec §3.5 指定 Apple 標準 cubic-bezier(0.22, 1, 0.36, 1)
  //   GSAP 3.x 不吃原始 CSS cubic-bezier() 字串（需 CustomEase plugin，
  //   但我們 Phase 1 沒 vendor CustomEase，只有 gsap + ScrollTrigger）
  //   GSAP 內建 "power3.out"（Bezier 近似 0.16, 0.84, 0.44, 1）最接近
  //   Apple 感，差距使用者不可見。Phase 4 若要 pixel-perfect 再 vendor
  //   CustomEase 並 registerPlugin(CustomEase)。
  const APPLE_EASE = "power3.out"

  // (1) 開場 timeline — eyebrow / h1 / lead / signals / actions 依序進
  const copy = host.querySelector<HTMLElement>(".home-hero__copy")
  if (copy) {
    const tl = gsap.timeline({
      defaults: { duration: 1.2, ease: APPLE_EASE },
    })
    tl.from(copy.querySelector(".home-hero__eyebrow"), { y: 18, opacity: 0, duration: 0.6 })
      .from(copy.querySelector(".home-hero__title"), { y: 32, opacity: 0 }, "-=0.4")
      .from(copy.querySelector(".home-hero__lead"), { y: 24, opacity: 0, duration: 0.8 }, "-=0.7")
      .from(
        copy.querySelectorAll(".home-hero__signals span"),
        { y: 16, opacity: 0, stagger: 0.08, duration: 0.5 },
        "-=0.5",
      )
      .from(
        copy.querySelectorAll(".home-hero__actions a"),
        { y: 16, opacity: 0, stagger: 0.08, duration: 0.5 },
        "-=0.4",
      )
  }

  // (2) ScrollTrigger — hero 離開 viewport 時整體淡出
  const st = ScrollTrigger.create({
    trigger: host,
    start: "top top",
    end: "bottom top",
    scrub: 0.5,
    animation: gsap.to(host, { opacity: 0.35, y: -40, ease: "none" }),
  })
  scrollTriggers.push(st)

  // (3) Stats count-up (spec §5.1 + §8.2)
  // 手機不跑 — 上面 mobileGate 已把整個 heroCinematic return 掉，手機會
  // 看到 SSR printed 的數字（靜態最終值），符合 spec §8.2「直接顯示最終值」。
  // 桌機才會走到這；ScrollTrigger 觸發、stats strip 進入 viewport 時啟動。
  {
    const targets = document.querySelectorAll<HTMLElement>(
      ".home-stats-strip__value[data-count-to]",
    )
    targets.forEach((el) => {
      const target = Number(el.dataset.countTo ?? "0")
      if (!Number.isFinite(target) || target <= 0) return

      // code-reviewer S2：stats 已滾過 viewport（例：SPA back 到已讀過的首頁、
      // 或 GSAP 載入慢）→ ScrollTrigger once+refresh 會補觸發 onEnter，但
      // 動畫視覺上會是「閃爍回 0 再跳回 target」，UX 破壞。先檢查 bounding
      // rect，若已滾過就直接設最終值，跳過動畫。
      const rect = el.getBoundingClientRect()
      if (rect.bottom < 0) {
        el.textContent = String(target)
        return
      }

      // code-reviewer S10：SSR 時 el.textContent 是 target（HomeLanding 印的），
      // 若讓 gsap.to 從 val=0 開始會產生「6 → 0 → 6」閃爍。動畫啟動前先把
      // 文字歸零，避免使用者看到突然跳回 0。
      el.textContent = "0"

      const counterObj = { val: 0 }
      const counterST = ScrollTrigger.create({
        trigger: el,
        start: "top 85%",
        once: true,
        onEnter: () => {
          gsap.to(counterObj, {
            val: target,
            duration: 1.2,
            ease: APPLE_EASE,
            onUpdate: () => {
              el.textContent = String(Math.round(counterObj.val))
            },
          })
        },
      })
      scrollTriggers.push(counterST)
    })
  }

  // refresh 一次讓 ScrollTrigger 重算 layout（字體已載入）
  ScrollTrigger.refresh()
}

document.addEventListener("nav", setupHeroCinematic)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
```

- [ ] **Step 2: Wire 進 `MotionRuntime.tsx`**

Modify `quartz/components/MotionRuntime.tsx`：

Import 加：

```tsx
// @ts-ignore
import heroCinematicScript from "./scripts/heroCinematic.inline"
```

`concatenateResources` 加 `heroCinematicScript`（放在 `gsapLoaderScript` 之後，要等 loader 註冊完）：

```tsx
MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  scrollRevealScript,
  focalCanvasScript,
  sectionCanvasScript,
  lenisScript,
  gsapLoaderScript,
  heroCinematicScript,   // Phase 2 新增，依賴 gsapLoader
)
```

- [ ] **Step 3: Build 驗證**

```bash
npx quartz build 2>&1 | tail -5
grep -c "heroCinematic\|__gsapLoader" public/postscript.js
# 預期：> 0
```

- [ ] **Step 4: 手動驗證首頁 hero 動畫 + Network 分析**

```bash
npx quartz build --serve &
sleep 3
```

桌機視窗開 `/`，DevTools Network：
- Filter: `gsap`
- 預期看到 `/static/vendor/gsap.min.js` 與 `/static/vendor/ScrollTrigger.min.js` 被載入
- Status 200、Content-Type `application/javascript`

Reload 頁面：
- Hero copy 應看得出進場動畫（eyebrow → h1 → lead → signals → actions 依序）
- 往下滾一點 hero 應有淡出 + translateY 位移

Console：

```js
window.gsap                      // 預期：function
window.ScrollTrigger             // 預期：function
window.ScrollTrigger.getAll().length
// 預期：>= 1（我們掛了一個 hero 的 ST）
```

- [ ] **Step 5: 驗證非 cinematic 頁面不載 GSAP**

瀏覽器開 `/manufacturing-ai/`（分類頁，Phase 2 尚未加 `data-hero-cinematic`），Network filter `gsap`：

- 預期：**無** `gsap.min.js` 請求（Task 9 的 `setupHeroCinematic` 在沒有 `[data-hero-cinematic]` 時 early return）

再開任一文章頁：

- 預期：**無** `gsap.min.js` 請求

這是 spec §9.2 的關鍵行為：只有 cinematic 頁面付 GSAP 載入成本。

- [ ] **Step 6: Reduced-motion 驗證**

DevTools Rendering → Emulate `prefers-reduced-motion: reduce`，refresh `/`：

- 預期：**無** `gsap.min.js` 請求（`setupHeroCinematic` 因 reduced-motion 直接 return，不 load GSAP）
- Hero copy 直接顯示（focal canvas 只畫一幀，見 Task 2 的 reduced 分支）

- [ ] **Step 7: Commit**

```bash
git add quartz/components/scripts/heroCinematic.inline.ts quartz/components/MotionRuntime.tsx
git commit -m "$(cat <<'EOF'
feat: heroCinematic inline script — GSAP 時間軸 + ScrollTrigger

spec §5.1 / §6.2 / §8.2 / §9.3 完整實作首頁 hero 的 cinematic 動畫：
- 動態 load GSAP + ScrollTrigger（走 Phase 1 window.__gsapLoader）
- eyebrow / h1 / lead / signals / actions 的 staged 進場 timeline，
  ease 用 "power3.out"（GSAP 內建 Bezier；spec §3.5 指定的 cubic-bezier
  字串需 CustomEase plugin，Phase 1 沒 vendor，Phase 4 再升級）
- ScrollTrigger scrub — hero 離開 viewport 時整體淡出 + 上位移
- Stats count-up：ScrollTrigger onEnter 觸發；用 getBoundingClientRect
  跳過已滾過的 stats 避免 refresh 閃爍，動畫前先把 textContent 設 "0"
  避免 SSR 最終值 → 0 → target 的視覺回彈
- navGeneration token 做 stale nav abort（對應 Phase 1 navLifecycle）
- reduced-motion + mobile 完全不載 GSAP（~46KB gzipped 省下來，對應
  spec §10 Phase 2 驗收「手機版無 GSAP」）
- 非 cinematic 頁面（無 [data-hero-cinematic]）不載 GSAP

Phase 2 最後一支 script；MotionRuntime 現含全部 8 支：motionFeatureDetect
/ navLifecycle / scrollReveal / focalCanvas / sectionCanvas / lenis /
gsapLoader / heroCinematic。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 10: 手動 regression + feature 驗證

**Files:**
- Create: `quartz/docs/superpowers/baselines/2026-04-24-phase2-verification.md`

**Files:** 純驗證 task，最後 commit 一份紀錄。

- [ ] **Step 1: Build production + 啟動 dev server**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
rm -rf public/
npx quartz build 2>&1 | tail -5
npx quartz build --serve &
sleep 3
```

- [ ] **Step 2: 首頁新視覺驗證（打開 `/`）**

| # | 項目 | 檢查 | 預期 |
|---|-----|------|------|
| 1 | Hero 100vh 區塊 | 滾到頁首 | 看到 eyebrow / H1（128px clamp）/ lead / signals / 兩顆 CTA |
| 2 | Focal canvas | Hero 右側 / mobile 上方 | 暖金漸層光暈 + 粒子浮動、隨滾動呼吸 |
| 3 | Hero GSAP 進場 | Reload / 換頁 | 5 段文字依序 stagger 進場 |
| 4 | Hero 離場 | 滾到 ~hero 底 | hero 整體淡出 + 略上移 |
| 5 | Stats strip | Hero 往下（桌機） | 3 格；`目前已發布 N 篇` 數字從 0 count-up 到實際值 |
| 5b | Stats strip mobile | DevTools iPhone 模式 refresh | 3 格直接顯示最終數字（無 count-up 動畫） |
| 6 | Three Pillars | 再往下 | 3 卡片 stagger 淡入 |
| 7 | Featured | 再往下 | 第一張橫跨兩欄；其餘淡入 |
| 8 | Recent list | 再往下 | 4 項項目，hover 邊框亮 |
| 9 | 無 Matter hero 殘留 | `document.querySelectorAll('.hero-object').length` | 0 |

- [ ] **Step 3: SPA 導航驗證**

點首頁「先看製造業 AI」CTA → 跳到 `/manufacturing-ai/`（不全頁 reload，Network 看沒全新 HTML 請求）。

再點瀏覽器返回 → 回到首頁、hero GSAP 動畫**重播**（因為 `nav` event 重新觸發 `setupHeroCinematic`；舊 `navGeneration` 已被 bump，舊 handler 不干擾）。

Console：

```js
window.__nav.currentGen()   // 應 >= 2（初次 + 一次 back）
window.ScrollTrigger.getAll().length   // 應 === 1（不是 2 疊加）
```

- [ ] **Step 4: Dark/light 切換**

點右上角主題圖示：
- 顏色切換
- Focal canvas 暖金色保持（canvas 用的是暖金 alpha，跟 theme 無關）
- Hero / Pillars / Featured 樣式全部切換正常

- [ ] **Step 5: Popover 驗證（舊功能不壞）**

進任一文章頁、hover wikilink：
- Popover 彈出、內容顯示正常
- Phase 1 的 `_popover-immersive.scss` 此時規則還匹配不到任何東西（Phase 3 才有 article-hero），無副作用

- [ ] **Step 6: TOC 驗證**

進一篇有多個 `## 標題` 的文章、滾動：
- TOC 高亮隨當前段落切換
- 未被 Lenis 破壞

- [ ] **Step 7: Search × Lenis 整合驗證**

首頁桌機視窗：
- 按 `/` 或點搜尋圖示 → Search modal 開啟
- Modal 開啟時底層滾輪 / 鍵盤無法動頁面（Lenis 已 stop）
- 關 modal（esc 或點背景）→ 滾動恢復

- [ ] **Step 8: Mobile 降級驗證**

DevTools Device Mode 選 iPhone，refresh `/`：

| 項目 | 預期 |
|-----|------|
| Lenis | 不啟動（`window.__lenis === undefined`） |
| Focal canvas | 啟動但解析度 dpr 降級、粒子數減半（18 顆） |
| GSAP | **不載入**（Network 無 `/static/vendor/gsap.min.js` 請求；對應 spec §10 Phase 2 驗收「手機版無 GSAP」） |
| Hero GSAP 動畫 | **沒有**（文字直接顯示） |
| Stats count-up | **沒有**（數字是 SSR 印的最終值） |
| Stats strip | 一欄 |
| Pillars | 一欄 |
| Featured | 一欄 |

- [ ] **Step 9: Reduced-motion 驗證**

DevTools Rendering → `prefers-reduced-motion: reduce`，refresh：

| 項目 | 預期 |
|-----|------|
| Lenis | 不啟動 |
| Focal canvas | 只畫第一幀，無 rAF |
| GSAP | **完全不載** |
| Hero 文字 | 直接顯示（無 stagger） |
| `[data-reveal]` | 立即 `.revealed`、無 transform |

- [ ] **Step 10: Console 0 error**

`/` / `/manufacturing-ai/` / 任一文章頁 / 404 頁 — DevTools Console 期望全程 0 error、0 warning（Quartz 本身若有 warning 視為 baseline，記錄但不 block）。

- [ ] **Step 11: Bundle size check**

```bash
ls -l public/postscript.js | awk '{print "postscript.js size:", $5, "bytes"}'
# 跟 Phase 1 baseline (docs/superpowers/baselines/2026-04-24-lighthouse.md 當時記的 size) 比
```

spec §9.6：postscript.js **淨變動 ≤ -10KB gzipped**（-25KB Matter + ~15KB Lenis/focalCanvas/heroCinematic）。

用 gzip 壓一下比較：

```bash
gzip -c public/postscript.js | wc -c
# 記錄此數值
```

- [ ] **Step 12: 寫驗證紀錄 + Commit**

Create `quartz/docs/superpowers/baselines/2026-04-24-phase2-verification.md`:

```markdown
# Phase 2 手動驗證紀錄

日期：YYYY-MM-DD
Commit：<Phase 2 最後一個 commit hash>

## 首頁新視覺（Task 10 step 2）
| # | 項目 | 結果 |
|---|-----|------|
| 1 | Hero 100vh + eyebrow / H1 / lead / signals / 兩 CTA | ✓/✗ |
| 2 | Focal canvas 暖金粒子呼吸 | ✓/✗ |
| 3 | Hero GSAP stagger 進場 | ✓/✗ |
| 4 | Hero 滾離場淡出 | ✓/✗ |
| 5 | Stats strip 3 格 | ✓/✗ |
| 6 | Three Pillars stagger 淡入 | ✓/✗ |
| 7 | Featured 第一張大卡 | ✓/✗ |
| 8 | Recent list 4 項 | ✓/✗ |
| 9 | Matter hero 不存在 | ✓/✗ |

## SPA / 主題切換 / 既有功能（step 3-7）
| 項目 | 結果 |
|-----|------|
| CTA 進分類頁 SPA nav | ✓/✗ |
| 返回後 hero 動畫不疊加 | ✓/✗ |
| Dark / light 切換 | ✓/✗ |
| Popover 仍正常 | ✓/✗ |
| TOC 高亮 | ✓/✗ |
| Search 開時 Lenis stop / 關時 start | ✓/✗ |

## 降級（step 8-9）
| 情境 | window.__lenis | GSAP 載入 | focal canvas | Hero 動畫 | Stats count-up |
|-----|--------------|---------|------------|---------|-------------|
| mobile | undefined | ✗ 不載 | 降級 dpr / 粒子 | ✗ 直接顯示 | ✗ 靜態 |
| reduced-motion | undefined | ✗ 不載 | 第一幀 | ✗ 直接顯示 | ✗ 靜態 |

## Bundle size
| 指標 | Phase 1 baseline | Phase 2 後 | diff |
|-----|---------------|---------|------|
| postscript.js raw | ??  | ??    | ??  |
| postscript.js gzipped | ?? | ?? | ?? |

**spec §9.6 目標**：淨變動 ≤ -10KB gzipped — 是 / 否

## Console 錯誤
（填入任何觀察到的 warning / error，或「全程 0 error / 0 warning」）

## 備註
（任何小觀察寫這）
```

填完數值後：

```bash
git add docs/superpowers/baselines/2026-04-24-phase2-verification.md
git commit -m "$(cat <<'EOF'
docs: Phase 2 手動驗證紀錄（首頁新視覺 + 降級 + bundle size）

Phase 2 完成後 11 項手動檢查通過：首頁新視覺 9 項、SPA / 主題 / 既有
功能 6 項、mobile / reduced-motion 降級、bundle size 對照 Phase 1 baseline。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Task 11: Phase 2 Lighthouse 對照

**Files:**
- Create: `quartz/docs/superpowers/baselines/2026-04-24-lighthouse-after-phase2.md`

- [ ] **Step 1: 啟動 dev server**

```bash
cd "C:/Users/user/Desktop/自有網域PoC/quartz"
npx quartz build 2>&1 | tail -3
npx quartz build --serve &
sleep 3
```

- [ ] **Step 2: 跑 Lighthouse desktop**

在 Chrome DevTools → Lighthouse tab，Desktop + Performance/Accessibility/Best Practices/SEO → Analyze page load，**分別**跑 3 頁：

1. `/`（首頁，有 GSAP + focal canvas + Lenis）
2. `/manufacturing-ai/`（分類頁，無 GSAP，Lenis ✓）
3. 任一文章頁（例：`/manufacturing-ai/企業內部推-AI-時，最常見的-5-種阻力`，無 GSAP，Lenis ✓）

記錄每頁的 Performance / Accessibility / Best Practices / SEO / LCP / CLS / INP。

- [ ] **Step 3: 對照 Phase 1 baseline**

從 `quartz/docs/superpowers/baselines/2026-04-24-lighthouse.md` 抓 Phase 1 數值。

- [ ] **Step 4: 寫 `lighthouse-after-phase2.md`**

Create `quartz/docs/superpowers/baselines/2026-04-24-lighthouse-after-phase2.md`:

```markdown
# Phase 2 完成後 Lighthouse 分數

日期：YYYY-MM-DD
Commit：<Phase 2 最後一個 commit hash>
Chrome 版本：<F12 → About 查>
Lighthouse 版本：<F12 Lighthouse panel 左下角>

## 首頁 `/`（含 GSAP + focal canvas + Lenis）

| 指標 | Phase 1 baseline | Phase 2 | diff |
|-----|---------------|---------|------|
| Performance | ?? | ?? | ?? |
| Accessibility | ?? | ?? | ?? |
| Best Practices | ?? | ?? | ?? |
| SEO | ?? | ?? | ?? |
| LCP (ms) | ?? | ?? | ?? |
| CLS | ?? | ?? | ?? |
| INP (ms) | ?? | ?? | ?? |

## 分類頁 `/manufacturing-ai/`（無 GSAP，Lenis ✓）

(同上格式)

## 文章頁（例：`/manufacturing-ai/企業內部推-AI-時，最常見的-5-種阻力`）

(同上格式)

## spec §9.6 目標對照

| 指標 | 目標 | 實測 | Pass? |
|-----|------|------|-------|
| LCP（所有頁） | < 2.5s | ?? | ? |
| INP | < 200ms | ?? | ? |
| CLS | < 0.1 | ?? | ? |
| postscript.js 淨變動 gzipped | -10 KB | ?? | ? |
| 首次載入 cinematic 頁含 GSAP | ≤ 50KB gzipped 額外 | ?? | ? |
| Lighthouse Performance 首頁 | ≥ 90 | ?? | ? |
| Lighthouse Performance 文章頁 | ≥ 95 | ?? | ? |
| Lighthouse Accessibility | ≥ 95 | ?? | ? |

## 備註 / 退步項目

（如有任何退步，記錄觀察：是否為可接受的 trade-off、Phase 3/4 是否需補救）
```

- [ ] **Step 5: Commit + 關閉 dev server**

```bash
git add docs/superpowers/baselines/2026-04-24-lighthouse-after-phase2.md
git commit -m "$(cat <<'EOF'
docs: Phase 2 完成後 Lighthouse 分數（對照 Phase 1 baseline 與 spec §9.6）

記錄 Phase 2 後三頁面（首頁 / 分類頁 / 文章頁）的 Lighthouse 分數 +
核心 web vitals + bundle size，對照 Phase 1 baseline 與 spec §9.6 目標。
退步項目（如有）寫在備註，讓 Phase 3/4 規劃時能補救。

Co-Authored-By: Jason simhope ai agent <jasonlin@simhope.com.tw>
EOF
)"
```

---

## Phase 2 完成標準（驗收）

完成所有 11 個 Task 後，check 下列全數滿足才算 Phase 2 ship：

- [ ] `npx quartz build` 無 warning / error
- [ ] `public/postscript.js` 含 8 支 motion script 的關鍵字（`__motion` / `__nav` / `__gsapLoader` / `__sectionCanvas` / `data-reveal` / `data-home-hero-focal` / `Lenis` / `heroCinematic`）
- [ ] `public/postscript.js` 不含 `matter-js` / `Engine.create`
- [ ] 首頁 DOM 有 `[data-hero-cinematic]` + `[data-home-hero-focal]`，無 `.hero-object`
- [ ] `package.json` 無 `matter-js` / `@types/matter-js`，有 `lenis`
- [ ] `custom.scss` 無 `home-landing__` / `home-hero-scene` / `hero-object`
- [ ] `quartz/static/scene/` 目錄已刪
- [ ] 手動 11 項驗證全過（Task 10）
- [ ] Lighthouse 對照 Phase 1 無退步、spec §9.6 目標達成或差距 < 5%（Task 11）
- [ ] Git log 顯示 11 個 Phase 2 commit（Task 1-11）

**若任一項失敗**：不要進 Phase 3，先修到過。Phase 2 是「首頁完工」的定義點。

---

## 接下來（Phase 3 預告）

Phase 2 ship 後進 Phase 3：分類頁 + 文章頁 hero（spec §10 Phase 3）。Phase 3 關鍵動作：

- `CategoryHero.tsx`（取代 `BrandIntro`，scroll-driven timeline）
- `ArticleHero.tsx`（section-themed canvas + TOC sticky）
- `popoverScroll.inline.ts`（MutationObserver scroll 到內容第一個元素，spec §6.3）
- `quartz.layout.ts` 按 spec §15 改 layout
- `cover:` / `accent:` / `hero-style:` frontmatter 支援
- 3 組 section 專屬 canvas（齒輪 / 粒子 / 蒸氣）

**不要現在就寫 Phase 3 plan** — Phase 2 跑過一輪真實的後，Phase 3 很多 script pattern（SPA race / 降級 / teardown）會按 Phase 2 實際經驗調整。Phase 3 plan 位置：`docs/superpowers/plans/YYYY-MM-DD-immersive-frontend-phase-3.md`。

Phase 2 ship 後建議先跑一次 `superpowers:code-reviewer` 針對本 plan 的實作結果找漏網。
