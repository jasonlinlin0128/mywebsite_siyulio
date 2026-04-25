import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { getSectionThemeForSlug } from "./sectionThemes"

/**
 * SectionBadge — section 歸屬小標（spec §4.1 Layer 3）
 * 用在 ArticleHero 內的 hero 角落，連回該 section 入口。
 * 若 slug 對應不到任何 section（例如 about 子頁），回傳 null。
 */
export default (() => {
  const SectionBadge: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const theme = getSectionThemeForSlug(slug)
    if (!theme) return null

    return (
      <a
        class="section-badge"
        href={resolveRelative(slug, theme.href)}
        data-section-theme={theme.key}
      >
        {theme.label}
      </a>
    )
  }

  return SectionBadge
}) satisfies QuartzComponentConstructor
