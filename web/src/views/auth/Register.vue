<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 relative overflow-hidden">
    <!-- 背景装饰 -->
    <AnimatedBackground/>
    <UserAgreement ref="uerAgreementModalRef"/>
    <PrivacyPolicy ref="privacyPolicyModalRef"/>

    <!-- 注册卡片 -->
    <n-card class="w-full max-w-md shadow-2xl relative z-10" :bordered="false">
      <!-- Logo区域 -->
      <div class="text-center mb-8">
        <div
            class="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-lg shadow-indigo-500/30 mb-6">
          <Icon icon="fluent:cube-24-filled" class="text-white text-3xl"/>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mb-2">创建账号</h1>
        <p class="text-gray-600">注册玄测后台管理系统账号</p>
      </div>

      <!-- 注册表单 -->
      <n-form
          ref="formRef"
          :model="formValue"
          :rules="rules"
          size="large"
      >
        <!-- 邀请码输入 -->
        <n-form-item path="inviteCode" :show-label="false">
          <n-input
              v-model:value="formValue.inviteCode"
              placeholder="请输入邀请码"
              class="h-12"
              maxlength="8"
          >
            <template #prefix>
              <Icon icon="fluent:ticket-diagonal-20-regular" class="text-gray-400"/>
            </template>
          </n-input>
        </n-form-item>

        <!-- 用户名输入 -->
        <n-form-item path="username" :show-label="false">
          <n-input
              v-model:value="formValue.username"
              placeholder="设置用户名"
              :input-props="{ autocomplete: 'username' }"
              class="h-12"
              maxlength="20"
          >
            <template #prefix>
              <Icon icon="fluent:person-20-regular" class="text-gray-400"/>
            </template>
            <template #suffix>
              <n-text v-if="usernameStatus === 'checking'" depth="3" class="text-xs">
                <Icon icon="fluent:spinner-ios-20-regular" class="animate-spin"/>
              </n-text>
              <n-text v-else-if="usernameStatus === 'available'" type="success" class="text-xs">
                <Icon icon="fluent:checkmark-circle-20-filled"/>
              </n-text>
              <n-text v-else-if="usernameStatus === 'taken'" type="error" class="text-xs">
                <Icon icon="fluent:dismiss-circle-20-filled"/>
              </n-text>
            </template>
          </n-input>
        </n-form-item>

        <!-- 密码输入 -->
        <n-form-item path="password" :show-label="false">
          <n-input
              v-model:value="formValue.password"
              type="password"
              show-password-on="click"
              placeholder="设置密码"
              :input-props="{ autocomplete: 'new-password' }"
              class="h-12"
              @input="checkPasswordStrength"
          >
            <template #prefix>
              <Icon icon="fluent:lock-closed-20-regular" class="text-gray-400"/>
            </template>
          </n-input>
        </n-form-item>

        <!-- 密码强度指示器 -->
        <div v-if="formValue.password" class="mb-4 -mt-2">
          <div class="flex gap-1 mb-1">
            <div
                v-for="i in 4"
                :key="i"
                class="flex-1 h-1 rounded-full transition-all duration-300"
                :class="getStrengthBarClass(i)"
            ></div>
          </div>
          <p class="text-xs" :class="getStrengthTextClass()">
            {{ strengthText }}
          </p>
        </div>

        <!-- 确认密码输入 -->
        <n-form-item path="confirmPassword" :show-label="false">
          <n-input
              v-model:value="formValue.confirmPassword"
              type="password"
              show-password-on="click"
              placeholder="确认密码"
              :input-props="{ autocomplete: 'new-password' }"
              class="h-12"
          >
            <template #prefix>
              <Icon icon="fluent:lock-closed-20-regular" class="text-gray-400"/>
            </template>
          </n-input>
        </n-form-item>

        <!-- 人机验证 -->
        <n-form-item :show-label="false">
          <div
              @click="toggleCaptcha"
              class="w-full h-12 border-2 border-dashed rounded-lg flex items-center justify-center gap-2 cursor-pointer transition-all"
              :class="captchaVerified
              ? 'border-green-500 bg-green-50 hover:bg-green-100'
              : 'border-gray-300 bg-gray-50 hover:bg-gray-100'"
          >
            <Icon
                :icon="captchaVerified ? 'fluent:checkmark-circle-20-filled' : 'fluent:shield-checkmark-20-regular'"
                :class="captchaVerified ? 'text-green-500' : 'text-gray-400'"
                class="text-xl"
            />
            <span :class="captchaVerified ? 'text-green-600' : 'text-gray-600'" class="font-medium">
              {{ captchaVerified ? '已通过人机验证' : '点击进行人机验证' }}
            </span>
          </div>
        </n-form-item>

        <!-- 用户协议 -->
        <div class="mb-6">
          <n-checkbox v-model:checked="formValue.agreement">
            <span class="text-gray-600 text-sm">
              我已阅读并同意
              <n-button text type="primary" size="tiny" @click.stop="showTerms">《用户协议》</n-button>
              和
              <n-button text type="primary" size="tiny" @click.stop="showPrivacy">《隐私政策》</n-button>
            </span>
          </n-checkbox>
        </div>

        <!-- 注册按钮 -->
        <div class="custom-primary-btn">
          <n-button
              type="primary"
              block
              size="large"
              :loading="loading"
              :disabled="!canRegister"
              @click="handleRegister"
              class="h-12 mb-4"
          >
            <template #icon>
              <Icon icon="fluent:person-add-20-filled" v-if="!loading"/>
            </template>
            {{ loading ? '注册中...' : '注册' }}
          </n-button>
        </div>

        <!-- 返回登录 -->
        <div class="text-center">
          <span class="text-gray-600 text-sm">已有账号？</span>
          <n-button text type="primary" size="small" @click="handleBackToLogin">
            返回登录
          </n-button>
        </div>
      </n-form>
    </n-card>

    <!-- 版权信息 -->
    <div class="absolute bottom-6 left-1/2 transform -translate-x-1/2 text-gray-500 text-sm">
      © 1926 - 至今 民生医药. 版权所有.
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, watch} from 'vue'
import {NForm, NFormItem, NInput, NButton, NCheckbox, NCard, NText, useMessage} from 'naive-ui'
import {Icon} from '@iconify/vue'
import type {FormInst, FormRules, FormItemRule} from 'naive-ui'
import {useRouter} from 'vue-router'
import AnimatedBackground from '@/components/background/AnimatedBackground.vue'
import UserAgreement from "@/components/sys/auth/UserAgreement.vue";
import PrivacyPolicy from "@/components/sys/auth/PrivacyPolicy.vue";

