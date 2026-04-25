// Section-themed canvas renderer (spec §7 + §4.4)
// Phase 3 實作版：替換 Phase 2 的 dormant stub。API 簽章不變。
//
// 由 ArticleHero 在 `nav` 事件呼叫：
//   const cleanup = window.__sectionCanvas.render(host, {
//     renderer: 'geometric-lines',
//     glowColor: 'rgba(200,169,107,0.24)',
//     particleDensity: 30,
//   })
// 在 prenav / cleanup 階段呼叫回傳的 cleanup() 釋放 rAF / canvas / listener。

export type SectionCanvasRenderer = "geometric-lines" | "particle-flow" | "steam-curves"

export interface SectionCanvasConfig {
  renderer: SectionCanvasRenderer
  glowColor: string
  particleDensity: number
}

declare const window: Window & {
  __sectionCanvas?: {
    render: (host: HTMLElement, config: SectionCanvasConfig) => () => void
  }
  __motion?: {
    prefersReducedMotion: () => boolean
    isMobileViewport: () => boolean
  }
}

interface RendererFn {
  (ctx: CanvasRenderingContext2D, w: number, h: number, t: number, config: SectionCanvasConfig): void
}

// ── 1. geometric-lines（manufacturing-ai 主題）──────────────────────────────
// 等距斜線 + 反向交叉線 + 中央 radial glow + 線條 shadowBlur 給「光纖」感
function renderGeometricLines(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  config: SectionCanvasConfig,
): void {
  ctx.clearRect(0, 0, w, h)

  // 中央 radial glow 先打底（給線條一個明亮中心對比）
  const cx = w * 0.65
  const cy = h * 0.5
  const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * 0.55)
  grad.addColorStop(0, config.glowColor)
  grad.addColorStop(0.4, config.glowColor.replace(/[\d.]+\)$/, "0.15)"))
  grad.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, w, h)

  // 主對角線（左上 → 右下）+ shadowBlur 給線條 glow
  const spacing = Math.max(56, w / Math.max(8, config.particleDensity))
  const drift = (t * 0.012) % spacing
  ctx.shadowColor = config.glowColor
  ctx.shadowBlur = 8
  ctx.strokeStyle = config.glowColor
  ctx.lineWidth = 1.5
  ctx.lineCap = "round"

  for (let i = -h; i < w + h; i += spacing) {
    ctx.beginPath()
    ctx.moveTo(i + drift, 0)
    ctx.lineTo(i + drift + h, h)
    ctx.stroke()
  }

  // 反向交叉線（右上 → 左下）— 較弱的 alpha 形成編織格紋
  ctx.strokeStyle = config.glowColor.replace(/[\d.]+\)$/, "0.25)")
  ctx.lineWidth = 1
  for (let i = -h; i < w + h; i += spacing * 1.6) {
    ctx.beginPath()
    ctx.moveTo(i + drift + h, 0)
    ctx.lineTo(i + drift, h)
    ctx.stroke()
  }

  ctx.shadowBlur = 0
}

// ── 2. particle-flow（ai-notes 主題）────────────────────────────────────────
const PARTICLE_STATE_KEY = "__pflow"
type ParticleState = {
  particles: Array<{ x: number; y: number; vx: number; vy: number; r: number; alpha: number }>
  initialized: boolean
}

