import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import Head from "./Head"
import { googleFontHref } from "../util/theme"

/**
 * CustomHead — 在 Quartz 預設 Head 之外加 Google Fonts stylesheet preload
 * （spec §3.1）。
 *
 * v3 定案：階段一用 stylesheet preload (as="style")，Google Fonts woff2
 * URL 含 hash 所以不能硬寫個別字重；preload stylesheet 讓瀏覽器早一步
 * 把 CSS 抓下來、早一步發現 font-face src，改善 LCP ~200-400ms。Phase 4
 * audit 若仍未達 LCP < 2.5s，升級到 self-host woff2（寫死 @font-face
 * 指向 static/vendor/fonts/）。
 *
 * 實作方式：**Fragment wrapper**（不碰 Preact VNode internals）。
 * 原 Head 組件照常 render，preload <link> 用 Fragment 放在它**前面**—
 * Preact SSR 會把 Fragment 攤平成連續 HTML，outer layout builder 把整包
 * 塞進 <head>，所以 preload link 會出現在其他 head content 之前。
 * 比 VNode 的 props.children spread 法更穩（不依賴 Preact 內部欄位如 __v
 * / $$typeof，Preact 大版更新不會破）。
 */
export default (() => {
  const BaseHead = Head()

  const CustomHead: QuartzComponent = (props: QuartzComponentProps) => {
    const { cfg } = props
    const shouldPreload =
      cfg.theme.cdnCaching && cfg.theme.fontOrigin === "googleFonts"

    return (
      <>
        {shouldPreload && (
          <link rel="preload" as="style" href={googleFontHref(cfg.theme)} />
        )}
        {(BaseHead as any)(props)}
      </>
    )
  }

  return CustomHead
}) satisfies QuartzComponentConstructor
