<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div
                class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-blue-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:ticket-diagonal-20-filled" :width="24" :height="24"/>
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:key-16-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              邀请码管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">管理系统注册邀请码配置</p>
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
                placeholder="搜索邀请码或备注"
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
            新增邀请码
          </n-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="px-6 py-4 grid grid-cols-4 gap-4">
      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">邀请码总数</p>
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-gray-800" v-else>{{ statisticsData?.total || 0 }}</p>
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:ticket-diagonal-20-filled" class="text-blue-600" :width="24" :height="24"/>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">已用完</p>
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-orange-600" v-else>{{ statisticsData?.runOut || 0 }}</p>
            </div>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:person-add-20-filled" class="text-orange-600" :width="24" :height="24"/>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500">未用完</p>
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-green-600" v-else>{{ statisticsData?.notRunOut || 0 }}</p>
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
            <p class="text-sm text-gray-500">已过期</p>
            <div class="h-8 flex items-center mt-1">
              <n-skeleton text :repeat="1" v-if="statisticsLoading" round style="width: 60px; height: 32px;"/>
              <p class="text-2xl font-bold text-red-600" v-else>{{ statisticsData?.expired || 0 }}</p>
            </div>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
            <Icon icon="fluent:clock-dismiss-20-filled" class="text-red-600" :width="24" :height="24"/>
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
              :data="dataList"
              :loading="loading"
              :pagination="false"
              :bordered="false"
              striped
              :max-height="tableHeight"
              :scroll-x="1200"
              :row-class-name="rowClassName"
          />
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && dataList.length === 0" class="flex flex-col items-center justify-center py-16">
          <div class="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Icon icon="fluent:ticket-diagonal-20-regular" class="text-gray-400" :width="48" :height="48"/>
          </div>
          <p class="text-gray-500 text-lg">暂无邀请码数据</p>
          <p class="text-gray-400 text-sm mt-2">点击上方"新增邀请码"按钮创建一个邀请码</p>
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

    <!-- 邀请码编辑组件 -->
    <InviteCodeEditModal
        ref="inviteCodeEditModalRef"
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
  NProgress,
  useNotification,
  useDialog,
  useMessage,
  type DataTableColumns,
  NSkeleton
} from 'naive-ui'
import {
  apiChangeInviteCodeEnabled,
  apiDeleteInviteCode,
  apiGetInviteCodePage, apiGetInviteCodeStatistics,
  type ChangeInviteCodeEnableParams,
  type DeleteInviteCodeParams,
  type InviteCodeDetail,
  type InviteCodePageParams,
  type InviteCodePageResponse, InviteCodeStatistics
} from '@/api/inviteCodeApiApi.ts'
import InviteCodeEditModal from '@/components/sys/invite/EditModal.vue'
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import duration from 'dayjs/plugin/duration';

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(duration);

const notification = useNotification()
const dialog = useDialog()
const message = useMessage()

// 组件引用
const inviteCodeEditModalRef = ref()

// 统计数据（模拟）
const statisticsData = ref<InviteCodeStatistics>({
  total: 0,
  runOut: 0,
  notRunOut: 0,
  expired: 0
})

// 数据状态
const loading = ref(false)
const statisticsLoading = ref(false)
const dataList = ref<InviteCodeDetail[]>([])
const total = ref(0)
const tableHeight = ref(400)

// 分页参数
const params = ref<InviteCodePageParams>({
  pageSize: 20,
  pageIndex: 1,
  search: null,
  searchFields: [],
  nameSort: null,
})

// 计算属性
const pageCount = computed(() => Math.ceil(total.value / params.value.pageSize))

// 计算表格高度
const calculateTableHeight = () => {
  const windowHeight = window.innerHeight
  tableHeight.value = windowHeight - 380
}

onMounted(() => {
  calculateTableHeight()
  window.addEventListener('resize', calculateTableHeight)
  getPage()
  getStatistics()
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateTableHeight)
})

// 行样式
const rowClassName = (row: InviteCodeDetail) => {
  if (!row.enabled) return 'disabled-row'
  if (isExpired(row.deadline)) return 'expired-row'
  return ''
}

// 判断是否过期
const isExpired = (deadline: Date) => {
  const deadlineStr = dayjs(deadline).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
  return dayjs(deadlineStr).isBefore(dayjs())
}

