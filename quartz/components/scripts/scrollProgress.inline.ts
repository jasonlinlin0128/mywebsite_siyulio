// ScrollProgress (spec §5.3)
// 1px top bar 寬度跟 scroll 進度，document.documentElement style 寫
// CSS var --scroll-progress (0-1)。passive listener，extremely cheap。
//
// 為什麼 inline script 自己創 element 不從 SSR：Quartz `sharedPageComponents
// .afterBody` 渲染在 `.page-footer` 內，而首頁有 `body[data-slug="index"]
// .page-footer { display: none }` rule 會連帶把 ScrollProgress div 隱藏。
// 改由 inline script 在 setup 時把 div 直接 append 到 document.body root，
// 跳出 .page-footer 的 display:none 影響。

let scrollHandler: (() => void) | null = null
let progressEl: HTMLElement | null = null

function ensureElement(): HTMLElement {
  // 找 SSR 印的（在 .page-footer 內的）或自己創一個
  let el = document.querySelector<HTMLElement>(".scroll-progress")
  if (el) {
    // 移到 body root，避開父層 display:none
    if (el.parentElement !== document.body) {
      document.body.appendChild(el)
    }
    return el
  }
  el = document.createElement("div")
  el.className = "scroll-progress"
  el.setAttribute("aria-hidden", "true")
  document.body.appendChild(el)
  return el
}

function setup() {
  teardown()
  progressEl = ensureElement()
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
  // 不刪 progressEl — SPA 切頁時 setup 重新 ensureElement 會把它接回 body
}

document.addEventListener("nav", setup)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
