// Hero cinematic timeline (spec §5.1 / §9.3 / §6.2)
// 首頁 hero copy 進場動畫 + scroll 驅動微動作
// 動態 load GSAP，走 Phase 1 window.__gsapLoader
//
// 搭配 §6.2 navGeneration token 做 race defense：
//   - 每個 await 之後 check myGen !== window.__nav.currentGen() → abort
//   - prenav 時被 Phase 1 navLifecycle++ 掉

declare const window: Window & {
  gsap?: any
  ScrollTrigger?: any
  __gsapLoader?: {
    loadGsap: () => Promise<void>
    bothLoaded: () => boolean
  }
  __nav?: {
    currentGen: () => number
  }
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
}

let scrollTriggers: any[] = []

function teardown() {
  for (const t of scrollTriggers) {
    try {
      t.kill?.()
    } catch {
      /* no-op */
    }
  }
  scrollTriggers = []
  // code-reviewer S6：不在 teardown 呼 ScrollTrigger.refresh()。
  // prenav 後頁面馬上要卸掉，refresh 會讓 ST 重算所有 Phase 3+ 的 trigger
  // layout，純白費功。新頁的 nav handler 自己會 refresh。
}

async function setupHeroCinematic() {
  teardown()

  const host = document.querySelector<HTMLElement>("[data-hero-cinematic]")
  if (!host) return  // 不是 cinematic 頁 → 不載 GSAP

  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  if (reduced) return  // spec §8.1：reduced-motion 不啟動 GSAP

  // code-reviewer spec gap：spec §10 Phase 2 驗收寫「手機版無 GSAP」，
  // plan v1 漏掉這條（只擋 reduced）。GSAP + ScrollTrigger ~46KB gzipped
  // 在手機上是純浪費（hero copy 文字直接顯示照樣好看、stats count-up 手機
  // 本來就靜態顯示），這裡擋掉讓手機只付 focalCanvas 的成本。
  const mobileGate = window.__motion?.isMobileViewport?.() ?? false
  if (mobileGate) return

  const myGen = window.__nav?.currentGen?.() ?? 0
  const staleNav = () => myGen !== (window.__nav?.currentGen?.() ?? 0)

  // code-reviewer M3：__gsapLoader 理論上由 Phase 1 gsapLoader.inline.ts 一定
  // 先註冊，但 non-null assertion (!) 會在 Phase 1 script 意外被移除時噴
  // cryptic `Cannot read properties of undefined`。顯式 check 給可讀診斷。
  if (!window.__gsapLoader) {
    console.warn("[heroCinematic] window.__gsapLoader missing — skipping")
    return
  }

  try {
    await window.__gsapLoader.loadGsap()
    if (staleNav()) return

    await document.fonts.ready
    if (staleNav()) return
  } catch (err) {
    console.warn("[heroCinematic] GSAP load failed, hero degraded to static", err)
    return
  }

  const gsap = window.gsap
  const ScrollTrigger = window.ScrollTrigger
  if (!gsap || !ScrollTrigger) return

  // GSAP ease 說明（code-reviewer B3）：
  //   spec §3.5 指定 Apple 標準 cubic-bezier(0.22, 1, 0.36, 1)
  //   GSAP 3.x 不吃原始 CSS cubic-bezier() 字串（需 CustomEase plugin，
  //   但我們 Phase 1 沒 vendor CustomEase，只有 gsap + ScrollTrigger）
  //   GSAP 內建 "power3.out"（Bezier 近似 0.16, 0.84, 0.44, 1）最接近
  //   Apple 感，差距使用者不可見。Phase 4 若要 pixel-perfect 再 vendor
  //   CustomEase 並 registerPlugin(CustomEase)。
  const APPLE_EASE = "power3.out"

  // (1) 開場 timeline — eyebrow / h1 / lead / signals / actions 依序進
  const copy = host.querySelector<HTMLElement>(".home-hero__copy")
  if (copy) {
    const tl = gsap.timeline({
      defaults: { duration: 1.2, ease: APPLE_EASE },
    })
    // code-reviewer M1：timeline 無 scrub/trigger 所以不會 leak listener，但
    // 若使用者在 ~2s 進場窗內快速 SPA 切頁，timeline 仍會繼續 tick 到完成
    // 才被 GC，浪費幾 frame。把 .kill() 包進 scrollTriggers 陣列讓 teardown
    // 一起處理，免這短暫 tick。
    scrollTriggers.push({ kill: () => tl.kill() })
    tl.from(copy.querySelector(".home-hero__eyebrow"), { y: 18, opacity: 0, duration: 0.6 })
      .from(copy.querySelector(".home-hero__title"), { y: 32, opacity: 0 }, "-=0.4")
      .from(copy.querySelector(".home-hero__lead"), { y: 24, opacity: 0, duration: 0.8 }, "-=0.7")
      .from(
        copy.querySelectorAll(".home-hero__signals span"),
        { y: 16, opacity: 0, stagger: 0.08, duration: 0.5 },
        "-=0.5",
      )
      .from(
        copy.querySelectorAll(".home-hero__actions a"),
        { y: 16, opacity: 0, stagger: 0.08, duration: 0.5 },
        "-=0.4",
      )
  }

  // (2) ScrollTrigger — hero 離開 viewport 時整體淡出
  const st = ScrollTrigger.create({
    trigger: host,
    start: "top top",
    end: "bottom top",
    scrub: 0.5,
    animation: gsap.to(host, { opacity: 0.35, y: -40, ease: "none" }),
  })
  scrollTriggers.push(st)

  // (3) Stats count-up (spec §5.1 + §8.2)
  // 手機不跑 — 上面 mobileGate 已把整個 heroCinematic return 掉，手機會
  // 看到 SSR printed 的數字（靜態最終值），符合 spec §8.2「直接顯示最終值」。
  // 桌機才會走到這；ScrollTrigger 觸發、stats strip 進入 viewport 時啟動。
  {
    const targets = document.querySelectorAll<HTMLElement>(
      ".home-stats-strip__value[data-count-to]",
    )
    targets.forEach((el) => {
      const target = Number(el.dataset.countTo ?? "0")
      if (!Number.isFinite(target) || target <= 0) return

      // code-reviewer S2：stats 已滾過 viewport（例：SPA back 到已讀過的首頁、
      // 或 GSAP 載入慢）→ ScrollTrigger once+refresh 會補觸發 onEnter，但
      // 動畫視覺上會是「閃爍回 0 再跳回 target」，UX 破壞。先檢查 bounding
      // rect，若已滾過就直接設最終值，跳過動畫。
      const rect = el.getBoundingClientRect()
      if (rect.bottom < 0) {
        el.textContent = String(target)
        return
      }

      // code-reviewer S10：SSR 時 el.textContent 是 target（HomeLanding 印的），
      // 若讓 gsap.to 從 val=0 開始會產生「6 → 0 → 6」閃爍。動畫啟動前先把
      // 文字歸零，避免使用者看到突然跳回 0。
      el.textContent = "0"

      const counterObj = { val: 0 }
      const counterST = ScrollTrigger.create({
        trigger: el,
        start: "top 85%",
        once: true,
        onEnter: () => {
          gsap.to(counterObj, {
            val: target,
            duration: 1.2,
            ease: APPLE_EASE,
            onUpdate: () => {
              el.textContent = String(Math.round(counterObj.val))
            },
          })
        },
      })
      scrollTriggers.push(counterST)
    })
  }

  // refresh 一次讓 ScrollTrigger 重算 layout（字體已載入）
  ScrollTrigger.refresh()
}

document.addEventListener("nav", setupHeroCinematic)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
