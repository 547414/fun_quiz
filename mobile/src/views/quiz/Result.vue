<template>
  <div class="min-h-screen flex flex-col" :style="bgStyle">
    <van-loading v-if="loading" class="m-auto mt-40" color="#7c3aed" size="32px"/>

    <template v-if="!loading && result">
      <!-- 顶部 -->
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

        <!-- 匹配度（vector/score类型） -->
        <div v-if="result.score !== null" class="bg-white/20 rounded-2xl px-6 py-3 mb-4">
          <span class="result-stroke-text result-stroke-text--subtle text-white/70 text-sm">匹配度 </span>
          <span class="result-stroke-text text-white text-2xl font-bold">{{ result.score }}%</span>
        </div>
      </div>

      <!-- 内容卡片 -->
      <div class="flex-1 bg-white rounded-t-4xl px-6 pt-8 pb-20 space-y-6">
        <!-- 标签 -->
        <div v-if="result.outcomeTags?.length" class="flex flex-wrap gap-2">
          <span v-for="tag in result.outcomeTags" :key="tag"
              class="px-3 py-1 bg-violet-100 text-violet-700 rounded-full text-sm font-medium">
            {{ tag }}
          </span>
        </div>

        <!-- 简介 -->
        <p v-if="result.outcomeSummary" class="text-gray-700 text-base font-medium leading-relaxed">
          {{ result.outcomeSummary }}
        </p>

        <!-- 详细文案 -->
        <div v-if="result.outcomeDetail" class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
          {{ result.outcomeDetail }}
        </div>

        <!-- 分享图 -->
        <div v-if="result.shareImage?.url" class="space-y-2">
          <p class="text-sm text-gray-500">保存图片分享给朋友</p>
          <img
            :src="result.shareImage.url"
            class="w-full rounded-2xl shadow-md cursor-pointer active:opacity-80"
            @click="showImagePreview({ images: [result.shareImage.url] })"
          />
        </div>
      </div>

      <!-- 底部固定 -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t px-5 py-3 pb-safe-bottom flex gap-3">
        <van-button plain round class="flex-1" @click="router.push({ name: 'QuizEntry', query: { token } })">再测一个</van-button>
        <van-button plain round class="flex-1" @click="handleShare">分享</van-button>
        <van-button round type="primary" color="#7c3aed" class="flex-1" @click="handleSaveImage" v-if="result.shareImage?.url">
          保存图片
        </van-button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { showToast, showImagePreview } from 'vant';
import { apiGetResult, QuizResultData, GetResultParams } from '@/api/quizApi.ts';

const route = useRoute();
const router = useRouter();
const token = route.query.token as string
const resultId = route.query.resultId as string
const loading = ref(true);
const result = ref<QuizResultData | null>(null);

const bgStyle = computed(() => {
  const cfg = result.value?.resultConfig || {};
  return { background: cfg.bgColor || 'linear-gradient(135deg, #7c3aed, #9333ea)' };
});

const handleShare = () => {
  if (navigator.share) {
    navigator.share({ title: result.value?.quizName || '趣味测验', text: `我的结果是：${result.value?.outcomeName}`, url: location.href });
  } else {
    navigator.clipboard.writeText(location.href);
    showToast('链接已复制');
  }
};

const handleSaveImage = () => {
  if (!result.value?.shareImage?.url) return;
  const a = document.createElement('a');
  a.href = result.value.shareImage.url;
  a.download = `${result.value.outcomeName}.png`;
  a.click();
};

onMounted(() => {
  const getResultParams: GetResultParams = {
    token: token,
    resultId : resultId
  }
  apiGetResult(getResultParams).then(res => {
    if (res.code === 200) {
      result.value = res.data
    }
  }).finally(() => {
    loading.value = false
  });
});
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
