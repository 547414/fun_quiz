<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-500">共 {{ questions.length }} 道题</span>
      <div class="flex gap-2">
        <n-button @click="handleAdd">新增题目</n-button>
        <n-button type="primary" :loading="saving" @click="handleSave">保存所有题目</n-button>
      </div>
    </div>

    <div v-for="(q, idx) in questions" :key="idx" class="bg-white rounded-xl border border-gray-100 p-4 space-y-3">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-full bg-violet-100 text-violet-700 text-sm font-bold flex items-center justify-center flex-shrink-0">{{ q.seq }}</span>
        <n-input v-model:value="q.content" placeholder="题目内容" class="flex-1"/>
        <n-checkbox v-model:checked="q.isHidden">隐藏判定题</n-checkbox>
        <n-button size="small" type="error" text @click="questions.splice(idx, 1)">
          <Icon icon="fluent:delete-20-regular"/>
        </n-button>
      </div>

      <!-- 题目图片 + 文生图提示词 -->
      <div class="pl-11 space-y-1.5">
        <p class="text-xs text-gray-400">题目图片</p>
        <ImageUploadList v-model="q.images" :max="5"/>
        <div v-if="q.imagePrompt?.prompt" class="flex items-start gap-1.5 bg-violet-50 rounded-lg px-3 py-2 text-xs text-violet-700">
          <span class="flex-shrink-0 font-medium mt-0.5">🖼 文生图提示词</span>
          <span class="text-violet-600 leading-relaxed">{{ q.imagePrompt.prompt }}</span>
        </div>
      </div>

      <!-- 选项列表 -->
      <div class="pl-11 space-y-2">
        <div v-for="(opt, oi) in q.options" :key="oi" class="flex flex-col gap-1.5 border border-gray-100 rounded-lg p-2">
          <div class="flex items-center gap-2">
          <span class="w-6 text-xs text-gray-400 font-mono flex-shrink-0">{{ opt.key }}</span>
          <n-input v-model:value="opt.label" placeholder="选项文字" style="width:200px"/>

          <!-- vector类型：维度分值 -->
          <template v-if="quizType === 'vector' && dimensions.length">
            <n-select
                v-model:value="opt._dim_code"
                :options="dimOptions"
                placeholder="维度"
                style="width:140px"
                @update:value="(v: string) => { opt.dimScores = { [v]: opt._dim_val || 2 } }"
            />
            <n-select
                v-model:value="opt._dim_val"
                :options="[{label:'L(1)',value:1},{label:'M(2)',value:2},{label:'H(3)',value:3}]"
                style="width:90px"
                @update:value="(v: number) => { if (opt._dim_code) opt.dimScores = { [opt._dim_code]: v } }"
            />
          </template>

          <!-- score类型：分值 -->
          <template v-if="quizType === 'score'">
            <n-input-number v-model:value="opt.score" placeholder="分值" style="width:90px" :min="0"/>
          </template>

          <!-- branch类型：跳转 -->
          <template v-if="quizType === 'branch'">
            <n-input-number v-model:value="opt.nextQuestionSeq" placeholder="下一题seq(-1结束)" style="width:160px"/>
            <n-input v-if="opt.nextQuestionSeq === -1" v-model:value="opt.outcomeCode" placeholder="结果code" style="width:130px"/>
          </template>

          <n-button size="tiny" text type="error" @click="q.options.splice(oi, 1)">
            <Icon icon="fluent:subtract-circle-20-regular"/>
          </n-button>
          </div>
          <!-- 选项图片 + 文生图提示词 -->
          <div class="space-y-1" style="margin-left:24px">
            <ImageUploadList v-model="opt.images" :max="3"/>
            <div v-if="opt.imagePrompt?.prompt" class="flex items-start gap-1.5 bg-amber-50 rounded-lg px-3 py-1.5 text-xs text-amber-700">
              <span class="flex-shrink-0 font-medium mt-0.5">🖼 文生图提示词</span>
              <span class="text-amber-600 leading-relaxed">{{ opt.imagePrompt.prompt }}</span>
            </div>
          </div>
        </div>
        <n-button size="small" dashed @click="addOption(q)">+ 新增选项</n-button>
      </div>
    </div>

    <n-button dashed block @click="handleAdd">+ 新增题目</n-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { apiGetQuestions, apiBatchSaveQuestions, QuizQuestion, GetQuestionsParams } from '@/api/quizApi.ts';
import ImageUploadList from '@/components/quiz/ImageUploadList.vue';

const props = defineProps<{
  quizId: string;
  quizType: string;
  algoConfig?: Record<string, any> | null;
}>();

const message = useMessage();
const saving = ref(false);
const questions = ref<any[]>([]);

const dimensions = computed(() => props.algoConfig?.dimensions || []);
const dimOptions = computed(() => dimensions.value.map((d: any) => ({ label: `${d.code} ${d.name}`, value: d.code })));

const loadQuestions = () => {
  const getQuestionsParams: GetQuestionsParams = {
    quizId: props.quizId,
  }
  apiGetQuestions(getQuestionsParams).then(res => {
    if (res.code === 200) {
      questions.value = res.data.map(q => ({
        ...q,
        images: q.images || [],
        options: (q.options || []).map((o: any) => ({
          ...o,
          images: o.images || [],
          _dim_code: o.dimScores ? Object.keys(o.dimScores)[0] : undefined,
          _dim_val: o.dimScores ? Object.values(o.dimScores)[0] : undefined,
        })),
      }))
    }
  })
}

const handleAdd = () => {
  const nextSeq = questions.value.length > 0 ? Math.max(...questions.value.map(q => q.seq)) + 1 : 1;
  questions.value.push({ seq: nextSeq, content: '', isHidden: false, images: [], options: [] });
};

const addOption = (q: any) => {
  const keys = ['A', 'B', 'C', 'D', 'E'];
  const nextKey = keys[q.options.length] || String(q.options.length + 1);
  q.options.push({ key: nextKey, label: '', score: 0, dimScores: {}, nextQuestionSeq: undefined, outcomeCode: undefined, images: [] });
};

const handleSave = () => {
  const cleanQuestions: QuizQuestion[] = questions.value.map(q => ({
    seq: q.seq,
    content: q.content,
    isHidden: q.isHidden,
    images: q.images?.length ? q.images : undefined,
    options: q.options.map((o: any) => {
      const clean: any = { key: o.key, label: o.label };
      if (props.quizType === 'vector') clean.dimScores = o.dimScores || {};
      if (props.quizType === 'score') clean.score = o.score || 0;
      if (props.quizType === 'branch') {
        clean.nextQuestionSeq = o.nextQuestionSeq;
        if (o.outcomeCode) clean.outcomeCode = o.outcomeCode;
      }
      if (o.images?.length) clean.images = o.images;
      return clean;
    }),
    branchConfig: q.branchConfig || null,
  }));

  saving.value = true;
  apiBatchSaveQuestions({ quizId: props.quizId, questions: cleanQuestions }).then(res => {
    if (res.code === 200) { message.success('题目已保存'); loadQuestions(); }
    else message.error(res.message || '保存失败');
  }).finally(() => { saving.value = false; });
};

onMounted(() => loadQuestions());
</script>
