<template>
  <div
      class="loading-content"
      :class="{'absolute-loading': props.absolute,'fixed-loading': !props.absolute}"
      :style="{zIndex: props.index, borderRadius: props.borderRadius}"
  >
    <div>
      <Icon icon="weui:star-outlined" color="#1989FA" style="width: 50px; height: 50px"/>
      <div style="color: #1989FA" class="mt-2">加载中···</div>
    </div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps({
  absolute: {
    type: Boolean,
    default: false
  },
  index: {
    type: Number,
    default: 9999
  },
  borderRadius: {
    type: String,
    default: '0'
  }
})
</script>
<style scoped lang="scss">
.absolute-loading {
  position: absolute;
  width: 100%;
  height: 100%;
}

.fixed-loading {
  position: fixed;
  width: 100vw;
  height: 100vh;
}

.loading-content {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
  // 旋转图标
  svg {
    animation: rotate 1.5s linear infinite;
  }
}

// 定义旋转动画
@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>