import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// helpers — frontmatter-aware ConditionalRender 條件
// 用 any 跟既有 layout 風格一致（QuartzComponentProps 從
// "./quartz/components/types" 來，但 ConditionalRender 的 condition
// signature 已 infer，運行時無 type 風險）
const isNonIndex = (page: any) => page.fileData.slug !== "index"
const heroStyleNone = (page: any) =>
  page.fileData.frontmatter?.["hero-style"] === "none"

export const sharedPageComponents: SharedLayout = {
  head: Component.CustomHead(),
  header: [Component.SiteHeaderNav()],
  afterBody: [
    Component.ScrollProgress(),  // Phase 4 — 1px 頂部進度條 (spec §5.3)
    Component.MotionRuntime(),   // 全站 motion 基礎建設 (Phase 1+2+3+4)
    Component.ConditionalRender({
      component: Component.RecentNotes({
        title: "繼續閱讀",
        limit: 3,
        showTags: false,
        filter: (file) => !!file.slug && file.slug !== "index" && !file.slug.endsWith("/index"),
      }),
      condition: (page) => {
        const slug = page.fileData.slug ?? ""
        return slug !== "index" && !slug.endsWith("/index")
      },
    }),
  ],
  footer: Component.Footer({
    links: {
      Home: "/",
      製造業AI: "/manufacturing-ai/",
      AI新知: "/ai-notes/",
      手沖咖啡: "/coffee/",
      個人經歷: "/about/",
    },
  }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    // 首頁：HomeLanding（Phase 2 內部含 HomeHeroApple）
    Component.ConditionalRender({
      component: Component.HomeLanding(),
      condition: (page) => page.fileData.slug === "index",
    }),
    // 非首頁且 hero-style !== "none"：Breadcrumbs + ArticleHero（Phase 3）
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => isNonIndex(page) && !heroStyleNone(page),
    }),
    Component.ConditionalRender({
      component: Component.ArticleHero(),
      condition: (page) => isNonIndex(page) && !heroStyleNone(page),
    }),
    // hero-style: "none" 的頁面走極簡 fallback（Breadcrumbs + 純 ArticleTitle）
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => isNonIndex(page) && heroStyleNone(page),
    }),
    Component.ConditionalRender({
      component: Component.ArticleTitle(),
      condition: (page) => isNonIndex(page) && heroStyleNone(page),
    }),
    // TagList 保留在所有非首頁
    Component.ConditionalRender({
      component: Component.TagList(),
      condition: isNonIndex,
    }),
  ],
  left: [],
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
  ],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.CategoryHero(),   // Phase 3 取代原本的 BrandIntro + ArticleTitle
  ],
  left: [],
  right: [],
}
