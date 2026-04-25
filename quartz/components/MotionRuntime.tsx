import { QuartzComponent, QuartzComponentConstructor } from "./types"
import { concatenateResources } from "../util/resources"

// @ts-ignore
import motionFeatureDetectScript from "./scripts/motionFeatureDetect.inline"
// @ts-ignore
import navLifecycleScript from "./scripts/navLifecycle.inline"
// @ts-ignore
import paragraphRevealScript from "./scripts/paragraphReveal.inline"
// @ts-ignore
import scrollRevealScript from "./scripts/scrollReveal.inline"
// @ts-ignore
import focalCanvasScript from "./scripts/focalCanvas.inline"
// @ts-ignore
import sectionCanvasScript from "./scripts/sectionCanvas.inline"
// @ts-ignore
import lenisScript from "./scripts/lenis.inline"
// @ts-ignore
import gsapLoaderScript from "./scripts/gsapLoader.inline"
// @ts-ignore
import heroCinematicScript from "./scripts/heroCinematic.inline"
// @ts-ignore
import categorySceneScript from "./scripts/categoryScene.inline"
// @ts-ignore
import popoverScrollScript from "./scripts/popoverScroll.inline"
// @ts-ignore
import scrollProgressScript from "./scripts/scrollProgress.inline"

/**
 * MotionRuntime 是個 no-render 組件。掛到 sharedPageComponents.afterBody
 * 讓 12 支 motion inline script 被全站載入（在 Quartz 的單一 postscript.js 裡）。
 *
 * 載入順序（重要）：
 *   1. motionFeatureDetect — 定義 window.__motion 給其他 script 用
 *   2. navLifecycle — 定義 window.__nav + prenav/nav handler 骨架
 *   3. paragraphReveal — Phase 4 文章段落自動加 [data-reveal]
 *                        (必須在 scrollReveal 前 register，spec §10 Phase 4)
 *   4. scrollReveal — 依賴 window.__motion.prefersReducedMotion
 *   5. focalCanvas — Phase 2 首頁 hero focal canvas (query [data-home-hero-focal])
 *   6. sectionCanvas — Phase 3 ArticleHero canvas API (exposes window.__sectionCanvas)
 *   7. lenis — Phase 2 全站 smooth scroll (exposes window.__lenis; spec §6.5)
 *   8. gsapLoader — 提供 window.__gsapLoader.loadGsap() 給下游用
 *   9. heroCinematic — Phase 2 首頁 hero GSAP timeline + stats count-up
 *  10. categoryScene — Phase 3 分類頁 scroll-driven 物件編隊 timeline
 *                      (依賴 gsapLoader + lenis，spec §5.2)
 *  11. popoverScroll — Phase 3 popover 預覽自動 scroll 過 hero (spec §6.3)
 *  12. scrollProgress — Phase 4 1px 頂部進度條 CSS var 更新 (spec §5.3)
 *
 * 見 spec §4.1 (Layer 2 inline scripts)。
 */
const MotionRuntime: QuartzComponent = () => null

MotionRuntime.afterDOMLoaded = concatenateResources(
  motionFeatureDetectScript,
  navLifecycleScript,
  paragraphRevealScript, // Phase 4 — 必須在 scrollReveal 前 register (spec §10)
  scrollRevealScript,
  focalCanvasScript,     // Phase 2 — 首頁 hero focal canvas (spec §5.1)
  sectionCanvasScript,   // Phase 2 dormant + Phase 3 實作 — ArticleHero canvas (spec §7)
  lenisScript,           // Phase 2 — 全站 smooth scroll (spec §6.5)
  gsapLoaderScript,
  heroCinematicScript,   // Phase 2 — 首頁 hero GSAP timeline (依賴 gsapLoader)
  categorySceneScript,   // Phase 3 — 分類頁 scroll-cinematic (spec §5.2)
  popoverScrollScript,   // Phase 3 — popover 預覽 scroll 過 hero (spec §6.3)
  scrollProgressScript,  // Phase 4 — 1px 頂部進度條 (spec §5.3)
)

export default (() => MotionRuntime) satisfies QuartzComponentConstructor
