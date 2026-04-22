<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gray-50">
    <div class="px-6 py-4 bg-white border-b flex items-center gap-4">
      <n-button text @click="router.back()">
        <template #icon><Icon icon="fluent:arrow-left-20-filled"/></template>
      </n-button>
      <span class="text-lg font-semibold text-gray-800">{{ quiz?.name || '测验配置' }}</span>
      <n-tag :type="statusTagType[quiz?.status]" size="small">{{ statusLabel }}</n-tag>
      <div class="ml-auto flex gap-3">
        <n-button v-if="quiz?.status === 'draft'" type="primary" @click="handlePublish">发布</n-button>
        <n-button v-if="quiz?.status === 'published'" @click="handleArchive">归档</n-button>
      </div>
    </div>

    <n-tabs v-model:value="activeTab" type="line" class="px-6 bg-white border-b" animated>
      <n-tab-pane name="basic" tab="基本信息"/>
      <n-tab-pane name="questions" tab="题目配置"/>
      <n-tab-pane name="outcomes" tab="结果配置"/>
      <n-tab-pane name="algo" tab="算法配置"/>
      <n-tab-pane name="stats" tab="数据统计"/>
    </n-tabs>

    <div class="flex-1 overflow-auto p-6">
      <!-- 基本信息 -->
      <div v-if="activeTab === 'basic'">
        <QuizForm :quiz="quiz || {}" @saved="loadQuiz" @cancel="() => {}"/>
      </div>

      <!-- 题目配置 -->
      <div v-if="activeTab === 'questions'">
        <QuestionEditor :quiz-id="quizId" :quiz-type="quiz?.quizType || 'vector'" :algo-config="quiz?.algoConfig"/>
      </div>

      <!-- 结果配置 -->
      <div v-if="activeTab === 'outcomes'">
        <OutcomeEditor :quiz-id="quizId" :quiz-type="quiz?.quizType || 'vector'"/>
      </div>

      <!-- 算法配置 -->
      <div v-if="activeTab === 'algo'">
        <AlgoConfigEditor :quiz="quiz || {}" @saved="loadQuiz"/>
      </div>

      <!-- 数据统计 -->
      <div v-if="activeTab === 'stats'">
        <QuizStats :quiz-id="quizId"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { apiGetQuizDetail, apiChangeQuizStatus, QuizDetail, QuizStatus, QuizDetailParams } from '@/api/quizApi.ts';
import QuizForm from '@/components/quiz/QuizForm.vue';
import QuestionEditor from '@/components/quiz/QuestionEditor.vue';
import OutcomeEditor from '@/components/quiz/OutcomeEditor.vue';
import AlgoConfigEditor from '@/components/quiz/AlgoConfigEditor.vue';
import QuizStats from '@/components/quiz/QuizStats.vue';

const route = useRoute();
const router = useRouter();
const message = useMessage();
const quizId = route.query.id as string;
const quiz = ref<QuizDetail | null>(null);
const activeTab = ref('basic');

const statusTagType: Record<QuizStatus, 'default' | 'success' | 'warning'> = {
  draft: 'default', published: 'success', archived: 'warning',
};
const statusLabel = computed(() => ({ draft: '草稿', published: '已发布', archived: '已归档' }[quiz.value?.status || 'draft']));

const loadQuiz = () => {
  const quizDetailParams: QuizDetailParams = {
    quizId: quizId,
  }
  apiGetQuizDetail(quizDetailParams).then(res => {
    if (res.code === 200) {
      quiz.value = res.data
    }
  })
}

const handlePublish = () => {
  apiChangeQuizStatus({ quizId: quizId, status: 'published' }).then(res => {
    if (res.code === 200) {
      message.success('已发布')
      loadQuiz()
    } else {
      message.error(res.message || '发布失败')
    }
  })
}

const handleArchive = () => {
  apiChangeQuizStatus({ quizId: quizId, status: 'archived' }).then(res => {
    if (res.code === 200) { message.success('已归档'); loadQuiz(); }
    else message.error(res.message || '操作失败');
  });
};

onMounted(() => loadQuiz());
</script>
