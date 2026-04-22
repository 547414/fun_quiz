<template>
  <button
      class="sidebar-item"
      :class="{
      'sidebar-item--active': active,
      'sidebar-item--parent': hasChildren,
      'sidebar-item--expanded': hasChildren && expanded,
      'sidebar-item--collapsed': collapsed
    }"
      @click="emit('click')"
      :title="collapsed ? label : ''"
  >
    <div class="item-content">
      <div class="item-icon-box">
        <Icon
            :icon="currentIcon"
            :width="20"
            :height="20"
            class="item-icon"
        />
      </div>
      <span class="item-label" :class="{ 'item-label--hidden': collapsed }">{{ label }}</span>

      <!-- 展开/收起箭头 -->
      <Icon
          v-if="hasChildren && !collapsed"
          icon="fluent:chevron-right-20-regular"
          :width="16"
          :height="16"
          class="expand-icon"
      />
    </div>

    <!-- 普通状态下的徽章 -->
    <transition name="badge">
      <span v-if="badge && !hasChildren && !collapsed" class="item-badge">
        {{ formatBadge(badge) }}
      </span>
    </transition>

    <!-- 折叠状态下的徽章显示为小圆点 -->
    <transition name="badge-dot">
      <span v-if="badge && collapsed" class="item-badge-dot"></span>
    </transition>
  </button>
</template>

<script setup lang="ts">
import {computed} from 'vue'
import {Icon} from '@iconify/vue'

interface Props {
  icon: string
  label: string
  active?: boolean
  badge?: string | number | null
  hasChildren?: boolean
  expanded?: boolean
  collapsed?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  active: false,
  badge: null,
  hasChildren: false,
  expanded: false,
  collapsed: false
})

const emit = defineEmits<{
  click: []
}>()

// 根据激活状态切换图标
const currentIcon = computed(() => {
  if (props.active && props.icon.includes('-regular')) {
    return props.icon.replace('-regular', '-filled')
  }
  return props.icon
})

// 格式化徽章显示
const formatBadge = (badge: string | number) => {
  if (typeof badge === 'number' && badge > 99) {
    return '99+'
  }
  return badge
}
</script>

<style lang="scss" scoped>
.sidebar-item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    // 更柔和的渐变背景
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.08) 0%,
        rgba(139, 92, 246, 0.06) 100%
    );
    opacity: 0;
    transition: opacity 0.25s ease;
    z-index: 0;
  }

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 30% 50%, rgba(255, 255, 255, 0.1), transparent 70%);
    opacity: 0;
    transition: opacity 0.25s ease;
    z-index: 1;
  }

  &:hover {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);

    &::after {
      opacity: 1;
    }

    .item-icon-box {
      transform: scale(1.05);
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }

    .item-icon {
      color: white;
    }

    .item-label {
      color: #1f2937;
      font-weight: 600;
    }
  }

  &:active {
    transform: scale(0.98);
  }

  &--active {
    &::before {
      opacity: 1;
    }

    &:hover {
      background: transparent;

      &::after {
        opacity: 0.5;
      }
    }

    .item-content,
    .item-badge {
      position: relative;
      z-index: 2;
    }

    .item-icon-box {
      // 更优雅的渐变背景
      background: linear-gradient(135deg,
          rgba(255, 255, 255, 0.95) 0%,
          rgba(249, 250, 251, 0.9) 100%
      );
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 4px 16px rgba(99, 102, 241, 0.08),
      0 2px 4px rgba(99, 102, 241, 0.04),
      inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }

    .item-icon {
      // 更鲜明的主题色
      color: #6366f1;
    }

    .item-label {
      // 更深的对比色，增强可读性
      color: #1f2937;
      font-weight: 650;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .item-badge {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: white;
      font-weight: 700;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25),
      0 2px 4px rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .item-badge-dot {
      background: #6366f1;
      box-shadow: 0 0 8px rgba(99, 102, 241, 0.5);
    }
  }

  // 父节点样式
  &--parent {
    position: relative;

    .item-content {
      .item-icon-box {
        // 使用普通灰色背景
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-color: rgba(226, 232, 240, 0.8);
        position: relative;

        .item-icon {
          color: #64748b;
        }

        // 折叠状态的小圆点指示器
        .children-indicator {
          position: absolute;
          top: -2px;
          right: -2px;
          width: 8px;
          height: 8px;
          background: #6366f1;
          border-radius: 50%;
          border: 2px solid white;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          animation: pulse 2s infinite;
        }
      }
    }

    &:hover {
      .item-icon-box {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);

        .item-icon {
          color: white;
        }
      }

      .expand-icon {
        color: #1f2937;
      }
    }

    &.sidebar-item--active {
      .item-icon-box {
        // 保持与普通激活项相同的样式
        background: linear-gradient(135deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(249, 250, 251, 0.9) 100%
        );
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.08),
        0 2px 4px rgba(99, 102, 241, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.5);

        .children-indicator {
          background: #6366f1;
          border-color: white;
        }

        .item-icon {
          color: #6366f1;
        }
      }

      .expand-icon {
        color: #6366f1;
      }
    }
  }

  // 展开状态
  &--expanded {
    .expand-icon {
      transform: rotate(90deg);
    }
  }

  .item-content {
    display: flex;
    align-items: center;
    gap: 0.875rem;
    position: relative;
    width: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    .item-icon-box {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
      border: 1px solid rgba(226, 232, 240, 0.8);
      border-radius: 10px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      flex-shrink: 0;

      .item-icon {
        color: #64748b;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 1;
      }
    }

    .item-label {
      font-size: 0.875rem;
      font-weight: 500;
      color: #4b5563;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      white-space: nowrap;
      letter-spacing: 0.01em;
      flex: 1;
      text-align: left;
      opacity: 1;
      transform: translateX(0);
      max-width: 200px;

      &--hidden {
        opacity: 0;
        transform: translateX(-10px);
        max-width: 0;
        overflow: hidden;
      }
    }

    .expand-icon {
      color: #9ca3af;
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      margin-left: auto;
      flex-shrink: 0;
    }
  }

  .item-badge {
    min-width: 20px;
    height: 20px;
    padding: 0 6px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.6875rem;
    font-weight: 600;
    background: #ef4444;
    color: white;
    border-radius: 10px;
    transition: all 0.25s ease;
    position: relative;
  }

  .item-badge-dot {
    width: 8px;
    height: 8px;
    background: #ef4444;
    border-radius: 50%;
    position: absolute;
    top: 6px;
    right: 6px;
    transition: all 0.25s ease;
  }

  // 徽章动画
  .badge-enter-active {
    animation: badge-bounce-in 0.5s;
  }

  .badge-leave-active {
    animation: badge-bounce-out 0.3s;
  }

  @keyframes badge-bounce-in {
    0% {
      opacity: 0;
      transform: scale(0);
    }
    50% {
      transform: scale(1.2);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }

  @keyframes badge-bounce-out {
    0% {
      opacity: 1;
      transform: scale(1);
    }
    100% {
      opacity: 0;
      transform: scale(0);
    }
  }

  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.1);
      opacity: 0.8;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }
}

// 响应式调整
@media (max-width: 1280px) {
  .sidebar-item {
    padding: 0.625rem 0.875rem;

    &--collapsed {
      padding: 0.625rem;
    }

    .item-content {
      gap: 0.75rem;

      .item-icon-box {
        width: 32px;
        height: 32px;
      }

      .item-label {
        font-size: 0.8125rem;
      }
    }
  }
}
</style>