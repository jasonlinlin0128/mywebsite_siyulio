import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"

function currentSection(slug: string) {
  if (slug === "index") return "Home"
  if (slug.startsWith("work-notes/")) return "工作心得"
  if (slug.startsWith("prompts/")) return "Prompts"
  if (slug.startsWith("obsidian-notes/")) return "Obsidian 筆記"
  if (slug.startsWith("interests-reading/")) return "興趣 / 閱讀"
  if (slug.startsWith("favorite-articles/")) return "喜好文章"
  return "Article"
}

export default (() => {
  function SiteHeaderNav({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)

    return (
      <div class="site-header-nav">
        <a class="site-header-nav__brand" href={resolveRelative(slug, "index" as FullSlug)}>
          <span class="site-header-nav__mark">JL</span>
          <span class="site-header-nav__wordmark">
            <strong>siyulio</strong>
            <small>Jason Lin</small>
          </span>
        </a>

        <nav class="site-header-nav__links" aria-label="Primary">
          <a href={resolveRelative(slug, "work-notes/index" as FullSlug)}>工作心得</a>
          <a href={resolveRelative(slug, "prompts/index" as FullSlug)}>Prompts</a>
          <a href={resolveRelative(slug, "obsidian-notes/index" as FullSlug)}>Obsidian 筆記</a>
          <a href={resolveRelative(slug, "interests-reading/index" as FullSlug)}>興趣 / 閱讀</a>
        </nav>

        <div class="site-header-nav__status">
          <span>{currentSection(slug)}</span>
        </div>
      </div>
    )
  }

  return SiteHeaderNav
}) satisfies QuartzComponentConstructor
