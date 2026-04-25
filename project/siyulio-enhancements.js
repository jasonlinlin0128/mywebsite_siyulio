// Sitewide enhancements: reading progress bar + keyboard shortcuts + theme toggle
// Drop into any siyulio page via <script src="siyulio-enhancements.js"></script>
(function() {
  // === Reading progress bar ===
  const bar = document.createElement('div');
  bar.style.cssText = 'position:fixed;top:0;left:0;height:2px;width:0%;background:linear-gradient(90deg,oklch(0.82 0.13 75),oklch(0.86 0.13 90));box-shadow:0 0 8px oklch(0.82 0.13 75);z-index:9998;transition:width .12s linear;pointer-events:none';
  document.addEventListener('DOMContentLoaded', () => document.body.appendChild(bar));
  const updateBar = () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const pct = h > 0 ? (window.scrollY / h) * 100 : 0;
    bar.style.width = Math.min(100, pct) + '%';
  };
  window.addEventListener('scroll', updateBar, { passive: true });
  window.addEventListener('resize', updateBar);

  // === Keyboard shortcuts ===
  const routes = {
    g: 'siyulio-final.html', m: 'siyulio-mfg.html', a: 'siyulio-ai-notes.html',
    c: 'siyulio-coffee.html', p: 'siyulio-about.html', s: 'siyulio-sitemap.html'
  };
  document.addEventListener('keydown', (e) => {
    const tag = (document.activeElement?.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (routes[e.key]) { window.location.href = routes[e.key]; }
    else if (e.key === 'j') { window.scrollBy({ top: 320, behavior: 'smooth' }); }
    else if (e.key === 'k') { window.scrollBy({ top: -320, behavior: 'smooth' }); }
  });

  // === Hint pill ===
  document.addEventListener('DOMContentLoaded', () => {
    const hint = document.createElement('button');
    hint.textContent = '?';
    hint.title = 'Press G / M / A / C / P / S to navigate · J / K to scroll';
    hint.style.cssText = 'position:fixed;bottom:24px;left:24px;z-index:100;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.12);color:oklch(0.82 0.13 75);font-family:JetBrains Mono,monospace;font-size:14px;font-weight:600;cursor:pointer;backdrop-filter:blur(8px)';
    document.body.appendChild(hint);
  });
})();