function renderParticleFlow(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  _t: number,
  config: SectionCanvasConfig,
): void {
  const canvas = ctx.canvas as HTMLCanvasElement & { [PARTICLE_STATE_KEY]?: ParticleState }
  let state = canvas[PARTICLE_STATE_KEY]
  if (!state || !state.initialized) {
    const count = config.particleDensity
    state = {
      initialized: true,
      particles: Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: 1.2 + Math.random() * 2.5,
        alpha: 0.5 + Math.random() * 0.5,
      })),
    }
    canvas[PARTICLE_STATE_KEY] = state
  }

  ctx.clearRect(0, 0, w, h)

  // 雙層 radial gradient 背景（取代單一 linear）
  const cx1 = w * 0.3
  const cy1 = h * 0.4
  const grad1 = ctx.createRadialGradient(cx1, cy1, 0, cx1, cy1, Math.max(w, h) * 0.5)
  grad1.addColorStop(0, config.glowColor)
  grad1.addColorStop(0.5, config.glowColor.replace(/[\d.]+\)$/, "0.2)"))
  grad1.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad1
  ctx.fillRect(0, 0, w, h)

  const cx2 = w * 0.7
  const cy2 = h * 0.65
  const grad2 = ctx.createRadialGradient(cx2, cy2, 0, cx2, cy2, Math.max(w, h) * 0.4)
  grad2.addColorStop(0, config.glowColor.replace(/[\d.]+\)$/, "0.4)"))
  grad2.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad2
  ctx.fillRect(0, 0, w, h)

  // 粒子加 glow halo
  ctx.shadowColor = config.glowColor.replace(/[\d.]+\)$/, "0.9)")
  for (const p of state.particles) {
    p.x += p.vx
    p.y += p.vy
    if (p.x < 0 || p.x > w) p.vx *= -1
    if (p.y < 0 || p.y > h) p.vy *= -1
    ctx.shadowBlur = p.r * 4
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(255, 247, 234, ${p.alpha})`
    ctx.fill()
  }
  ctx.shadowBlur = 0
}

// ── 3. steam-curves（coffee 主題）──────────────────────────────────────────
function renderSteamCurves(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  config: SectionCanvasConfig,
): void {
  ctx.clearRect(0, 0, w, h)

  // 暖底光暈（兩層）
  const cx = w * 0.5
  const cy = h * 0.75
  const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * 0.6)
  grad.addColorStop(0, config.glowColor)
  grad.addColorStop(0.4, config.glowColor.replace(/[\d.]+\)$/, "0.18)"))
  grad.addColorStop(1, "rgba(0, 0, 0, 0)")
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, w, h)

  // 蒸氣曲線：N 條 sin wave + shadowBlur 給「光纖蒸氣」感
  const curveCount = Math.max(5, Math.floor(config.particleDensity / 4))
  ctx.shadowColor = config.glowColor.replace(/[\d.]+\)$/, "0.8)")
  ctx.shadowBlur = 12
  ctx.lineCap = "round"

  for (let i = 0; i < curveCount; i++) {
    const phase = (t * 0.0006) + i * 0.7
    const xCenter = w * (0.15 + (i / curveCount) * 0.7)
    const amplitude = 20 + i * 5
    const lineAlpha = 0.85 - i * 0.08
    ctx.strokeStyle = config.glowColor.replace(/[\d.]+\)$/, `${lineAlpha})`)
    ctx.lineWidth = 2 - i * 0.15

    ctx.beginPath()
    for (let y = h; y > 0; y -= 3) {
      const progress = (h - y) / h
      const x = xCenter + Math.sin(progress * Math.PI * 2 + phase) * amplitude * progress
      if (y === h) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.stroke()
  }

  // 細白色高光 spark — 在曲線交織處點綴
  ctx.shadowBlur = 6
  ctx.shadowColor = "rgba(255, 247, 234, 0.6)"
  for (let i = 0; i < 4; i++) {
    const phase = (t * 0.0008) + i * 1.4
    const x = w * (0.25 + (i / 4) * 0.5) + Math.sin(phase) * 30
    const y = h * (0.4 + Math.cos(phase) * 0.2)
    ctx.beginPath()
    ctx.arc(x, y, 1.2, 0, Math.PI * 2)
    ctx.fillStyle = "rgba(255, 247, 234, 0.8)"
    ctx.fill()
  }

  ctx.shadowBlur = 0
}

const renderers: Record<SectionCanvasRenderer, RendererFn> = {
  "geometric-lines": renderGeometricLines,
  "particle-flow": renderParticleFlow,
  "steam-curves": renderSteamCurves,
}

// ── 主渲染函數 ─────────────────────────────────────────────────────────────
function render(host: HTMLElement, config: SectionCanvasConfig): () => void {
  const reduced = window.__motion?.prefersReducedMotion?.() ?? false
  const mobile = window.__motion?.isMobileViewport?.() ?? false

  let canvas = host.querySelector<HTMLCanvasElement>(":scope > canvas")
  if (!canvas) {
    canvas = document.createElement("canvas")
    canvas.setAttribute("aria-hidden", "true")
    canvas.setAttribute("role", "presentation")
    host.appendChild(canvas)
  }
  const ctx = canvas.getContext("2d")
  if (!ctx) return () => {}

  const dpr = mobile ? Math.min(window.devicePixelRatio || 1, 1.5) : window.devicePixelRatio || 1
  let w = 0
  let h = 0
  let resizeObs: ResizeObserver | null = null
  let rafId = 0
  let timeoutId = 0
  let lastFrame = 0
  let frameTimes: number[] = []
  let lowPowerMode = false

  // 先抓 renderer 給 resize() callback 用
  const renderer = renderers[config.renderer]

  function resize() {
    const rect = host.getBoundingClientRect()
    w = Math.max(1, rect.width)
    h = Math.max(1, rect.height)
    canvas!.width = Math.floor(w * dpr)
    canvas!.height = Math.floor(h * dpr)
    canvas!.style.width = `${w}px`
    canvas!.style.height = `${h}px`
    ctx!.scale(dpr, dpr)
    delete (canvas as any)[PARTICLE_STATE_KEY]
    // canvas.width = N 會清空 canvas → 立即重畫一幀避免空白
    // （reduced-motion 路徑沒 rAF loop，不重畫會永遠空白）
    renderer(ctx!, w, h, lastFrame || 0, config)
  }
  resize()

  function loop(t: number) {
    if (document.hidden) {
      rafId = requestAnimationFrame(loop)
      return
    }

    if (lastFrame > 0) {
      const dt = t - lastFrame
      frameTimes.push(dt)
      if (frameTimes.length > 30) frameTimes.shift()
      if (frameTimes.length === 30) {
        const avg = frameTimes.reduce((a, b) => a + b, 0) / 30
        // One-way switch: no hysteresis back to high-power.
        if (avg > 22 && !lowPowerMode) lowPowerMode = true
      }
    }
    lastFrame = t

    renderer(ctx!, w, h, t, config)

    if (lowPowerMode) {
      timeoutId = window.setTimeout(() => {
        timeoutId = 0
        rafId = requestAnimationFrame(loop)
      }, 33)
    } else {
      rafId = requestAnimationFrame(loop)
    }
  }

  if (reduced) {
    renderer(ctx, w, h, 0, config)
  } else {
    renderer(ctx, w, h, 0, config)
    lastFrame = performance.now()
    rafId = requestAnimationFrame(loop)
  }

  resizeObs = new ResizeObserver(() => resize())
  resizeObs.observe(host)

  return () => {
    cancelAnimationFrame(rafId)
    rafId = 0
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = 0
    }
    resizeObs?.disconnect()
    resizeObs = null
    frameTimes = []
    lowPowerMode = false
    lastFrame = 0
    delete (canvas as any)[PARTICLE_STATE_KEY]
  }
}

window.__sectionCanvas = { render }
