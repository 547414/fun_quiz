<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div
                class="w-12 h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-violet-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:shield-keyhole-20-filled" :width="24" :height="24"/>
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:checkmark-12-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              功能权限管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">管理系统功能权限及授权配置</p>
          </div>
        </div>

        <!-- 操作按钮组 -->
        <div class="flex items-center gap-4">
          <n-tooltip>
            <template #trigger>
              <div class="flex items-center gap-2 text-sm text-amber-600 bg-amber-50 px-3 py-2 rounded-lg">
                <Icon icon="fluent:warning-16-filled"/>
                <span>此处的菜单节点是指web端</span>
              </div>
            </template>
            仅管理web端的菜单权限
          </n-tooltip>
          <div class="relative">
            <n-input
                v-model:value="params.search"
                placeholder="搜索权限名称"
                clearable
                @clear="handleSearch(true)"
                @keyup.enter="handleSearch(false)"
                size="large"
                :style="{ width: '280px' }"
            />
          </div>

          <n-button
              type="primary"
              size="large"
              @click="handleAdd"
              class="shadow-md hover:shadow-lg transition-all duration-200"
          >
            <template #icon>
              <Icon icon="fluent:add-circle-20-filled"/>
            </template>
            新增权限
          </n-button>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 px-6 pb-6 overflow-hidden mt-6">
      <div class="h-full bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <!-- 表格区域 -->
        <div class="p-6 pb-0">
          <n-data-table
              :columns="columns"
              :data="permissionList"
              :loading="loading"
              :pagination="false"
              :bordered="false"
              striped
              :max-height="tableHeight"
              :scroll-x="1200"
              :row-class-name="rowClassName"
              @update:filters="handleFilterChange"
              @update:sorter="handleSorterChange"
          />
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && permissionList.length === 0" class="flex flex-col items-center justify-center py-16">
          <div class="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Icon icon="fluent:shield-keyhole-20-regular" class="text-gray-400" :width="48" :height="48"/>
          </div>
          <p class="text-gray-500 text-lg">暂无权限数据</p>
          <p class="text-gray-400 text-sm mt-2">点击上方"新增权限"按钮创建一个权限项</p>
        </div>

        <!-- 分页区域 -->
        <div class="px-6 py-4 border-t border-gray-100 flex items-center justify-between">
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <Icon icon="fluent:info-16-regular"/>
            共 <span class="font-medium text-gray-700 mx-1">{{ total }}</span> 条记录
          </div>
          <n-pagination
              v-model:page="params.pageIndex"
              v-model:page-size="params.pageSize"
              :page-count="pageCount"
              :page-sizes="[10, 20, 50, 100]"
              show-size-picker
              @update:page="handlePageChange"
              @update:page-size="handlePageSizeChange"
          />
        </div>
      </div>
    </div>

    <!-- 权限编辑组件 -->
    <PermissionEditModal
        ref="permissionEditModalRef"
        @success="handleEditSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import {ref, computed, h, onMounted, onUnmounted} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NDataTable,
  NButton,
  NSwitch,
  NPagination,
  NInput,
  NSpace,
  NTag,
  NTooltip,
  NPopover,
  useNotification,
  useDialog,
  type DataTableColumns,
  type DataTableFilterState,
  type DataTableSortState
} from 'naive-ui'
import {
  apiChangePermissionEnabled, apiDeletePermission,
  apiGetPermissionPage,
  type ChangePermissionEnabledParams, DeletePermissionParams,
  type PermissionPageDetail,
  type PermissionPageParams,
} from '@/api/permissionApi.ts'
import {
  apiChangeBackendApiIgnoreAuth,
  type ChangeBackendApiIgnoreAuthParams
} from '@/api/backendApiApi.ts'
import {formatAllowAssignShortText, formatDenyAssignShortText} from '@/utils/format.ts'
import {PageSortEnum} from '@/enum/pageSortEnum.ts'
import PermissionEditModal from '@/components/sys/permission/EditModal.vue'