const router = useRouter()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const captchaVerified = ref(false)
const usernameStatus = ref<'idle' | 'checking' | 'available' | 'taken'>('idle')
const passwordStrength = ref(0)
const strengthText = ref('')
const uerAgreementModalRef = ref()
const privacyPolicyModalRef = ref()

const formValue = ref({
  inviteCode: '',
  username: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

// 密码验证规则
const validatePasswordConfirm = (_rule: FormItemRule, value: string) => {
  if (value !== formValue.value.password) {
    return new Error('两次输入的密码不一致')
  }
  return true
}

const rules: FormRules = {
  inviteCode: {
    required: true,
    message: '请输入邀请码',
    trigger: ['blur', 'input']
  },
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: ['blur', 'input']
    },
    {
      min: 3,
      max: 20,
      message: '用户名长度应为3-20个字符',
      trigger: ['blur', 'input']
    },
    {
      pattern: /^[a-zA-Z0-9_]+$/,
      message: '用户名只能包含字母、数字和下划线',
      trigger: ['blur', 'input']
    }
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: ['blur', 'input']
    },
    {
      min: 6,
      message: '密码长度不能少于6位',
      trigger: ['blur', 'input']
    }
  ],
  confirmPassword: [
    {
      required: true,
      message: '请确认密码',
      trigger: ['blur', 'input']
    },
    {
      validator: validatePasswordConfirm,
      trigger: ['blur', 'input']
    }
  ]
}

// 检查用户名可用性
let checkTimer: any = null
watch(() => formValue.value.username, (newVal) => {
  if (checkTimer) clearTimeout(checkTimer)

  if (!newVal || newVal.length < 3) {
    usernameStatus.value = 'idle'
    return
  }

  usernameStatus.value = 'checking'
  checkTimer = setTimeout(() => {
    // 模拟检查用户名
    const taken = Math.random() > 0.7
    usernameStatus.value = taken ? 'taken' : 'available'
  }, 800)
})

// 检查密码强度
const checkPasswordStrength = () => {
  const pwd = formValue.value.password
  let strength = 0

  if (pwd.length >= 8) strength++
  if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) strength++
  if (/\d/.test(pwd)) strength++
  if (/[^a-zA-Z\d]/.test(pwd)) strength++

  passwordStrength.value = strength

  const strengthMap = ['', '弱', '中', '强', '很强']
  strengthText.value = strengthMap[strength]
}

// 获取密码强度条样式
const getStrengthBarClass = (index: number) => {
  if (index <= passwordStrength.value) {
    const colors = ['', 'bg-red-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500']
    return colors[passwordStrength.value]
  }
  return 'bg-gray-200'
}

// 获取密码强度文字样式
const getStrengthTextClass = () => {
  const colors = ['', 'text-red-500', 'text-yellow-500', 'text-blue-500', 'text-green-500']
  return colors[passwordStrength.value]
}

// 是否可以注册
const canRegister = computed(() => {
  return captchaVerified.value && formValue.value.agreement
})

// 切换人机验证状态
const toggleCaptcha = () => {
  captchaVerified.value = !captchaVerified.value
  if (captchaVerified.value) {
    message.success('人机验证成功')
  }
}

// 注册处理
const handleRegister = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      if (usernameStatus.value === 'taken') {
        message.error('用户名已被占用')
        return
      }

      loading.value = true
      setTimeout(() => {
        loading.value = false
        message.success('注册成功，请登录')
        router.push('/login')
      }, 2000)
    }
  })
}

// 返回登录
const handleBackToLogin = () => {
  router.push('/login')
}

// 显示用户协议
const showTerms = () => {
  message.info('显示用户协议')
  uerAgreementModalRef.value.openModal()
}

// 显示隐私政策
const showPrivacy = () => {
  message.info('显示隐私政策')
  privacyPolicyModalRef.value.openModal()
}
</script>

<style scoped lang="scss">
/* 仅保留必要的自定义样式 */
:deep(.n-card) {
  border-radius: 1.5rem;
  padding: 1.5rem;

  background-color: rgba(255, 255, 255, 0.25); // 半透明白
  backdrop-filter: blur(20px); // 高斯模糊
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2); // 柔和边框
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); // 轻柔阴影
  transition: all 0.3s ease;

  .n-input__input-el {
    padding: 7px 0 0 0;
  }
}

:deep(.n-input) {
  border-radius: 0.75rem;
}

:deep(.n-form-item) {
  margin-bottom: 4px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>