// 计算使用进度
const getUsageProgress = (row: InviteCodeDetail) => {
  if (!row.maxLimit || row.maxLimit === 0) return 0
  return Math.round((row.registerNum / row.maxLimit) * 100)
}

// 表格列定义
const columns: DataTableColumns<InviteCodeDetail> = [
  {
    title: '邀请码',
    key: 'code',
    width: 296,
    fixed: 'left',
    render(row: InviteCodeDetail) {
      const isExpiredCode = isExpired(row.deadline)
      return h('div', {class: 'flex items-center gap-3'}, [
        h('div', {
          class: 'relative'
        }, [
          isExpiredCode && h('div', {
            class: 'absolute -top-1 -right-1 w-4 h-4 bg-red-600 rounded-full flex items-center justify-center'
          }, h(Icon, {icon: 'fluent:warning-12-filled', class: 'text-white', width: 10, height: 10}))
        ]),
        h('div', [
          h('div', {class: 'font-mono font-medium text-gray-800'}, row.code),
          h('div', {class: 'text-xs text-gray-500 mt-0.5'}, `已使用 ${row.registerNum || 0} 次`)
        ])
      ])
    }
  },
  {
    title: '备注',
    key: 'brief',
    ellipsis: {
      tooltip: true
    },
    render(row: InviteCodeDetail) {
      return h('span', {class: 'text-gray-600 text-sm'}, row.brief || '-')
    }
  },
  {
    title: '使用情况',
    key: 'usage',
    width: 200,
    render(row: InviteCodeDetail) {
      const progress = getUsageProgress(row)
      const color = progress >= 90 ? 'error' : progress >= 70 ? 'warning' : 'success'

      return h('div', {class: 'space-y-2'}, [
        h('div', {class: 'flex justify-between text-sm'}, [
          h('span', {class: 'text-gray-600'}, `${row.registerNum || 0} / ${row.maxLimit || '∞'}`),
          h('span', {class: 'text-gray-500'}, row.maxLimit ? `${progress}%` : '无限制')
        ]),
        row.maxLimit && h(NProgress, {
          type: 'line',
          percentage: progress,
          status: color as any,
          showIndicator: false,
          fillBorderRadius: 3,
          railBorderRadius: 3
        })
      ])
    }
  },
  {
    title: '有效期',
    key: 'deadline',
    width: 180,
    render(row: InviteCodeDetail) {
      const deadline = dayjs(row.deadline).tz('Asia/Shanghai')
      const isExpiredCode = isExpired(row.deadline)
      const daysLeft = deadline.diff(dayjs(), 'day')

      return h('div', {class: 'space-y-1'}, [
        h('div', {class: `text-sm ${isExpiredCode ? 'text-red-600' : 'text-gray-600'}`},
            deadline.format('YYYY-MM-DD')
        ),
        h(NTag, {
          type: isExpiredCode ? 'error' : daysLeft <= 7 ? 'warning' : 'success',
          size: 'small',
          round: true
        }, {
          icon: () => h(Icon, {
            icon: isExpiredCode ? 'fluent:clock-dismiss-16-filled' : 'fluent:clock-16-regular'
          }),
          default: () => isExpiredCode ? '已过期' : `剩余 ${daysLeft} 天`
        })
      ])
    }
  },
  {
    title: '状态',
    key: 'enabled',
    width: 100,
    align: 'center',
    render(row: InviteCodeDetail) {
      return h('div', {class: 'flex items-center justify-center'}, [
        h(NSwitch, {
          value: row.enabled,
          disabled: isExpired(row.deadline),
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
    width: 240,
    fixed: 'right',
    align: 'center',
    render(row: InviteCodeDetail) {
      return h(NSpace, {size: 'small', justify: 'center'}, () => [
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'warning',
            secondary: true,
            circle: true,
            onClick: () => handleShare(row)
          }, {
            icon: () => h(Icon, {icon: 'fluent:share-20-regular'})
          }),
          default: () => '分享'
        }),
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

// 获取统计数据（模拟）
const getStatistics = () => {
  statisticsLoading.value = true
  apiGetInviteCodeStatistics().then((res) => {
    if (res.code === 200) {
      statisticsData.value = res.data
    } else {
      notification.error({
        title: '获取统计数据失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '获取统计数据失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    statisticsLoading.value = false
  })
}

// 获取邀请码列表
const getPage = () => {
  loading.value = true
  apiGetInviteCodePage(params.value).then((res: InviteCodePageResponse) => {
    if (res.code === 200) {
      total.value = res.data.filterCount
      dataList.value = res.data.data
      getStatistics()
    } else {
      notification.error({
        title: '获取邀请码列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '获取邀请码列表失败',
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
  dataList.value = []
  params.value.searchFields = params.value.search ? ['code', 'brief'] : []
  params.value.pageIndex = 1
  getPage()
}

// 分页处理
const handlePageChange = (page: number) => {
  params.value.pageIndex = page
  getPage()
}

const handlePageSizeChange = (pageSize: number) => {
  params.value.pageSize = pageSize
  params.value.pageIndex = 1
  dataList.value = []
  getPage()
}

// 启用/禁用邀请码
const handleEnabledChange = (inviteCode: InviteCodeDetail, enabled: boolean) => {
  const params: ChangeInviteCodeEnableParams = {
    inviteCodeId: inviteCode.id,
    enabled
  }

  loading.value = true
  apiChangeInviteCodeEnabled(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: `已${enabled ? '启用' : '禁用'}邀请码【${inviteCode.code}】`,
        duration: 3000
      })
      getPage()
    } else {
      notification.error({
        title: '操作失败',
        content: res.message,
        duration: 3000
      })
      // 恢复原状态
      inviteCode.enabled = !enabled
    }
  }).catch((err: string) => {
    notification.error({
      title: '操作失败',
      content: err,
      duration: 3000
    })
    // 恢复原状态
    inviteCode.enabled = !enabled
  }).finally(() => {
    loading.value = false
  })
}

// 新增邀请码
const handleAdd = () => {
  inviteCodeEditModalRef.value?.open()
}

// 编辑邀请码
const handleEdit = (inviteCode: InviteCodeDetail) => {
  inviteCodeEditModalRef.value?.open(inviteCode)
}

// 分享邀请码
const handleShare = (inviteCode: InviteCodeDetail) => {
  const url = `${window.location.origin}/login?inviteCode=${inviteCode.code}`

  navigator.clipboard.writeText(url).then(() => {
    message.success('分享链接已复制到剪贴板')
  }).catch(() => {
    // 降级方案：显示链接让用户手动复制
    dialog.info({
      title: '分享邀请码',
      content: () => h('div', {class: 'space-y-2'}, [
        h('p', {class: 'text-sm text-gray-600'}, '请复制以下链接：'),
        h('div', {class: 'p-3 bg-gray-100 rounded-lg'}, [
          h('code', {class: 'text-xs break-all'}, url)
        ])
      ]),
      positiveText: '确定'
    })
  })
}

// 删除邀请码
const handleDelete = (inviteCode: InviteCodeDetail) => {
  dialog.warning({
    title: '删除确认',
    content: `确定要删除邀请码【${inviteCode.code}】吗？删除后不可恢复。`,
    positiveText: '确定删除',
    negativeText: '取消',
    onPositiveClick: () => {
      doDelete(inviteCode)
    }
  })
}

const doDelete = (inviteCode: InviteCodeDetail) => {
  const deleteParams: DeleteInviteCodeParams = {
    inviteCodeId: inviteCode.id,
  }

  loading.value = true
  apiDeleteInviteCode(deleteParams).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '删除成功',
        content: `邀请码【${inviteCode.code}】已删除`,
        duration: 3000
      })
      params.value.pageIndex = 1
      getPage()
    } else {
      notification.error({
        title: '删除失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
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
  getPage()
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

    &.expired-row {
      background-color: #fef2f2;

      &:hover {
        background: linear-gradient(to right, #fee2e2, #fecaca);
      }
    }
  }
}

// 按钮样式增强
:deep(.n-button) {
  &:not(:disabled) {
    &.n-button--primary-type {
      background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
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
}

// 输入框样式
:deep(.n-input) {
  &.n-input--focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
}

// 进度条样式
:deep(.n-progress) {
  .n-progress-graph-line-rail {
    background: #f3f4f6;
  }
}
</style>