<template>
  <n-form ref="formRef" :model="form" label-placement="left" label-width="90px">
    <n-form-item label="测验名称" path="name" :rule="{ required: true, message: '请输入名称' }">
      <n-input v-model:value="form.name" placeholder="例：职场人格测试"/>
    </n-form-item>
    <n-form-item label="测验编码" path="code" :rule="{ required: !form.id, message: '请输入编码' }">
      <n-input v-model:value="form.code" placeholder="例：workplace_sbti" :disabled="!!form.id"/>
    </n-form-item>
    <n-form-item label="测验类型" path="quizType">
      <n-select v-model:value="form.quizType" :options="typeOptions" :disabled="!!form.id"/>
    </n-form-item>
    <n-form-item label="封面图片">
      <div class="w-full space-y-2">
        <ImageUploadList v-model="form.covers"/>
        <div v-if="form.coverPrompt?.prompt" class="flex items-start gap-1.5 bg-violet-50 rounded-lg px-3 py-2 text-xs text-violet-700">
          <span class="flex-shrink-0 font-medium mt-0.5">🖼 文生图提示词</span>
          <span class="text-violet-600 leading-relaxed">{{ form.coverPrompt.prompt }}</span>
        </div>
      </div>
    </n-form-item>
    <n-form-item label="分享标题">
      <n-input v-model:value="form.shareTitle" placeholder="分享到微信时显示的标题"/>
    </n-form-item>
    <n-form-item label="分享描述">
      <n-input v-model:value="form.shareDesc" type="textarea" :rows="2"/>
    </n-form-item>
    <n-form-item label="排序">
      <n-input-number v-model:value="form.sortOrder" :min="0"/>
    </n-form-item>
    <div class="flex justify-end gap-3 mt-4">
      <n-button @click="$emit('cancel')">取消</n-button>
      <n-button type="primary" :loading="saving" @click="handleSave">保存</n-button>
    </div>
  </n-form>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue';
import { useMessage } from 'naive-ui';
import { apiEditQuiz, QuizDetail } from '@/api/quizApi.ts';
import ImageUploadList from '@/components/quiz/ImageUploadList.vue';

const props = defineProps<{ quiz: Partial<QuizDetail> }>();
const emit = defineEmits(['saved', 'cancel']);
const message = useMessage();
const formRef = ref();
const saving = ref(false);

const typeOptions = [
  { label: '向量匹配 (SBTI/MBTI)', value: 'vector' },
  { label: '累分映射', value: 'score' },
  { label: '分支跳题', value: 'branch' },
  { label: '加权随机', value: 'random' },
];

const form = reactive<Partial<QuizDetail>>({
  id: undefined, name: '', code: '', quizType: 'vector',
  covers: [], shareTitle: '', shareDesc: '', sortOrder: 0,
});

watch(() => props.quiz, (val) => {
  Object.assign(form, { name: '', code: '', quizType: 'vector', shareTitle: '', shareDesc: '', sortOrder: 0, ...val });
  if (!form.covers) form.covers = []
}, { immediate: true });

const handleSave = () => {
  formRef.value?.validate((errors: any) => {
    if (errors) return;
    saving.value = true;
    apiEditQuiz(form).then(res => {
      if (res.code === 200) { message.success('保存成功'); emit('saved'); }
      else message.error(res.message || '保存失败');
    }).finally(() => { saving.value = false; });
  });
};
</script>
