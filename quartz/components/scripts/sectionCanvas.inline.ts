// Section-themed canvas renderer (spec §7 / §4.4)
// Phase 2: dormant — 只暴露 API surface，無 DOM target
// Phase 3: ArticleHero 會在 nav 事件呼叫 window.__sectionCanvas.render(el, config)
//         來繪製 geometric-lines / particle-flow / steam-curves 其中一種視覺
//
// 為什麼 Phase 2 就建檔：spec §10 Phase 2 commit 2 要求「focal canvas +
// sectionCanvas 繪製器」同 commit 進 repo，避免 Phase 3 一次要 review 太多
// canvas 邏輯。此 commit 後 window.__sectionCanvas API 已可呼叫（renderer
// 回傳 no-op 處理函數），不破壞任何現有行為。

export type SectionCanvasRenderer = "geometric-lines" | "particle-flow" | "steam-curves"

export interface SectionCanvasConfig {
  renderer: SectionCanvasRenderer
  glowColor: string          // rgba / hex，Phase 3 由 sectionThemes.motionConfig.glowColorDark/Light 傳入
  particleDensity: number
}

declare const window: Window & {
  __sectionCanvas?: {
    render: (host: HTMLElement, config: SectionCanvasConfig) => () => void
  }
}

// Phase 2 dormant stub — 三個 renderer 的具體繪製邏輯在 Phase 3 實作，
// 現階段只保證 API 存在且 cleanup 函數可呼叫。Phase 3 會覆寫這些函數體。
function renderGeometricLines(
  _ctx: CanvasRenderingContext2D,
  _w: number,
  _h: number,
  _config: SectionCanvasConfig,
): void {
  // Phase 3: 等距幾何線條（manufacturing-ai 主題）
}

function renderParticleFlow(
  _ctx: CanvasRenderingContext2D,
  _w: number,
  _h: number,
  _config: SectionCanvasConfig,
): void {
  // Phase 3: 粒子流（ai-notes 主題）
}

function renderSteamCurves(
  _ctx: CanvasRenderingContext2D,
  _w: number,
  _h: number,
  _config: SectionCanvasConfig,
): void {
  // Phase 3: 蒸氣曲線 + 光斑（coffee 主題）
}

const renderers = {
  "geometric-lines": renderGeometricLines,
  "particle-flow": renderParticleFlow,
  "steam-curves": renderSteamCurves,
}

/**
 * Phase 3 API — 呼叫此函數附加 canvas 繪製到指定 host element。
 * 回傳 cleanup 函數讓呼叫方在 prenav / teardown 時反註冊。
 * Phase 2 dormant：回傳的函數可安全呼叫（no-op）。
 */
function render(host: HTMLElement, config: SectionCanvasConfig): () => void {
  // Phase 3 實作大綱（目前不執行）：
  // 1. 找 host 裡的 canvas 或創一個
  // 2. resize to host bounding rect × dpr
  // 3. setInterval 或 rAF 呼叫 renderers[config.renderer]
  // 4. 回傳 cleanup
  void host
  void config
  void renderers
  return () => {
    /* Phase 3 會填 teardown；Phase 2 no-op */
  }
}

window.__sectionCanvas = { render }
