<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 relative overflow-hidden">
    <AnimatedBackground/>
    <ValidateCaptchaModal
        ref="validateCaptchaModalRef"
        @operate-success="handleValidateCaptchaSuccess"
    />
    <UserAgreement ref="uerAgreementModalRef"/>
    <PrivacyPolicy ref="privacyPolicyModalRef"/>
    <!-- 登录卡片 -->
    <n-card class="w-full max-w-md shadow-2xl relative z-10" :bordered="false">
      <!-- Logo区域 -->
      <div class="text-center mb-8">
        <div
            class="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-lg shadow-indigo-500/30 mb-6">
          <Icon icon="fluent:cube-24-filled" class="text-white text-3xl"/>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mb-2">欢迎回来</h1>
        <p class="text-gray-600">登录到玄测后台管理系统</p>
      </div>

      <!-- 登录表单 -->
      <n-form
          ref="formRef"
          :model="formValue"
          :rules="rules"
          size="large"
      >
        <!-- 用户名输入 -->
        <n-form-item path="name" :show-label="false">
          <n-input
              v-model:value="formValue.name"
              placeholder="请输入用户名"
              :input-props="{ autocomplete: 'name' }"
              class="h-12"
          >
            <template #prefix>
              <Icon icon="fluent:person-20-regular" class="text-gray-400"/>
            </template>
          </n-input>
        </n-form-item>

        <!-- 密码输入 -->
        <n-form-item path="password" :show-label="false">
          <n-input
              v-model:value="formValue.password"
              type="password"
              show-password-on="click"
              placeholder="请输入密码"
              :input-props="{ autocomplete: 'current-password' }"
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

        <!-- 记住账号和其他链接 -->
        <div class="flex items-center justify-between mb-4">
          <n-checkbox v-model:checked="formValue.remember">
            记住账号
          </n-checkbox>
          <div class="flex items-center gap-2 text-sm">
            <n-button text type="primary" @click="handleRegister">注册账号</n-button>
            <span class="text-gray-300">·</span>
            <n-button text type="primary" @click="handleForgotPassword">忘记密码？</n-button>
          </div>
        </div>

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

        <!-- 登录按钮 -->
        <div class="custom-primary-btn">
          <n-button
              type="primary"
              block
              size="large"
              :loading="loading"
              :disabled="!captchaVerified || !formValue.agreement"
              @click="handleLogin"
              class="h-12"
          >
            <template #icon>
              <Icon icon="fluent:arrow-right-20-filled" v-if="!loading"/>
            </template>
            {{ loading ? '登录中...' : '登录' }}
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
import {ref} from 'vue'
import {NForm, NFormItem, NInput, NButton, NCheckbox, NCard, useMessage, useNotification, FormItemRule} from 'naive-ui'
import {Icon} from '@iconify/vue'
import {useRouter} from 'vue-router'
import type {FormInst, FormRules} from 'naive-ui'
import AnimatedBackground from '@/components/background/AnimatedBackground.vue'
import ValidateCaptchaModal from '@/components/sys/captcha/ValidateCaptchaModal.vue'
import UserAgreement from "@/components/sys/auth/UserAgreement.vue";
import PrivacyPolicy from "@/components/sys/auth/PrivacyPolicy.vue";
import {apiWebUserLogin, WebUserLoginDetail, WebUserLoginParams} from "@/api/webUserApi.ts";
import {getUnionUserInfo} from "@/utils/userUtil.ts";

const router = useRouter()
const message = useMessage()
const notification = useNotification()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const captchaVerified = ref(false)
const validateCaptchaModalRef = ref()
const uerAgreementModalRef = ref()
const privacyPolicyModalRef = ref()

