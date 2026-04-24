// Hero focal canvas — spec §5.1 / §7
// 單一 canvas，暖金漸層光暈 + 緩動粒子，scroll 驅動呼吸
// 純 Canvas 2D，無第三方依賴。~3KB gzipped。

declare const window: Window & {
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
  __nav?: { currentGen: () => number }
}

interface Particle {
  x: number
  y: number
  r: number
  vx: number
  vy: number
  alpha: number
  hueShift: number
}

// code-reviewer S3：低電量模式下 loop 用 setTimeout 安排下一幀，此時
// rafId 裡存的是 timeout ID。teardown 不能只呼叫 cancelAnimationFrame，
// 還得 clearTimeout — 分開追蹤兩個 ID 最乾淨。
let rafId = 0
let timeoutId = 0
let resizeObs: ResizeObserver | null = null
let scrollListener: (() => void) | null = null

// FPS 降級 rolling avg（spec §7）
let frameTimes: number[] = []
let lowPowerMode = false
let lastFrame = 0

function setupFocalCanvas() {
  teardown()

  const host = document.querySelector<HTMLElement>("[data-home-hero-focal]")
  if (!host) return  // 目標不存在 → early return
  const canvas = host.querySelector<HTMLCanvasElement>(".home-hero__canvas")
  if (!canvas) return
  const ctx = canvas.getContext("2d")
  if (!ctx) return

  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  const mobile = window.__motion?.isMobileViewport?.() ?? false

  const dpr = mobile ? Math.min(window.devicePixelRatio || 1, 1.5) : window.devicePixelRatio || 1
  let w = 0
  let h = 0

  function resize() {
    const rect = host!.getBoundingClientRect()
    w = Math.max(1, rect.width)
    h = Math.max(1, rect.height)
    canvas!.width = Math.floor(w * dpr)
    canvas!.height = Math.floor(h * dpr)
    canvas!.style.width = `${w}px`
    canvas!.style.height = `${h}px`
    ctx!.scale(dpr, dpr)
  }
  resize()

  // spec §5.1: 「暖金漸層光暈 + 緩動粒子」
  const particleCount = mobile ? 18 : 40
  const particles: Particle[] = []
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 1 + Math.random() * 2.2,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      alpha: 0.35 + Math.random() * 0.35,
      hueShift: Math.random() * 20 - 10,
    })
  }

  let scrollProgress = 0   // 0-1，spec §5.1 "隨 scroll 呼吸"
  scrollListener = () => {
    const max = window.innerHeight * 1.2
    scrollProgress = Math.min(1, Math.max(0, window.scrollY / max))
  }
  window.addEventListener("scroll", scrollListener, { passive: true })

  function drawFrame(t: number) {
    // FPS rolling avg 降級（spec §7：30-frame avg > 22ms 則切 low-power）
    if (lastFrame > 0) {
      const dt = t - lastFrame
      frameTimes.push(dt)
      if (frameTimes.length > 30) frameTimes.shift()
      if (frameTimes.length === 30) {
        const avg = frameTimes.reduce((a, b) => a + b, 0) / 30
        if (avg > 22 && !lowPowerMode) {
          lowPowerMode = true
        }
      }
    }
    lastFrame = t

    ctx!.clearRect(0, 0, w, h)

    // 漸層光暈（中心 → 邊緣 fade），暖金色
    const cx = w * (0.52 + 0.04 * Math.sin(t * 0.0006))
    const cy = h * (0.5 + 0.03 * Math.cos(t * 0.0005) + scrollProgress * 0.08)
    const rMax = Math.hypot(w, h) * 0.7
    const grad = ctx!.createRadialGradient(cx, cy, 0, cx, cy, rMax)
    grad.addColorStop(0, `rgba(200, 169, 107, ${0.42 - scrollProgress * 0.2})`)
    grad.addColorStop(0.35, `rgba(200, 169, 107, ${0.2 - scrollProgress * 0.1})`)
    grad.addColorStop(1, "rgba(200, 169, 107, 0)")
    ctx!.fillStyle = grad
    ctx!.fillRect(0, 0, w, h)

    // 粒子
    for (const p of particles) {
      p.x += p.vx
      p.y += p.vy
      if (p.x < 0 || p.x > w) p.vx *= -1
      if (p.y < 0 || p.y > h) p.vy *= -1
      ctx!.beginPath()
      ctx!.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx!.fillStyle = `rgba(255, 247, 234, ${p.alpha * (1 - scrollProgress * 0.4)})`
      ctx!.fill()
    }
  }

  function loop(t: number) {
    if (document.hidden) {
      rafId = requestAnimationFrame(loop)
      return
    }
    drawFrame(t)
    if (lowPowerMode) {
      // 30fps fallback — 用 setTimeout 拖到下一個 ~33ms tick，再重新排 rAF
      timeoutId = window.setTimeout(() => {
        timeoutId = 0
        rafId = requestAnimationFrame(loop)
      }, 33)
    } else {
      rafId = requestAnimationFrame(loop)
    }
  }

  // Reduced-motion：只畫第一幀（spec §8.1）
  if (reduced) {
    drawFrame(0)
    return
  }

  // 先畫第一幀（LCP 之前），再啟動 rAF
  drawFrame(0)

  // spec §9.5: 延後到 LCP 後才啟動 rAF loop
  const startLoop = () => {
    lastFrame = performance.now()
    rafId = requestAnimationFrame(loop)
  }
  if ("PerformanceObserver" in window) {
    try {
      new PerformanceObserver((list) => {
        if (list.getEntries().some((e) => e.entryType === "largest-contentful-paint")) {
          startLoop()
        }
      }).observe({ type: "largest-contentful-paint", buffered: true })
    } catch {
      setTimeout(startLoop, 350)
    }
  } else {
    setTimeout(startLoop, 350)
  }

  // ResizeObserver：容器尺寸改變時重新 layout
  resizeObs = new ResizeObserver(() => resize())
  resizeObs.observe(host)

  // visibilitychange：隱藏 tab 時已在 loop 內 guard，不需額外 listener
}

function teardown() {
  cancelAnimationFrame(rafId)
  rafId = 0
  if (timeoutId) {
    clearTimeout(timeoutId)  // low-power fallback 可能 pending 中
    timeoutId = 0
  }
  resizeObs?.disconnect()
  resizeObs = null
  if (scrollListener) {
    window.removeEventListener("scroll", scrollListener)
    scrollListener = null
  }
  frameTimes = []
  lowPowerMode = false
  lastFrame = 0
}

document.addEventListener("nav", setupFocalCanvas)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
