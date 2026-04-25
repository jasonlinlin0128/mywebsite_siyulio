import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import { resolveRelative, FullSlug } from "../../util/path"

/**
 * 404 NotFound — Apple 風（spec §5.4）
 * 大字「404」+ 暖光暈 + 兩顆 CTA。覆寫 Quartz upstream 預設版本。
 */
const NotFound: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const slug = fileData.slug ?? ("404" as FullSlug)
  return (
    <section class="not-found" data-section-theme="home">
      <div class="not-found__glow" aria-hidden="true" />
      <div class="not-found__copy">
        <p class="not-found__eyebrow">PAGE NOT FOUND</p>
        <h1 class="not-found__code">404</h1>
        <p class="not-found__lead">這個頁面已經不存在，或從來不曾存在。</p>
        <div class="not-found__actions">
          <a
            class="not-found__cta not-found__cta--primary"
            href={resolveRelative(slug, "" as FullSlug)}
          >
            回首頁
          </a>
          <a
            class="not-found__cta"
            href={resolveRelative(slug, "manufacturing-ai/index" as FullSlug)}
          >
            看製造業 AI
          </a>
        </div>
      </div>
    </section>
  )
}

export default (() => NotFound) satisfies QuartzComponentConstructor
