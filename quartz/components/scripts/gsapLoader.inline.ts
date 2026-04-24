// GSAP dynamic loader (spec §9.3)
// Phase 1: 檔案就位不啟動
// Phase 2+: HomeHeroApple / CategoryHero 的 nav handler 會呼叫 loadGsap()

declare global {
  interface Window {
    gsap?: any
    ScrollTrigger?: any
    __gsapLoader?: {
      loadGsap: () => Promise<void>
      bothLoaded: () => boolean
    }
  }
}

let loadPromise: Promise<void> | null = null

function bothLoaded(): boolean {
  return !!(window.gsap && window.ScrollTrigger)
}

export function loadGsap(): Promise<void> {
  // (1) 雙檢查：gsap AND ScrollTrigger 都要在
  if (bothLoaded()) return Promise.resolve()
  if (loadPromise) return loadPromise

  loadPromise = new Promise<void>((resolve, reject) => {
    // (2) 10 秒 timeout
    const timeoutId = window.setTimeout(() => {
      loadPromise = null
      reject(new Error("GSAP load timeout (10s)"))
    }, 10000)

    const loadScript = (src: string) =>
      new Promise<void>((res, rej) => {
        const s = document.createElement("script")
        s.src = src
        s.onload = () => res()
        s.onerror = () => rej(new Error(`Failed to load ${src}`))
        document.head.appendChild(s)
      })

    loadScript("/static/vendor/gsap.min.js")
      .then(() => loadScript("/static/vendor/ScrollTrigger.min.js"))
      .then(() => {
        clearTimeout(timeoutId)
        window.gsap.registerPlugin(window.ScrollTrigger)
        resolve()
      })
      .catch((err) => {
        clearTimeout(timeoutId)
        loadPromise = null   // (3) 允許 retry
        reject(err)
      })
  })

  return loadPromise
}

// (4) prenav 中斷時：若兩個 global 還沒齊，reset loader
document.addEventListener("prenav", () => {
  if (!bothLoaded()) {
    loadPromise = null
  }
})

// 掛到 window 讓其他 inline script 不用 import
window.__gsapLoader = { loadGsap, bothLoaded }
