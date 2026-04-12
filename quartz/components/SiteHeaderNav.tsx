import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { getSectionStatus, getThemeKeyForSlug, sectionThemes } from "./sectionThemes"

type NavItem = {
  label: string
  href: FullSlug
  key: string
  matches: (slug: string) => boolean
}

const navItems: NavItem[] = sectionThemes.map((theme) => ({
  label: theme.navLabel,
  href: theme.href,
  key: theme.key,
  matches: (slug) => slug.startsWith(theme.slugPrefix),
}))

function currentSection(slug: string) {
  if (slug === "index") return "首頁"
  if (slug.endsWith("/index")) {
    return navItems.find((item) => item.matches(slug))?.label ?? "分類頁"
  }
  return navItems.find((item) => item.matches(slug))?.label ?? "文章"
}

function pageKind(slug: string) {
  if (slug === "index") return "home"
  return slug.endsWith("/index") ? "section" : "article"
}

export default (() => {
  function SiteHeaderNav({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const sectionLabel = currentSection(slug)

    return (
      <div
        class="site-header-nav"
        data-section-theme={getThemeKeyForSlug(slug)}
        data-page-kind={pageKind(slug)}
      >
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
              data-section-theme={item.key}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div class="site-header-nav__status">
          <span>{sectionLabel}</span>
          <span>{getSectionStatus(slug)}</span>
        </div>
      </div>
    )
  }

  return SiteHeaderNav
}) satisfies QuartzComponentConstructor
