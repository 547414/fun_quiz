<template>
  <div
      :class="{ 'absolute' :props.absolute, 'loading-content': !props.absolute }"
      :style="{ zIndex: 9999 }"
  >
    <van-loading vertical custom-style="z-index: 99999">
      <template #icon>
        <van-icon name="star-o" size="30"/>
      </template>
      加载中...
    </van-loading>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  absolute: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped lang="scss">
.loading-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 如果传入 absolute=true，则覆盖为相对父元素定位 */
.absolute {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
