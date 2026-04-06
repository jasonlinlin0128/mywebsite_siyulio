import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [Component.SiteHeaderNav()],
  afterBody: [
    Component.ConditionalRender({
      component: Component.RecentNotes({
        title: "Continue Reading",
        limit: 3,
        showTags: false,
        filter: (file) => !!file.slug && file.slug !== "index" && !file.slug.endsWith("/index"),
      }),
      condition: (page) => page.fileData.slug !== "index",
    }),
  ],
  footer: Component.Footer({
    links: {
      Home: "/",
      Prompts: "/prompts/",
      工作心得: "/work-notes/",
      興趣閱讀: "/interests-reading/",
      Obsidian筆記: "/obsidian-notes/",
    },
  }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.BrandIntro(),
      condition: (page) => page.fileData.slug !== "index",
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
  beforeBody: [Component.BrandIntro(), Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [],
  right: [],
}
