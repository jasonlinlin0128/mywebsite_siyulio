import { FullSlug } from "../util/path"

export type SectionKey = "home" | "manufacturing-ai" | "ai-notes" | "coffee" | "about"

export type SceneObject = {
  variant: string
  x: number
  y: number
  size: number
  rotate: number
  depth: number
  reactive?: boolean
}

export type SectionTheme = {
  key: Exclude<SectionKey, "home">
  slugPrefix: `${string}/`
  href: FullSlug
  label: string
  navLabel: string
  title: string
  copy: string
  description: string
  status: string
  sceneIntro: string
  sceneNote: string
  signals: string[]
  sceneInteractive: boolean
  sceneObjects: SceneObject[]
}

export const homeTheme = {
  key: "home" as const,
  status: "Curated signal map",
  sceneIntro: "首頁是整站入口，不追求資訊塞滿，而是讓動線更清楚。",
}

export const sectionThemes: SectionTheme[] = [
  {
    key: "manufacturing-ai",
    slugPrefix: "manufacturing-ai/",
    href: "manufacturing-ai/index" as FullSlug,
    label: "Manufacturing AI",
    navLabel: "製造業 AI",
    title: "企業裡推動 AI 的現場筆記",
    copy: "聚焦製造現場裡真正會卡住的流程、阻力與推進方式，讓 AI 不只停在簡報上。",
    description: "落地阻力、流程拆解、協作現場與導入節奏。",
    status: "Factory signal system",
    sceneIntro: "用模組節點和流程脈衝去表現工廠、流程與系統感。",
    sceneNote: "把複雜導入過程拆成能討論、能落地、能持續修正的步驟。",
    signals: ["落地流程", "跨部門協作", "阻力拆解"],
    sceneInteractive: false,
    sceneObjects: [
      { variant: "module", x: 14, y: 22, size: 92, rotate: -6, depth: 0.8 },
      { variant: "ring", x: 48, y: 28, size: 138, rotate: 0, depth: 1 },
      { variant: "node", x: 78, y: 24, size: 56, rotate: 12, depth: 1.2 },
      { variant: "beam", x: 28, y: 70, size: 124, rotate: -10, depth: 0.95 },
      { variant: "module", x: 68, y: 66, size: 104, rotate: 8, depth: 1.15 },
      { variant: "node", x: 86, y: 78, size: 42, rotate: 0, depth: 1.1 },
    ],
  },
  {
    key: "ai-notes",
    slugPrefix: "ai-notes/",
    href: "ai-notes/index" as FullSlug,
    label: "AI Notes",
    navLabel: "AI 新知",
    title: "工具、Prompt 與工作流的新知整理",
    copy: "把真的會反覆使用的 AI 工具、方法與工作流留下來，讓新工具不只停在收藏清單裡。",
    description: "工具評析、Prompt 方法、值得保留的工作流。",
    status: "Prompt signal layer",
    sceneIntro: "以資料流、膠囊訊號和抽象光點建立比較輕的科技節奏。",
    sceneNote: "不是追最新，而是整理出真正會留下來的工具感與使用脈絡。",
    signals: ["工具評析", "Prompt 方法", "工作流整理"],
    sceneInteractive: false,
    sceneObjects: [
      { variant: "pill", x: 18, y: 20, size: 104, rotate: -14, depth: 0.85 },
      { variant: "pulse", x: 44, y: 18, size: 124, rotate: 0, depth: 1.1 },
      { variant: "spark", x: 76, y: 20, size: 64, rotate: 12, depth: 1.05 },
      { variant: "spark", x: 24, y: 52, size: 40, rotate: 0, depth: 0.9 },
      { variant: "pill", x: 58, y: 56, size: 112, rotate: 8, depth: 1.2 },
      { variant: "pulse", x: 80, y: 72, size: 92, rotate: 0, depth: 0.95 },
    ],
  },
  {
    key: "coffee",
    slugPrefix: "coffee/",
    href: "coffee/index" as FullSlug,
    label: "Hand Drip Coffee",
    navLabel: "手沖咖啡",
    title: "把手沖咖啡的節奏，做成這一區自己的場景",
    copy: "這裡會更有材質感、呼吸感，也把咖啡豆作為互動主體，讓分類頁本身就像一個慢下來的入口。",
    description: "沖煮日誌、器材收藏、豆子風味與生活節奏。",
    status: "Coffee motion field",
    sceneIntro: "咖啡豆會因為游標靠近被推開，保留微妙、安靜但有記憶點的互動。",
    sceneNote: "互動只是一種手感，不搶文章內容，讓停留時多一點呼吸與溫度。",
    signals: ["沖煮日誌", "器材與豆子", "節奏感"],
    sceneInteractive: true,
    sceneObjects: [
      { variant: "bean", x: 16, y: 18, size: 68, rotate: -18, depth: 1.1, reactive: true },
      { variant: "bean", x: 36, y: 30, size: 92, rotate: 18, depth: 1.2, reactive: true },
      { variant: "bean", x: 62, y: 18, size: 74, rotate: -10, depth: 0.95, reactive: true },
      { variant: "bean", x: 82, y: 34, size: 88, rotate: 22, depth: 1.05, reactive: true },
      { variant: "bean", x: 22, y: 62, size: 96, rotate: 14, depth: 1.15, reactive: true },
      { variant: "bean", x: 48, y: 58, size: 120, rotate: -12, depth: 1.25, reactive: true },
      { variant: "bean", x: 74, y: 62, size: 82, rotate: 16, depth: 1, reactive: true },
      { variant: "bean", x: 56, y: 82, size: 72, rotate: -20, depth: 0.85, reactive: true },
    ],
  },
  {
    key: "about",
    slugPrefix: "about/",
    href: "about/index" as FullSlug,
    label: "About",
    navLabel: "個人經歷",
    title: "工作背景、專案經歷與學習路徑",
    copy: "把我的工作背景、專案經驗與持續在做的事情收整成一個比較安靜、比較明確的入口。",
    description: "認識 Jason Lin、看過去的路徑，也知道現在在做什麼。",
    status: "Personal orbit",
    sceneIntro: "這區最克制，以 monogram、軌道與留白去撐起辨識度。",
    sceneNote: "把履歷式資訊轉成更像個人品牌檔案的閱讀節奏。",
    signals: ["工作背景", "專案經歷", "現在進行式"],
    sceneInteractive: false,
    sceneObjects: [
      { variant: "orbit", x: 52, y: 50, size: 174, rotate: 0, depth: 1 },
      { variant: "core", x: 52, y: 50, size: 72, rotate: 0, depth: 1.1 },
      { variant: "satellite", x: 22, y: 36, size: 38, rotate: 0, depth: 0.9 },
      { variant: "satellite", x: 78, y: 66, size: 30, rotate: 0, depth: 1.05 },
      { variant: "trace", x: 70, y: 26, size: 96, rotate: 18, depth: 0.8 },
    ],
  },
]

export function getSectionThemeForSlug(slug?: string): SectionTheme | null {
  const resolvedSlug = slug ?? "index"
  return (
    sectionThemes.find(
      (theme) =>
        resolvedSlug.startsWith(theme.slugPrefix) ||
        resolvedSlug === theme.slugPrefix.slice(0, -1) ||
        resolvedSlug === `${theme.slugPrefix}index`,
    ) ?? null
  )
}

export function getThemeKeyForSlug(slug?: string): SectionKey {
  return getSectionThemeForSlug(slug)?.key ?? "home"
}

export function getSectionStatus(slug?: string) {
  return getSectionThemeForSlug(slug)?.status ?? homeTheme.status
}
