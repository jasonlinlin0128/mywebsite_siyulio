import { QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { formatDate, getDate } from "./Date"

type SectionConfig = {
  label: string
  title: string
  href: FullSlug
  slugPrefix: string
  description: string
}

const homeSections: SectionConfig[] = [
  {
    label: "Manufacturing AI",
    title: "製造業 AI 筆記",
    href: "manufacturing-ai/index" as FullSlug,
    slugPrefix: "manufacturing-ai/",
    description: "在傳統製造業推動 AI 落地，真正會卡住的阻力、流程與突破方式。",
  },
  {
    label: "AI Notes",
    title: "AI 新知",
    href: "ai-notes/index" as FullSlug,
    slugPrefix: "ai-notes/",
    description: "深度文章與連結分享並存——工具評析、Prompt 方法與值得留下的 AI 工作流。",
  },
  {
    label: "Hand Drip Coffee",
    title: "手沖咖啡",
    href: "coffee/index" as FullSlug,
    slugPrefix: "coffee/",
    description: "沖煮日誌、器材收藏、咖啡知識與產業觀察。認真喝咖啡的人留下的紀錄。",
  },
  {
    label: "About",
    title: "個人經歷",
    href: "about/index" as FullSlug,
    slugPrefix: "about/",
    description: "工作背景、專案經歷與學習歷程——快速認識 Jason Lin 是誰、在做什麼。",
  },
]

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

  if (fromDescription) {
    return fromDescription
  }

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

function articlesForSection(allFiles: QuartzPluginData[], slugPrefix: string) {
  return allFiles
    .filter((page) => isRealArticle(page) && page.slug!.startsWith(slugPrefix))
    .sort((a, b) => (getDateSafe(b)?.getTime() ?? 0) - (getDateSafe(a)?.getTime() ?? 0))
}

function getDateSafe(page: QuartzPluginData) {
  try {
    return getDate({ defaultDateType: "modified" } as any, page)
  } catch {
    return page.dates?.modified
  }
}

export default (() => {
  function HomeLanding({ fileData, allFiles, cfg }: QuartzComponentProps) {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const articles = allFiles.filter(isRealArticle)
    const recentArticles = [...articles]
      .sort((a, b) => (getDateSafe(b)?.getTime() ?? 0) - (getDateSafe(a)?.getTime() ?? 0))
      .slice(0, 6)
    const featuredArticles = featuredSlugs
      .map((targetSlug) => articles.find((page) => page.slug === targetSlug))
      .filter((page): page is QuartzPluginData => !!page)

    return (
      <section class="home-landing">
        <div class="home-landing__hero">
          <div class="home-landing__copy">
            <p class="home-landing__eyebrow">JASON LIN / AI FIELD NOTES</p>
            <h1>把企業裡真的用得上的 AI，整理成可以開始的做法。</h1>
            <p class="home-landing__lead">
              我在傳統製造業做 AI 落地，橫跨軟體開發與 PM，也是認真對待手沖咖啡的人。
              這裡不是 AI 新聞站，而是一個把現場經驗、工具方法與生活感受慢慢寫清楚的地方。
            </p>
            <div class="home-landing__signals">
              <span>製造業 AI 落地</span>
              <span>AI 工具與方法</span>
              <span>手沖咖啡</span>
            </div>
            <div class="home-landing__actions">
              <a href={resolveRelative(slug, "manufacturing-ai/index" as FullSlug)}>先看製造業 AI</a>
              <a href={resolveRelative(slug, "ai-notes/index" as FullSlug)}>再看 AI 新知</a>
            </div>
          </div>
          <div class="home-landing__summary">
            <div>
              <span>目前已發布</span>
              <strong>{articles.length} 篇文章</strong>
            </div>
            <div>
              <span>主軸內容</span>
              <strong>製造業 AI / AI 工具 / 手沖咖啡</strong>
            </div>
            <div>
              <span>最近更新</span>
              <strong>
                {recentArticles[0] && getDateSafe(recentArticles[0])
                  ? formatDate(getDateSafe(recentArticles[0])!, cfg.locale)
                  : "持續整理中"}
              </strong>
            </div>
          </div>
        </div>

        <div class="home-landing__feature-grid">
          {featuredArticles.map((page, index) => (
            <a
              href={resolveRelative(slug, page.slug! as FullSlug)}
              class={`home-landing__feature-card ${index === 0 ? "is-primary" : ""}`}
            >
              <p>
                {homeSections.find((section) => page.slug!.startsWith(section.slugPrefix))?.label}
              </p>
              <h2>{page.frontmatter?.title}</h2>
              <span>{summarize(page)}</span>
            </a>
          ))}
        </div>

        <section class="home-landing__recent">
          <div class="home-landing__section-heading">
            <div>
              <p class="home-landing__section-label">START HERE</p>
              <h2>先從代表文章開始，不需要先把整個網站翻完。</h2>
              <p class="home-landing__section-copy">
                我把最值得先看的內容直接擺在首頁，第一次進來也能快速抓到重點。
              </p>
            </div>
          </div>
          <div class="home-landing__recent-list">
            {recentArticles.map((page) => (
              <a
                href={resolveRelative(slug, page.slug! as FullSlug)}
                class="home-landing__recent-item"
              >
                <div class="home-landing__recent-meta">
                  <span>
                    {
                      homeSections.find((section) => page.slug!.startsWith(section.slugPrefix))
                        ?.title
                    }
                  </span>
                  <time>{getDateSafe(page) ? formatDate(getDateSafe(page)!, cfg.locale) : ""}</time>
                </div>
                <strong>{page.frontmatter?.title}</strong>
                <p>{summarize(page)}</p>
              </a>
            ))}
          </div>
        </section>

        <section class="home-landing__shelves">
          {homeSections.map((section) => {
            const sectionArticles = articlesForSection(allFiles, section.slugPrefix).slice(0, 2)
            return (
              <div class="home-landing__shelf">
                <div class="home-landing__shelf-intro">
                  <p>{section.label}</p>
                  <h3>{section.title}</h3>
                  <span>{section.description}</span>
                  <a href={resolveRelative(slug, section.href)}>看這個分類</a>
                </div>
                <div class="home-landing__shelf-list">
                  {sectionArticles.map((page) => (
                    <a
                      href={resolveRelative(slug, page.slug! as FullSlug)}
                      class="home-landing__shelf-item"
                    >
                      <strong>{page.frontmatter?.title}</strong>
                      <p>{summarize(page)}</p>
                    </a>
                  ))}
                </div>
              </div>
            )
          })}
        </section>
      </section>
    )
  }

  return HomeLanding
}) satisfies QuartzComponentConstructor
