// SPA navigation lifecycle skeleton (spec §6.2)
// Phase 1: navGeneration token + fonts.ready + focusFirstHeading
// Phase 2+: 各 hero script 自己 addEventListener('nav', handler) 並
//          capture navGeneration 做 stale-handler 防禦。

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

function currentGen() {
  return navGeneration
}

// Attach to window so Phase 2+ inline scripts can check navGeneration
declare global {
  interface Window {
    __nav?: {
      readonly generation: number
      currentGen: () => number
    }
  }
}

window.__nav = {
  get generation() {
    return navGeneration
  },
  currentGen,
}
