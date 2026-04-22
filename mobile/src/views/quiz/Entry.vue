<template>
  <div class="h-screen flex flex-col bg-gray-50 overflow-hidden">
    <van-loading v-if="loading" class="flex items-center justify-center flex-1" color="#7c3aed" size="36px"/>

    <template v-if="!loading && error">
      <div class="flex items-center justify-center flex-1">
        <div class="text-center space-y-3 p-8">
          <div class="text-5xl">😢</div>
          <p class="text-gray-600">{{ error }}</p>
        </div>
      </div>
    </template>

    <template v-if="!loading && entryData">
      <!-- 顶部状态栏 -->
      <div class="bg-gradient-to-br from-violet-500 to-purple-700 px-5 pt-safe-top pb-6 flex-shrink-0">
        <div class="pt-4 flex items-start justify-between">
          <div>
            <p class="text-white/70 text-sm mb-1">你的专属测验通行证</p>
            <div class="flex items-center gap-3">
              <span
                class="px-3 py-1 rounded-full text-xs font-bold"
                :class="statusBadgeClass"
              >{{ statusLabel }}</span>
              <span v-if="entryData.maxUses !== null" class="text-white/60 text-sm">
                已用 {{ entryData.usedCount }} / {{ entryData.maxUses }} 次
              </span>
              <span v-else class="text-white/60 text-sm">无限次数</span>
            </div>
          </div>
          <button
            v-if="entryData.hasHistory"
            @click="showHistory = true"
            class="flex flex-col items-center gap-0.5 text-white/80 active:text-white"
          >
            <van-icon name="records-o" size="22"/>
            <span class="text-xs">历史</span>
          </button>
        </div>
      </div>

      <!-- 搜索框（固定，不随列表滚动） -->
      <div v-if="canPlay" class="bg-white flex-shrink-0 border-b border-gray-100">
        <div class="px-4 pt-3 pb-0">
          <h2 class="text-base font-semibold text-gray-700">选个测验开始吧</h2>
        </div>
        <van-search
          v-model="quizSearch"
          placeholder="搜索测验名称"
          background="transparent"
          shape="round"
          @update:model-value="onQuizSearch"
        />
      </div>

      <!-- 可滚动内容区 -->
      <div class="flex-1 overflow-auto pb-20">
        <template v-if="canPlay">
          <van-list
            v-model:loading="quizListLoading"
            :finished="quizFinished"
            finished-text="没有更多了"
            @load="loadMoreQuizzes"
            class="px-4 mt-3 space-y-3"
          >
            <div
              v-for="quiz in quizList"
              :key="quiz.quizId"
              @click="goPlay(quiz.quizId)"
              class="bg-white rounded-2xl p-4 flex items-center gap-4 shadow-sm active:scale-95 transition-transform cursor-pointer"
            >
              <img
                v-if="quiz.covers?.[0]?.url"
                :src="quiz.covers[0].url"
                class="w-14 h-14 rounded-xl object-cover flex-shrink-0 cursor-pointer active:opacity-80"
                @click.stop="showImagePreview({ images: [quiz.covers[0].url] })"
              />
              <div v-else class="w-14 h-14 rounded-xl bg-violet-100 flex items-center justify-center text-2xl flex-shrink-0">🎯</div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-800 truncate">{{ quiz.quizName }}</p>
                <p v-if="quiz.shareDesc" class="text-xs text-gray-400 mt-0.5 truncate">{{ quiz.shareDesc }}</p>
              </div>
              <van-icon name="arrow" class="text-gray-300"/>
            </div>
            <p v-if="quizFinished && quizList.length === 0" class="text-center text-gray-400 text-sm py-6">没有匹配的测验</p>
          </van-list>
        </template>

        <template v-else>
          <div class="mx-4 mt-4 bg-amber-50 border border-amber-200 rounded-2xl p-4 text-center">
            <p class="text-amber-700 font-medium">{{ exhaustedMsg }}</p>
          </div>
        </template>
      </div>
    </template>

    <QuizFlowPopup
      v-model:show="showQuizFlow"
      :token="token"
      :quiz-id="selectedQuizId"
      @result="onQuizResult"
    />

    <HistoryPopup
      ref="historyPopup"
      v-model:show="showHistory"
      :token="token"
      @select-result="onSelectResult"
    />

    <ResultPopup
      v-model:show="showResult"
      :token="token"
      :result-id="selectedResultId"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, useTemplateRef } from 'vue'
