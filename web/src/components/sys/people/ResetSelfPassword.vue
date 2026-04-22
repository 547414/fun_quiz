<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 flex items-center justify-center p-4">
    <n-spin :show="loading" size="large">
      <div class="w-full max-w-md">
        <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <!-- 头部 -->
          <div class="flex items-center gap-3 mb-6">
            <div
                class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-blue-500/25">
              <Icon icon="fluent:key-reset-20-filled" :width="24" :height="24"/>
            </div>
            <div>
              <h2 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                重置密码
              </h2>
              <p class="text-sm text-gray-500 mt-1">为确保账户安全，请定期重置密码</p>
            </div>
          </div>

          <!-- 警告提示 -->
          <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-6">
            <div class="flex items-start gap-3">
              <Icon icon="fluent:warning-20-filled" class="text-amber-600 mt-0.5" :width="20" :height="20"/>
              <div>
                <p class="text-amber-800 font-medium text-sm">安全提醒</p>
                <p class="text-amber-700 text-xs mt-1">为确保账户安全，请定期重置密码并使用强密码</p>
              </div>
            </div>
          </div>

          <!-- 表单 -->
          <n-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-placement="top"
              size="large"
          >
            <n-form-item label="原始密码" path="oldPassword">
              <n-input
                  v-model:value="form.oldPassword"
                  type="password"
                  placeholder="请输入原始密码"
                  show-password-on="click"
                  class="form-input"
              >
                <template #prefix>
                  <Icon icon="fluent:lock-closed-20-regular" class="text-gray-400"/>
                </template>
              </n-input>
            </n-form-item>

            <n-form-item label="新密码" path="newPassword">
              <n-input
                  v-model:value="form.newPassword"
                  type="password"
                  placeholder="请输入新密码（8-16位，包含大小写字母和数字）"
                  show-password-on="click"
                  class="form-input"
              >
                <template #prefix>
                  <Icon icon="fluent:lock-shield-20-regular" class="text-gray-400"/>
                </template>
              </n-input>
            </n-form-item>

            <n-form-item label="确认新密码" path="newPasswordRepeat">
              <n-input
                  v-model:value="form.newPasswordRepeat"
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password-on="click"
                  class="form-input"
              >
                <template #prefix>
                  <Icon icon="fluent:checkmark-lock-20-regular" class="text-gray-400"/>
                </template>
              </n-input>
            </n-form-item>
          </n-form>

          <!-- 提交按钮 -->
          <n-button
              type="primary"
              size="large"
              block
              class="mt-6 submit-btn"
              @click="resetPassword"
              :loading="loading"
          >
            <template #icon>
              <Icon icon="fluent:key-reset-20-filled"/>
            </template>
            重置密码
          </n-button>

          <!-- 密码强度提示 -->
          <div class="mt-4 p-3 bg-gray-50 rounded-xl">
            <div class="flex items-start gap-2">
              <Icon icon="fluent:shield-checkmark-20-regular" class="text-gray-600 mt-0.5" :width="16" :height="16"/>
              <div class="text-xs text-gray-600">
                <p class="font-medium mb-1">密码安全要求：</p>
                <ul class="space-y-0.5">
                  <li>• 长度8-16个字符</li>
                  <li>• 包含大写字母（A-Z）</li>
                  <li>• 包含小写字母（a-z）</li>
                  <li>• 包含数字（0-9）</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Icon} from "@iconify/vue";
import {
  NForm,
  NFormItem,
  NInput,
  NButton,
  NSpin,
  useNotification,
  useDialog,
  type FormInst,
  type FormRules,
  type FormItemRule
} from "naive-ui";
import {apiResetSelfPassword, type ResetSelfPasswordParams} from "@/api/webUserApi.ts";
import {type Response} from "@/utils/requestTypes.ts";
import {clearUserInfo} from "@/utils/userUtil.ts";

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const notification = useNotification()
const dialog = useDialog()

