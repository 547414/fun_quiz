<template>
  <div class="soft-glow-background">
    <!-- 背景渐变 -->
    <div class="animated-gradient"></div>

    <!-- 粒子 -->
    <div class="particles">
      <div
        v-for="i in particleCount"
        :key="`particle-${i}`"
        class="particle"
        :style="getParticleStyle(i)"
      ></div>
    </div>

    <!-- 中心扩散光圈 -->
    <div class="glow-circle"></div>
  </div>
</template>

<script setup lang="ts">
const particleCount = 100

const getParticleStyle = (_index: number) => {
  const size = Math.random() * 10 + 6  // 6~16px
  const x = Math.random() * 100
  const y = Math.random() * 100
  const duration = Math.random() * 40 + 40  // ⏳ 40~80s 漂浮
  const delay = Math.random() * 15

  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`
  }
}
</script>

<style lang="scss">
.soft-glow-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

// 🌈 背景渐变（45s 一轮）
.animated-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #dbeafe, #e0e7ff, #f5f3ff, #dbeafe, #e0f2fe);
  background-size: 600% 600%;
  animation: bgShift 45s ease-in-out infinite;
  z-index: 1;
  filter: blur(10px);
  opacity: 0.97;
}

@keyframes bgShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

// 🫧 粒子漂浮（更慢 + 柔和）
.particles {
  position: absolute;
  inset: 0;
  z-index: 2;
}

.particle {
  position: absolute;
  background: radial-gradient(circle, rgba(150, 180, 255, 0.6) 0%, transparent 70%);
  border-radius: 50%;
  animation: float linear infinite, twinkle 8s ease-in-out infinite alternate;
}

@keyframes float {
  0% {
    transform: translateY(100vh) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-10vh) scale(1.2);
    opacity: 0;
  }
}

@keyframes twinkle {
  0% {
    filter: blur(1px);
    opacity: 0.3;
  }
  100% {
    filter: blur(2px);
    opacity: 0.9;
  }
}

// 💫 中心光圈扩散（更大更慢）
.glow-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 480px;
  height: 480px;
  margin-left: -240px;
  margin-top: -240px;
  background: radial-gradient(circle, rgba(200, 220, 255, 0.35) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 20s ease-in-out infinite;
  z-index: 3;
  filter: blur(50px);
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.8);
    opacity: 0.15;
  }
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
}
</style>
