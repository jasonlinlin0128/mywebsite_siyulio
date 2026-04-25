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
