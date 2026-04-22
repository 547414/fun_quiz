<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div class="w-12 h-12 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-amber-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:key-20-filled" :width="24" :height="24"/>
            </div>
            <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-violet-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:add-16-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              Token 管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">生成和管理测验访问令牌</p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <n-select
              v-model:value="params.status"
              :options="statusOptions"
              clearable
              placeholder="状态筛选"
              size="large"
              style="width: 140px"
              @update:value="loadPage"
          />
          <div class="relative">
            <Icon
                icon="fluent:search-20-regular"
                class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
                :width="20" :height="20"
            />
            <n-input
                v-model:value="params.batchCode"
                placeholder="搜索批次编码"
                clearable
                size="large"
                style="width: 240px"
                @keyup.enter="loadPage"
                @clear="loadPage"
            />
          </div>
          <n-button
              type="primary"
              size="large"
              @click="showGenerate = true"
              class="shadow-md hover:shadow-lg transition-all duration-200"
          >
            <template #icon>
              <Icon icon="fluent:key-multiple-20-filled"/>
            </template>
            生成 Token
          </n-button>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 px-6 pb-6 pt-4 overflow-hidden">
      <div class="h-full bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
        <!-- 表格 -->
        <div class="flex-1 p-6 pb-0 overflow-hidden">
          <n-data-table
              :columns="columns"
              :data="tableData"
              :loading="loading"
              :pagination="false"
              :bordered="false"
              striped
              :max-height="tableHeight"
              :scroll-x="900"
          />
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && tableData.length === 0" class="flex flex-col items-center justify-center py-16">
          <div class="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Icon icon="fluent:key-20-regular" class="text-gray-400" :width="48" :height="48"/>
          </div>
          <p class="text-gray-500 text-lg">暂无 Token 数据</p>
          <p class="text-gray-400 text-sm mt-2">点击右上角「生成 Token」按钮创建访问令牌</p>
        </div>

        <!-- 分页 -->
        <div class="px-6 py-4 border-t border-gray-100 flex items-center justify-between flex-shrink-0">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <Icon icon="fluent:info-16-regular"/>
            共 <span class="font-medium text-gray-700 mx-1">{{ total }}</span> 条记录
          </div>
          <n-pagination
              v-model:page="params.pageIndex"
              v-model:page-size="params.pageSize"
              :item-count="total"
              :page-sizes="[10, 20, 50, 100]"
              show-size-picker
              @update:page="loadPage"
              @update:page-size="handleSizeChange"
          />
        </div>
      </div>
    </div>

    <!-- 生成弹窗 -->
    <n-modal v-model:show="showGenerate" preset="card" title="生成 Token" style="width: 480px">
      <n-form :model="genForm" label-placement="left" label-width="90px" class="mt-2">
        <n-form-item label="生成数量">
          <n-input-number v-model:value="genForm.count" :min="1" :max="1000" style="width: 100%"/>
        </n-form-item>
        <n-form-item label="可用次数">
          <n-input-number
              v-model:value="genForm.maxUses"
              :min="1"
              clearable
              placeholder="不填则不限次数"
              style="width: 100%"
          />
          <template #feedback>
            <span class="text-xs text-gray-400">每个 Token 最多可参加测验的次数，留空表示不限</span>
          </template>
        </n-form-item>
        <n-form-item label="批次编码">
          <n-input v-model:value="genForm.batchCode" placeholder="留空自动生成"/>
        </n-form-item>
        <n-form-item label="来源">
          <n-select v-model:value="genForm.source" :options="sourceOptions"/>
        </n-form-item>
        <n-form-item label="授权测验">
          <div class="flex items-center gap-2 w-full">
            <n-button style="flex-shrink:0" @click="showQuizPicker = true">选择测验</n-button>
            <span class="text-sm text-gray-500">
              {{ genForm.quizIds?.length ? `已选 ${genForm.quizIds.length} 个` : '不限制，用户可参与所有已发布测验' }}
            </span>
            <n-button v-if="genForm.quizIds?.length" text type="error" style="flex-shrink:0" @click="genForm.quizIds = null">清除</n-button>
          </div>
        </n-form-item>
        <n-form-item label="过期时间">
          <n-date-picker
              v-model:value="genForm.expiresAt"
              type="datetime"
              clearable
              style="width: 100%"
              placeholder="不填则永不过期"
          />
        </n-form-item>
        <div class="flex justify-end gap-3 mt-4">
          <n-button size="large" @click="showGenerate = false">取消</n-button>
          <n-button type="primary" size="large" :loading="generating" @click="handleGenerate">
            生成
          </n-button>
        </div>
      </n-form>
    </n-modal>

    <QuizPickerModal
        v-model:show="showQuizPicker"
        :selected-ids="genForm.quizIds ?? []"
        @confirm="(ids) => { genForm.quizIds = ids.length ? ids : null }"
    />

    <QuizPickerModal
        v-model:show="showEditQuizPicker"
        :selected-ids="editingToken?.quizIds ?? []"
        @confirm="handleEditQuizConfirm"
    />

    <!-- 生成结果弹窗 -->
    <n-modal v-model:show="showResult" preset="card" title="生成成功" style="width: 580px">
      <div class="space-y-4">
        <n-alert type="success" :bordered="false">
          成功生成 <strong>{{ generatedResult?.count }}</strong> 个 Token，批次编码：<strong>{{ generatedResult?.batchCode }}</strong>
        </n-alert>
        <n-input :value="generatedResult?.tokens.map(t => buildTokenUrl(t)).join('\n')" type="textarea" :rows="10" readonly/>
        <div class="flex justify-end gap-3">
          <n-button size="large" @click="copyTokens">
            <template #icon><Icon icon="fluent:copy-20-regular"/></template>
            复制全部
          </n-button>
          <n-button type="primary" size="large" @click="showResult = false">关闭</n-button>
        </div>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, onMounted, onUnmounted, h } from 'vue';
