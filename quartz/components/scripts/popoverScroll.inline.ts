// Popover 預覽自動 scroll 過 hero（spec §6.3 Phase 3）
// 配 _popover-immersive.scss（Phase 1 已就位 dormant，Phase 3 ArticleHero
// 進 layout 後 CSS 自動匹配）。本 script 主動把 popover 內容滾到第一個
// 有意義的元素，避免 popover 開出來只看到隱藏 hero 留下的空白頂端。
//
// 為什麼不直接改 upstream popover.inline.ts：避免未來 Quartz 升級需
// re-apply patch（spec §6.3 v3 決策）。

let mo: MutationObserver | null = null

function setupPopoverScroll() {
  mo?.disconnect()
  mo = new MutationObserver((mutations) => {
    for (const m of mutations) {
      for (const node of Array.from(m.addedNodes)) {
        if (!(node instanceof HTMLElement)) continue
        // popover.inline.ts upstream 把 popover-inner 包在 popover 容器裡，
        // 但插入順序取決於版本。同時檢查 node 自己是 .popover-inner 與
        // node 內含 .popover-inner，二擇一覆蓋兩種插法。
        const inner =
          node.classList.contains("popover-inner")
            ? node
            : node.querySelector?.<HTMLElement>(".popover-inner")
        if (!inner) continue

        requestAnimationFrame(() => {
          const firstContent = inner.querySelector<HTMLElement>(
            "p, h2, h3, pre, ul, ol",
          )
          if (!firstContent) return
          const offset = firstContent.offsetTop - 20
          if (offset > 0) inner.scrollTop = offset
        })
      }
    }
  })
  mo.observe(document.body, { childList: true, subtree: true })
}

function teardown() {
  mo?.disconnect()
  mo = null
}

document.addEventListener("nav", setupPopoverScroll)
document.addEventListener("prenav", teardown)
window.addEventListener("beforeunload", teardown)
