<template>
  <n-modal
      v-model:show="visible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :style="{ width: '750px' }"
      :bordered="false"
      segmented
      class="role-select-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon icon="fluent:people-team-20-filled" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">选择角色</span>
      </div>
    </template>

    <div class="flex flex-col h-[600px]">
      <!-- 搜索栏 -->
      <div class="px-6 py-4 border-b border-gray-100">
        <n-input-group>
          <n-input
              v-model:value="params.search"
              placeholder="请输入角色名称或编码"
              clearable
              @clear="handleClearSearch"
              @keyup.enter="handleSearch"
              size="large"
          >
            <template #prefix>
              <Icon icon="fluent:search-20-regular" class="text-gray-400"/>
            </template>
          </n-input>
          <n-button type="primary" size="large" @click="handleSearch">
            搜索
          </n-button>
        </n-input-group>
      </div>

      <!-- 表格区域 -->
      <div class="flex-1 px-6 overflow-hidden">
        <n-data-table
            :columns="columns"
            :data="roleList"
            :loading="loading"
            :pagination="false"
            :bordered="false"
            striped
            :max-height="400"
            :single-line="false"
            @row-click="handleRowClick"
            :row-class-name="getRowClassName"
            class="role-select-table"
        />
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && roleList.length === 0" class="flex flex-col items-center justify-center py-12">
        <Icon icon="fluent:folder-open-20-regular" class="text-gray-400 mb-3" :width="48" :height="48"/>
        <p class="text-gray-500">暂无角色数据</p>
      </div>

      <!-- 分页区域 -->
      <div class="px-6 py-4 border-t border-gray-100">
        <n-pagination
            v-model:page="params.pageIndex"
            v-model:page-size="params.pageSize"
            :page-count="pageCount"
            :page-sizes="[10, 20, 50, 100]"
            show-size-picker
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
            class="justify-center"
        />
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import {ref, computed, h} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NModal,
  NDataTable,
  NButton,
  NPagination,
  NInput,
  NInputGroup,
  NTag,
  NRadio,
  useNotification,
  type DataTableColumns
} from 'naive-ui'
import {
  apiGetRolePage,
  type RoleDetail,
  type RolePageParams
} from '@/api/roleApi.ts'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts"

const notification = useNotification()
const emit = defineEmits(['selected'])

// 状态
const visible = ref(false)
const loading = ref(false)
const roleList = ref<RoleDetail[]>([])
const total = ref(0)
const selectedId = ref<string | null>(null)

// 分页参数
const params = ref<RolePageParams>({
  pageSize: 20,
  pageIndex: 1,
  search: null,
  searchFields: []
})

// 计算属性
const pageCount = computed(() => Math.ceil(total.value / params.value.pageSize))

// 表格列定义
const columns: DataTableColumns<RoleDetail> = [
  {
    title: '选择',
    key: 'select',
    width: 60,
    align: 'center',
    render(row) {
      return h(NRadio, {
        checked: selectedId.value === row.id,
        onUpdateChecked: (checked: boolean) => {
          if (checked) {
            handleSelect(row)
          }
        }
      })
    }
  },
  {
    title: '角色名称',
    key: 'name',
    render(row) {
      return h('div', {class: 'flex items-center gap-3'}, [
        h('div', {
          class: `w-8 h-8 rounded-lg ${
              row.enabled
                  ? 'bg-gradient-to-br from-indigo-500 to-purple-600'
                  : 'bg-gray-400'
          } flex items-center justify-center text-white text-xs font-bold`
        }, row.name.substring(0, 2)),
        h('div', [
          h('div', {class: 'font-medium text-gray-800'}, row.name),
          h('div', {class: 'text-xs text-gray-500'}, row.code)
        ])
      ])
    }
  },
  {
    title: '角色编码',
    key: 'code',
    width: 150,
    render(row) {
      const typeMap = {
        'SUPER_ADMIN': {type: 'error', icon: 'fluent:shield-lock-20-filled'},
        'ADMIN': {type: 'warning', icon: 'fluent:building-20-filled'},
        'WEB_USER': {type: 'info', icon: 'fluent:person-20-filled'},
      }
      const config = typeMap[row.code] || {type: 'default', icon: 'fluent:tag-20-filled'}

      return h(NTag, {
        type: config.type as any,
        round: true,
        size: 'small'
      }, {
        icon: () => h(Icon, {icon: config.icon}),
        default: () => row.code
      })
    }
  },
  {
    title: '状态',
    key: 'enabled',
    width: 80,
    align: 'center',
    render(row) {
      return h(NTag, {
        type: row.enabled ? 'success' : 'default',
        size: 'small',
        round: true
      }, {
        default: () => row.enabled ? '启用' : '禁用'
      })
    }
  }
]

