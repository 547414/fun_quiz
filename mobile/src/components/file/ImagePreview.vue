<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="visible" class="custom-image-preview" @click="handleClose">
        <!-- 遮罩层 -->
        <div class="preview-overlay"></div>

        <!-- 图片容器 -->
        <div class="preview-container" @click.stop>
          <!-- 关闭按钮 -->
          <div class="close-btn" @click="handleClose">
            <van-icon name="cross" size="24" color="#fff"/>
          </div>

          <!-- 图片索引 -->
          <div class="image-index">{{ currentIndex + 1 }} / {{ images.length }}</div>

          <!-- 图片轮播 -->
          <div class="swipe-wrapper">
            <div
                class="swipe-track"
                :style="{ transform: `translateX(-${currentIndex * 100}vw)` }"
                @touchstart="handleTouchStart"
                @touchmove="handleTouchMove"
                @touchend="handleTouchEnd"
            >
              <div
                  v-for="(image, index) in images"
                  :key="index"
                  class="swipe-item"
              >
                <div class="image-wrapper">
                  <img
                      :src="image"
                      :alt="`图片${index + 1}`"
                      :style="{
                      transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
                    }"
                      @click.stop="handleImageClick"
                      @touchstart="handleImageTouchStart"
                      @touchmove="handleImageTouchMove"
                      @touchend="handleImageTouchEnd"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 左右切换按钮 -->
          <template v-if="images.length > 1">
            <div
                v-if="currentIndex > 0"
                class="nav-btn prev-btn"
                @click.stop="handlePrev"
            >
              <van-icon name="arrow-left" size="24" color="#fff"/>
            </div>
            <div
                v-if="currentIndex < images.length - 1"
                class="nav-btn next-btn"
                @click.stop="handleNext"
            >
              <van-icon name="arrow" size="24" color="#fff"/>
            </div>
          </template>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';

interface Props {
  visible: boolean;
  images: string[];
  startIndex?: number;
}

interface Emits {
  (e: 'update:visible', value: boolean): void;

  (e: 'close'): void;
}

const props = withDefaults(defineProps<Props>(), {
  startIndex: 0
});

const emit = defineEmits<Emits>();

const currentIndex = ref(0);

// 触摸相关
const touchStartX = ref(0);
const touchStartY = ref(0);
const touchMoveX = ref(0);
const isSwiping = ref(false);

// 图片缩放相关
const scale = ref(1);
const imageStartDistance = ref(0);
const imageStartScale = ref(1);
const translateX = ref(0);
const translateY = ref(0);
const startTranslateX = ref(0);
const startTranslateY = ref(0);
const isZooming = ref(false);
const isDragging = ref(false);

// 监听起始索引变化
watch(() => props.startIndex, (val) => {
  currentIndex.value = val;
}, {immediate: true});

// 监听visible变化，重置状态
watch(() => props.visible, (val) => {
  if (val) {
    currentIndex.value = props.startIndex;
    scale.value = 1;
    translateX.value = 0;
    translateY.value = 0;
  }
});

// 监听图片切换，重置缩放
watch(currentIndex, () => {
  scale.value = 1;
  translateX.value = 0;
  translateY.value = 0;
});

// 关闭预览
const handleClose = () => {
  emit('update:visible', false);
  emit('close');
};

// 上一张
const handlePrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  }
};

// 下一张
const handleNext = () => {
  if (currentIndex.value < props.images.length - 1) {
    currentIndex.value++;
  }
};

// 轮播触摸开始
const handleTouchStart = (e: TouchEvent) => {
  // 只有在未缩放状态下才处理轮播滑动
  if (e.touches.length === 1 && scale.value === 1) {
    touchStartX.value = e.touches[0].clientX;
    touchStartY.value = e.touches[0].clientY;
    isSwiping.value = false;
  }
};

// 轮播触摸移动
const handleTouchMove = (e: TouchEvent) => {
  // 只有在未缩放状态下才处理轮播滑动
  if (e.touches.length === 1 && scale.value === 1) {
    touchMoveX.value = e.touches[0].clientX;
    const deltaX = Math.abs(touchMoveX.value - touchStartX.value);
    const deltaY = Math.abs(e.touches[0].clientY - touchStartY.value);

    // 判断是否为横向滑动
    if (deltaX > deltaY && deltaX > 10) {
      isSwiping.value = true;
    }
  }
};

// 轮播触摸结束
const handleTouchEnd = () => {
  if (isSwiping.value && scale.value === 1) {
    const delta = touchMoveX.value - touchStartX.value;

    // 滑动距离超过50px才切换
    if (Math.abs(delta) > 50) {
      if (delta > 0 && currentIndex.value > 0) {
        handlePrev();
      } else if (delta < 0 && currentIndex.value < props.images.length - 1) {
        handleNext();
      }
    }
  }

  isSwiping.value = false;
  touchStartX.value = 0;
  touchStartY.value = 0;
  touchMoveX.value = 0;
};

