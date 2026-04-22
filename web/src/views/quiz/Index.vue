<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-violet-500/25">
            <Icon icon="fluent:quiz-new-20-filled" :width="24" :height="24"/>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">测验管理</h1>
            <p class="text-sm text-gray-500 mt-1">创建和管理各类趣味测验</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <n-select v-model:value="params.status" :options="statusOptions" clearable placeholder="状态筛选" style="width:130px"/>
          <n-select v-model:value="params.quizType" :options="typeOptions" clearable placeholder="类型筛选" style="width:130px"/>
          <n-input v-model:value="params.search" placeholder="搜索名称/编码" clearable @keyup.enter="loadPage()" style="width:220px"/>
          <n-button type="default" @click="showImport = true">
            <template #icon><Icon icon="fluent:arrow-upload-20-filled"/></template>
            AI导入
          </n-button>
          <n-button type="primary" @click="handleCreate">
            <template #icon><Icon icon="fluent:add-circle-20-filled"/></template>
            新建测验
          </n-button>
        </div>
      </div>
    </div>

    <!-- 列表 -->
    <div class="flex-1 overflow-auto p-6">
      <n-data-table
          :columns="columns"
          :data="tableData"
          :loading="loading"
          :pagination="pagination"
          @update:page="handlePageChange"
          remote
      />
    </div>

    <!-- 新建/编辑弹窗 -->
    <n-modal v-model:show="showEdit" preset="card" title="测验信息" style="width:600px">
      <QuizForm :quiz="editTarget" @saved="onSaved" @cancel="showEdit = false"/>
    </n-modal>

    <!-- AI导入弹窗 -->
    <n-modal v-model:show="showImport" preset="card" title="AI生成导入" style="width:700px">
      <div class="space-y-4">
        <n-alert type="info" :show-icon="false">
          将 <code>doc/generated/xxx.json</code> 的内容粘贴到下方，或直接上传 JSON 文件
        </n-alert>
        <n-input v-model:value="importJson" type="textarea" :rows="12" placeholder="粘贴 Quiz Definition JSON..."/>
        <div class="flex justify-end gap-3">
          <n-button @click="showImport = false">取消</n-button>
          <n-button type="primary" :loading="importLoading" @click="handleImport">导入</n-button>
        </div>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, reactive, onMounted, h } from 'vue';
import { useRouter } from 'vue-router';
import { NButton, NTag, NSpace, useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import {
  apiGetQuizPage, apiDeleteQuiz, apiChangeQuizStatus, apiImportQuiz,
  QuizDetail, QuizStatus
} from '@/api/quizApi.ts';
import QuizForm from '@/components/quiz/QuizForm.vue';

const router = useRouter();
const message = useMessage();

const loading = ref(false);
const importLoading = ref(false);
const showEdit = ref(false);
const showImport = ref(false);
const importJson = ref('');
const editTarget = ref<Partial<QuizDetail>>({});
const tableData = ref<QuizDetail[]>([]);
const totalCount = ref(0);

const params = reactive({
  pageIndex: 1,
  pageSize: 20,
  search: null as string | null,
  quizType: null as string | null,
  status: null as string | null,
});

const pagination = reactive({ page: 1, pageSize: 20, itemCount: 0, showSizePicker: true, pageSizes: [20, 50] });

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' },
  { label: '已归档', value: 'archived' },
];

const typeOptions = [
  { label: '向量匹配', value: 'vector' },
  { label: '累分映射', value: 'score' },
  { label: '分支跳题', value: 'branch' },
  { label: '加权随机', value: 'random' },
];

const statusTagType: Record<QuizStatus, 'default' | 'success' | 'warning'> = {
  draft: 'default', published: 'success', archived: 'warning',
};

const columns = [
  { title: '名称', key: 'name', render: (row: QuizDetail) => h('span', { class: 'font-medium' }, row.name) },
  { title: '编码', key: 'code', render: (row: QuizDetail) => h('span', { class: 'text-gray-400 text-xs' }, row.code) },
  { title: '类型', key: 'quizType', width: 100 },
  {
    title: '状态', key: 'status', width: 90,
    render: (row: QuizDetail) => h(NTag, { type: statusTagType[row.status], size: 'small' }, { default: () => statusOptions.find(s => s.value === row.status)?.label })
  },
  { title: '题目', key: 'questionCount', width: 70, render: (row: QuizDetail) => row.questionCount ?? '-' },
  { title: '结果', key: 'outcomeCount', width: 70, render: (row: QuizDetail) => row.outcomeCount ?? '-' },
  { title: '参与', key: 'participateCount', width: 70, render: (row: QuizDetail) => row.participateCount ?? 0 },
  {
    title: '操作', key: 'actions', width: 280,
    render: (row: QuizDetail) => h(NSpace, {}, {
      default: () => [
        h(NButton, { size: 'small', onClick: () => handleEdit(row) }, { default: () => '编辑' }),
        h(NButton, { size: 'small', onClick: () => router.push({ name: 'QuizDetail', query: { id: row.id } }) }, { default: () => '配置' }),
        row.status === 'draft'
          ? h(NButton, { size: 'small', type: 'primary', onClick: () => handleStatus(row, 'published') }, { default: () => '发布' })
          : h(NButton, { size: 'small', onClick: () => handleStatus(row, 'archived') }, { default: () => '归档' }),
        h(NButton, { size: 'small', type: 'error', onClick: () => handleDelete(row) }, { default: () => '删除' }),
      ]
    })
  },
];

const loadPage = () => {
  loading.value = true;
  // @ts-ignore
  apiGetQuizPage({ ...params }).then(res => {
    if (res.code === 200) {
      tableData.value = res.data.data;
      totalCount.value = res.data.totalCount;
      pagination.itemCount = res.data.totalCount;
    }
  }).finally(() => { loading.value = false; });
};

const handlePageChange = (page: number) => {
  params.pageIndex = page;
  pagination.page = page;
  loadPage();
};

const handleCreate = () => {
  editTarget.value = {};
  showEdit.value = true;
};

const handleEdit = (row: QuizDetail) => {
  editTarget.value = { ...row };
  showEdit.value = true;
};

const handleStatus = (row: QuizDetail, status: QuizStatus) => {
  apiChangeQuizStatus({ quizId: row.id, status }).then(res => {
    if (res.code === 200) { message.success('状态已更新'); loadPage(); }
    else message.error(res.message || '操作失败');
  });
};

const handleDelete = (row: QuizDetail) => {
  apiDeleteQuiz({ quizId: row.id }).then(res => {
    if (res.code === 200) { message.success('已删除'); loadPage(); }
    else message.error(res.message || '删除失败');
  });
};

const onSaved = () => {
  showEdit.value = false;
  loadPage();
};

const handleImport = () => {
  let definition: Record<string, any>;
  try {
    definition = JSON.parse(importJson.value);
  } catch {
    message.error('JSON格式错误，请检查');
    return;
  }
  importLoading.value = true;
  apiImportQuiz({ definition }).then(res => {
    if (res.code === 200) {
      message.success('导入成功，状态为草稿，请审核后发布');
      showImport.value = false;
      importJson.value = '';
      loadPage();
    } else {
      message.error(res.message || '导入失败');
    }
  }).finally(() => { importLoading.value = false; });
};

onMounted(() => loadPage());
</script>
