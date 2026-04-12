function resetObjectField(objects: HTMLElement[]) {
  objects.forEach((object) => {
    object.style.setProperty("--offset-x", "0px")
    object.style.setProperty("--offset-y", "0px")
  })
}

document.addEventListener("nav", () => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  const coarsePointer = window.matchMedia("(pointer: coarse)").matches
  const scenes = [
    ...document.querySelectorAll(".brand-intro__scene[data-scene-interactive='true']"),
  ]

  for (const scene of scenes) {
    const sceneElement = scene as HTMLElement
    const objects = [
      ...sceneElement.querySelectorAll(".brand-object[data-reactive='true']"),
    ] as HTMLElement[]

    if (prefersReducedMotion || coarsePointer || objects.length === 0) {
      resetObjectField(objects)
      continue
    }

    let frame = 0

    const updateField = (clientX: number, clientY: number) => {
      cancelAnimationFrame(frame)
      frame = window.requestAnimationFrame(() => {
        const rect = sceneElement.getBoundingClientRect()
        const radius = Math.max(120, rect.width * 0.24)

        for (const object of objects) {
          const originX = Number(object.dataset.originX ?? 0)
          const originY = Number(object.dataset.originY ?? 0)
          const depth = Number(object.dataset.depth ?? 1)
          const centerX = rect.left + rect.width * (originX / 100)
          const centerY = rect.top + rect.height * (originY / 100)
          const deltaX = centerX - clientX
          const deltaY = centerY - clientY
          const distance = Math.hypot(deltaX, deltaY)
          const force = Math.max(0, radius - distance) / radius
          const multiplier = 24 * depth * force
          const normalizedX = distance === 0 ? 0 : deltaX / distance
          const normalizedY = distance === 0 ? 0 : deltaY / distance

          object.style.setProperty("--offset-x", `${(normalizedX * multiplier).toFixed(2)}px`)
          object.style.setProperty("--offset-y", `${(normalizedY * multiplier).toFixed(2)}px`)
        }
      })
    }

    const onPointerMove = (event: PointerEvent) => {
      updateField(event.clientX, event.clientY)
    }

    const onPointerLeave = () => {
      cancelAnimationFrame(frame)
      resetObjectField(objects)
    }

    sceneElement.addEventListener("pointermove", onPointerMove)
    sceneElement.addEventListener("pointerleave", onPointerLeave)
    window.addCleanup(() => {
      cancelAnimationFrame(frame)
      sceneElement.removeEventListener("pointermove", onPointerMove)
      sceneElement.removeEventListener("pointerleave", onPointerLeave)
      resetObjectField(objects)
    })
  }
})
