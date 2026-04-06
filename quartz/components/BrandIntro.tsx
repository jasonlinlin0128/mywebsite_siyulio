import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"

function sectionLabel(slug: string) {
  if (slug.startsWith("prompts/")) return "Prompts"
  if (slug.startsWith("work-notes/")) return "工作心得"
  if (slug.startsWith("interests-reading/")) return "興趣 / 閱讀"
  if (slug.startsWith("favorite-articles/")) return "喜好文章"
  if (slug.startsWith("obsidian-notes/")) return "Obsidian 筆記"
  if (slug.startsWith("Projects/")) return "Obsidian 筆記"
  if (slug.startsWith("tags/")) return "Tags"
  return "Section"
}

export default (() => {
  function BrandIntro({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const current = slug.replace(/\/index$/, "").replace(/\.md$/, "")

    return (
      <section class="brand-intro">
        <div class="brand-intro__identity">
          <div class="brand-intro__mark">JL</div>
          <div>
            <p class="brand-intro__eyebrow">Jason Lin / siyulio</p>
            <h2 class="brand-intro__title">在傳統製造業落地 AI，也把工具與知識整理成能實際使用的方法。</h2>
          </div>
        </div>
        <p class="brand-intro__copy">
          這裡不只記錄企業導入 AI 的阻力，也會整理我實際在用的工具、Prompts、Obsidian 工作流，以及手沖咖啡和閱讀的生活節奏。
        </p>
        <div class="brand-intro__meta">
          <span>{sectionLabel(slug)}</span>
          <span>{current}</span>
        </div>
        <div class="brand-intro__links">
          <a href={resolveRelative(slug, "index" as FullSlug)}>Home</a>
          <a href={resolveRelative(slug, "work-notes/index" as FullSlug)}>工作心得</a>
          <a href={resolveRelative(slug, "prompts/index" as FullSlug)}>Prompts</a>
          <a href={resolveRelative(slug, "obsidian-notes/index" as FullSlug)}>Obsidian 筆記</a>
        </div>
      </section>
    )
  }

  return BrandIntro
}) satisfies QuartzComponentConstructor
