<template>
  <n-modal :show="show" @update:show="$emit('update:show', $event)" preset="card" title="选择授权测验" style="width: 680px">
    <div class="flex flex-col gap-3">
      <div class="flex items-center gap-3">
        <n-input
            v-model:value="search"
            placeholder="搜索测验名称"
            clearable
            style="width: 240px"
            @keyup.enter="loadPage(1)"
            @clear="loadPage(1)"
        />
        <n-button @click="loadPage(1)">搜索</n-button>
        <span class="text-sm text-gray-500 ml-auto">已选 {{ checkedIds.length }} 个</span>
      </div>

      <n-data-table
          :columns="columns"
          :data="data"
          :loading="loading"
          :pagination="false"
          :bordered="false"
          :row-key="(row: QuizDetail) => row.id"
          :row-class-name="rowClassName"
          :row-props="rowProps"
          :max-height="360"
          striped
      />

      <div class="flex items-center justify-between">
        <n-pagination
            v-model:page="pageIndex"
            v-model:page-size="pageSize"
            :item-count="total"
            :page-sizes="[10, 20, 50]"
            show-size-picker
            @update:page="loadPage"
            @update:page-size="(s: number) => { pageSize = s; loadPage(1) }"
        />
        <div class="flex gap-3">
          <n-button @click="$emit('update:show', false)">取消</n-button>
          <n-button type="primary" @click="handleConfirm">确认</n-button>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="tsx">
import { ref, watch, h } from 'vue'
import { NTag } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { apiGetQuizPage, type QuizDetail } from '@/api/quizApi.ts'
import { Icon } from '@iconify/vue'

const props = defineProps<{ show: boolean; selectedIds: string[] }>()
const emit = defineEmits<{
  (e: 'update:show', val: boolean): void
  (e: 'confirm', ids: string[]): void
}>()

const search = ref('')
const loading = ref(false)
const data = ref<QuizDetail[]>([])
const total = ref(0)
const pageIndex = ref(1)
const pageSize = ref(10)
const checkedIds = ref<string[]>([])

const columns: DataTableColumns<QuizDetail> = [
  {
    key: 'selected',
    width: 44,
    align: 'center',
    render: (row) => {
      const checked = checkedIds.value.includes(row.id)
      return h('div', { class: 'flex items-center justify-center' }, [
        h('div', {
          class: [
            'w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all',
            checked
              ? 'bg-violet-500 border-violet-500'
              : 'border-gray-300',
          ].join(' '),
        }, checked
          ? [h(Icon, { icon: 'fluent:checkmark-12-filled', color: 'white', width: 12, height: 12 })]
          : []
        ),
      ])
    },
  },
  { title: '测验名称', key: 'name', ellipsis: { tooltip: true } },
  {
    title: '类型', key: 'quizType', width: 90, align: 'center',
    render: (row) => h(NTag, { size: 'small', bordered: false }, { default: () => row.quizType }),
  },
  {
    title: '状态', key: 'status', width: 80, align: 'center',
    render: (row) => h(NTag, {
      size: 'small', bordered: false,
      type: row.status === 'published' ? 'success' : 'default',
    }, { default: () => row.status === 'published' ? '已发布' : '草稿' }),
  },
]

const rowProps = (row: QuizDetail) => ({
  style: 'cursor: pointer',
  onClick: () => {
    const idx = checkedIds.value.indexOf(row.id)
    if (idx >= 0) {
      checkedIds.value.splice(idx, 1)
    } else {
      checkedIds.value.push(row.id)
    }
  },
})

const rowClassName = (row: QuizDetail) =>
  checkedIds.value.includes(row.id) ? 'quiz-picker-row--selected' : ''

const loadPage = (page?: number) => {
  if (page) {
    pageIndex.value = page
  }
  loading.value = true
  apiGetQuizPage({
    pageIndex: pageIndex.value,
    pageSize: pageSize.value,
    search: search.value || null,
    status: 'published',
  }).then(res => {
    if (res.code === 200) {
      data.value = res.data.data
      total.value = res.data.totalCount
    }
  }).finally(() => {
    loading.value = false
  })
}

const handleConfirm = () => {
  emit('confirm', [...checkedIds.value])
  emit('update:show', false)
}

watch(() => props.show, (val) => {
  if (val) {
    checkedIds.value = [...props.selectedIds]
    search.value = ''
    pageIndex.value = 1
    loadPage(1)
  }
})
</script>

<style scoped>
:deep(.quiz-picker-row--selected td) {
  background: #f5f3ff !important;
}
</style>
