<template>
  <n-modal
      v-model:show="showModal"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      :closable="false"
      preset="card"
      class="password-modal"
      :style="{ maxWidth: '480px' }"
  >
    <template #header>
      <div class="flex items-center">
        <div
            class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md shadow-indigo-500/20 relative overflow-hidden">
          <Icon icon="fluent:key-20-filled" :width="22" :height="22"/>
          <div
              class="absolute -top-1/2 -right-1/2 w-full h-full bg-gradient-to-br from-transparent via-white/30 to-transparent animate-shine"></div>
        </div>
        <div class="ml-3">
          <span
              class="text-lg font-semibold bg-gradient-to-br from-indigo-600 to-purple-600 bg-clip-text text-transparent">重置密码</span>
          <p class="text-xs text-gray-500 mt-0.5">请输入新的密码以保护账户安全</p>
        </div>
        <n-button
            text
            class="ml-auto -mr-2"
            @click="handleClose"
        >
          <Icon
              icon="fluent:dismiss-circle-20-regular"
              class="text-xl text-gray-400 hover:text-gray-600 transition-colors"
          />
        </n-button>
      </div>
    </template>
    <div class="custom-form-modal-content">
      <div class="custom-form-content">
        <div class="password-content">
          <!-- 安全提示 -->
          <div
              class="update-info flex items-center mb-2 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg border border-indigo-100">
            <Icon icon="fluent:shield-checkmark-20-filled" class="mr-2 text-indigo-600"/>
            <span class="text-sm text-gray-700">为了您的账户安全，请定期更换密码</span>
          </div>

          <n-form
              ref="formRef"
              :model="formModel"
              :rules="rules"
              label-placement="left"
              label-width="0"
              require-mark-placement="right-hanging"
          >
            <!-- 旧密码 -->
            <n-form-item path="oldPassword" :show-label="false">
              <div class="form-item-wrapper">
                <label class="form-label">
                  <Icon icon="fluent:lock-closed-20-regular" class="mr-2"/>
                  原密码
                </label>
                <n-input
                    v-model:value="formModel.oldPassword"
                    type="password"
                    placeholder="请输入原密码"
                    size="large"
                    :input-props="{
                autocomplete: 'current-password'
              }"
                    class="custom-input"
                />
              </div>
            </n-form-item>

            <!-- 新密码 -->
            <n-form-item path="newPassword" :show-label="false">
              <div class="form-item-wrapper">
                <label class="form-label">
                  <Icon icon="fluent:key-20-regular" class="mr-2"/>
                  新密码
                </label>
                <n-input
                    v-model:value="formModel.newPassword"
                    type="password"
                    placeholder="请输入新密码（8位以上）"
                    size="large"
                    show-password-on="click"
                    :input-props="{
                autocomplete: 'new-password'
              }"
                    class="custom-input"
                />
              </div>
            </n-form-item>

            <!-- 确认新密码 -->
            <n-form-item path="newPasswordRepeat" :show-label="false">
              <div class="form-item-wrapper">
                <label class="form-label">
                  <Icon icon="fluent:shield-checkmark-20-regular" class="mr-2"/>
                  确认新密码
                </label>
                <n-input
                    v-model:value="formModel.newPasswordRepeat"
                    type="password"
                    placeholder="请再次输入新密码"
                    size="large"
                    show-password-on="click"
                    :disabled="!formModel.newPassword"
                    :input-props="{
                autocomplete: 'new-password'
              }"
                    class="custom-input"
                />
              </div>
            </n-form-item>

            <!-- 密码强度提示 -->
            <Transition name="strength-fade">
              <div v-if="formModel.newPassword" class="mb-6">
                <div
                    class="strength-container p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center">
                      <Icon icon="fluent:shield-20-regular" :width="16" :height="16" class="text-indigo-600 mr-2"/>
                      <span class="text-sm font-medium text-gray-700">密码强度</span>
                    </div>
                    <span class="text-xs font-semibold" :class="strengthTextColor">{{ strengthText }}</span>
                  </div>
                  <div class="flex gap-1.5 mb-3">
                    <div
                        v-for="i in 4"
                        :key="i"
                        class="flex-1 h-2 rounded-full transition-all duration-500 ease-out"
                        :class="i <= passwordStrength ? strengthColors[passwordStrength] : 'bg-gray-200'"
                    ></div>
                  </div>
                  <div class="space-y-1.5">
                    <div class="flex items-center text-xs" :class="hasLength ? 'text-green-600' : 'text-gray-500'">
                      <Icon :icon="hasLength ? 'fluent:checkmark-circle-12-filled' : 'fluent:circle-12-regular'"
                            class="mr-1.5"/>
                      <span>至少8个字符</span>
                    </div>
                    <div class="flex items-center text-xs" :class="hasUpperLower ? 'text-green-600' : 'text-gray-500'">
                      <Icon :icon="hasUpperLower ? 'fluent:checkmark-circle-12-filled' : 'fluent:circle-12-regular'"
                            class="mr-1.5"/>
                      <span>包含大小写字母</span>
                    </div>
                    <div class="flex items-center text-xs" :class="hasNumber ? 'text-green-600' : 'text-gray-500'">
                      <Icon :icon="hasNumber ? 'fluent:checkmark-circle-12-filled' : 'fluent:circle-12-regular'"
                            class="mr-1.5"/>
                      <span>包含数字</span>
                    </div>
                    <div class="flex items-center text-xs" :class="hasSpecial ? 'text-green-600' : 'text-gray-500'">
                      <Icon :icon="hasSpecial ? 'fluent:checkmark-circle-12-filled' : 'fluent:circle-12-regular'"
                            class="mr-1.5"/>
                      <span>包含特殊字符（可选）</span>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>

            <!-- 按钮区域 -->
            <div class="flex gap-3 mt-6 pt-4 border-t border-gray-100">
              <n-button
                  size="large"
                  class="flex-1"
                  @click="handleClose"
              >
                取消
              </n-button>
              <n-button
                  size="large"
                  type="primary"
                  class="flex-1"
                  :loading="loading"
                  :disabled="!isFormValid"
                  @click="handleSubmit"
              >
                <template #icon>
                  <Icon icon="fluent:checkmark-circle-20-filled"/>
                </template>
                确认修改
              </n-button>
            </div>
          </n-form>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import {ref, computed, watch} from 'vue'
