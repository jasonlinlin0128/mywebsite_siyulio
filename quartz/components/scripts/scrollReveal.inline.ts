// Lightweight reveal observer (spec §4.1 Layer 2)
// 任何元素加 [data-reveal] 就會在進入 viewport 時得到 .revealed class，
// 配合 _motion-tokens.scss 的 CSS transition 產生淡入效果。
// 不用 GSAP，純 IntersectionObserver，~1KB gzipped。

declare global {
  interface Window {
    __motion?: {
      prefersReducedMotion: () => boolean
      isMobileViewport: () => boolean
      isCoarsePointer: () => boolean
      bodyOptsIn: (flag: string) => boolean
    }
  }
}

let currentObserver: IntersectionObserver | null = null

function setupReveal() {
  // 先 disconnect 上一次的（SPA 導航時）
  currentObserver?.disconnect()

  const reduced = window.__motion?.prefersReducedMotion() ?? false
  const targets = document.querySelectorAll<HTMLElement>("[data-reveal]")

  // reduced-motion 或沒目標：直接標 revealed，不啟動 observer
  if (reduced || targets.length === 0) {
    targets.forEach((el) => el.classList.add("revealed"))
    currentObserver = null
    return
  }

  currentObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed")
          // 一次性：淡入後不再 observe
          currentObserver?.unobserve(entry.target)
        }
      })
    },
    {
      rootMargin: "0px 0px -12% 0px",   // 對應 $motion-reveal-offset
      threshold: 0.01,
    },
  )

  targets.forEach((el) => currentObserver!.observe(el))
}

document.addEventListener("nav", setupReveal)

window.addEventListener("beforeunload", () => {
  currentObserver?.disconnect()
  currentObserver = null
})
