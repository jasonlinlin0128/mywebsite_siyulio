import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { Date as DateComp, getDate } from "./Date"
import readingTime from "reading-time"
import { i18n } from "../i18n"
import { getSectionThemeForSlug } from "./sectionThemes"
import SectionBadge from "./SectionBadge"

/**
 * ArticleHero — 文章頁 60vh hero（spec §5.3）
 * 完整取代既有 ArticleTitle + ContentMeta（在 quartz.layout.ts 的 v3 版本中）。
 *
 * Frontmatter 支援：
 *   cover:        URL 或相對路徑 → 取代 canvas 用 <img> 背景
 *   accent:       hex / rgb 字串 → 透過 inline-style 覆蓋 --article-hero-accent
 *   hero-style:   "themed"（預設） | "minimal" | "none"
 *                 "none" 已在 layout 端轉走 ArticleTitle fallback path
 *                 tags/* 與 about/* slug 自動推斷為 minimal（spec §4.3 / §5.4）
 *
 * Canvas 啟動：透過 afterDOMLoaded 注入小段 inline JS，由 nav 事件呼叫
 *   window.__sectionCanvas.render(host, config)，prenav 時呼叫 cleanup。
 *   theme 切換（saved-theme MutationObserver）時重 render 用對應 glow。
 */

const inlineScript = `
(function(){
  let cleanup = null
  let myGen = 0
  function currentGen() { return window.__nav?.currentGen?.() ?? 0 }
  function pickGlow(host) {
    const dark = document.documentElement.getAttribute('saved-theme') !== 'light'
    return dark
      ? (host.dataset.glowColorDark ?? host.dataset.glowColor ?? 'rgba(255,255,255,0.18)')
      : (host.dataset.glowColorLight ?? host.dataset.glowColor ?? 'rgba(0,0,0,0.18)')
  }
  function setup() {
    cleanup?.()
    cleanup = null
    myGen = currentGen()
    const host = document.querySelector('[data-section-hero-canvas]')
    if (!host) return
    if (!window.__sectionCanvas) return
    if (myGen !== currentGen()) return
    const renderer = host.dataset.canvasRenderer
    const density = Number(host.dataset.particleDensity ?? '30')
    if (!renderer) return
    cleanup = window.__sectionCanvas.render(host, {
      renderer,
      glowColor: pickGlow(host),
      particleDensity: Number.isFinite(density) ? density : 30,
    })
  }
  function teardown() {
    cleanup?.()
    cleanup = null
  }
  let themeMo = null
  function watchTheme() {
    themeMo?.disconnect()
    themeMo = new MutationObserver(() => {
      if (cleanup) setup()
    })
    themeMo.observe(document.documentElement, { attributes: true, attributeFilter: ['saved-theme'] })
  }
  document.addEventListener('nav', () => { setup(); watchTheme(); })
  document.addEventListener('prenav', () => { teardown(); themeMo?.disconnect(); themeMo = null })
  window.addEventListener('beforeunload', teardown)
})();
`

// XSS defense: accent / cover 都是 user-controlled string 進 inline style
function sanitizeAccent(value: string): string {
  return value.replace(/[^a-zA-Z0-9#(),.\s%-]/g, "").trim().slice(0, 64)
}

function sanitizeCoverUrl(value: string): string {
  return encodeURI(value.trim()).slice(0, 512)
}

// auto-minimal 推斷規則（spec §4.3 / §5.4）
// Phase 4：about 頁有 cover frontmatter 時走 themed（顯示 portrait card 變體）
function inferHeroStyle(
  slug: string,
  frontmatterValue: string | undefined,
  hasCover: boolean,
): "themed" | "minimal" {
  if (frontmatterValue === "minimal") return "minimal"
  if (slug.startsWith("tags/")) return "minimal"
  if ((slug === "about" || slug.startsWith("about/")) && !hasCover) return "minimal"
  return "themed"
}

export default (() => {
  const Badge = SectionBadge()

  function ArticleHero(props: QuartzComponentProps) {
    const { fileData, cfg } = props
    const slug = fileData.slug ?? "index"
    const title = fileData.frontmatter?.title ?? ""
    const fm = fileData.frontmatter as Record<string, unknown> | undefined
    const coverRaw = typeof fm?.cover === "string" ? fm.cover : undefined
    const accentRaw = typeof fm?.accent === "string" ? fm.accent : undefined
    const heroStyleRaw = typeof fm?.["hero-style"] === "string" ? (fm["hero-style"] as string) : undefined

    const heroStyle = inferHeroStyle(slug, heroStyleRaw, !!coverRaw)
    const cover = coverRaw ? sanitizeCoverUrl(coverRaw) : undefined
    const accent = accentRaw ? sanitizeAccent(accentRaw) : undefined

    const theme = getSectionThemeForSlug(slug)
    const themeKey = theme?.key ?? "about"
    const motionCfg = theme?.motionConfig

    const glowDark = motionCfg?.glowColorDark ?? "rgba(255, 247, 234, 0.18)"
    const glowLight = motionCfg?.glowColorLight ?? "rgba(18, 16, 13, 0.18)"
    const renderer = motionCfg?.canvasRenderer ?? "geometric-lines"
    const density = motionCfg?.particleDensity ?? 30

    const accentStyle = accent ? `--article-hero-accent: ${accent};` : ""

    const text = fileData.text ?? ""
    const minutes = text ? Math.ceil(readingTime(text).minutes) : 0
    const readingLabel =
      minutes > 0 ? i18n(cfg.locale).components.contentMeta.readingTime({ minutes }) : ""

    const badgeNode = Badge(props)

    return (
      <header
        class="article-hero"
        data-section-theme={themeKey}
        data-hero-style={heroStyle}
        data-has-cover={heroStyle === "themed" && cover ? "true" : undefined}
        style={accentStyle}
      >
        {heroStyle === "themed" && cover && (
          <div class="article-hero__cover" style={`background-image: url("${cover}");`} />
        )}
        {heroStyle === "themed" && !cover && (
          <div
            class="article-hero__canvas-host"
            data-section-hero-canvas="true"
            data-canvas-renderer={renderer}
            data-glow-color-dark={glowDark}
            data-glow-color-light={glowLight}
            data-particle-density={String(density)}
            aria-hidden="true"
          />
        )}
        <div class="article-hero__copy">
          {badgeNode}
          <h1 class="article-hero__title">{title}</h1>
          {(fileData.dates || readingLabel) && (
            <p class="article-hero__meta">
              {fileData.dates && <DateComp date={getDate(cfg, fileData)!} locale={cfg.locale} />}
              {readingLabel && <span class="article-hero__reading-time">{readingLabel}</span>}
            </p>
          )}
        </div>
      </header>
    )
  }

  ArticleHero.afterDOMLoaded = inlineScript

  return (() => ArticleHero) satisfies QuartzComponentConstructor
})()