import {Icon} from '@iconify/vue'
import {NModal, NForm, NFormItem, NInput, NButton, useNotification, useDialog, FormInst, FormRules} from 'naive-ui'
import {apiResetSelfPassword, ResetSelfPasswordParams} from "@/api/webUserApi.ts";
import {useRouter} from "vue-router";
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts";

const notification = useNotification()
const dialog = useDialog()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const showModal = ref(false)
const router = useRouter()

const formModel = ref<ResetSelfPasswordParams>({
  oldPassword: '',
  newPassword: '',
  newPasswordRepeat: ''
})

const validatePasswordMatch = (_: any, value: string) => {
  if (value !== formModel.value.newPassword) {
    return new Error('两次输入的密码不一致')
  }
  return true
}

const validatePasswordStrength = (_: any, value: string) => {
  if (value.length < 8) {
    return new Error('密码长度至少为8位')
  }
  if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
    return new Error('密码必须包含大小写字母和数字')
  }
  return true
}

const rules: FormRules = {
  oldPassword: {
    required: true,
    message: '请输入当前密码',
    trigger: ['input', 'blur']
  },
  newPassword: [
    {
      required: true,
      message: '请输入新密码',
      trigger: ['input', 'blur']
    },
    {
      validator: validatePasswordStrength,
      trigger: ['input', 'blur']
    }
  ],
  newPasswordRepeat: [
    {
      required: true,
      message: '请再次输入新密码',
      trigger: ['input', 'blur']
    },
    {
      validator: validatePasswordMatch,
      trigger: ['input', 'blur']
    }
  ]
}

// 密码检查
const hasLength = computed(() => formModel.value.newPassword.length >= 8)
const hasUpperLower = computed(() => /[a-z]/.test(formModel.value.newPassword) && /[A-Z]/.test(formModel.value.newPassword))
const hasNumber = computed(() => /\d/.test(formModel.value.newPassword))
const hasSpecial = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(formModel.value.newPassword))

