// @ts-ignore
import sectionSceneScript from "./scripts/sectionScene.inline"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { getSectionThemeForSlug } from "./sectionThemes"

export default (() => {
  const BrandIntro: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    const slug = fileData.slug ?? "index"
    const theme = getSectionThemeForSlug(slug)

    if (!theme) {
      return null
    }

    return (
      <section class="brand-intro brand-intro--section" data-section-theme={theme.key}>
        <div class="brand-intro__content">
          <p class="brand-intro__eyebrow">{theme.label}</p>
          <h2 class="brand-intro__title">{theme.title}</h2>
          <p class="brand-intro__copy">{theme.copy}</p>

          <div class="brand-intro__signal-row">
            {theme.signals.map((signal) => (
              <span>{signal}</span>
            ))}
          </div>
        </div>

        <div
          class="brand-intro__scene"
          data-scene-theme={theme.key}
          data-scene-interactive={theme.sceneInteractive ? "true" : undefined}
        >
          <div class="brand-intro__scene-head">
            <p>{theme.status}</p>
            <span>{theme.sceneIntro}</span>
          </div>

          <div class="brand-intro__object-field" aria-hidden="true">
            {theme.sceneObjects.map((object, index) => (
              <span
                class={`brand-object brand-object--${object.variant}`}
                data-reactive={object.reactive ? "true" : undefined}
                data-origin-x={object.x}
                data-origin-y={object.y}
                data-depth={object.depth}
                style={`--x:${object.x}%; --y:${object.y}%; --size:${object.size}px; --rotate:${object.rotate}deg; --delay:${index * 90}ms;`}
              />
            ))}
          </div>

          <div class="brand-intro__scene-foot">
            <strong>{theme.label}</strong>
            <p>{theme.sceneNote}</p>
          </div>
        </div>
      </section>
    )
  }

  BrandIntro.afterDOMLoaded = sectionSceneScript
  return BrandIntro
}) satisfies QuartzComponentConstructor
