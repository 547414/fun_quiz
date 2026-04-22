<template>
  <div class="bg-white rounded-xl p-6 space-y-6">
    <div class="text-sm text-gray-500">测验类型：<span class="font-semibold text-gray-800">{{ typeLabel }}</span></div>

    <!-- vector类型：维度配置 -->
    <template v-if="quiz.quizType === 'vector'">
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="font-medium">维度配置</span>
          <n-button size="small" @click="addDimension">新增维度</n-button>
        </div>
        <div class="space-y-2">
          <div v-for="(dim, i) in dimensions" :key="i" class="flex gap-2 items-center">
            <n-input v-model:value="dim.code" placeholder="编码 S1" style="width:80px"/>
            <n-input v-model:value="dim.name" placeholder="名称 自尊自信" style="width:140px"/>
            <n-input v-model:value="dim.groupCode" placeholder="组编码 S" style="width:70px"/>
            <n-input v-model:value="dim.groupName" placeholder="组名 自我模型" style="width:120px"/>
            <n-input-number v-model:value="dim.sortOrder" style="width:80px" placeholder="排序"/>
            <n-button size="small" text type="error" @click="dimensions.splice(i, 1)">
              <Icon icon="fluent:delete-20-regular"/>
            </n-button>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm text-gray-500">相似度阈值（低于此值使用兜底结果）</span>
          <n-input-number v-model:value="similarityThreshold" :min="0" :max="100" style="width:100px"/>
          <span class="text-xs text-gray-400">%</span>
        </div>
      </div>
    </template>

    <!-- score类型 -->
    <template v-if="quiz.quizType === 'score'">
      <div class="flex gap-4 items-center">
        <span class="text-sm">总分范围：</span>
        <n-input-number v-model:value="totalMin" placeholder="最低分" style="width:100px"/>
        <span>~</span>
        <n-input-number v-model:value="totalMax" placeholder="最高分" style="width:100px"/>
      </div>
    </template>

    <!-- 特殊规则 -->
    <div class="space-y-3">
      <div class="flex justify-between items-center">
        <span class="font-medium">特殊判定规则</span>
        <n-button size="small" @click="addRule">新增规则</n-button>
      </div>
      <div v-for="(rule, i) in specialRules" :key="i" class="flex gap-2 items-center">
        <span class="text-xs text-gray-400">当第</span>
        <n-input-number v-model:value="rule.questionSeq" placeholder="题号" style="width:80px"/>
        <span class="text-xs text-gray-400">题选</span>
        <n-input v-model:value="rule.optionKey" placeholder="选项 如C" style="width:70px"/>
        <span class="text-xs text-gray-400">时触发</span>
        <n-input v-model:value="rule.triggerOutcomeCode" placeholder="结果code" style="width:140px"/>
        <n-button size="small" text type="error" @click="specialRules.splice(i, 1)">
          <Icon icon="fluent:delete-20-regular"/>
        </n-button>
      </div>
    </div>

    <div class="flex justify-end">
      <n-button type="primary" :loading="saving" @click="handleSave">保存配置</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { apiEditQuiz, QuizDetail } from '@/api/quizApi.ts';

const props = defineProps<{ quiz: Partial<QuizDetail> }>();
const emit = defineEmits(['saved']);
const message = useMessage();
const saving = ref(false);

const dimensions = ref<any[]>([]);
const similarityThreshold = ref(60);
const totalMin = ref(0);
const totalMax = ref(100);
const specialRules = ref<any[]>([]);

const typeLabel = computed(() => ({ vector: '向量匹配', score: '累分映射', branch: '分支跳题', random: '加权随机' }[props.quiz.quizType || 'vector']));

onMounted(() => {
  const cfg = props.quiz.algoConfig || {};
  if (props.quiz.quizType === 'vector') {
    dimensions.value = cfg.dimensions ? [...cfg.dimensions] : [];
    similarityThreshold.value = cfg.similarityThreshold ?? 60;
  }
  if (props.quiz.quizType === 'score') {
    totalMin.value = cfg.totalMin ?? 0;
    totalMax.value = cfg.totalMax ?? 100;
  }
  specialRules.value = props.quiz.specialRules ? [...props.quiz.specialRules] : [];
});

const addDimension = () => {
  dimensions.value.push({ code: '', name: '', groupCode: '', groupName: '', sortOrder: dimensions.value.length + 1 });
};

const addRule = () => {
  specialRules.value.push({ conditionType: 'option_selected', questionSeq: null, optionKey: '', triggerOutcomeCode: '' });
};

const handleSave = () => {
  let algoConfig: Record<string, any> = {};
  if (props.quiz.quizType === 'vector') algoConfig = { dimensions: dimensions.value, similarityThreshold: similarityThreshold.value };
  if (props.quiz.quizType === 'score') algoConfig = { totalMin: totalMin.value, totalMax: totalMax.value };

  saving.value = true;
  // @ts-ignore
  apiEditQuiz({ id: props.quiz.id, version: props.quiz.version, algoConfig, specialRules: specialRules.value }).then(res => {
    if (res.code === 200) { message.success('配置已保存'); emit('saved'); }
    else message.error(res.message || '保存失败');
  }).finally(() => { saving.value = false; });
};
</script>
