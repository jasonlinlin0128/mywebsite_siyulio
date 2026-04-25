// 原 in-view observer（upstream，spec §5.3 v3 不動）保留
const inViewObserver = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    const slug = entry.target.id
    const tocEntryElements = document.querySelectorAll(`a[data-for="${slug}"]`)
    const windowHeight = entry.rootBounds?.height
    if (windowHeight && tocEntryElements.length > 0) {
      if (entry.boundingClientRect.y < windowHeight) {
        tocEntryElements.forEach((tocEntryElement) => tocEntryElement.classList.add("in-view"))
      } else {
        tocEntryElements.forEach((tocEntryElement) => tocEntryElement.classList.remove("in-view"))
      }
    }
  }
})

// 新 active observer（Phase 3 新增，spec §5.3 v3）
// code-reviewer S1：IntersectionObserver entries 參數只含「狀態變化」的 entry，
// 不是「目前所有 intersecting」。所以維護一個 module-scope Set<id> 記
// 「目前正 intersect 的所有 heading id」，callback 內依 entry.isIntersecting
// add/remove，最後從 set 撈出 boundingClientRect.top 最小（最頂）那個當 active。
let lastActiveSlug: string | null = null
const intersectingHeadings = new Set<string>()

function pickTopmostActiveHeading(): string | null {
  let topmost: { id: string; top: number } | null = null
  intersectingHeadings.forEach((id) => {
    const el = document.getElementById(id)
    if (!el) return
    const top = el.getBoundingClientRect().top
    if (topmost === null || top < topmost.top) {
      topmost = { id, top }
    }
  })
  if (topmost === null) return null
  return (topmost as { id: string; top: number }).id
}

const activeObserver = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      const id = entry.target.id
      if (entry.isIntersecting) intersectingHeadings.add(id)
      else intersectingHeadings.delete(id)
    }
    const slug = pickTopmostActiveHeading()
    if (slug === lastActiveSlug) return
    lastActiveSlug = slug
    document
      .querySelectorAll(".toc-content a.active")
      .forEach((a) => a.classList.remove("active"))
    if (slug) {
      document
        .querySelectorAll(`a[data-for="${slug}"]`)
        .forEach((a) => a.classList.add("active"))
    }
  },
  {
    rootMargin: "-10% 0px -75% 0px",
    threshold: 0,
  },
)

function toggleToc(this: HTMLElement) {
  this.classList.toggle("collapsed")
  this.setAttribute(
    "aria-expanded",
    this.getAttribute("aria-expanded") === "true" ? "false" : "true",
  )
  const content = this.nextElementSibling as HTMLElement | undefined
  if (!content) return
  content.classList.toggle("collapsed")
}

function setupToc() {
  for (const toc of document.getElementsByClassName("toc")) {
    const button = toc.querySelector(".toc-header")
    const content = toc.querySelector(".toc-content")
    if (!button || !content) return
    button.addEventListener("click", toggleToc)
    window.addCleanup(() => button.removeEventListener("click", toggleToc))
  }
}

document.addEventListener("nav", () => {
  setupToc()

  inViewObserver.disconnect()
  activeObserver.disconnect()
  lastActiveSlug = null
  intersectingHeadings.clear()
  const headers = document.querySelectorAll("h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]")
  headers.forEach((header) => {
    inViewObserver.observe(header)
    activeObserver.observe(header)
  })
})
