import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

export const sharedPageComponents: SharedLayout = {
  head: Component.CustomHead(),
  header: [Component.SiteHeaderNav()],
  afterBody: [
    Component.MotionRuntime(),   // 全站 motion 基礎建設 (Phase 1)
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
    Component.ConditionalRender({
      component: Component.HomeLanding(),
      condition: (page) => page.fileData.slug === "index",
    }),
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ConditionalRender({
      component: Component.ArticleTitle(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ConditionalRender({
      component: Component.ContentMeta(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ConditionalRender({
      component: Component.TagList(),
      condition: (page) => page.fileData.slug !== "index",
    }),
  ],
  left: [],
  right: [],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.BrandIntro(), Component.ArticleTitle()],
  left: [],
  right: [],
}
