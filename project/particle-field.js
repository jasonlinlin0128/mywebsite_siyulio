// particle-field.js — full-viewport gold particle field with mouse repulsion
// Plain vanilla JS, no React. Drop a <canvas id="particle-field"> wherever.
// Auto-mounts on DOMContentLoaded; scales to devicePixelRatio.

(function () {
  function init() {
    let canvas = document.getElementById('particle-field');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'particle-field';
      canvas.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;z-index:0;pointer-events:none;';
      document.body.insertBefore(canvas, document.body.firstChild);
    }
    const ctx = canvas.getContext('2d');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const config = {
      density: 0.00011,    // particles per px²
      maxRadius: 2.6,
      minRadius: 0.8,
      baseAlpha: 0.6,
      mouseRadius: 180,    // px – influence range
      pushStrength: 60,    // px – max displacement at center
      returnEase: 0.018,   // 0..1 – slower spring back (antigravity-like)
      driftSpeed: 0.08,
      color: '232, 200, 120',
    };

    let W = 0, H = 0;
    const mouse = { x: -9999, y: -9999, active: false };
    let particles = [];

    function resize() {
      W = window.innerWidth;
      H = window.innerHeight;
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width = W + 'px';
      canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    }

    function seed() {
      const count = Math.round(W * H * config.density);
      particles = new Array(count).fill(0).map(() => {
        const r = config.minRadius + Math.random() * (config.maxRadius - config.minRadius);
        return {
          ox: Math.random() * W,        // origin (where it wants to be)
          oy: Math.random() * H,
          x: 0, y: 0,                   // current
          vx: 0, vy: 0,                 // velocity
          r,
          a: config.baseAlpha * (0.4 + Math.random() * 0.6),
          phase: Math.random() * Math.PI * 2, // for drift
        };
      });
      // initialize current pos = origin
      particles.forEach(p => { p.x = p.ox; p.y = p.oy; });
    }

    function step(t) {
      ctx.clearRect(0, 0, W, H);

      const mr = config.mouseRadius;
      const mr2 = mr * mr;

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Ambient slow drift around origin (Lissajous-ish)
        const driftX = Math.cos(t * 0.0003 + p.phase) * 6;
        const driftY = Math.sin(t * 0.00025 + p.phase * 1.3) * 6;
        const targetX = p.ox + driftX;
        const targetY = p.oy + driftY;

        // Mouse repulsion
        if (mouse.active) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < mr2 && d2 > 0.5) {
            const d = Math.sqrt(d2);
            const force = (1 - d / mr) * config.pushStrength;
            const nx = dx / d;
            const ny = dy / d;
            p.vx += nx * force * 0.32;
            p.vy += ny * force * 0.32;
          }
        }

        // Spring back to drifted target
        p.vx += (targetX - p.x) * config.returnEase;
        p.vy += (targetY - p.y) * config.returnEase;

        // Damping (lower = floatier, glides longer)
        p.vx *= 0.92;
        p.vy *= 0.92;

        p.x += p.vx;
        p.y += p.vy;

        // Draw
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${config.color}, ${p.a})`;
        ctx.fill();
      }

      requestAnimationFrame(step);
    }

    function onMove(e) {
      const t = e.touches ? e.touches[0] : e;
      mouse.x = t.clientX;
      mouse.y = t.clientY;
      mouse.active = true;
    }
    function onLeave() {
      mouse.active = false;
      mouse.x = -9999; mouse.y = -9999;
    }

    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('touchmove', onMove, { passive: true });
    window.addEventListener('mouseleave', onLeave);
    window.addEventListener('blur', onLeave);

    resize();
    requestAnimationFrame(step);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
