// particle-field.js — full-viewport gold particle field with mouse repulsion
// Plain vanilla JS, no framework. Auto-mounts on DOMContentLoaded.
// Scales to devicePixelRatio. Particles drift slowly and scatter on mouse approach.

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
      density:      0.00011,   // particles per px²
      maxRadius:    2.6,
      minRadius:    0.8,
      baseAlpha:    0.6,
      mouseRadius:  180,       // influence range (px)
      pushStrength: 60,        // max displacement at cursor centre
      returnEase:   0.018,     // spring-back speed (lower = floatier)
      color:        '232, 200, 120',
    };

    let W = 0, H = 0;
    const mouse = { x: -9999, y: -9999, active: false };
    let particles = [];

    function resize() {
      W = window.innerWidth;
      H = window.innerHeight;
      canvas.width  = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width  = W + 'px';
      canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    }

    function seed() {
      const count = Math.round(W * H * config.density);
      particles = Array.from({ length: count }, () => {
        const r = config.minRadius + Math.random() * (config.maxRadius - config.minRadius);
        return {
          ox: Math.random() * W,
          oy: Math.random() * H,
          x: 0, y: 0,
          vx: 0, vy: 0,
          r,
          a: config.baseAlpha * (0.4 + Math.random() * 0.6),
          phase: Math.random() * Math.PI * 2,
        };
      });
      particles.forEach(p => { p.x = p.ox; p.y = p.oy; });
    }

    function step(t) {
      ctx.clearRect(0, 0, W, H);

      const mr  = config.mouseRadius;
      const mr2 = mr * mr;

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Ambient drift (Lissajous-like)
        const driftX = Math.cos(t * 0.0003  + p.phase) * 6;
        const driftY = Math.sin(t * 0.00025 + p.phase * 1.3) * 6;
        const tx = p.ox + driftX;
        const ty = p.oy + driftY;

        // Mouse repulsion
        if (mouse.active) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < mr2 && d2 > 0.5) {
            const d     = Math.sqrt(d2);
            const force = (1 - d / mr) * config.pushStrength;
            p.vx += (dx / d) * force * 0.32;
            p.vy += (dy / d) * force * 0.32;
          }
        }

        // Spring back + integrate
        p.vx += (tx - p.x) * config.returnEase;
        p.vy += (ty - p.y) * config.returnEase;
        p.vx *= 0.92;
        p.vy *= 0.92;
        p.x  += p.vx;
        p.y  += p.vy;

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
      mouse.x = -9999;
      mouse.y = -9999;
    }

    window.addEventListener('resize',     resize);
    window.addEventListener('mousemove',  onMove);
    window.addEventListener('touchmove',  onMove, { passive: true });
    window.addEventListener('mouseleave', onLeave);
    window.addEventListener('blur',       onLeave);

    resize();
    requestAnimationFrame(step);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
