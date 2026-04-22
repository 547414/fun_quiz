<template>
  <van-popup
    :show="show"
    @update:show="$emit('update:show', $event)"
    position="bottom"
    round
    :style="{ height: '92vh' }"
    class="flex flex-col"
  >
    <!-- 关闭按钮，不随内容滚动 -->
    <div class="absolute top-3 right-3 z-20">
      <button @click="$emit('update:show', false)" class="w-8 h-8 bg-black/20 rounded-full flex items-center justify-center">
        <van-icon name="cross" color="white" size="16"/>
      </button>
    </div>

    <!-- Intro 步骤 -->
    <template v-if="step === 'intro'">
      <van-loading v-if="introLoading" class="m-auto mt-40" color="#fff" size="32px"/>
      <template v-if="!introLoading && introError">
        <div class="flex-1 flex flex-col bg-gradient-to-br from-violet-500 to-purple-700 items-center justify-center px-8 text-white text-center gap-4">
          <div class="text-5xl">😢</div>
          <p>{{ introError }}</p>
        </div>
      </template>
      <template v-if="!introLoading && playData">
        <div class="flex-1 flex flex-col bg-gradient-to-br from-violet-500 to-purple-700 overflow-y-auto">
          <div class="flex-1 flex flex-col items-center justify-center px-8 pt-16 pb-8 text-white text-center">
            <img v-if="playData.covers?.[0]?.url" :src="playData.covers[0].url" class="w-40 h-40 object-cover rounded-3xl shadow-2xl mb-8"/>
            <div v-else class="w-40 h-40 bg-white/20 rounded-3xl flex items-center justify-center mb-8 text-6xl">🎯</div>
            <h1 class="text-3xl font-bold mb-3">{{ playData.quizName }}</h1>
            <p class="text-white/70 text-sm">共 {{ playData.questions.length }} 道题 · 测一测你是哪种类型</p>
          </div>
          <div class="px-8 pb-10">
            <van-button block round type="default" size="large" @click="startPlay" class="!bg-white !text-violet-700 !font-bold !text-lg shadow-xl">
              开始测试
            </van-button>
          </div>
        </div>
      </template>
    </template>

    <!-- Play 步骤 -->
    <template v-if="step === 'play'">
      <div class="flex flex-col h-full bg-gray-50 overflow-hidden">
        <template v-if="currentQuestion">
        <!-- 进度条，不滚动 -->
        <div class="bg-white px-4 pt-3 pb-3 shadow-sm flex-shrink-0">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs text-gray-400">{{ currentIndex + 1 }} / {{ visibleQuestions.length }}</span>
            <span class="text-xs text-gray-400">{{ playData?.quizName }}</span>
          </div>
          <van-progress :percentage="progress" :show-pivot="false" color="#7c3aed" track-color="#e5e7eb"/>
        </div>

        <!-- 题目内容，可滚动 -->
        <div class="flex-1 overflow-y-auto px-5 py-6">
          <!-- 题目图片（多图横排） -->
          <div v-if="currentQuestion.images?.length" class="flex gap-2 overflow-x-auto mb-4 pb-1">
            <img
              v-for="(img, i) in currentQuestion.images"
              :key="i"
              :src="img.url"
              class="h-40 w-auto rounded-2xl object-cover flex-shrink-0 cursor-pointer active:opacity-80"
              @click="previewImages(currentQuestion.images.map(x => x.url), i)"
            />
          </div>
          <p class="text-gray-800 text-lg font-medium leading-relaxed mb-6">{{ currentQuestion.content }}</p>
          <div class="space-y-3">
            <div
              v-for="opt in currentQuestion.options"
              :key="opt.key"
              @click="handleAnswer(opt.key)"
              class="flex flex-col bg-white rounded-2xl p-4 border-2 transition-all cursor-pointer active:scale-95"
              :class="answers[currentQuestion.seq] === opt.key ? 'border-violet-500 bg-violet-50' : 'border-transparent'"
            >
              <div class="flex items-center gap-4">
                <span
                  class="w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm font-bold flex-shrink-0 transition-all"
                  :class="answers[currentQuestion.seq] === opt.key ? 'border-violet-500 bg-violet-500 text-white' : 'border-gray-200 text-gray-400'"
                >{{ opt.key }}</span>
                <span class="text-gray-700 flex-1">{{ opt.label }}</span>
              </div>
              <!-- 选项图片 -->
              <div v-if="opt.images?.length" class="flex gap-2 overflow-x-auto mt-3 pl-12">
                <img
                  v-for="(img, i) in opt.images"
                  :key="i"
                  :src="img.url"
                  class="h-24 w-auto rounded-xl object-cover flex-shrink-0 cursor-pointer active:opacity-80"
                  @click.stop="previewImages(opt.images.map(x => x.url), i)"
                />
              </div>
            </div>
          </div>
        </div>

        </template>

        <!-- 底部导航，不滚动 -->
        <div class="bg-white border-t px-5 py-3 pb-safe-bottom flex gap-3 flex-shrink-0">
          <van-button plain round @click="handlePrev" :disabled="currentIndex === 0" class="flex-1">上一题</van-button>
          <van-button
            v-if="currentIndex < visibleQuestions.length - 1"
            round type="primary" color="#7c3aed"
            @click="handleNext"
            :disabled="!currentQuestion || !answers[currentQuestion.seq]"
            class="flex-1"
          >下一题</van-button>
          <van-button
            v-else
            round type="primary" color="#7c3aed"
            @click="handleSubmit"
            :disabled="!currentQuestion || !answers[currentQuestion.seq]"
            :loading="submitting"
            class="flex-1"
          >提交答案</van-button>
        </div>
      </div>
    </template>
  </van-popup>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { showToast, showImagePreview } from 'vant'
