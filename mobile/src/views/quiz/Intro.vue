<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-violet-500 to-purple-700">
    <van-loading v-if="loading" class="m-auto mt-40" color="#fff" size="32px"/>

    <template v-if="!loading && errorMsg">
      <div class="flex-1 flex flex-col items-center justify-center px-8 text-white text-center">
        <div class="text-6xl mb-6">😢</div>
        <p class="text-lg mb-8">{{ errorMsg }}</p>
        <van-button round type="default" size="normal" @click="goEntry" class="!bg-white !text-violet-700 !font-bold px-8">
          返回入口查看历史记录
        </van-button>
      </div>
    </template>

    <template v-if="!loading && playData">
      <!-- 封面 -->
      <div class="flex-1 flex flex-col items-center justify-center px-8 pt-16 pb-8 text-white text-center">
        <img v-if="playData.covers?.[0]?.url" :src="playData.covers[0].url" class="w-40 h-40 object-cover rounded-3xl shadow-2xl mb-8"/>
        <div v-else class="w-40 h-40 bg-white/20 rounded-3xl flex items-center justify-center mb-8 text-6xl">🎯</div>
        <h1 class="text-3xl font-bold mb-3">{{ playData.quizName }}</h1>
        <p class="text-white/70 text-sm">共 {{ playData.questions.length }} 道题 · 测一测你是哪种类型</p>
      </div>

      <!-- 开始按钮 -->
      <div class="px-8 pb-16 space-y-3">
        <van-button block round type="default" size="large" @click="startPlay" class="!bg-white !text-violet-700 !font-bold !text-lg shadow-xl">
          开始测试
        </van-button>
        <p class="text-white/50 text-xs text-center">完成后可在入口页查看历史记录</p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiGetPlayData, QuizPlayData, PlayDataParams } from '@/api/quizApi.ts';

const route = useRoute();
const router = useRouter();
const token = route.query.token as string;
const quizId = route.query.quizId as string;
const loading = ref(true);
const playData = ref<QuizPlayData | null>(null);
const errorMsg = ref('');

const startPlay = () => router.push({ name: 'QuizPlay', query: { token, quizId } })
const goEntry = () => router.replace({ name: 'QuizEntry', query: { token } })

onMounted(() => {
  const playDataParams: PlayDataParams = {
    token: token,
    quizId: quizId,
  }
  apiGetPlayData(playDataParams).then(res => {
    if (res.code === 200) {
      playData.value = res.data
    } else {
      errorMsg.value = res.message || '无法开始测验'
    }
  }).catch((err) => {
    errorMsg.value = typeof err === 'string' ? err : '测验次数已用完或链接已失效'
  }).finally(() => {
    loading.value = false
  })
})
</script>
