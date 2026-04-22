<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-500">共 {{ outcomes.length }} 个结果 <span v-if="!hasFallback" class="text-red-400">（缺少兜底结果）</span></span>
      <div class="flex gap-2">
        <n-button @click="handleAdd">新增结果</n-button>
        <n-button type="primary" :loading="saving" @click="handleSave">保存所有结果</n-button>
      </div>
    </div>

    <div v-for="(o, idx) in outcomes" :key="idx" class="bg-white rounded-xl border border-gray-100 p-4 space-y-3">
      <div class="flex items-center gap-3">
        <n-input v-model:value="o.code" placeholder="结果编码 如 ATM-er" style="width:160px" :disabled="!!o.id"/>
        <n-input v-model:value="o.name" placeholder="结果名称" style="width:160px"/>
        <n-checkbox v-model:checked="o.isFallback">兜底结果</n-checkbox>
        <n-checkbox v-model:checked="o.isSpecial">特殊触发</n-checkbox>
        <n-button size="small" type="error" text @click="outcomes.splice(idx, 1)">
          <Icon icon="fluent:delete-20-regular"/>
        </n-button>
      </div>

      <div class="space-y-1.5">
        <div class="flex items-center gap-3">
          <span class="text-sm text-gray-500 flex-shrink-0">结果头像</span>
          <ImageUploadList
            :model-value="o.avatar ? [o.avatar] : []"
            :max="1"
            @update:model-value="o.avatar = $event[0] ?? null"
          />
        </div>
        <div v-if="o.avatarPrompt?.prompt" class="flex items-start gap-1.5 bg-violet-50 rounded-lg px-3 py-2 text-xs text-violet-700">
          <span class="flex-shrink-0 font-medium mt-0.5">🖼 文生图提示词</span>
          <span class="text-violet-600 leading-relaxed">{{ o.avatarPrompt.prompt }}</span>
        </div>
      </div>

      <n-input v-model:value="o.summary" placeholder="简短描述（结果页副标题）"/>

      <!-- matchConfig by type -->
      <div class="flex gap-3 items-center text-sm">
        <template v-if="quizType === 'vector'">
          <span class="text-gray-500">15维向量：</span>
          <n-input v-model:value="o._vectorStr" placeholder="例：3,2,3,1,2,3,2,1,3,2,3,1,2,3,1" style="width:350px"
              @blur="parseVector(o)"/>
          <span class="text-gray-400 text-xs">L=1 M=2 H=3，逗号分隔</span>
        </template>
        <template v-if="quizType === 'score'">
          <span class="text-gray-500">分数区间：</span>
          <n-input-number v-model:value="o._scoreMin" placeholder="最低分" style="width:100px"/>
          <span>~</span>
          <n-input-number v-model:value="o._scoreMax" placeholder="最高分" style="width:100px"/>
        </template>
        <template v-if="quizType === 'random'">
          <span class="text-gray-500">随机权重：</span>
          <n-input-number v-model:value="o._weight" placeholder="权重" :min="1" style="width:100px"/>
        </template>
      </div>

      <n-input v-model:value="o.detail" type="textarea" :rows="3" placeholder="详细解读文案"/>
    </div>

    <n-button dashed block @click="handleAdd">+ 新增结果</n-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { apiGetOutcomes, apiBatchSaveOutcomes, QuizOutcome, GetOutcomesParams } from '@/api/quizApi.ts';
import ImageUploadList from '@/components/quiz/ImageUploadList.vue';

const props = defineProps<{ quizId: string; quizType: string }>();
const message = useMessage();
const saving = ref(false);
const outcomes = ref<any[]>([]);
const hasFallback = computed(() => outcomes.value.some(o => o.isFallback));

const loadOutcomes = () => {
  const getOutcomesParams: GetOutcomesParams = {
    quizId: props.quizId,
  }
  apiGetOutcomes(getOutcomesParams).then(res => {
    if (res.code === 200) {
      outcomes.value = res.data.map(o => ({
        ...o,
        _vectorStr: o.matchConfig?.dimVector?.join(',') || '',
        _scoreMin: o.matchConfig?.scoreMin ?? 0,
        _scoreMax: o.matchConfig?.scoreMax ?? 0,
        _weight: o.matchConfig?.weight ?? 1,
      }))
    }
  })
}

const parseVector = (o: any) => {
  const nums = (o._vectorStr || '').split(',').map((s: string) => parseInt(s.trim())).filter((n: number) => !isNaN(n));
  o.matchConfig = { ...(o.matchConfig || {}), dimVector: nums };
};

const handleAdd = () => {
  outcomes.value.push({ code: '', name: '', summary: '', detail: '', isFallback: false, isSpecial: false, sortOrder: outcomes.value.length, _vectorStr: '', _scoreMin: 0, _scoreMax: 0, _weight: 1 });
};

const handleSave = () => {
  const clean: QuizOutcome[] = outcomes.value.map(o => {
    let matchConfig: Record<string, any> = {};
    if (props.quizType === 'vector') { parseVector(o); matchConfig = o.matchConfig || {}; }
    if (props.quizType === 'score') matchConfig = { scoreMin: o._scoreMin, scoreMax: o._scoreMax };
    if (props.quizType === 'random') matchConfig = { weight: o._weight };
    return { code: o.code, name: o.name, avatar: o.avatar ?? null, summary: o.summary, detail: o.detail, isFallback: o.isFallback, isSpecial: o.isSpecial, sortOrder: o.sortOrder, matchConfig };
  });

  saving.value = true;
  apiBatchSaveOutcomes({ quizId: props.quizId, outcomes: clean }).then(res => {
    if (res.code === 200) { message.success('结果已保存'); loadOutcomes(); }
    else message.error(res.message || '保存失败');
  }).finally(() => { saving.value = false; });
};

onMounted(() => loadOutcomes());
</script>
