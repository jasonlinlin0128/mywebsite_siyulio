import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { formatDate, getDate } from "./Date"
import { getSectionThemeForSlug, sectionThemes } from "./sectionThemes"
import HomeHeroApple from "./HomeHeroApple"

const featuredSlugs = [
  "manufacturing-ai/在傳統製造業導入-AI，最先卡住的不是模型",
  "manufacturing-ai/企業內部推-AI-時，最常見的-5-種阻力",
  "ai-notes/我目前最常用的-AI-工具組合",
  "coffee/泡咖啡這件事，怎麼幫我整理思緒",
] as const

function isRealArticle(page: QuartzPluginData) {
  const slug = page.slug
  return !!slug && slug !== "index" && !slug.endsWith("/index") && !slug.startsWith("tags/")
}

function summarize(page: QuartzPluginData) {
  const fromDescription = page.frontmatter?.description?.trim()
  if (fromDescription) return fromDescription

  const paragraphs =
    page.text
      ?.split(/\n+/)
      .map((line) =>
        line
          .replace(/^#+\s*/, "")
          .replace(/^[-*]\s*/, "")
          .replace(/^\d+\.\s*/, "")
          .replace(/\[\[(.*?)\]\]/g, "$1")
          .replace(/\s+/g, " ")
          .trim(),
      )
      .filter((line) => line.length > 32) ?? []

  const candidate = paragraphs[0] ?? page.description?.trim() ?? page.frontmatter?.title ?? ""
  return candidate.slice(0, 92) + (candidate.length > 92 ? "..." : "")
}

function getDateSafe(page: QuartzPluginData) {
  try {
    return getDate({ defaultDateType: "modified" } as any, page)
  } catch {
    return page.dates?.modified
  }
}

export default (() => {
  const HeroComponent = HomeHeroApple()

  function HomeLanding(props: QuartzComponentProps) {
    const { fileData, allFiles, cfg } = props
    const slug = fileData.slug ?? ("index" as FullSlug)
    const articles = allFiles.filter(isRealArticle)
    const featuredArticles = featuredSlugs
      .map((targetSlug) => articles.find((page) => page.slug === targetSlug))
      .filter((page): page is QuartzPluginData => !!page)
    // 全文章按日期排序，給「最近更新」stat 用（不能排除 featured，否則 stat
    // 會錯把較舊的非-featured 文章當成最後更新）
    const allSortedByDate = [...articles].sort(
      (a, b) => (getDateSafe(b)?.getTime() ?? 0) - (getDateSafe(a)?.getTime() ?? 0),
    )
    // 「繼續閱讀」排除 featured 避免同篇文章在首頁出現兩次（同篇 card UI 重複）
    const featuredSlugSet = new Set(featuredArticles.map((p) => p.slug))
    const recentArticles = allSortedByDate.filter((p) => !featuredSlugSet.has(p.slug)).slice(0, 4)
    const mostRecent = allSortedByDate[0]
    const lastUpdated =
      mostRecent && getDateSafe(mostRecent)
        ? formatDate(getDateSafe(mostRecent)!, cfg.locale)
        : "持續整理中"
    const pillarThemes = sectionThemes.filter((t) => t.key !== "about")

    return (
      <div class="home-landing" data-section-theme="home">
        <HeroComponent {...props} />

        <section class="home-stats-strip" data-reveal>
          <div class="home-stats-strip__item">
            <span class="home-stats-strip__label">目前已發布</span>
            <strong class="home-stats-strip__value" data-count-to={articles.length}>
              {articles.length}
            </strong>
          </div>
          <div class="home-stats-strip__item">
            <span class="home-stats-strip__label">主軸內容</span>
            <strong class="home-stats-strip__value">3 個領域</strong>
          </div>
          <div class="home-stats-strip__item">
            <span class="home-stats-strip__label">最近更新</span>
            <strong class="home-stats-strip__value">{lastUpdated}</strong>
          </div>
        </section>

        <section class="home-pillars">
          {pillarThemes.map((section) => (
            <a
              href={resolveRelative(slug, section.href)}
              class="home-pillars__card"
              data-section-theme={section.key}
              data-reveal
            >
              <p>{section.label}</p>
              <strong>{section.navLabel}</strong>
              <span>{section.description}</span>
              <small>{section.status}</small>
            </a>
          ))}
        </section>

        {featuredArticles.length > 0 && (
          <section class="home-featured">
            {featuredArticles.map((page, index) => {
              const theme = getSectionThemeForSlug(page.slug)
              return (
                <a
                  href={resolveRelative(slug, page.slug! as FullSlug)}
                  class={`home-featured__card ${index === 0 ? "home-featured__card--primary" : ""}`}
                  data-section-theme={theme?.key}
                  data-reveal
                >
                  <p>{theme?.label}</p>
                  <h2>{page.frontmatter?.title}</h2>
                  <span>{summarize(page)}</span>
                </a>
              )
            })}
          </section>
        )}

        <section class="home-recent">
          <header class="home-recent__heading">
            <p>START HERE</p>
            <h2>先從代表文章開始，不需要先把整個網站翻完。</h2>
            <p class="home-recent__copy">
              我把最值得先看的內容直接擺在首頁，第一次進來也能快速抓到重點。
            </p>
          </header>
          <div class="home-recent__list">
            {recentArticles.map((page) => {
              const theme = getSectionThemeForSlug(page.slug)
              const date = getDateSafe(page)
              return (
                <a
                  href={resolveRelative(slug, page.slug! as FullSlug)}
                  class="home-recent__item"
                  data-section-theme={theme?.key}
                  data-reveal
                >
                  <div class="home-recent__meta">
                    <span>{theme?.navLabel}</span>
                    {date ? (
                      <time datetime={date.toISOString()}>{formatDate(date, cfg.locale)}</time>
                    ) : (
                      <time />
                    )}
                  </div>
                  <strong>{page.frontmatter?.title}</strong>
                  <p>{summarize(page)}</p>
                </a>
              )
            })}
          </div>
        </section>
      </div>
    )
  }

  return HomeLanding
}) satisfies QuartzComponentConstructor
