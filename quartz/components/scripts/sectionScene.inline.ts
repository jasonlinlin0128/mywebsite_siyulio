function resetObjectField(objects: HTMLElement[]) {
  objects.forEach((object) => {
    object.style.setProperty("--offset-x", "0px")
    object.style.setProperty("--offset-y", "0px")
  })
}

function resetStageField(items: HTMLElement[]) {
  items.forEach((item) => {
    item.style.setProperty("--stage-offset-x", "0px")
    item.style.setProperty("--stage-offset-y", "0px")
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

  const stages = [...document.querySelectorAll("[data-stage-parallax='true']")]

  for (const stage of stages) {
    const stageElement = stage as HTMLElement
    const items = [...stageElement.querySelectorAll("[data-parallax-depth]")] as HTMLElement[]

    if (prefersReducedMotion || coarsePointer || items.length === 0) {
      resetStageField(items)
      continue
    }

    let frame = 0

    const onPointerMove = (event: PointerEvent) => {
      cancelAnimationFrame(frame)
      frame = window.requestAnimationFrame(() => {
        const rect = stageElement.getBoundingClientRect()
        const centerX = rect.left + rect.width / 2
        const centerY = rect.top + rect.height / 2
        const deltaX = (event.clientX - centerX) / rect.width
        const deltaY = (event.clientY - centerY) / rect.height

        for (const item of items) {
          const depth = Number(item.dataset.parallaxDepth ?? 1)
          item.style.setProperty("--stage-offset-x", `${(deltaX * depth * 24).toFixed(2)}px`)
          item.style.setProperty("--stage-offset-y", `${(deltaY * depth * 24).toFixed(2)}px`)
        }
      })
    }

    const onPointerLeave = () => {
      cancelAnimationFrame(frame)
      resetStageField(items)
    }

    stageElement.addEventListener("pointermove", onPointerMove)
    stageElement.addEventListener("pointerleave", onPointerLeave)
    window.addCleanup(() => {
      cancelAnimationFrame(frame)
      stageElement.removeEventListener("pointermove", onPointerMove)
      stageElement.removeEventListener("pointerleave", onPointerLeave)
      resetStageField(items)
    })
  }
})
