import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"

/**
 * HomeHeroApple — 首頁 hero 外殼（spec §5.1）
 *
 * 結構：
 *   .home-hero
 *     .home-hero__focal   — 單一 canvas 容器（focalCanvas.inline.ts 會 attach）
 *     .home-hero__copy
 *       .home-hero__eyebrow
 *       h1.home-hero__title     — LCP 候選（128px）
 *       p.home-hero__lead
 *       .home-hero__signals
 *       .home-hero__actions     — 兩顆 CTA
 *
 * 這個組件不自帶 afterDOMLoaded；focal canvas 啟動邏輯走 MotionRuntime
 * 裡的 focalCanvas.inline.ts（Task 2 建立），透過 `[data-home-hero-focal]`
 * 屬性 DOM lookup。heroCinematic（GSAP timeline）走同樣 pattern（Task 9）。
 */
export default (() => {
  function HomeHeroApple({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)

    return (
      <section class="home-hero" data-hero-cinematic="true">
        <div
          class="home-hero__focal"
          data-home-hero-focal="true"
          aria-hidden="true"
        >
          <canvas class="home-hero__canvas" />
        </div>
        <div class="home-hero__copy">
          <p class="home-hero__eyebrow">JASON LIN / AI FIELD NOTES</p>
          <h1 class="home-hero__title">把企業裡真的用得上的 AI，整理成可以開始的做法。</h1>
          <p class="home-hero__lead">
            我在傳統製造業做 AI 落地，橫跨軟體開發與 PM，也是認真對待手沖咖啡的人。
            這裡不是 AI 新聞站，而是一個把現場經驗、工具方法與生活感受慢慢寫清楚的地方。
          </p>
          <div class="home-hero__signals">
            <span>製造業 AI 落地</span>
            <span>AI 工具與方法</span>
            <span>手沖咖啡</span>
          </div>
          <div class="home-hero__actions">
            <a
              class="home-hero__cta home-hero__cta--primary"
              href={resolveRelative(slug, "manufacturing-ai/index" as FullSlug)}
            >
              先看製造業 AI
            </a>
            <a
              class="home-hero__cta"
              href={resolveRelative(slug, "ai-notes/index" as FullSlug)}
            >
              再看 AI 新知
            </a>
          </div>
        </div>
      </section>
    )
  }

  return HomeHeroApple
}) satisfies QuartzComponentConstructor
