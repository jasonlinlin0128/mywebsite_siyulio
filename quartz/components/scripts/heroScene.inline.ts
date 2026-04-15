import { Engine, Runner, Bodies, Body, Composite } from "matter-js"

document.addEventListener("nav", () => {
  const container = document.querySelector("[data-hero-scene='true']") as HTMLElement | null
  if (!container) return

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  const coarsePointer = window.matchMedia("(pointer: coarse)").matches
  const objectEls = [...container.querySelectorAll(".hero-object")] as HTMLElement[]
  if (objectEls.length === 0) return

  if (prefersReducedMotion || coarsePointer) {
    // Static placement: just use CSS left/top set by TSX
    return
  }

  const rect = container.getBoundingClientRect()
  const W = rect.width || window.innerWidth
  const H = rect.height || 500

  // ── Matter.js engine (no gravity) ────────────────────────────────────
  const engine = Engine.create({ gravity: { x: 0, y: 0, scale: 0 } })
  const runner = Runner.create()
  Runner.run(runner, engine)

  // Invisible boundary walls so objects don't escape
  const T = 80
  Composite.add(engine.world, [
    Bodies.rectangle(W / 2, -T / 2, W + T * 2, T, { isStatic: true }),
    Bodies.rectangle(W / 2, H + T / 2, W + T * 2, T, { isStatic: true }),
    Bodies.rectangle(-T / 2, H / 2, T, H + T * 2, { isStatic: true }),
    Bodies.rectangle(W + T / 2, H / 2, T, H + T * 2, { isStatic: true }),
  ])

  interface ObjEntry {
    el: HTMLElement
    body: Matter.Body
    homeX: number
    homeY: number
    halfSize: number
  }

  const objects: ObjEntry[] = objectEls.map((el) => {
    const hxPct = Number(el.dataset.homeX ?? 50)
    const hyPct = Number(el.dataset.homeY ?? 50)
    const sizeVal = Number(el.dataset.size ?? 64)
    const initRotDeg = Number(el.dataset.rotate ?? 0)
    const initRot = (initRotDeg * Math.PI) / 180
    const halfSize = sizeVal / 2
    const homeX = (hxPct / 100) * W
    const homeY = (hyPct / 100) * H

    const body = Bodies.circle(homeX, homeY, halfSize * 0.8, {
      frictionAir: 0.055,
      restitution: 0.6,
      density: 0.0008,
    })
    Body.setAngle(body, initRot)
    Composite.add(engine.world, body)

    // Switch to transform-based positioning (no CSS left/top offset)
    el.style.position = "absolute"
    el.style.left = "0"
    el.style.top = "0"
    el.style.transform = `translate(${(homeX - halfSize).toFixed(2)}px, ${(homeY - halfSize).toFixed(2)}px) rotate(${initRot.toFixed(3)}rad)`

    return { el, body, homeX, homeY, halfSize }
  })

  // ── Mouse tracking ────────────────────────────────────────────────────
  let mouseX = -9999
  let mouseY = -9999

  const onPointerMove = (e: PointerEvent) => {
    const r = container.getBoundingClientRect()
    mouseX = e.clientX - r.left
    mouseY = e.clientY - r.top
  }

  const onPointerLeave = () => {
    mouseX = -9999
    mouseY = -9999
  }

  container.addEventListener("pointermove", onPointerMove)
  container.addEventListener("pointerleave", onPointerLeave)

  // ── RAF render loop ───────────────────────────────────────────────────
  const MOUSE_RADIUS = 150
  const MOUSE_FORCE = 0.0009
  const SPRING_K = 0.000038

  let rafId = 0

  const loop = () => {
    rafId = requestAnimationFrame(loop)

    for (const { el, body, homeX, homeY, halfSize } of objects) {
      // Repulsion from mouse cursor
      const dx = body.position.x - mouseX
      const dy = body.position.y - mouseY
      const dist = Math.hypot(dx, dy)
      if (dist < MOUSE_RADIUS && dist > 1) {
        const f = (1 - dist / MOUSE_RADIUS) * MOUSE_FORCE
        Body.applyForce(body, body.position, {
          x: (dx / dist) * f,
          y: (dy / dist) * f,
        })
      }

      // Gentle spring toward home position
      Body.applyForce(body, body.position, {
        x: (homeX - body.position.x) * SPRING_K,
        y: (homeY - body.position.y) * SPRING_K,
      })

      // Sync DOM element to physics body
      const px = body.position.x - halfSize
      const py = body.position.y - halfSize
      el.style.transform = `translate(${px.toFixed(2)}px,${py.toFixed(2)}px) rotate(${body.angle.toFixed(3)}rad)`
    }
  }

  loop()

  // ── Cleanup on page navigation ────────────────────────────────────────
  window.addCleanup(() => {
    cancelAnimationFrame(rafId)
    Runner.stop(runner)
    Engine.clear(engine)
    Composite.clear(engine.world, false)
    container.removeEventListener("pointermove", onPointerMove)
    container.removeEventListener("pointerleave", onPointerLeave)
  })
})
