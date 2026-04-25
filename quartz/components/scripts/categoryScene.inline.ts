// CategoryHero scroll-driven cinematic timeline (spec §5.2 + §6.2 + §8.1 + §8.2)
//
// 0-30%   scroll progress：物件從原點偏移（飄入感）
// 30-70%  ：重新編隊，depth 越大移動越多
// 70-100% ：物件散開 + 淡出（hero 離開 viewport 前）
//
// reduced-motion / mobile 不載 GSAP → 物件保持 SSR 靜態 CSS var 位置不動

declare const window: Window & {
  gsap?: any
  ScrollTrigger?: any
  __gsapLoader?: { loadGsap: () => Promise<void> }
  __nav?: { currentGen: () => number }
  __lenis?: {
    on?: (event: string, fn: (...args: any[]) => void) => void
    off?: (event: string, fn: (...args: any[]) => void) => void
    raf?: (time: number) => void
    isActive?: () => boolean
  }
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
}

let scrollTriggers: any[] = []
let lenisScrollHandler: ((...args: any[]) => void) | null = null

function teardown() {
  for (const t of scrollTriggers) {
    try { t.kill?.() } catch { /* no-op */ }
  }
  scrollTriggers = []
  // code-reviewer S8：解除 Lenis × ScrollTrigger sync listener
  if (lenisScrollHandler && window.__lenis?.off) {
    try { window.__lenis.off("scroll", lenisScrollHandler) } catch { /* no-op */ }
  }
  lenisScrollHandler = null
}

async function setupCategoryScene() {
  teardown()

  // 用 .category-hero class 直接抓 host — 不重用 data-hero-cinematic
  // 屬性以避免跟 Phase 2 heroCinematic.inline.ts 的 querySelector 撞車
  const host = document.querySelector<HTMLElement>(".category-hero")
  if (!host) return

  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  if (reduced) return  // SSR 靜態位置足夠

  const mobileGate = window.__motion?.isMobileViewport?.() ?? false
  if (mobileGate) return  // spec §8.2

  if (!window.__gsapLoader) {
    console.warn("[categoryScene] window.__gsapLoader missing — skipping")
    return
  }

  const myGen = window.__nav?.currentGen?.() ?? 0
  const staleNav = () => myGen !== (window.__nav?.currentGen?.() ?? 0)

  try {
    await window.__gsapLoader.loadGsap()
    if (staleNav()) return
    await document.fonts.ready
    if (staleNav()) return
  } catch (err) {
    console.warn("[categoryScene] GSAP load failed, scene stays static", err)
    return
  }

  const gsap = window.gsap
  const ScrollTrigger = window.ScrollTrigger
  if (!gsap || !ScrollTrigger) return

  // code-reviewer S8：Lenis smooth scroll 跑自己的 RAF loop，scroll 位置
  // 跟 native window.scrollY 不同步，scrub timeline 會感覺黏滯。
  // 解法：把 Lenis 的 scroll event 餵給 ScrollTrigger.update。
  if (window.__lenis?.on) {
    lenisScrollHandler = () => ScrollTrigger.update()
    try { window.__lenis.on("scroll", lenisScrollHandler) } catch { /* no-op */ }
  }

  const objects = host.querySelectorAll<HTMLElement>(".category-scene-object")
  if (objects.length === 0) return

  // 為每個物件建立 scroll-scrub timeline；重新編隊位置 = 隨機偏移依 depth scale
  objects.forEach((el) => {
    const depth = Number(el.dataset.depth ?? "1")
    const idx = Number(el.dataset.index ?? "0")
    // 用 idx 做偽隨機，保證 SSR / hydrate 一致
    const seed = (idx * 37 + 11) % 100
    const dx1 = (seed - 50) * depth * 0.6
    const dy1 = ((seed * 7) % 100 - 50) * depth * 0.4
    const dx2 = -dx1 * 0.7
    const dy2 = dy1 * -1.2

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: host,
        start: "top top",
        end: "bottom top",
        scrub: 0.6,
      },
    })

    tl.fromTo(
      el,
      { xPercent: 0, yPercent: 0, opacity: 0.6, rotation: 0 },
      { xPercent: dx1, yPercent: dy1, opacity: 0.85, rotation: 4 * depth, ease: "none" },
      0,
    )
      .to(el, { xPercent: dx1 * 0.4, yPercent: dy1 * 0.4, rotation: -2 * depth, ease: "none" }, 0.3)
      .to(el, { xPercent: dx2, yPercent: dy2, opacity: 0, ease: "none" }, 0.7)

    scrollTriggers.push(tl.scrollTrigger)
  })

  ScrollTrigger.refresh()
}

document.addEventListener("nav", setupCategoryScene)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
