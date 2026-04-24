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
