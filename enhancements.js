// enhancements.js — siyulio.com production script
// Handles: reading progress bar, glow card/row tracking, custom gold cursor,
//          theme toggle, keyboard navigation, keyboard overlay.

(function () {

  // ── Reading progress bar ──────────────────────────────────────────
  function initProgressBar() {
    const bar = document.createElement('div');
    bar.className = 'reading-progress';
    document.body.prepend(bar);
    function update() {
      const h   = document.documentElement.scrollHeight - window.innerHeight;
      const pct = h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0;
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  // ── Glow card / row tracking (cursor-position → --mx / --my) ─────
  function initGlow() {
    document.querySelectorAll('.card, .row').forEach(el => {
      el.addEventListener('mousemove', function (e) {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top)  + 'px');
      });
    });
  }

  // ── Custom gold cursor (desktop pointer only) ─────────────────────
  function initCursor() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    const ring = Object.assign(document.createElement('div'), { className: 'gold-cursor' });
    const dot  = Object.assign(document.createElement('div'), { className: 'gold-cursor-dot' });
    document.body.append(ring, dot);

    let rx = window.innerWidth / 2, ry = window.innerHeight / 2;
    let dx = rx, dy = ry;

    window.addEventListener('mousemove', function (e) {
      dx = e.clientX;
      dy = e.clientY;
      dot.style.left = dx + 'px';
      dot.style.top  = dy + 'px';
      const interactive = e.target.closest('a, button, .card, .row, input, select, [role="button"]');
      ring.classList.toggle('is-hover', !!interactive);
    });

    window.addEventListener('mouseleave', function () {
      ring.style.opacity = '0';
      dot.style.opacity  = '0';
    });
    window.addEventListener('mouseenter', function () {
      ring.style.opacity = '1';
      dot.style.opacity  = '1';
    });

    (function tick() {
      rx += (dx - rx) * 0.18;
      ry += (dy - ry) * 0.18;
      ring.style.left = rx + 'px';
      ring.style.top  = ry + 'px';
      requestAnimationFrame(tick);
    })();
  }

  // ── Theme toggle ──────────────────────────────────────────────────
  function initTheme() {
    const saved = localStorage.getItem('siyulio-theme') || 'dark';
    if (saved === 'light') document.body.classList.add('theme-light');
    syncThemeIcons();

    document.addEventListener('click', function (e) {
      if (!e.target.closest('[data-theme-toggle]')) return;
      const isLight = document.body.classList.toggle('theme-light');
      localStorage.setItem('siyulio-theme', isLight ? 'light' : 'dark');
      syncThemeIcons();
    });
  }

  function syncThemeIcons() {
    const isLight = document.body.classList.contains('theme-light');
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      const sun  = btn.querySelector('.icon-sun');
      const moon = btn.querySelector('.icon-moon');
      // In dark mode show sun (→ click switches to light); in light show moon (→ switches to dark)
      if (sun)  sun.style.display  = isLight ? 'none'  : 'block';
      if (moon) moon.style.display = isLight ? 'block' : 'none';
      btn.title = isLight ? '切換到深色模式 (T)' : '切換到亮色模式 (T)';
    });
  }

  // ── Keyboard navigation ───────────────────────────────────────────
  const ROUTES = {
    g: 'index.html',
    m: 'siyulio-mfg.html',
    a: 'siyulio-ai-notes.html',
    c: 'siyulio-coffee.html',
    p: 'siyulio-about.html',
    s: 'siyulio-sitemap.html',
  };

  function initKeyboard() {
    window.addEventListener('keydown', function (e) {
      const tag = (document.activeElement && document.activeElement.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      const key = e.key.toLowerCase();

      if (ROUTES[key]) {
        window.location.href = ROUTES[key];
        return;
      }

      switch (key) {
        case 't':
          var btn = document.querySelector('[data-theme-toggle]');
          if (btn) btn.click();
          break;

        case 'j':
          window.scrollBy({ top: 300, behavior: 'smooth' });
          break;

        case 'k':
          window.scrollBy({ top: -300, behavior: 'smooth' });
          break;

        case '?':
        case '/':
          if (key === '/' && !e.shiftKey) break;
          e.preventDefault();
          toggleOverlay();
          break;

        case 'escape':
          closeOverlay();
          break;
      }
    });
  }

  // ── Keyboard overlay ──────────────────────────────────────────────
  function toggleOverlay() {
    var overlay = document.getElementById('kbd-overlay');
    if (!overlay) return;
    var hidden = overlay.style.display === 'none' || overlay.style.display === '';
    overlay.style.display = hidden ? 'flex' : 'none';
  }

  function closeOverlay() {
    var overlay = document.getElementById('kbd-overlay');
    if (overlay) overlay.style.display = 'none';
  }

  function initOverlay() {
    var overlay = document.getElementById('kbd-overlay');
    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeOverlay();
      });
    }
    var hintBtn = document.getElementById('kbd-hint');
    if (hintBtn) {
      hintBtn.addEventListener('click', toggleOverlay);
    }
  }

  // ── Boot ──────────────────────────────────────────────────────────
  function boot() {
    initProgressBar();
    initGlow();
    initCursor();
    initTheme();
    initKeyboard();
    initOverlay();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

})();
