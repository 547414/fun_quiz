<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <van-loading v-if="loading" class="m-auto mt-40" color="#7c3aed" size="32px"/>

    <template v-if="!loading && errorMsg">
      <div class="flex-1 flex flex-col items-center justify-center px-8 text-center gap-5">
        <div class="text-5xl">😵</div>
        <p class="text-gray-700 font-medium text-lg">{{ errorMsg }}</p>
        <van-button round type="primary" color="#7c3aed" @click="router.replace({ name: 'QuizEntry', query: { token } })">
          返回首页
        </van-button>
      </div>
    </template>

    <template v-if="!loading && !errorMsg && currentQuestion">
      <!-- 进度条 -->
      <div class="sticky top-0 bg-white px-4 pt-safe-top pb-3 shadow-sm z-10">
        <div class="h-3"></div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs text-gray-400">{{ currentIndex + 1 }} / {{ visibleQuestions.length }}</span>
          <span class="text-xs text-gray-400">{{ playData?.quizName }}</span>
        </div>
        <van-progress :percentage="progress" :show-pivot="false" color="#7c3aed" track-color="#e5e7eb"/>
      </div>

      <!-- 题目 -->
      <div class="flex-1 px-5 py-6">
        <!-- 题目图片 -->
        <div v-if="currentQuestion.images?.length" class="flex gap-2 overflow-x-auto mb-4 pb-1">
          <img
            v-for="(img, i) in currentQuestion.images"
            :key="i"
            :src="img.url"
            class="h-40 w-auto rounded-2xl object-cover flex-shrink-0 cursor-pointer active:opacity-80"
            @click="previewImages(currentQuestion.images.map(x => x.url), i)"
          />
        </div>

        <p class="text-gray-800 text-lg font-medium leading-relaxed mb-6">
          {{ currentQuestion.content }}
        </p>

        <!-- 选项 -->
        <div class="space-y-3">
          <div
              v-for="opt in currentQuestion.options"
              :key="opt.key"
              @click="handleAnswer(opt.key)"
              class="flex flex-col bg-white rounded-2xl p-4 border-2 transition-all cursor-pointer active:scale-95"
              :class="answers[currentQuestion.seq] === opt.key
                ? 'border-violet-500 bg-violet-50'
                : 'border-transparent hover:border-gray-200'"
          >
            <div class="flex items-center gap-4">
              <span class="w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm font-bold flex-shrink-0 transition-all"
                  :class="answers[currentQuestion.seq] === opt.key ? 'border-violet-500 bg-violet-500 text-white' : 'border-gray-200 text-gray-400'">
                {{ opt.key }}
              </span>
              <span class="text-gray-700 flex-1">{{ opt.label }}</span>
            </div>
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

      <!-- 底部导航 -->
      <div class="sticky bottom-0 bg-white border-t px-5 py-3 pb-safe-bottom flex gap-3">
        <van-button plain round @click="handlePrev" :disabled="currentIndex === 0" class="flex-1">上一题</van-button>
        <van-button
            v-if="currentIndex < visibleQuestions.length - 1"
            round type="primary" color="#7c3aed"
            @click="handleNext"
            :disabled="!answers[currentQuestion.seq]"
            class="flex-1"
        >下一题</van-button>
        <van-button
            v-else
            round type="primary" color="#7c3aed"
            @click="handleSubmit"
            :disabled="!answers[currentQuestion.seq]"
            :loading="submitting"
            class="flex-1"
        >提交答案</van-button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { showToast, showImagePreview } from 'vant';
import { apiGetPlayData, apiSubmitAnswers, QuizPlayData, QuizQuestion, PlayDataParams, SubmitAnswersParams } from '@/api/quizApi.ts';

const route = useRoute();
const router = useRouter();
const token = route.query.token as string;
const quizId = route.query.quizId as string;
const loading = ref(true);
const submitting = ref(false);
const errorMsg = ref('');
const playData = ref<QuizPlayData | null>(null);
const answers = ref<Record<number, string>>({});
const currentIndex = ref(0);

// branch类型动态题目序列；其他类型按seq顺序
const questionSeqOrder = ref<number[]>([]);

const visibleQuestions = computed<QuizQuestion[]>(() => {
  if (!playData.value) return [];
  const qMap = Object.fromEntries(playData.value.questions.map(q => [q.seq, q]));
  if (playData.value.quizType === 'branch') {
    return questionSeqOrder.value.map(seq => qMap[seq]).filter(Boolean);
  }
  return playData.value.questions.filter(q => !q.isHidden);
});

const currentQuestion = computed(() => visibleQuestions.value[currentIndex.value] || null);
const progress = computed(() => Math.round((currentIndex.value / Math.max(visibleQuestions.value.length, 1)) * 100));

const handleAnswer = (key: string) => {
  if (!currentQuestion.value) return;
  answers.value[currentQuestion.value.seq] = key;

  // branch类型：记录下一题
  if (playData.value?.quizType === 'branch') {
    const opt = currentQuestion.value.options.find(o => o.key === key);
    const nextSeq = opt?.nextQuestionSeq;
    if (nextSeq !== undefined && nextSeq !== -1) {
      // 若下一题不在序列中则追加
      if (!questionSeqOrder.value.includes(nextSeq)) {
        questionSeqOrder.value = [...questionSeqOrder.value.slice(0, currentIndex.value + 1), nextSeq];
      }
    }
  }

  // 非branch类型自动跳下一题（延迟200ms有动画感）
  if (playData.value?.quizType !== 'branch' && currentIndex.value < visibleQuestions.value.length - 1) {
    setTimeout(() => { currentIndex.value++; }, 200);
  }
};

const previewImages = (urls: string[], startPosition: number) => {
  showImagePreview({ images: urls, startPosition })
}

const handlePrev = () => { if (currentIndex.value > 0) currentIndex.value--; };
const handleNext = () => { if (currentIndex.value < visibleQuestions.value.length - 1) currentIndex.value++; };

const handleSubmit = () => {
  const unanswered = visibleQuestions.value.filter(q => !answers.value[q.seq])
  if (unanswered.length) {
    showToast('请回答所有题目')
    return
  }

  // 合并隐藏题答案（固定答案或不参与）
  const fullAnswers: Record<string, string> = {}
  Object.entries(answers.value).forEach(([seq, key]) => {
    fullAnswers[seq] = key
  })

  submitting.value = true
  const submitAnswersParams: SubmitAnswersParams = {
    token: token,
    quizId: quizId,
    answers: fullAnswers,
  }
  apiSubmitAnswers(submitAnswersParams).then(res => {
    if (res.code === 200) {
      router.replace({ name: 'QuizResult', query: { token, resultId: res.data.resultId } })
    } else {
      showToast(res.message || '提交失败，请重试')
    }
  }).finally(() => {
    submitting.value = false
  })
}

onMounted(() => {
  const playDataParams: PlayDataParams = {
    token: token,
    quizId: quizId,
  }
  apiGetPlayData(playDataParams).then(res => {
    if (res.code === 200) {
      playData.value = res.data
      if (res.data.quizType === 'branch' && res.data.questions.length) {
        questionSeqOrder.value = [res.data.questions[0].seq]
      }
    } else {
      router.replace({ name: 'QuizEntry', query: { token } })
    }
  }).catch((err: any) => {
    errorMsg.value = typeof err === 'string' ? err : '无法加载测验，请返回重试'
  }).finally(() => {
    loading.value = false
  })
});
</script>