import {
  apiGetPlayData, apiSubmitAnswers,
  QuizPlayData, QuizQuestion,
} from '@/api/quizApi.ts'

const props = defineProps<{ token: string; quizId: string; show: boolean }>()
const emit = defineEmits<{
  (e: 'update:show', val: boolean): void
  (e: 'result', resultId: string): void
}>()

const step = ref<'intro' | 'play'>('intro')
const introLoading = ref(false)
const introError = ref('')
const playData = ref<QuizPlayData | null>(null)

const answers = ref<Record<number, string>>({})
const currentIndex = ref(0)
const submitting = ref(false)
const questionSeqOrder = ref<number[]>([])

const visibleQuestions = computed<QuizQuestion[]>(() => {
  if (!playData.value) {
    return []
  }
  const qMap = Object.fromEntries(playData.value.questions.map(q => [q.seq, q]))
  if (playData.value.quizType === 'branch') {
    return questionSeqOrder.value.map(seq => qMap[seq]).filter(Boolean)
  }
  return playData.value.questions.filter(q => !q.isHidden)
})

const currentQuestion = computed(() => visibleQuestions.value[currentIndex.value] || null)
const progress = computed(() => Math.round((currentIndex.value / Math.max(visibleQuestions.value.length, 1)) * 100))

const previewImages = (urls: string[], startPosition: number) => {
  showImagePreview({ images: urls, startPosition })
}

const resetPlay = () => {
  step.value = 'intro'
  answers.value = {}
  currentIndex.value = 0
  submitting.value = false
  questionSeqOrder.value = []
  playData.value = null
  introError.value = ''
}

const loadIntro = () => {
  introLoading.value = true
  introError.value = ''
  apiGetPlayData({ token: props.token, quizId: props.quizId }).then(res => {
    if (res.code === 200) {
      playData.value = res.data
      if (res.data.quizType === 'branch' && res.data.questions.length) {
        questionSeqOrder.value = [res.data.questions[0].seq]
      }
    } else {
      introError.value = res.message || '无法加载测验'
    }
  }).catch(() => {
    introError.value = '网络异常，请重试'
  }).finally(() => {
    introLoading.value = false
  })
}

const startPlay = () => {
  step.value = 'play'
}

const handleAnswer = (key: string) => {
  if (!currentQuestion.value) {
    return
  }
  answers.value[currentQuestion.value.seq] = key
  if (playData.value?.quizType === 'branch') {
    const opt = currentQuestion.value.options.find(o => o.key === key)
    const nextSeq = opt?.nextQuestionSeq
    if (nextSeq !== undefined && nextSeq !== -1) {
      if (!questionSeqOrder.value.includes(nextSeq)) {
        questionSeqOrder.value = [...questionSeqOrder.value.slice(0, currentIndex.value + 1), nextSeq]
      }
    }
  }
  if (playData.value?.quizType !== 'branch' && currentIndex.value < visibleQuestions.value.length - 1) {
    setTimeout(() => { currentIndex.value++ }, 200)
  }
}

const handlePrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const handleNext = () => {
  if (currentIndex.value < visibleQuestions.value.length - 1) {
    currentIndex.value++
  }
}

const handleSubmit = () => {
  const unanswered = visibleQuestions.value.filter(q => !answers.value[q.seq])
  if (unanswered.length) {
    showToast('请回答所有题目')
    return
  }
  const fullAnswers: Record<string, string> = {}
  Object.entries(answers.value).forEach(([seq, key]) => {
    fullAnswers[seq] = key
  })
  submitting.value = true
  apiSubmitAnswers({ token: props.token, quizId: props.quizId, answers: fullAnswers }).then(res => {
    if (res.code === 200) {
      emit('update:show', false)
      emit('result', res.data.resultId)
    } else {
      showToast(res.message || '提交失败，请重试')
    }
  }).finally(() => {
    submitting.value = false
  })
}

watch(() => [props.show, props.quizId] as const, ([show]) => {
  if (show) {
    resetPlay()
    loadIntro()
  }
}, { immediate: false })
</script>
