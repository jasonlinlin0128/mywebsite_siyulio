import { QuartzComponent, QuartzComponentConstructor } from "./types"

/**
 * ScrollProgress — 1px 頂部進度條（spec §5.3）
 * Width 由 CSS var --scroll-progress（0-1）控制，inline script 寫入。
 * aria-hidden 因為純 visual feedback（spec §8.5）。
 */
const ScrollProgress: QuartzComponent = () => {
  return <div class="scroll-progress" aria-hidden="true" />
}

export default (() => ScrollProgress) satisfies QuartzComponentConstructor
