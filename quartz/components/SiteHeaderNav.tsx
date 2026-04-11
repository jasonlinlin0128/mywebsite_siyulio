import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"

type NavItem = {
  label: string
  href: FullSlug
  matches: (slug: string) => boolean
}

const navItems: NavItem[] = [
  {
    label: "製造業 AI",
    href: "manufacturing-ai/index" as FullSlug,
    matches: (slug) => slug.startsWith("manufacturing-ai/"),
  },
  {
    label: "AI 新知",
    href: "ai-notes/index" as FullSlug,
    matches: (slug) => slug.startsWith("ai-notes/"),
  },
  {
    label: "手沖咖啡",
    href: "coffee/index" as FullSlug,
    matches: (slug) => slug.startsWith("coffee/"),
  },
  {
    label: "個人經歷",
    href: "about/index" as FullSlug,
    matches: (slug) => slug.startsWith("about/"),
  },
]

function currentSection(slug: string) {
  if (slug === "index") return "首頁"
  if (slug.endsWith("/index")) {
    return navItems.find((item) => item.matches(slug))?.label ?? "分類頁"
  }
  return navItems.find((item) => item.matches(slug))?.label ?? "文章"
}

export default (() => {
  function SiteHeaderNav({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const sectionLabel = currentSection(slug)

    return (
      <div class="site-header-nav">
        <a class="site-header-nav__brand" href={resolveRelative(slug, "index" as FullSlug)}>
          <span class="site-header-nav__mark">JL</span>
          <span class="site-header-nav__wordmark">
            <strong>siyulio</strong>
            <small>AI field notes by Jason Lin</small>
          </span>
        </a>

        <nav class="site-header-nav__links" aria-label="Primary">
          {navItems.map((item) => (
            <a
              href={resolveRelative(slug, item.href)}
              data-active={item.matches(slug) ? "true" : undefined}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div class="site-header-nav__status">
          <span>{sectionLabel}</span>
          <span>更新中的內容花園</span>
        </div>
      </div>
    )
  }

  return SiteHeaderNav
}) satisfies QuartzComponentConstructor