import { useRoute } from 'vue-router'
import { showImagePreview } from 'vant'
import { apiGetQuizEntry, QuizEntryData, apiGetEntryQuizzes, PublishedQuiz } from '@/api/quizApi.ts'
import HistoryPopup from './HistoryPopup.vue'
import ResultPopup from './ResultPopup.vue'
import QuizFlowPopup from './QuizFlowPopup.vue'

const route = useRoute()
const token = route.query.token as string
const loading = ref(true)
const error = ref('')
const entryData = ref<QuizEntryData | null>(null)

const quizList = ref<PublishedQuiz[]>([])
const quizPage = ref(0)
const quizFinished = ref(false)
const quizListLoading = ref(false)
const quizSearch = ref('')
let quizSearchTimer: ReturnType<typeof setTimeout> | null = null

const historyPopupRef = useTemplateRef('historyPopup')
const showHistory = ref(false)
const showResult = ref(false)
const selectedResultId = ref('')
const showQuizFlow = ref(false)
const selectedQuizId = ref('')

const canPlay = computed(() => entryData.value?.status === 'active')

const statusLabel = computed(() => {
  switch (entryData.value?.status) {
    case 'active': return '可用'
    case 'exhausted': return '已用完'
    case 'expired': return '已过期'
    default: return ''
  }
})

const statusBadgeClass = computed(() => {
  switch (entryData.value?.status) {
    case 'active': return 'bg-green-400 text-white'
    case 'exhausted': return 'bg-amber-400 text-white'
    case 'expired': return 'bg-red-400 text-white'
    default: return 'bg-gray-400 text-white'
  }
})

const exhaustedMsg = computed(() => {
  if (entryData.value?.status === 'expired') {
    return '此通行证已过期，无法继续测验'
  }
  return '测验次数已用完，点击右上角查看历史记录吧'
})

const loadMoreQuizzes = () => {
  const nextPage = quizPage.value + 1
  apiGetEntryQuizzes({ token, search: quizSearch.value, pageIndex: nextPage, pageSize: 20 }).then(res => {
    if (res.code === 200) {
      quizList.value.push(...res.data.data)
      quizPage.value = nextPage
      quizFinished.value = quizList.value.length >= res.data.filterCount
    } else {
      quizFinished.value = true
    }
  }).catch(() => {
    quizFinished.value = true
  }).finally(() => {
    quizListLoading.value = false
  })
}

const onQuizSearch = () => {
  if (quizSearchTimer) {
    clearTimeout(quizSearchTimer)
  }
  quizSearchTimer = setTimeout(() => {
    quizList.value = []
    quizPage.value = 0
    quizFinished.value = false
    quizListLoading.value = true
    loadMoreQuizzes()
  }, 300)
}

const goPlay = (quizId: string) => {
  selectedQuizId.value = quizId
  showQuizFlow.value = true
}

const onQuizResult = (resultId: string) => {
  historyPopupRef.value?.reset()
  selectedResultId.value = resultId
  showResult.value = true
  apiGetQuizEntry({ token }).then(res => {
    if (res.code === 200) {
      entryData.value = res.data
    }
  })
}

const onSelectResult = (resultId: string) => {
  showHistory.value = false
  selectedResultId.value = resultId
  showResult.value = true
}

onMounted(() => {
  if (!token) {
    error.value = '无效的访问链接'
    loading.value = false
    return
  }
  apiGetQuizEntry({ token }).then(res => {
    if (res.code !== 200) {
      error.value = res.message || '链接无效'
    } else {
      entryData.value = res.data
    }
  }).catch(() => {
    error.value = '网络异常，请稍后重试'
  }).finally(() => {
    loading.value = false
  })
})
</script>
