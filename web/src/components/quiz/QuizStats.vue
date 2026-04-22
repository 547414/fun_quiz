<template>
  <div class="space-y-6">
    <div class="grid grid-cols-3 gap-4">
      <div class="bg-white rounded-xl p-5 border border-gray-100">
        <p class="text-sm text-gray-500">Token总数</p>
        <p class="text-3xl font-bold text-gray-800 mt-1">{{ stats?.totalTokens ?? '-' }}</p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-gray-100">
        <p class="text-sm text-gray-500">已使用</p>
        <p class="text-3xl font-bold text-violet-600 mt-1">{{ stats?.usedTokens ?? '-' }}</p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-gray-100">
        <p class="text-sm text-gray-500">核销率</p>
        <p class="text-3xl font-bold text-green-600 mt-1">
          {{ stats ? Math.round(stats.usedTokens / (stats.totalTokens || 1) * 100) : '-' }}%
        </p>
      </div>
    </div>

    <div class="bg-white rounded-xl p-5 border border-gray-100">
      <p class="font-medium text-gray-700 mb-4">结果分布</p>
      <div v-if="stats?.outcomeDistribution?.length" class="space-y-3">
        <div v-for="item in stats.outcomeDistribution" :key="item.outcomeCode" class="flex items-center gap-3">
          <span class="text-sm w-32 truncate text-gray-700">{{ item.outcomeName || item.outcomeCode }}</span>
          <div class="flex-1 bg-gray-100 rounded-full h-2">
            <div class="bg-violet-500 h-2 rounded-full transition-all" :style="{ width: barWidth(item.count) + '%' }"/>
          </div>
          <span class="text-sm text-gray-500 w-12 text-right">{{ item.count }}</span>
        </div>
      </div>
      <div v-else class="text-gray-400 text-sm text-center py-8">暂无数据</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { apiGetQuizStats, QuizStats, GetQuizStatsParams } from '@/api/quizApi.ts';

const props = defineProps<{ quizId: string }>();
const stats = ref<QuizStats | null>(null);

const maxCount = computed(() => Math.max(...(stats.value?.outcomeDistribution?.map(i => i.count) || [1])))
const barWidth = (count: number) => Math.round(count / maxCount.value * 100)

onMounted(() => {
  const getQuizStatsParams: GetQuizStatsParams = {
    quizId: props.quizId,
  }
  apiGetQuizStats(getQuizStatsParams).then(res => {
    if (res.code === 200) {
      stats.value = res.data
    }
  })
})
</script>
