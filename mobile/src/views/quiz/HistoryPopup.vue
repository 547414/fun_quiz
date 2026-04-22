<template>
  <van-popup
    :show="show"
    @update:show="$emit('update:show', $event)"
    position="bottom"
    round
    :style="{ maxHeight: '70vh' }"
    class="flex flex-col"
  >
    <div class="flex items-center justify-between px-4 pt-4 pb-2">
      <span class="text-base font-semibold text-gray-800">历史记录</span>
      <van-icon name="cross" class="text-gray-400" size="18" @click="$emit('update:show', false)"/>
    </div>
    <van-search
      v-model="search"
      placeholder="搜索测验或结果"
      background="transparent"
      shape="round"
      @update:model-value="onSearch"
    />
    <van-list
      v-model:loading="listLoading"
      :finished="finished"
      finished-text="没有更多了"
      @load="loadMore"
      class="overflow-y-auto px-4 pb-6 mt-1 space-y-3"
    >
      <div
        v-for="item in list"
        :key="item.resultId"
        @click="$emit('select-result', item.resultId)"
        class="bg-gray-50 rounded-2xl p-4 flex items-center gap-4 active:scale-95 transition-transform cursor-pointer"
      >
        <div class="w-12 h-12 rounded-xl bg-violet-100 flex items-center justify-center flex-shrink-0">
          <img
            v-if="item.outcomeAvatar?.url"
            :src="item.outcomeAvatar.url"
            class="w-12 h-12 rounded-xl object-cover cursor-pointer active:opacity-80"
            @click.stop="showImagePreview({ images: [item.outcomeAvatar.url] })"
          />
          <span v-else class="text-xl">🎯</span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-xs text-gray-400">{{ item.quizName }}</p>
          <p class="font-medium text-gray-800 truncate">{{ item.outcomeName }}</p>
          <p v-if="item.outcomeSummary" class="text-xs text-gray-400 truncate">{{ item.outcomeSummary }}</p>
        </div>
        <div class="text-right flex-shrink-0">
          <span v-if="item.score !== null" class="text-xs text-violet-500 font-bold">{{ item.score }}%</span>
          <van-icon name="arrow" class="text-gray-300 ml-2"/>
        </div>
      </div>
      <p v-if="finished && list.length === 0" class="text-center text-gray-400 text-sm py-6">没有匹配的记录</p>
    </van-list>
  </van-popup>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showImagePreview } from 'vant'
import { apiGetEntryHistory, HistoryItem } from '@/api/quizApi.ts'

const props = defineProps<{ token: string; show: boolean }>()
defineEmits<{
  (e: 'update:show', val: boolean): void
  (e: 'select-result', resultId: string): void
}>()

const list = ref<HistoryItem[]>([])
const page = ref(0)
const finished = ref(false)
const listLoading = ref(false)
const search = ref('')
let searchTimer: ReturnType<typeof setTimeout> | null = null

const loadMore = () => {
  const nextPage = page.value + 1
  apiGetEntryHistory({ token: props.token, search: search.value, pageIndex: nextPage, pageSize: 20 }).then(res => {
    if (res.code === 200) {
      list.value.push(...res.data.data)
      page.value = nextPage
      finished.value = list.value.length >= res.data.filterCount
    } else {
      finished.value = true
    }
  }).catch(() => {
    finished.value = true
  }).finally(() => {
    listLoading.value = false
  })
}

const onSearch = () => {
  if (searchTimer) {
    clearTimeout(searchTimer)
  }
  searchTimer = setTimeout(() => {
    list.value = []
    page.value = 0
    finished.value = false
    listLoading.value = true
    loadMore()
  }, 300)
}

const reset = () => {
  list.value = []
  page.value = 0
  finished.value = false
  search.value = ''
}

defineExpose({ reset })
</script>
