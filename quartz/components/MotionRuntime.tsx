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