const form = ref<ResetSelfPasswordParams>({
  oldPassword: '',
  newPassword: '',
  newPasswordRepeat: ''
})

const validatePasswordRepeat = (_rule: FormItemRule, value: string) => {
  if (value !== form.value.newPassword) {
    return new Error('两次输入密码不一致')
  }
  return true
}

const rules: FormRules = {
  oldPassword: [
    {required: true, message: '请填写旧密码', trigger: 'blur'},
    {min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur'},
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    },
  ],
  newPassword: [
    {required: true, message: '请填写新密码', trigger: 'blur'},
    {min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur'},
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    },
  ],
  newPasswordRepeat: [
    {required: true, message: '请填写重复密码', trigger: 'blur'},
    {min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur'},
    {
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    },
    {validator: validatePasswordRepeat, trigger: 'blur'}
  ],
}

const resetPassword = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      confirmResetPassword()
    }
  })
}

const confirmResetPassword = () => {
  dialog.warning({
    title: '确认重置密码',
    content: '是否确认重置密码？重置后需要重新登录。',
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      resetSelfPassword()
    }
  })
}

const resetSelfPassword = () => {
  loading.value = true
  apiResetSelfPassword(form.value).then((res: Response) => {
    if (res.code === 200) {
      notification.success({
        title: '重置密码成功',
        content: '请重新登录',
        duration: 2000
      })
      clearUserInfo()
      setTimeout(() => {
        window.location.href = '/login'
      }, 2000)
    } else {
      notification.error({
        title: '重置密码失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((error: string) => {
    notification.error({
      title: '重置密码失败',
      content: error,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}
</script>

<style scoped lang="scss">
// 表单输入框样式
:deep(.form-input) {
  .n-input {
    border-radius: 0.75rem;
    transition: all 0.3s ease;

    &:hover {
      border-color: #60a5fa;
    }

    &.n-input--focus {
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .n-input__input-el {
      padding: 12px 16px;
    }

    .n-input__prefix {
      padding-left: 16px;
    }
  }
}

// 提交按钮样式
:deep(.submit-btn) {
  font-weight: 500;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
  border: none;
  border-radius: 0.75rem;
  transition: all 0.3s ease;

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    background: #e5e7eb;
    color: #9ca3af;
  }
}

// 表单项样式
:deep(.n-form-item) {
  margin-bottom: 20px;

  .n-form-item-label {
    font-weight: 500;
    color: #374151;
    margin-bottom: 6px;
    font-size: 14px;
  }

  .n-form-item-feedback {
    font-size: 12px;
    margin-top: 4px;
  }
}

// 加载状态样式
:deep(.n-spin) {
  .n-spin-container {
    border-radius: 1.5rem;
  }

  .n-spin-content {
    opacity: 0.6;
    transition: opacity 0.3s ease;
  }
}

// 页面背景动画
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.bg-gradient-to-br {
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
  }
}

// 卡片阴影动画
.bg-white {
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  }
}

// 密码强度指示器样式
.password-strength {
  .strength-indicator {
    height: 4px;
    border-radius: 2px;
    background: #e5e7eb;
    overflow: hidden;
    position: relative;

    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      transition: width 0.3s ease, background-color 0.3s ease;
    }

    &.weak::after {
      width: 33%;
      background: #ef4444;
    }

    &.medium::after {
      width: 66%;
      background: #f59e0b;
    }

    &.strong::after {
      width: 100%;
      background: #10b981;
    }
  }
}

// 安全提示样式美化
:deep(.n-alert) {
  border-radius: 0.75rem;
  border: none;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);

  .n-alert__icon {
    color: #d97706;
  }

  .n-alert__content {
    color: #92400e;
  }
}

// 响应式设计
@media (max-width: 640px) {
  .w-full.max-w-md {
    margin: 0 16px;
  }

  .bg-white {
    padding: 24px;
  }

  :deep(.submit-btn) {
    height: 44px;
    font-size: 14px;
  }
}
</style>