// 获取两个触摸点之间的距离
const getDistance = (touch1: Touch, touch2: Touch) => {
  const x = touch1.clientX - touch2.clientX;
  const y = touch1.clientY - touch2.clientY;
  return Math.sqrt(x * x + y * y);
};

// 图片点击（双击放大）
const handleImageClick = () => {
  if (scale.value > 1) {
    // 如果已放大，则平滑重置
    animateReset();
  }
};

// 平滑重置动画
const animateReset = () => {
  const startScale = scale.value;
  const startX = translateX.value;
  const startY = translateY.value;
  const duration = 300;
  const startTime = Date.now();

  const animate = () => {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // 使用easeOutCubic缓动函数
    const easeProgress = 1 - Math.pow(1 - progress, 3);

    scale.value = startScale + (1 - startScale) * easeProgress;
    translateX.value = startX * (1 - easeProgress);
    translateY.value = startY * (1 - easeProgress);

    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      scale.value = 1;
      translateX.value = 0;
      translateY.value = 0;
    }
  };

  requestAnimationFrame(animate);
};

// 图片触摸开始（支持缩放和拖拽）
const handleImageTouchStart = (e: TouchEvent) => {
  e.stopPropagation();

  if (e.touches.length === 2) {
    // 双指缩放
    isZooming.value = true;
    isDragging.value = false;
    imageStartDistance.value = getDistance(e.touches[0], e.touches[1]);
    imageStartScale.value = scale.value;
  } else if (e.touches.length === 1 && scale.value > 1) {
    // 单指拖拽（仅在放大时）
    isDragging.value = true;
    isZooming.value = false;
    touchStartX.value = e.touches[0].clientX;
    touchStartY.value = e.touches[0].clientY;
    startTranslateX.value = translateX.value;
    startTranslateY.value = translateY.value;
  }
};

// 图片触摸移动（支持缩放和拖拽）
const handleImageTouchMove = (e: TouchEvent) => {
  e.stopPropagation();
  e.preventDefault();

  if (e.touches.length === 2 && isZooming.value) {
    // 双指缩放 - 使用requestAnimationFrame优化
    requestAnimationFrame(() => {
      const distance = getDistance(e.touches[0], e.touches[1]);
      const scaleChange = distance / imageStartDistance.value;
      const newScale = imageStartScale.value * scaleChange;
      scale.value = Math.max(1, Math.min(4, newScale));
    });
  } else if (e.touches.length === 1 && isDragging.value && scale.value > 1) {
    // 单指拖拽 - 使用requestAnimationFrame优化
    requestAnimationFrame(() => {
      const deltaX = e.touches[0].clientX - touchStartX.value;
      const deltaY = e.touches[0].clientY - touchStartY.value;
      translateX.value = startTranslateX.value + deltaX / scale.value;
      translateY.value = startTranslateY.value + deltaY / scale.value;
    });
  }
};

// 图片触摸结束
const handleImageTouchEnd = (e: TouchEvent) => {
  e.stopPropagation();

  // 如果缩放小于1.1，则平滑重置
  if (scale.value < 1.1) {
    animateReset();
  }

  isZooming.value = false;
  isDragging.value = false;
};
</script>

<style scoped lang="scss">
.custom-image-preview {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  width: 100vw;
  height: 100vh;

  .preview-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
  }

  .preview-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    cursor: pointer;
    z-index: 10;

    &:active {
      background: rgba(0, 0, 0, 0.7);
    }
  }

  .image-index {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: #fff;
    font-size: 16px;
    background: rgba(0, 0, 0, 0.5);
    padding: 6px 16px;
    border-radius: 20px;
    z-index: 10;
  }

  .swipe-wrapper {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
  }

  .swipe-track {
    display: flex;
    height: 100%;
    transition: transform 0.3s ease;
    will-change: transform;
  }

  .swipe-item {
    flex-shrink: 0;
    width: 100vw;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;

    .image-wrapper {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    img {
      width: calc(100vw - 40px);
      height: calc(100vw - 40px);
      max-width: calc(100vh - 40px);
      max-height: calc(100vh - 40px);
      object-fit: contain;
      user-select: none;
      -webkit-user-drag: none;
      transform-origin: center center;
      background: transparent;
      will-change: transform;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      -webkit-transform: translateZ(0);
      transform: translateZ(0);
    }
  }

  .nav-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    cursor: pointer;
    z-index: 10;

    &:active {
      background: rgba(0, 0, 0, 0.7);
    }

    &.prev-btn {
      left: 20px;
    }

    &.next-btn {
      right: 20px;
    }
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>