import { NTag, NButton, NTooltip, useNotification, type DataTableColumns } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { apiGetTokenPage, apiGenerateTokens, apiUpdateTokenQuizIds, type TokenDetail, type GeneratedTokensResult } from '@/api/quizTokenApi.ts';
import QuizPickerModal from './QuizPickerModal.vue';

const notification = useNotification();
const loading = ref(false);
const generating = ref(false);
const showGenerate = ref(false);
const showResult = ref(false);

const showQuizPicker = ref(false);
const showEditQuizPicker = ref(false);
const editingToken = ref<TokenDetail | null>(null);
const updatingQuiz = ref(false);
const tableData = ref<TokenDetail[]>([]);
const total = ref(0);
const generatedResult = ref<GeneratedTokensResult | null>(null);
const tableHeight = ref(400);

const calculateTableHeight = () => {
  tableHeight.value = window.innerHeight - 310;
};

const params = reactive({
  pageIndex: 1,
  pageSize: 20,
  batchCode: null as string | null,
  status: null as string | null,
});

const genForm = reactive({
  count: 10,
  maxUses: null as number | null,
  batchCode: '',
  source: 'admin',
  quizIds: null as string[] | null,
  expiresAt: null as number | null,
});


const statusOptions = [
  { label: '可用', value: 'active' },
  { label: '已用完', value: 'exhausted' },
  { label: '已过期', value: 'expired' },
];

const sourceOptions = [
  { label: '后台发放', value: 'admin' },
  { label: '购买', value: 'purchase' },
  { label: '赠送', value: 'gift' },
  { label: '批量', value: 'batch' },
];

const statusTagType: Record<string, 'success' | 'warning' | 'error'> = {
  active: 'success',
  exhausted: 'warning',
  expired: 'error',
};
const statusLabel: Record<string, string> = {
  active: '可用',
  exhausted: '已用完',
  expired: '已过期',
};

const columns: DataTableColumns<TokenDetail> = [
  {
    title: 'Token',
    key: 'token',
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', { class: 'font-mono text-xs text-gray-600 select-all' }, row.token);
    },
  },
  {
    title: '已用 / 上限',
    key: 'usedCount',
    width: 110,
    align: 'center',
    render(row) {
      return h('span', { class: 'text-gray-700' }, `${row.usedCount} / ${row.maxUses ?? '不限'}`);
    },
  },
  {
    title: '状态',
    key: 'status',
    width: 90,
    align: 'center',
    filterOptions: statusOptions.map(s => ({ label: s.label, value: s.value })),
    filter: true,
    render(row) {
      return h(NTag, { type: statusTagType[row.status] || 'default', size: 'small', round: true, bordered: false }, {
        default: () => statusLabel[row.status] || row.status,
      });
    },
  },
  {
    title: '批次',
    key: 'batchCode',
    width: 160,
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', { class: 'text-gray-600 text-sm' }, row.batchCode || '-');
    },
  },
  {
    title: '授权测验',
    key: 'quizIds',
    width: 200,
    render(row) {
      if (!row.quizIds || row.quizIds.length === 0) {
        return h(NTag, { type: 'default', size: 'small', bordered: false }, { default: () => '全部' });
      }
      return h(NTag, { type: 'info', size: 'small', bordered: false }, { default: () => `${row.quizIds.length} 个测验` });
    },
  },
  {
    title: '来源',
    key: 'source',
    width: 90,
    align: 'center',
    render(row) {
      return h('span', { class: 'text-gray-600 text-sm' }, row.source);
    },
  },
  {
    title: '过期时间',
    key: 'expiresAt',
    width: 170,
    render(row) {
      return h('span', { class: 'text-gray-600 text-sm' }, row.expiresAt || '永不过期');
    },
  },
  {
    title: '创建时间',
    key: 'createdAt',
    width: 170,
    render(row) {
      return h('span', { class: 'text-gray-600 text-sm' }, row.createdAt);
    },
  },
  {
    title: '操作',
    key: 'operate',
    width: 120,
    fixed: 'right',
    align: 'center',
    render(row) {
      return h('div', { class: 'flex items-center justify-center gap-1' }, [
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            circle: true,
            onClick: () => copySingleToken(row.token),
          }, { icon: () => h(Icon, { icon: 'fluent:copy-20-regular' }) }),
          default: () => '复制链接',
        }),
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            circle: true,
            onClick: () => openEditQuizPicker(row),
          }, { icon: () => h(Icon, { icon: 'fluent:edit-20-regular' }) }),
          default: () => '编辑授权测验',
        }),
      ]);
    },
  },
];

