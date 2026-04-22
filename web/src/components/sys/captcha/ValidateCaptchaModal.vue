<template>
  <n-modal
      v-model:show="dialogVisible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      :closable="false"
      preset="card"
      class="validate-modal"
      :style="{ maxWidth: '450px' }"
  >
    <template #header>
      <div class="flex items-center">
        <Icon icon="fluent:shield-checkmark-20-filled" class="text-indigo-500 text-xl mr-2"/>
        <span class="text-lg font-semibold text-gray-800">安全验证</span>
        <n-button
            text
            class="ml-auto -mr-2"
            @click="closeModal"
        >
          <Icon
              icon="fluent:dismiss-circle-20-regular"
              class="text-xl text-gray-400 hover:text-gray-600 transition-colors"
          />
        </n-button>
      </div>
    </template>
    <div style="padding: 0 16px 16px 16px">
      <div class="space-y-4">
        <!-- 验证码图片容器 -->
        <div class="relative bg-gray-50 rounded-lg overflow-hidden">
          <n-spin :show="captchaLoading" size="large">
            <div class="captcha-container relative" style="min-height: 280px">
              <img
                  v-if="captchaDetail?.captchaBase64 && !captchaLoading"
                  :src="captchaDetail.captchaBase64"
                  class="w-full cursor-pointer select-none rounded-lg"
                  @click="handleCaptchaClick"
                  alt="验证码"
              />
              <!-- 点击标记 -->
              <div
                  v-for="(point, index) in clickPoints"
                  :key="`point-${index}`"
                  class="absolute w-6 h-6 bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-lg transform -translate-x-1/2 -translate-y-1/2 pointer-events-none z-10"
                  :style="{ left: `${point.x}px`, top: `${point.y}px` }"
              >
                {{ index + 1 }}
              </div>
            </div>
          </n-spin>
        </div>

        <!-- 文字提示区域 -->
        <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-4" style="min-height: 110px">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <Icon icon="fluent:cursor-click-20-regular" class="text-indigo-600 text-lg mr-2"/>
              <span class="text-sm font-medium text-gray-700">请依次点击：</span>
            </div>
            <div class="flex items-center gap-2">
              <n-button
                  text
                  size="small"
                  @click="resetClick"
                  :disabled="clickPoints.length === 0"
              >
                <Icon
                    icon="fluent:arrow-sync-circle-20-regular"
                    class="text-lg text-indigo-500 hover:text-indigo-600 transition-colors"
                />
              </n-button>
              <n-tag
                  :type="clickPoints.length === 3 ? 'success' : 'default'"
                  size="small"
                  round
              >
                {{ clickPoints.length }}/3
              </n-tag>
            </div>
          </div>

          <div class="flex items-center mt-3 space-x-4">
            <template v-if="captchaDetail && !captchaLoading">
              <div
                  v-for="(text, idx) in captchaDetail.correctTexts"
                  :key="`text-${idx}`"
                  class="text-center group"
              >
                <div class="text-xs text-indigo-600 font-medium">
                  {{ captchaDetail.correctPinyinTexts[idx] }}
                </div>
                <div class="text-lg font-bold text-gray-800 group-hover:text-indigo-600 transition-colors">
                  {{ text }}
                </div>
              </div>
            </template>
            <n-skeleton v-else text :repeat="3" class="flex-1 mt-5"/>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-3 mt-4">
          <n-button
              size="large"
              block
              @click="generateCaptcha"
              :disabled="captchaLoading"
              class="flex-1"
          >
            <template #icon>
              <Icon icon="fluent:arrow-counterclockwise-20-regular"/>
            </template>
            刷新
          </n-button>
          <n-button
              type="primary"
              size="large"
              block
              @click="onValidate"
              :disabled="clickPoints.length < 3"
              :loading="validating"
              class="flex-1"
          >
            <template #icon>
              <Icon icon="fluent:checkmark-circle-20-filled" v-if="!validating"/>
            </template>
            验证
          </n-button>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {NModal, NButton, NSpin, NTag, NSkeleton, useNotification} from 'naive-ui'
import {Icon} from '@iconify/vue'
import {
  apiGenerateCaptcha,
  apiValidateCaptcha,
  CaptchaDetail,
  ValidateCaptchaParams,
  ValidateCaptchaTextPositionsParams
} from '@/api/captchaApi.ts'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts";

const notification = useNotification()
const dialogVisible = ref(false)
const captchaLoading = ref(false)
const validating = ref(false)
const captchaDetail = ref<CaptchaDetail>()
const clickPoints = ref<{ x: number; y: number }[]>([])

const emit = defineEmits(['operateSuccess'])

const closeModal = () => {
  dialogVisible.value = false
}

const openModal = () => {
  dialogVisible.value = true
  generateCaptcha()
}

const generateCaptcha = async () => {
  clickPoints.value = []
  captchaLoading.value = true

  try {
    const res = await apiGenerateCaptcha()
    if (res.code === 200) {
      captchaDetail.value = res.data
    } else {
      notification.error({
        title: '错误',
        content: res.message || '获取验证码失败，请重试',
        duration: 3000
      })
    }
  } catch (err) {
    console.error(err)
    notification.error({
      title: '错误',
      content: '获取验证码失败，请检查网络连接',
      duration: 3000
    })
  } finally {
    captchaLoading.value = false
  }
}

const handleCaptchaClick = (event: MouseEvent) => {
  if (clickPoints.value.length >= 3) {
    notification.warning({
      title: '警告',
      content: '已选择3个点，请点击验证或重置',
      duration: 3000
    })
    return
  }

  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()

  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  clickPoints.value.push({x: Math.round(x), y: Math.round(y)})
}

const resetClick = () => {
  clickPoints.value = []
  notification.info({
    title: '提示',
    content: '已重置选择，请重新点击验证码',
    duration: 3000
  })
}

const onValidate = async () => {
  if (clickPoints.value.length < 3) {
    notification.warning({
      title: '警告',
      content: '请点击3个位置',
      duration: 3000
    })
    return
  }

  validating.value = true

  const textPositions: ValidateCaptchaTextPositionsParams[] = clickPoints.value.map((point, idx) => ({
    text: captchaDetail.value!.correctTexts[idx],
    x: point.x,
    y: point.y
  }))

  const params: ValidateCaptchaParams = {
    captchaId: captchaDetail.value!.captchaId,
    textPositions
  }

  apiValidateCaptcha(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '验证成功',
        content: '请继续操作',
        duration: 3000
      })
      emit('operateSuccess', {
        validateCaptchaAuthCode: res.data,
        captchaId: captchaDetail.value!.captchaId
      })
      dialogVisible.value = false
    } else {
      notification.error({
        title: '错误',
        content: res.message || '验证失败，请重试',
        duration: 3000
      })
      generateCaptcha()
    }
  }).catch((err) => {
    notification.error({
      title: '错误',
      content: `验证请求失败: ${err.message || '请稍后再试'}`,
      duration: 3000
    })
    generateCaptcha()
  }).finally(() => {
    validating.value = false
  })
}

defineExpose({
  openModal
})
</script>

<style scoped lang="scss">
:deep(.n-card) {
  border-radius: 1.5rem;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

:deep(.n-card-header) {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

:deep(.n-card__content) {
  padding: 1.5rem;
}

.captcha-container {
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.n-spin-content) {
  width: 100%;
}

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

:deep(.n-tag) {
  background-color: rgba(99, 102, 241, 0.1);
  color: #6366f1;

  &.n-tag--success-type {
    background-color: rgba(16, 185, 129, 0.1);
    color: #10b981;
  }
}
</style>