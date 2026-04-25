import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug } from "../util/path"
import { getSectionThemeForSlug } from "./sectionThemes"

/**
 * CategoryHero — 分類頁 75vh hero（spec §5.2）
 * 取代 BrandIntro。內容主要從 sectionThemes 取，scene 物件由
 * categoryScene.inline.ts 用 GSAP ScrollTrigger 動畫。
 *
 * 註：不重用 data-hero-cinematic 屬性 — Phase 2 heroCinematic.inline.ts
 * 用 querySelector("[data-hero-cinematic]") 抓 host，若這裡也設此屬性
 * 會被誤抓並對整個 hero 套 home hero 的 fade-out scrub。Task 5 的
 * categoryScene.inline.ts 用 .category-hero class 直接抓 host。
 */
export default (() => {
  const CategoryHero: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const slug = fileData.slug ?? ("index" as FullSlug)
    const theme = getSectionThemeForSlug(slug)

    if (!theme) return null

    return (
      <header class="category-hero" data-section-theme={theme.key}>
        <div class="category-hero__copy">
          <p class="category-hero__eyebrow">{theme.label}</p>
          <h1 class="category-hero__title">{theme.title}</h1>
          <p class="category-hero__copy-text">{theme.copy}</p>
        </div>
        <div
          class="category-hero__stage"
          data-category-scene="true"
          aria-hidden="true"
          role="presentation"
        >
          {theme.sceneObjects.map((object, index) => (
            <span
              class="category-scene-object"
              data-variant={object.variant}
              data-index={index}
              data-origin-x={object.x}
              data-origin-y={object.y}
              data-depth={object.depth}
              style={`--x: ${object.x}%; --y: ${object.y}%; --size: ${object.size}px; --rotate: ${object.rotate}deg;`}
            />
          ))}
        </div>
      </header>
    )
  }

  return CategoryHero
}) satisfies QuartzComponentConstructor