const loadPage = () => {
  loading.value = true;
  apiGetTokenPage({ ...params }).then(res => {
    if (res.code === 200) {
      tableData.value = res.data.data;
      total.value = res.data.totalCount;
    } else {
      notification.error({ title: '加载失败', content: res.message, duration: 3000 });
    }
  }).catch((err: string) => {
    notification.error({ title: '加载失败', content: err, duration: 3000 });
  }).finally(() => { loading.value = false; });
};

const handleSizeChange = (size: number) => {
  params.pageSize = size;
  params.pageIndex = 1;
  loadPage();
};

const handleGenerate = () => {
  generating.value = true;
  apiGenerateTokens({
    count: genForm.count,
    maxUses: genForm.maxUses || null,
    source: genForm.source,
    batchCode: genForm.batchCode || null,
    quizIds: genForm.quizIds?.length ? genForm.quizIds : null,
    expiresAt: genForm.expiresAt ? new Date(genForm.expiresAt).toISOString() : null,
  }).then(res => {
    if (res.code === 200) {
      generatedResult.value = res.data;
      showGenerate.value = false;
      showResult.value = true;
      loadPage();
    } else {
      notification.error({ title: '生成失败', content: res.message, duration: 3000 });
    }
  }).catch((err: string) => {
    notification.error({ title: '生成失败', content: err, duration: 3000 });
  }).finally(() => { generating.value = false; });
};

const buildTokenUrl = (token: string) => {
  return `${import.meta.env.VITE_APP_MOBILE_URL}/quiz?token=${token}`
}

const copyTokens = () => {
  const text = generatedResult.value?.tokens.map(t => buildTokenUrl(t)).join('\n') || ''
  navigator.clipboard.writeText(text).then(() => {
    notification.success({ title: '已复制全部链接', duration: 2000 })
  })
}

const openEditQuizPicker = (row: TokenDetail) => {
  editingToken.value = row;
  showEditQuizPicker.value = true;
};

const handleEditQuizConfirm = (ids: string[]) => {
  if (!editingToken.value) return;
  updatingQuiz.value = true;
  apiUpdateTokenQuizIds({
    tokenId: editingToken.value.id,
    quizIds: ids.length ? ids : null,
  }).then(res => {
    if (res.code === 200) {
      notification.success({ title: '授权测验已更新', duration: 2000 });
      loadPage();
    } else {
      notification.error({ title: '更新失败', content: res.message, duration: 3000 });
    }
  }).catch((err: string) => {
    notification.error({ title: '更新失败', content: err, duration: 3000 });
  }).finally(() => { updatingQuiz.value = false; });
};

const copySingleToken = (token: string) => {
  navigator.clipboard.writeText(buildTokenUrl(token)).then(() => {
    notification.success({ title: '已复制链接', duration: 1500 })
  })
}

onMounted(() => {
  calculateTableHeight();
  window.addEventListener('resize', calculateTableHeight);
  loadPage();
});

onUnmounted(() => {
  window.removeEventListener('resize', calculateTableHeight);
});
</script>

<style scoped lang="scss">
:deep(.n-data-table__body) {
  &::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  &::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 4px;
  }
  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 4px;
    &:hover {
      background: #9ca3af;
    }
  }
}

:deep(.n-data-table) {
  .n-data-table-th {
    background: linear-gradient(to bottom, #fafafa, #f5f5f5);
    font-weight: 600;
    color: #374151;
    border-bottom: 1px solid #e5e7eb;
  }
  .n-data-table-td {
    padding: 16px 16px;
    border-bottom: 1px solid #f3f4f6;
  }
  .n-data-table-tr:hover {
    background: linear-gradient(to right, #f9fafb, #f3f4f6);
  }
}

:deep(.n-button) {
  &:not(:disabled).n-button--primary-type {
    background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
    border: none;
    &:hover {
      background: linear-gradient(135deg, #d97706 0%, #ea580c 100%);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
    }
  }
}

:deep(.n-pagination) {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>
