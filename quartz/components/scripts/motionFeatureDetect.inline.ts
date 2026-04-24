// Motion feature detection utility (spec §8.1 / §8.2)
// 全部 motion-related inline script 共用的降級判斷。

function prefersReducedMotion(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
}

function isMobileViewport(): boolean {
  // 跟 Quartz base.scss 定義的手機斷點一致（< 768px）
  return window.matchMedia("(max-width: 767px)").matches
}

function isCoarsePointer(): boolean {
  return window.matchMedia("(pointer: coarse)").matches
}

/**
 * 檢查 <body> 是否有指定 opt-in flag（例如 data-motion-lenis）
 * 讓 Phase 2+ 可以按頁面選擇性啟動 Lenis 等重量級動畫
 */
function bodyOptsIn(flag: string): boolean {
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
