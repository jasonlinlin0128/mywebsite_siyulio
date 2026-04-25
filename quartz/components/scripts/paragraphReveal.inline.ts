// 文章段落 reveal (spec §10 Phase 4)
// 對 article 內的 block 元素自動加 [data-reveal]，讓 Phase 1 scrollReveal
// IntersectionObserver 接手做 fade-in。reduced-motion 由 scrollReveal 內部
// 處理（直接 .revealed，無動畫），這裡不另外 gate。
//
// MotionRuntime 載入順序：放 scrollReveal 之前，確保 nav listener register
// 順序 → paragraphReveal 先設 attribute，scrollReveal 才 query [data-reveal]。

const SELECTORS =
  "article p, article h2, article h3, article h4, article pre, article ul, article ol, article blockquote, article figure"

let added: HTMLElement[] = []

function setup() {
  teardown()
  const els = document.querySelectorAll<HTMLElement>(SELECTORS)
  els.forEach((el) => {
    if (el.hasAttribute("data-reveal")) return
    el.setAttribute("data-reveal", "")
    added.push(el)
  })
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
