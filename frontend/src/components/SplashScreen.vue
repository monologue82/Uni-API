<template>
  <div class="splash" :class="{ 'splash--leaving': leaving }">
    <div class="splash__glow"></div>
    <div ref="container" class="splash__logo"></div>
    <p class="splash__title">Uni-API</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['done'])
const container = ref(null)
const leaving = ref(false)

onMounted(async () => {
  try {
    const res = await fetch('/logo-lines.svg')
    const svgText = await res.text()

    const parser = new DOMParser()
    const svgDoc = parser.parseFromString(svgText, 'image/svg+xml')
    const svgEl = svgDoc.querySelector('svg')

    svgEl.setAttribute('viewBox', '-50 -50 2150 600')
    svgEl.setAttribute('width', '100%')
    svgEl.setAttribute('height', '100%')
    svgEl.setAttribute('preserveAspectRatio', 'xMidYMid meet')

    svgEl.style.visibility = 'hidden'
    container.value.appendChild(svgEl)

    const paths = svgEl.querySelectorAll('path')
    const total = paths.length
    let maxEndTime = 0

    paths.forEach((path, i) => {
      path.style.fill = 'transparent'

      let len
      try { len = path.getTotalLength() } catch { len = 500 }
      if (!len || len < 1) len = 500

      const drawDelay = (i / total) * 1.1
      const drawDuration = 0.6 + Math.random() * 0.3
      const fillDelay = drawDelay + drawDuration + 0.1

      path.style.setProperty('--len', len)
      path.style.setProperty('--dd', `${drawDelay}s`)
      path.style.setProperty('--dur', `${drawDuration}s`)
      path.style.setProperty('--fd', `${fillDelay}s`)

      const end = fillDelay + 0.3
      if (end > maxEndTime) maxEndTime = end
    })

    svgEl.style.visibility = 'visible'

    setTimeout(() => {
      leaving.value = true
      setTimeout(() => emit('done'), 250)
    }, maxEndTime * 1000)
  } catch {
    emit('done')
  }
})
</script>

<style scoped>
.splash {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: #000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: opacity 0.25s ease;
}

.splash--leaving {
  opacity: 0;
  pointer-events: none;
}

.splash__glow {
  position: absolute;
  width: 50%;
  height: 50%;
  background: radial-gradient(ellipse, rgba(255,255,255,0.03) 0%, transparent 70%);
  pointer-events: none;
  animation: glowPulse 1.5s 0.5s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

.splash__logo {
  width: 80vw;
  max-width: 900px;
}

.splash__logo :deep(svg path) {
  stroke: #ffffff;
  stroke-width: 1.5;
  stroke-dasharray: var(--len);
  stroke-dashoffset: var(--len);
  animation:
    drawLine var(--dur) var(--dd) cubic-bezier(0.4, 0, 0.2, 1) forwards,
    fillIn 0.3s var(--fd) ease forwards;
}

@keyframes drawLine {
  to { stroke-dashoffset: 0; }
}

@keyframes fillIn {
  0%   { fill: transparent; }
  100% { fill: #ffffff; }
}

.splash__title {
  color: #fff;
  font-size: 1.2rem;
  font-weight: 300;
  letter-spacing: 0.3em;
  margin-top: 2rem;
  opacity: 0;
  animation: titleFade 0.5s 0.75s ease forwards;
}

@keyframes titleFade {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 0.6; transform: translateY(0); }
}
</style>
