import { QuartzComponentConstructor, QuartzComponentProps } from "./types"

type SectionInfo = {
  label: string
  title: string
  copy: string
}

function sectionInfo(slug: string): SectionInfo {
  if (slug.startsWith("prompts/")) {
    return {
      label: "Prompts",
      title: "工具、Prompt 與工作場景整理",
      copy: "把我真的會反覆使用的 AI 工具、Prompts 和工作流程整理成比較容易開始的入口。",
    }
  }

  if (slug.startsWith("work-notes/")) {
    return {
      label: "Work Notes",
      title: "企業裡推動 AI 的現場筆記",
      copy: "記錄傳統製造業導入 AI 時，真正會遇到的阻力、協作問題和推進方式。",
    }
  }

  if (slug.startsWith("obsidian-notes/") || slug.startsWith("Projects/")) {
    return {
      label: "Obsidian Notes",
      title: "知識系統與工作流整理",
      copy: "把專案、會議、工具使用經驗和想法，整理成可以持續維護的 Obsidian 筆記系統。",
    }
  }

  if (slug.startsWith("interests-reading/")) {
    return {
      label: "Interests / Reading",
      title: "咖啡、閱讀與生活感",
      copy: "除了 AI，我也想把手沖咖啡、閱讀和日常裡的節奏感留在這個網站。",
    }
  }

  if (slug.startsWith("favorite-articles/")) {
    return {
      label: "Favorite Articles",
      title: "收藏與再整理",
      copy: "這裡會收我想留下來、也值得再讀一次的文章與延伸觀察。",
    }
  }

  return {
    label: "Section",
    title: "Jason Lin 的內容筆記",
    copy: "把企業 AI 落地、工具整理、知識系統和生活節奏放在同一個內容網站裡。",
  }
}

export default (() => {
  function BrandIntro({ fileData }: QuartzComponentProps) {
    const slug = fileData.slug ?? "index"
    const info = sectionInfo(slug)

    return (
      <section class="brand-intro brand-intro--section">
        <p class="brand-intro__eyebrow">{info.label}</p>
        <h2 class="brand-intro__title">{info.title}</h2>
        <p class="brand-intro__copy">{info.copy}</p>
      </section>
    )
  }

  return BrandIntro
}) satisfies QuartzComponentConstructor
