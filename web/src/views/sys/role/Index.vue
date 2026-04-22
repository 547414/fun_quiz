<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div
                class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:people-team-20-filled" :width="24" :height="24"/>
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:checkmark-12-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              角色管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">管理系统角色及权限配置</p>
          </div>
        </div>

        <!-- 操作按钮组 -->
        <div class="flex items-center gap-4">
          <div class="relative">
            <Icon
                icon="fluent:search-20-regular"
                class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
                :width="20"
                :height="20"
            />
            <n-input
                v-model:value="params.search"
                placeholder="搜索角色名称"
                clearable
                @clear="handleSearch(true)"
                @keyup.enter="handleSearch(false)"
                size="large"
                :style="{ width: '280px'}"
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
            新增角色
          </n-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片 - 修复跳动问题 -->
    <div class="px-6 py-4 grid grid-cols-4 gap-4">
      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">角色总数</p>
            <!-- 固定高度容器，避免跳动 -->
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-gray-800" v-else>{{ statisticsData?.total }}</p>
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:people-20-filled" class="text-blue-600" :width="24" :height="24"/>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">已启用</p>
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-green-600" v-else>{{ statisticsData?.enabledCount }}</p>
            </div>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:checkmark-circle-20-filled" class="text-green-600" :width="24" :height="24"/>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">已禁用</p>
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-red-600" v-else>{{ statisticsData?.disableCount }}</p>
            </div>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:dismiss-circle-20-filled" class="text-red-600" :width="24" :height="24"/>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">最近更新</p>
            <!-- 最近更新需要更高的容器来容纳两行文本 -->
            <div class="h-12 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" class="mb-3" round
                          style="width: 140px; height: 32px;"/>
              <p
                  class="text-sm font-medium text-gray-800"
                  v-if="statisticsData?.newestUpdatedAt && !statisticsLoading"
              >
                {{ dayjs(statisticsData.newestUpdatedAt).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss') }}
              </p>
            </div>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:clock-20-filled" class="text-purple-600" :width="24" :height="24"/>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 px-6 pb-6 overflow-hidden">
      <div class="h-full bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <!-- 表格区域 -->
        <div class="p-6 pb-0">
          <n-data-table
              :columns="columns"
              :data="roleList"
              :loading="loading"
              :pagination="false"
              :bordered="false"
              striped
              :max-height="tableHeight"
              :scroll-x="1000"
              :row-class-name="rowClassName"
          />
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && roleList.length === 0" class="flex flex-col items-center justify-center py-16">
          <div class="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Icon icon="fluent:folder-open-20-regular" class="text-gray-400" :width="48" :height="48"/>
          </div>
          <p class="text-gray-500 text-lg">暂无角色数据</p>
          <p class="text-gray-400 text-sm mt-2">点击上方"新增角色"按钮创建一个角色</p>
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

    <!-- 角色编辑组件 -->
    <RoleEditModal
        ref="roleEditModalRef"
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
  useNotification,
  useDialog,
  type DataTableColumns, NSkeleton
} from 'naive-ui'
import {
  apiChangeRoleEnabled, apiDeleteRole,
  apiGetRolePage, apiGetRoleStatistics,
  type ChangeRoleEnabledParams, DeleteRoleParams,
  type RoleDetail,
  type RolePageParams, RoleStatistics,
} from '@/api/roleApi.ts'
import RoleEditModal from '@/components/sys/role/EditModal.vue'
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import duration from 'dayjs/plugin/duration';

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(duration);

const notification = useNotification()
const dialog = useDialog()

// 组件引用
const roleEditModalRef = ref()

const statisticsData = ref<RoleStatistics>()

// 数据状态
const loading = ref(false)
const statisticsLoading = ref(false)
const roleList = ref<RoleDetail[]>([])
const total = ref(0)
const tableHeight = ref(400)

// 分页参数
const params = ref<RolePageParams>({
  pageSize: 20,
  pageIndex: 1,
  search: null,
  searchFields: []
})

const getRoleStatistics = (init: boolean = false) => {
  statisticsLoading.value = true
  if (init) {
    loading.value = true
  }
  apiGetRoleStatistics().then((res) => {
    if (res.code === 200) {
      statisticsData.value = res.data
      if (init) {
        // 初始化时获取第一页数据
        params.value.pageIndex = 1
        getRolePage()
      }
    } else {
      notification.error({
        title: '获取角色统计信息失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '获取角色统计信息失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    statisticsLoading.value = false
  })
}
getRoleStatistics(true)
// 计算属性
const pageCount = computed(() => Math.ceil(total.value / params.value.pageSize))

// 计算表格高度
const calculateTableHeight = () => {
  // 动态计算表格高度，确保分页器在底部
  const windowHeight = window.innerHeight
  tableHeight.value = windowHeight - 380 // 减去头部、统计卡片、分页等高度
}

onMounted(() => {
  calculateTableHeight()
  window.addEventListener('resize', calculateTableHeight)
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateTableHeight)
})

// 行样式
const rowClassName = (row: RoleDetail) => {
  if (!row.enabled) return 'disabled-row'
  return ''
}

// 表格列定义
const columns: DataTableColumns<RoleDetail> = [
  {
    title: '角色名称',
    key: 'name',
    width: 220,
    fixed: 'left',
    render(row: RoleDetail) {
      return h('div', {class: 'flex items-center gap-3'}, [
        h('div', {
          class: 'relative'
        }, [
          h('div', {
            class: `w-10 h-10 rounded-xl ${
                row.enabled
                    ? 'bg-gradient-to-br from-indigo-500 to-purple-600'
                    : 'bg-gray-400'
            } flex items-center justify-center text-white text-sm font-bold shadow-sm transition-all duration-200 hover:scale-105`
          }, row.name.substring(0, 2)),
          row.code === 'SUPER_ADMIN' && h('div', {
            class: 'absolute -top-1 -right-1 w-4 h-4 bg-yellow-500 rounded-full flex items-center justify-center'
          }, h(Icon, {icon: 'fluent:crown-16-filled', class: 'text-white', width: 10, height: 10}))
        ]),
        h('div', [
          h('div', {class: 'font-medium text-gray-800'}, row.name),
          h('div', {class: 'text-xs text-gray-500 mt-0.5'}, row.code)
        ])
      ])
    }
  },
  {
    title: '角色编码',
    key: 'code',
    width: 160,
    render(row: RoleDetail) {
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
    title: '角色描述',
    key: 'brief',
    ellipsis: {
      tooltip: true
    },
    render(row: RoleDetail) {
      return h('span', {class: 'text-white-600 text-sm'}, row.brief || '-')
    }
  },
  {
    title: '创建时间',
    key: 'createdAt',
    width: 180,
    render(row: RoleDetail) {
      // 使用 dayjs 格式化时间
      const formattedTime = dayjs(row.createdAt).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
      return h('div', {class: 'text-sm'}, [
        h('div', {class: 'text-gray-600'}, formattedTime.split(' ')[0]),
        h('div', {class: 'text-gray-400 text-xs'}, formattedTime.split(' ')[1])
      ])
    }
  },
  {
    title: '更新时间',
    key: 'updatedAt',
    width: 180,
    render(row: RoleDetail) {
      // 使用 dayjs 格式化时间
      const formattedTime = dayjs(row.updatedAt).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
      return h('div', {class: 'text-sm'}, [
        h('div', {class: 'text-gray-600'}, formattedTime.split(' ')[0]),
        h('div', {class: 'text-gray-400 text-xs'}, formattedTime.split(' ')[1])
      ])
    }
  },
  {
    title: '状态',
    key: 'enabled',
    width: 100,
    align: 'center',
    render(row: RoleDetail) {
      return h('div', {class: 'flex items-center justify-center'}, [
        h(NSwitch, {
          value: row.enabled,
          disabled: row.code === 'SUPER_ADMIN',
          size: 'medium',
          onUpdateValue: (value: boolean) => handleEnabledChange(row, value)
        }, {
          checked: () => '启用',
          unchecked: () => '禁用'
        })
      ])
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 180,
    fixed: 'right',
    align: 'center',
    render(row: RoleDetail) {
      return h(NSpace, {size: 'small', justify: 'center'}, () => [
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'primary',
            ghost: false,
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
            type: 'info',
            secondary: true,
            circle: true,
            onClick: () => handlePermission(row)
          }, {
            icon: () => h(Icon, {icon: 'fluent:key-20-regular'})
          }),
          default: () => '权限配置'
        }),
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'error',
            secondary: true,
            circle: true,
            disabled: row.code === 'SUPER_ADMIN',
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
const handleSearch = (clear: boolean = false) => {
  if (clear) {
    params.value.search = null
  }
  roleList.value = []
  params.value.searchFields = params.value.search ? ['name', 'code'] : []
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
  roleList.value = []
  getRolePage()
}

// 启用/禁用角色
const handleEnabledChange = (role: RoleDetail, enabled: boolean) => {
  dialog.info({
    title: '确认操作',
    content: `确定要${enabled ? '启用' : '禁用'}角色【${role.name}】吗？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      const params: ChangeRoleEnabledParams = {
        id: role.id,
        enabled
      }
      doChangeEnabled(params, role)
    },
    onNegativeClick: () => {
    }
  })
}

const doChangeEnabled = (params: ChangeRoleEnabledParams, role: RoleDetail) => {
  loading.value = true
  apiChangeRoleEnabled(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: `已${params.enabled ? '启用' : '禁用'}角色【${role.name}】`,
        duration: 3000
      })
      getRolePage()
      getRoleStatistics()
    } else {
      notification.error({
        title: '操作失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '操作失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 新增角色
const handleAdd = () => {
  roleEditModalRef.value?.open()
}

// 编辑角色
const handleEdit = (role: RoleDetail) => {
  roleEditModalRef.value?.open(role)
}

// 权限配置
const handlePermission = (role: RoleDetail) => {
  notification.info({
    title: '功能开发中',
    content: `角色【${role.name}】的权限配置功能正在开发中`,
    duration: 3000
  })
}

// 删除角色
const handleDelete = (role: RoleDetail) => {
  dialog.warning({
    title: '删除确认',
    content: `确定要删除角色【${role.name}】吗？删除后不可恢复。`,
    positiveText: '确定删除',
    negativeText: '取消',
    onPositiveClick: () => {
      deleteRole(role)
    }
  })
}

const deleteRole = (role: RoleDetail) => {
  const deleteParams: DeleteRoleParams = {
    roleId: role.id
  }
  loading.value = true
  apiDeleteRole(deleteParams).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '删除成功',
        content: `角色【${role.name}】已删除`,
        duration: 3000
      })
      params.value.pageIndex = 1
      getRolePage()
      getRoleStatistics()
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
  }).finally(() => {
    loading.value = false
  })
}

// 编辑成功回调
const handleEditSuccess = () => {
  getRolePage()
  getRoleStatistics()
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
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #5558e3 0%, #7c4ce3 100%);
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
  padding: 0 12px;

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
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
  }
}
</style>