const notification = useNotification()
const dialog = useDialog()

// 组件引用
const permissionEditModalRef = ref()

// 数据状态
const loading = ref(false)
const permissionList = ref<PermissionPageDetail[]>([])
const total = ref(0)
const tableHeight = ref(400)

// 分页参数
const params = ref<PermissionPageParams>({
  pageSize: 10,
  pageIndex: 1,
  search: null,
  categoryList: null,
  nameSort: null,
  searchFields: []
})

// 计算属性
const pageCount = computed(() => Math.ceil(total.value / params.value.pageSize))

// 类别选项
const categoryOptions = [
  {label: '菜单节点', value: 'MENU'},
  {label: '后端接口', value: 'BACKEND_API'}
]

// 计算表格高度
const calculateTableHeight = () => {
  const windowHeight = window.innerHeight
  tableHeight.value = windowHeight - 320
}

onMounted(() => {
  calculateTableHeight()
  window.addEventListener('resize', calculateTableHeight)
  getPermissionPage()
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateTableHeight)
})

// 行样式
const rowClassName = (row: PermissionPageDetail) => {
  if (!row.enabled) return 'disabled-row'
  return ''
}

// 表格列定义
const columns: DataTableColumns<PermissionPageDetail> = [
  {
    title: '名称',
    key: 'name',
    width: 200,
    sorter: true,
    fixed: 'left',
    render(row) {
      return h('div', {class: 'flex items-center gap-3'}, [
        h('div', [
          h('div', {class: 'font-medium text-gray-800'}, row.name),
          h('div', {class: 'text-xs text-gray-500 mt-0.5'}, `ID: ${row.id}`)
        ])
      ])
    }
  },
  {
    title: '编码',
    key: 'code',
    width: 180,
    render(row) {
      return h(NTag, {
        round: true,
        size: 'small'
      }, {
        default: () => row.code || '-'
      })
    }
  },
  {
    title: '类型',
    key: 'resourceCategoryDisplay',
    width: 120,
    filter: true,
    filterOptions: categoryOptions,
    render(row) {
      const typeConfig = row.resourceCategoryDisplay === 'MENU'
          ? {type: 'info' as const, icon: 'fluent:navigation-20-filled', text: '菜单节点'}
          : {type: 'warning' as const, icon: 'fluent:code-20-filled', text: '后端接口'}

      return h(NTag, {
        type: typeConfig.type,
        round: true,
        size: 'small'
      }, {
        icon: () => h(Icon, {icon: typeConfig.icon}),
        default: () => typeConfig.text
      })
    }
  },
  {
    title: '授权给',
    key: 'assignList',
    width: 280,
    render(row) {
      if (!row.assignList || row.assignList.length === 0) {
        return h('span', {class: 'text-gray-400 text-sm'}, '暂无授权')
      }

      const maxDisplay = 2
      const displayList = row.assignList.slice(0, maxDisplay)
      const remaining = row.assignList.length - maxDisplay

      return h('div', {class: 'flex flex-wrap gap-2'}, [
        ...displayList.map(assign => {
          const isAllow = assign.policy === 'ALLOW'
          const text = isAllow ? formatAllowAssignShortText(assign) : formatDenyAssignShortText(assign)

          return h(NTooltip, {}, {
            trigger: () => h(NTag, {
              type: isAllow ? 'success' : 'error',
              size: 'small',
              round: true
            }, {
              icon: () => h(Icon, {
                icon: isAllow ? 'fluent:checkmark-circle-16-filled' : 'fluent:dismiss-circle-16-filled'
              }),
              default: () => text
            }),
            default: () => text
          })
        }),
        remaining > 0 && h(NPopover, {
          trigger: 'hover',
          placement: 'top'
        }, {
          trigger: () => h(NTag, {
            type: 'default',
            size: 'small',
            round: true
          }, () => `+${remaining}`),
          default: () => h('div', {class: 'space-y-2'},
              row.assignList.slice(maxDisplay).map(assign => {
                const isAllow = assign.policy === 'ALLOW'
                const text = isAllow ? formatAllowAssignShortText(assign) : formatDenyAssignShortText(assign)
                return h(NTag, {
                  type: isAllow ? 'success' : 'error',
                  size: 'small',
                  round: true
                }, {
                  icon: () => h(Icon, {
                    icon: isAllow ? 'fluent:checkmark-circle-16-filled' : 'fluent:dismiss-circle-16-filled'
                  }),
                  default: () => text
                })
              })
          )
        })
      ])
    }
  },
  {
    title: '忽略验证',
    key: 'ignoreAuth',
    width: 120,
    align: 'center',
    render(row) {
      if (row.ignoreAuth === null) {
        return h('span', {class: 'text-gray-400 text-sm'}, '无此属性')
      }

      return h('div', {class: 'flex items-center justify-center'}, [
        h(NSwitch, {
          value: row.ignoreAuth,
          size: 'medium',
          onUpdateValue: (value: boolean) => handleIgnoreAuthChange(row, value)
        })
      ])
    }
  },
  {
    title: '启用状态',
    key: 'enabled',
    width: 100,
    align: 'center',
    render(row) {
      return h('div', {class: 'flex items-center justify-center'}, [
        h(NSwitch, {
          value: row.enabled,
          size: 'medium',
          onUpdateValue: (value: boolean) => handleEnabledChange(row, value)
        })
      ])
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    fixed: 'right',
    align: 'center',
    render(row) {
      return h(NSpace, {size: 'small', justify: 'center'}, () => [
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'primary',
            circle: true,
            onClick: () => handleEdit(row)
          }, {
            icon: () => h(Icon, {icon: 'fluent:edit-20-regular'})
          }),
          default: () => '编辑'
        }),
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'error',
            secondary: true,
            circle: true,
            onClick: () => handleDelete(row)
          }, {
            icon: () => h(Icon, {icon: 'fluent:delete-20-regular'})
          }),
          default: () => '删除'
        })
      ])
    }
  }
]