const localUnionUserInfo = localStorage.getItem('unionUserInfo')
if (localUnionUserInfo) {
  notification.info({
    title: '提示',
    content: '您已登录，正在跳转到首页...',
    duration: 3000
  })
  const unionUserInfo: WebUserLoginDetail = getUnionUserInfo()
  if (!unionUserInfo) {
    router.push('/')
  } else {
    for (const [_idx, user] of unionUserInfo?.unionUserInfo?.userList?.entries()) {
      if (user.unionUserUserCategory === 'WEB_USER') {
        if (user.currentRoleCode === 'WEB_USER') {
          router.push('/')
          break
        } else {
          router.push('/quiz/list')
          break
        }
      }
    }
  }
}

const formValue = ref<WebUserLoginParams>({
  name: null,
  sceneId: null,
  unionUserId: null,
  verificationCode: null,
  password: '',
  remember: true,
  agreement: false,
  captchaId: null,
  validateCaptchaAuthCode: null
})

const rules: FormRules = {
  name: {
    required: true,
    trigger: ['blur', 'input'],
    validator(_rule: FormItemRule, value: string) {
      if (!value) {
        return new Error('请输入用户名')
      } else if (value.trim() === '') {
        return new Error('请输入用户名')
      }
      return true
    },
  },
  password: {
    required: true,
    message: '请输入密码',
    trigger: ['blur', 'input']
  }
}

// 切换人机验证状态
const toggleCaptcha = () => {
  if (!captchaVerified.value) {
    validateCaptchaModalRef.value.openModal()
  }
}

// 验证成功后的回调
const handleValidateCaptchaSuccess = (
    data: {
      validateCaptchaAuthCode: string
      captchaId: string
    }
) => {
  console.log('验证成功', data)
  captchaVerified.value = true
  formValue.value.captchaId = data.captchaId
  formValue.value.validateCaptchaAuthCode = data.validateCaptchaAuthCode
}

// 登录处理
const handleLogin = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      if (!captchaVerified.value) {
        notification.warning({
          title: '提示',
          content: '请先完成人机验证',
          duration: 3000
        })
        return
      }
      if (!formValue.value.agreement) {
        notification.warning({
          title: '提示',
          content: '请同意用户协议和隐私政策',
          duration: 3000
        })
        return
      }
      loading.value = true
      webUserLogin()
    }
  })
}

const webUserLogin = () => {
  apiWebUserLogin(formValue.value).then((res) => {
    if (res.code === 200) {
      if (formValue.value.remember) {
        localStorage.setItem('unionUserInfo', JSON.stringify(res.data))
        sessionStorage.removeItem('unionUserInfo')
      } else {
        localStorage.setItem('unionUserInfo', JSON.stringify(res.data))
        localStorage.removeItem('unionUserInfo')
      }
      notification.success({
        title: '登录成功',
        content: '欢迎回来！',
        duration: 3000
      })
      // 登录成功后跳转到首页或其他页面
      const unionUserInfo: WebUserLoginDetail = getUnionUserInfo()
      if (!unionUserInfo) {
        router.push('/')
      } else {
        for (const [_idx, user] of unionUserInfo?.unionUserInfo?.userList?.entries()) {
          if (user.unionUserUserCategory === 'WEB_USER') {
            if (user.currentRoleCode === 'WEB_USER') {
              router.push('/sys/people')
              break
            } else {
              router.push('/quiz/list')
              break
            }
          }
        }
      }
    } else {
      notification.error({
        title: '登录失败',
        content: res.message || '用户名或密码错误，请重试',
        duration: 3000
      })
    }
  }).catch((err) => {
    console.error(err)
    notification.error({
      title: '登录失败',
      content: '登录请求失败，请稍后再试',
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 注册跳转
const handleRegister = () => {
  router.push('/register')
}

// 忘记密码跳转
const handleForgotPassword = () => {
  message.info('跳转到找回密码页面')
  // router.push('/forgot-password')
}

// 显示用户协议
const showTerms = () => {
  uerAgreementModalRef.value.openModal()
}

// 显示隐私政策
const showPrivacy = () => {
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

:deep(.n-divider) {
  margin: 2rem 0;
}

:deep(.n-form-item) {
  margin-bottom: 4px;
}
</style>