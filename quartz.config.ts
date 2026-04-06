import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "siyulio",
    pageTitleSuffix: " | AI・心得・興趣",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "zh-TW",
    baseUrl: "siyulio.com",
    ignorePatterns: ["private", "templates", "Templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Outfit",
        body: "Noto Sans TC",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#12100d",
          lightgray: "#26211a",
          gray: "#8d7b5f",
          darkgray: "#e9dcc2",
          dark: "#fff7ea",
          secondary: "#c8a96b",
          tertiary: "#f3d79a",
          highlight: "rgba(200, 169, 107, 0.14)",
          textHighlight: "#f3d79a55",
        },
        darkMode: {
          light: "#090806",
          lightgray: "#1a1611",
          gray: "#9a8564",
          darkgray: "#eadfc8",
          dark: "#fff7ea",
          secondary: "#d2b375",
          tertiary: "#f4dda4",
          highlight: "rgba(210, 179, 117, 0.16)",
          textHighlight: "#f4dda455",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      // Disabled for faster local preview builds.
      // Plugin.CustomOgImages(),
    ],
  },
}

export default config