// 获取行样式
const getRowClassName = (row: RoleDetail) => {
  if (selectedId.value === row.id) return 'selected-row'
  return ''
}

// 打开弹窗
const open = () => {
  visible.value = true
  selectedId.value = null
  getRolePage()
}

// 关闭弹窗
const close = () => {
  visible.value = false
}

// 获取角色列表
const getRolePage = () => {
  loading.value = true
  apiGetRolePage(params.value).then((res) => {
    if (res.code === 200) {
      total.value = res.data.filterCount
      roleList.value = res.data.data
    } else {
      notification.error({
        title: '获取角色列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取角色列表失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 搜索处理
const handleSearch = () => {
  params.value.searchFields = params.value.search ? ['name', 'code'] : []
  params.value.pageIndex = 1
  getRolePage()
}

const handleClearSearch = () => {
  params.value.search = null
  params.value.searchFields = []
  params.value.pageIndex = 1
  getRolePage()
}

// 分页处理
const handlePageChange = (page: number) => {
  params.value.pageIndex = page
  getRolePage()
}

const handlePageSizeChange = (pageSize: number) => {
  params.value.pageSize = pageSize
  params.value.pageIndex = 1
  getRolePage()
}

// 行点击处理
const handleRowClick = (row: RoleDetail) => {
  handleSelect(row)
}

// 选择角色
const handleSelect = (role: RoleDetail) => {
  selectedId.value = role.id
  emit('selected', role)
  close()
}

// 暴露方法
defineExpose({
  open,
  close
})
</script>

<style scoped lang="scss">
// 弹窗样式
:deep(.n-card) {
  border-radius: 1.5rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);

  .n-card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #f3f4f6;
  }

  .n-card__content {
    padding: 0;
  }
}

// 数据表格样式优化
:deep(.role-select-table) {
  .n-data-table-th {
    background: linear-gradient(to bottom, #fafafa, #f5f5f5);
    font-weight: 600;
    color: #374151;
  }

  .n-data-table-td {
    padding: 16px;
  }

  .n-data-table-tr {
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: linear-gradient(to right, #f9fafb, #f3f4f6);
    }

    &.selected-row {
      background: linear-gradient(to right, #ede9fe, #e9d5ff);
    }
  }
}

// 输入框样式
:deep(.n-input) {
  &.n-input--focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1);
  }
}

// 按钮样式
:deep(.n-button) {
  &.n-button--primary-type {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border: none;

    &:hover {
      background: linear-gradient(135deg, #5558e3 0%, #7c4ce3 100%);
    }
  }
}

// 标签样式
:deep(.n-tag) {
  font-weight: 500;

  &.n-tag--success-type {
    background: rgba(16, 185, 129, 0.1);
    color: #059669;
    border-color: rgba(16, 185, 129, 0.2);
  }

  &.n-tag--error-type {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    border-color: rgba(239, 68, 68, 0.2);
  }

  &.n-tag--warning-type {
    background: rgba(245, 158, 11, 0.1);
    color: #d97706;
    border-color: rgba(245, 158, 11, 0.2);
  }

  &.n-tag--info-type {
    background: rgba(59, 130, 246, 0.1);
    color: #2563eb;
    border-color: rgba(59, 130, 246, 0.2);
  }
}
</style>