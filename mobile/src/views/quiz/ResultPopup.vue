<template>
  <van-popup
    :show="show"
    @update:show="$emit('update:show', $event)"
    position="bottom"
    round
    :style="{ height: '92vh' }"
    class="flex flex-col"
  >
    <!-- 关闭按钮：固定在弹窗右上角，不随内容滚动 -->
    <div class="absolute top-3 right-3 z-20">
      <button @click="$emit('update:show', false)" class="w-8 h-8 bg-black/20 rounded-full flex items-center justify-center">
        <van-icon name="cross" color="white" size="16"/>
      </button>
    </div>

    <van-loading v-if="loading" class="m-auto mt-40" color="#7c3aed" size="32px"/>

    <div v-if="!loading && result" class="flex-1 overflow-y-auto" :style="bgStyle">
      <div class="flex flex-col items-center pt-16 pb-8 px-6 text-center">
        <p class="result-stroke-text result-stroke-text--subtle text-sm text-white/60 mb-2">你的人格类型是</p>
        <h1 class="result-stroke-text text-4xl font-black text-white mb-1">{{ result.outcomeName }}</h1>
        <p class="result-stroke-text result-stroke-text--subtle text-white/80 font-mono text-lg">{{ result.outcomeCode }}</p>
        <img
          v-if="result.outcomeAvatar?.url"
          :src="result.outcomeAvatar.url"
          class="w-48 h-48 object-cover rounded-3xl shadow-2xl my-8 cursor-pointer active:opacity-80"
          @click="showImagePreview({ images: [result.outcomeAvatar.url] })"
        />
        <div v-else class="w-40 h-40 bg-white/20 rounded-3xl flex items-center justify-center my-8 text-7xl">🎯</div>
        <div v-if="result.score !== null" class="bg-white/20 rounded-2xl px-6 py-3 mb-4">
          <span class="result-stroke-text result-stroke-text--subtle text-white/70 text-sm">匹配度 </span>
          <span class="result-stroke-text text-white text-2xl font-bold">{{ result.score }}%</span>
        </div>
      </div>
      <div class="bg-white rounded-t-4xl px-6 pt-8 pb-6 space-y-6">
        <div v-if="result.outcomeTags?.length" class="flex flex-wrap gap-2">
          <span v-for="tag in result.outcomeTags" :key="tag"
            class="px-3 py-1 bg-violet-100 text-violet-700 rounded-full text-sm font-medium">
            {{ tag }}
          </span>
        </div>
        <p v-if="result.outcomeSummary" class="text-gray-700 text-base font-medium leading-relaxed">
          {{ result.outcomeSummary }}
        </p>
        <div v-if="result.outcomeDetail" class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
          {{ result.outcomeDetail }}
        </div>
        <div v-if="result.shareImage?.url" class="space-y-2">
          <p class="text-sm text-gray-500">保存图片分享给朋友</p>
          <img
            :src="result.shareImage.url"
            class="w-full rounded-2xl shadow-md cursor-pointer active:opacity-80"
            @click="showImagePreview({ images: [result.shareImage.url] })"
          />
        </div>
      </div>
    </div>

    <!-- 底部按钮：固定在弹窗底部，不随内容滚动 -->
    <div v-if="!loading && result" class="bg-white border-t px-5 py-3 pb-safe-bottom flex gap-3 flex-shrink-0">
      <van-button plain round class="flex-1" @click="$emit('update:show', false)">关闭</van-button>
      <van-button plain round class="flex-1" @click="handleShare">分享</van-button>
      <van-button round type="primary" color="#7c3aed" class="flex-1" @click="handleSaveImage" v-if="result.shareImage?.url">
        保存图片
      </van-button>
    </div>
  </van-popup>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { showToast, showImagePreview } from 'vant'
import { apiGetResult, QuizResultData } from '@/api/quizApi.ts'

const props = defineProps<{ token: string; resultId: string; show: boolean }>()
defineEmits<{ (e: 'update:show', val: boolean): void }>()

const loading = ref(false)
const result = ref<QuizResultData | null>(null)

const bgStyle = computed(() => {
  const cfg = result.value?.resultConfig || {}
  return { background: (cfg as any).bgColor || 'linear-gradient(135deg, #7c3aed, #9333ea)' }
})

const handleShare = () => {
  if (!result.value) {
    return
  }
  const shareUrl = `${location.origin}/quiz/result?token=${props.token}&resultId=${props.resultId}`
  if (navigator.share) {
    navigator.share({ title: result.value.quizName || '趣味测验', text: `我的结果是：${result.value.outcomeName}`, url: shareUrl })
  } else {
    navigator.clipboard.writeText(shareUrl)
    showToast('链接已复制')
  }
}

const handleSaveImage = () => {
  if (!result.value?.shareImage?.url) {
    return
  }
  const a = document.createElement('a')
  a.href = result.value.shareImage.url
  a.download = `${result.value.outcomeName}.png`
  a.click()
}

watch(() => [props.show, props.resultId] as const, ([show, resultId]) => {
  if (!show || !resultId) {
    return
  }
  loading.value = true
  result.value = null
  apiGetResult({ token: props.token, resultId }).then(res => {
    if (res.code === 200) {
      result.value = res.data
    }
  }).finally(() => {
    loading.value = false
  })
}, { immediate: false })
</script>

<style scoped>
.result-stroke-text {
  -webkit-text-stroke: 1px rgba(15, 23, 42, 0.72);
  paint-order: stroke fill;
  text-shadow: 0 1px 2px rgba(15, 23, 42, 0.28);
}
.result-stroke-text--subtle {
  -webkit-text-stroke-width: 0.6px;
  -webkit-text-stroke-color: rgba(15, 23, 42, 0.62);
  text-shadow: 0 1px 1px rgba(15, 23, 42, 0.22);
}
</style>