// 计算密码强度
const passwordStrength = computed(() => {
  const pwd = formModel.value.newPassword
  if (!pwd) return 0

  let strength = 0
  if (hasLength.value) strength++
  if (hasUpperLower.value) strength++
  if (hasNumber.value) strength++
  if (hasSpecial.value) strength++

  return strength
})

const strengthColors = {
  1: 'bg-red-400',
  2: 'bg-orange-400',
  3: 'bg-yellow-400',
  4: 'bg-green-400'
}

const strengthText = computed(() => {
  const texts = ['', '弱', '一般', '强', '非常强']
  return texts[passwordStrength.value]
})

const strengthTextColor = computed(() => {
  const colors = ['', 'text-red-600', 'text-orange-600', 'text-yellow-600', 'text-green-600']
  return colors[passwordStrength.value]
})

const isFormValid = computed(() => {
  return formModel.value.oldPassword &&
      formModel.value.newPassword &&
      formModel.value.newPasswordRepeat &&
      formModel.value.newPassword === formModel.value.newPasswordRepeat &&
      passwordStrength.value >= 2
})

// 打开弹窗的方法
const openModal = () => {
  showModal.value = true
  // 重置表单
  formModel.value = {
    oldPassword: '',
    newPassword: '',
    newPasswordRepeat: ''
  }
  formRef.value?.restoreValidation()
}

const handleClose = () => {
  formModel.value = {
    oldPassword: '',
    newPassword: '',
    newPasswordRepeat: ''
  }
  showModal.value = false
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    dialog.info({
      title: '确认修改密码',
      content: '您确定要修改密码吗？',
      positiveText: '确认',
      negativeText: '取消',
      onPositiveClick: () => {
        resetSelfPassword()
      },
      onNegativeClick: () => {
      }
    })
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const resetSelfPassword = () => {
  apiResetSelfPassword(formModel.value).then((res) => {
    loading.value = true
    if (res.code === 200) {
      notification.success({
        title: '成功',
        content: '密码修改成功, 请重新登录',
        duration: 3000
      })
      localStorage.clear()
      sessionStorage.clear()
      handleClose()
      router.push('/login')
    } else {
      notification.error({
        title: '错误',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((error) => {
    notification.error({
      title: '错误',
      content: error,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 监听新密码变化，清空确认密码
watch(() => formModel.value.newPassword, () => {
  if (formModel.value.newPasswordRepeat) {
    formModel.value.newPasswordRepeat = ''
  }
})

// 暴露方法给父组件
defineExpose({
  openModal
})
</script>

<style scoped lang="scss">
// Modal样式
:deep(.n-card) {
  border-radius: 1.25rem;
  background-color: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

:deep(.n-card-header) {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

:deep(.n-card__content) {
  padding: 0;
}

.password-content {
  padding: 0 1.5rem;
}

// 表单样式
.form-item-wrapper {
  width: 100%;
}

.form-label {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

// 自定义输入框样式
:deep(.custom-input) {
  .n-input__wrapper {
    padding: 0 16px;
    background: #f9fafb;
    border: 1.5px solid #e5e7eb;
    border-radius: 0.75rem;
    transition: all 0.3s ease;

    &:hover {
      background: #f3f4f6;
      border-color: #d1d5db;
    }
  }

  &.n-input--focus .n-input__wrapper {
    background: white;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }

  .n-input__input {
    font-size: 15px;
    height: 44px;

    &::placeholder {
      color: #9ca3af;
    }
  }

  .n-input__suffix {
    color: #6b7280;
  }
}

// 按钮样式
:deep(.n-button) {
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;

  &.n-button--large-type {
    height: 44px;
  }
}

:deep(.n-button--primary-type) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #5a67d8 0%, #6b5b95 100%);
  }
}

// 强度指示器动画
.strength-fade-enter-active,
.strength-fade-leave-active {
  transition: all 0.3s ease;
}

.strength-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.strength-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

// 闪光动画
@keyframes shine {
  0% {
    transform: translateX(-100%) translateY(-100%);
  }
  100% {
    transform: translateX(200%) translateY(200%);
  }
}

.animate-shine {
  animation: shine 3s infinite;
}

// 强度条容器
.strength-container {
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 50%,
            transparent 70%
    );
    animation: shimmer 3s infinite;
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) translateY(-100%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) translateY(100%) rotate(45deg);
  }
}
</style>