// 获取权限列表
const getPermissionPage = () => {
  loading.value = true
  apiGetPermissionPage(params.value).then((res) => {
    if (res.code === 200) {
      total.value = res.data.filterCount
      permissionList.value = res.data.data
    } else {
      notification.error({
        title: '获取权限列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取权限列表失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 搜索处理
const handleSearch = (clear: boolean = false) => {
  if (clear) {
    params.value.search = null
  }
  params.value.searchFields = params.value.search ? ['name', 'code'] : []
  params.value.pageIndex = 1
  getPermissionPage()
}

// 筛选处理
const handleFilterChange = (filters: DataTableFilterState) => {
  params.value.categoryList = filters.resourceCategoryDisplay as string[] || null
  getPermissionPage()
}

// 排序处理
const handleSorterChange = (sorter: DataTableSortState) => {
  if (sorter && sorter.columnKey === 'name') {
    if (sorter.order === 'ascend') {
      params.value.nameSort = PageSortEnum.ASC
    } else if (sorter.order === 'descend') {
      params.value.nameSort = PageSortEnum.DESC
    } else {
      params.value.nameSort = null
    }
  } else {
    params.value.nameSort = null
  }
  getPermissionPage()
}

// 分页处理
const handlePageChange = (page: number) => {
  params.value.pageIndex = page
  getPermissionPage()
}

const handlePageSizeChange = (pageSize: number) => {
  params.value.pageSize = pageSize
  params.value.pageIndex = 1
  getPermissionPage()
}

// 启用/禁用权限
const handleEnabledChange = (permission: PermissionPageDetail, enabled: boolean) => {
  dialog.info({
    title: '确认操作',
    content: `确定要${enabled ? '启用' : '禁用'}权限【${permission.name}】吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: () => {
      const params: ChangePermissionEnabledParams = {
        id: permission.id,
        enabled
      }
      doChangeEnabled(params, permission)
    }
  })
}

const doChangeEnabled = (params: ChangePermissionEnabledParams, permission: PermissionPageDetail) => {
  loading.value = true
  apiChangePermissionEnabled(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: `已${params.enabled ? '启用' : '禁用'}权限【${permission.name}】`,
        duration: 3000
      })
      getPermissionPage()
    } else {
      notification.error({
        title: '操作失败',
        content: res.message,
        duration: 3000
      })
      permission.enabled = !permission.enabled
    }
  }).catch((err) => {
    notification.error({
      title: '操作失败',
      content: err,
      duration: 3000
    })
    permission.enabled = !permission.enabled
  }).finally(() => {
    loading.value = false
  })
}

// 忽略验证开关
const handleIgnoreAuthChange = (permission: PermissionPageDetail, ignoreAuth: boolean) => {
  dialog.info({
    title: '确认操作',
    content: `确定要${ignoreAuth ? '忽略验证' : '启用验证'}【${permission.name}】吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: () => {
      const params: ChangeBackendApiIgnoreAuthParams = {
        id: permission.resourceId,
        ignoreAuth
      }
      doChangeIgnoreAuth(params, permission)
    }
  })
}

const doChangeIgnoreAuth = (params: ChangeBackendApiIgnoreAuthParams, permission: PermissionPageDetail) => {
  loading.value = true
  apiChangeBackendApiIgnoreAuth(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: `已${params.ignoreAuth ? '忽略验证' : '启用验证'}【${permission.name}】`,
        duration: 3000
      })
      getPermissionPage()
    } else {
      notification.error({
        title: '操作失败',
        content: res.message,
        duration: 3000
      })
      permission.ignoreAuth = !permission.ignoreAuth
    }
  }).catch((err) => {
    notification.error({
      title: '操作失败',
      content: err,
      duration: 3000
    })
    permission.ignoreAuth = !permission.ignoreAuth
  }).finally(() => {
    loading.value = false
  })
}

// 新增权限
const handleAdd = () => {
  permissionEditModalRef.value?.open()
}

// 编辑权限
const handleEdit = (permission: PermissionPageDetail) => {
  permissionEditModalRef.value?.open(permission.id)
}

const handleDelete = (permission: PermissionPageDetail) => {
  dialog.warning({
    title: '确认操作',
    content: `是否确认删除【${permission.name}】?`,
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      deletePermission(permission)
    },
    onNegativeClick: () => {
    }
  })
}

const deletePermission = (permission: PermissionPageDetail) => {
  const deleteParams: DeletePermissionParams = {
    permissionId: permission.id
  }
  apiDeletePermission(deleteParams).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '删除成功',
        content: '权限已成功删除',
        duration: 3000
      })
      getPermissionPage()
    } else {
      notification.error({
        title: '删除失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '删除失败',
      content: err,
      duration: 3000
    })
  })
}

// 编辑成功回调
const handleEditSuccess = () => {
  getPermissionPage()
}
</script>

<style scoped lang="scss">
// 自定义滚动条
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

// 数据表格样式优化
:deep(.n-data-table) {
  .n-data-table-th {
    background: linear-gradient(to bottom, #fafafa, #f5f5f5);
    font-weight: 600;
    color: #374151;
    border-bottom: 1px solid #e5e7eb;
  }

  .n-data-table-td {
    padding: 20px 16px;
    border-bottom: 1px solid #f3f4f6;
  }

  .n-data-table-tr {
    &:hover {
      background: linear-gradient(to right, #f9fafb, #f3f4f6);
    }

    &.disabled-row {
      opacity: 0.6;

      .n-data-table-td {
        color: #9ca3af;
      }
    }
  }
}

// 按钮样式增强
:deep(.n-button) {
  &:not(:disabled) {
    &.n-button--primary-type {
      background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
      }
    }
  }
}

// 开关样式
:deep(.n-switch) {
  &.n-switch--active {
    .n-switch__rail {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
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

// 输入框样式
:deep(.n-input) {
  &.n-input--focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1);
  }
}
</style>