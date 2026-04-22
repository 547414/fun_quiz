<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <router-view/>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import {NConfigProvider, NMessageProvider, NNotificationProvider, NDialogProvider} from 'naive-ui'
import type {GlobalThemeOverrides} from 'naive-ui'
  import { zhCN, dateZhCN } from 'naive-ui'

// 自定义主题配置
const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#6366f1',
    primaryColorHover: '#4f46e5',
    primaryColorPressed: '#4338ca',
    primaryColorSuppl: '#818cf8',
    borderRadius: '12px',
    borderRadiusSmall: '8px',
  },
  Button: {
    borderRadiusMedium: '10px'
  },
  Card: {
    borderRadius: '16px'
  }
}
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f5f6fb;
}

/* 强制修改所有 Dialog 按钮为实色样式 */
.n-dialog {

  .n-base-close::before {
    width: 26px;
    height: 26px;
    border-radius: 50%;
  }

  /* 警告类型按钮 */
  button[type="button"].n-button.n-button--warning-type {
    background-color: #f59e0b !important;
    border-color: #f59e0b !important;
    color: #ffffff !important;


    &:hover:not(:disabled) {
      background-color: #d97706 !important;
      border-color: #d97706 !important;
      color: #ffffff !important;
    }

    &:focus:not(:disabled) {
      background-color: #d97706 !important;
      border-color: #d97706 !important;
      color: #ffffff !important;
    }

    &:active:not(:disabled) {
      background-color: #b45309 !important;
      border-color: #b45309 !important;
      color: #ffffff !important;
    }
  }

  /* 错误类型按钮 */
  button[type="button"].n-button.n-button--error-type {
    background-color: #ef4444 !important;
    border-color: #ef4444 !important;
    color: #ffffff !important;

    &:hover:not(:disabled) {
      background-color: #dc2626 !important;
      border-color: #dc2626 !important;
      color: #ffffff !important;
    }
  }

  /* 主要类型按钮 */
  button[type="button"].n-button.n-button--primary-type {
    background-color: #6366f1 !important;
    border-color: #6366f1 !important;
    color: #ffffff !important;

    &:hover:not(:disabled) {
      background-color: #4f46e5 !important;
      border-color: #4f46e5 !important;
      color: #ffffff !important;
    }
  }

  /* 成功类型按钮 */
  button[type="button"].n-button.n-button--success-type {
    background-color: #10b981 !important;
    border-color: #10b981 !important;
    color: #ffffff !important;

    &:hover:not(:disabled) {
      background-color: #059669 !important;
      border-color: #059669 !important;
      color: #ffffff !important;
    }
  }

  /* 信息类型按钮 */
  button[type="button"].n-button.n-button--info-type {
    background-color: #3b82f6 !important;
    border-color: #3b82f6 !important;
    color: #ffffff !important;

    &:hover:not(:disabled) {
      background-color: #2563eb !important;
      border-color: #2563eb !important;
      color: #ffffff !important;
    }
  }

  /* 默认类型按钮（取消按钮） */
  button[type="button"].n-button.n-button--default-type {
    background-color: #ffffff !important;
    border-color: #e5e7eb !important;
    color: #374151 !important;

    &:hover:not(:disabled) {
      background-color: #f9fafb !important;
      border-color: #d1d5db !important;
      color: #111827 !important;
    }
  }
}

/* 如果上面的不够强，再加一层 */
.n-dialog__action {
  .n-button {
    /* 移除所有可能的透明背景 */
    &.n-button--ghost {
      background-color: transparent !important;
    }

    /* 然后强制应用实色背景 */
    &.n-button--warning-type {
      background-color: #f59e0b !important;
      color: #ffffff !important;
    }

    &.n-button--error-type {
      background-color: #ef4444 !important;
      color: #ffffff !important;
    }

    &.n-button--primary-type {
      background-color: #6366f1 !important;
      color: #ffffff !important;
    }

    &.n-button--success-type {
      background-color: #10b981 !important;
      color: #ffffff !important;
    }

    &.n-button--info-type {
      background-color: #3b82f6 !important;
      color: #ffffff !important;
    }
  }
}

/* Dialog 样式优化 */
.n-modal-mask {
  /* 调整背景遮罩透明度，减少紫色阴影 */
  background-color: rgba(0, 0, 0, 0.3) !important;
}


/* 对话框卡片阴影 */
.n-modal-body-wrapper {
  .n-dialog {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
  }
}
</style>