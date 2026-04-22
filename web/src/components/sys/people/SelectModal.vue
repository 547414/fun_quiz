<template>
  <n-modal
      v-model:show="visible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :style="{ width: '70vw' }"
      :bordered="false"
      segmented
      class="user-select-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon icon="fluent:people-team-20-filled" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">选择人员</span>
      </div>
    </template>

    <div class="flex flex-col h-[700px]">
      <!-- 搜索栏 -->
      <div class="px-6 py-4 border-b border-gray-100">
        <n-input-group>
          <n-input
              v-model:value="params.search"
              placeholder="请输入用户名称或邮箱"
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

      <!-- 已选用户显示 -->
      <div class="px-6 bg-gray-50 border-b border-gray-100 selected-users-container">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-700">已选择 {{ selectedUsers.length }} 人</span>
          <n-button size="small" quaternary @click="handleClearSelected">
            清空选择
          </n-button>
        </div>
        <div class="selected-users-scroll">
          <div class="flex gap-2">
            <n-tag
                v-for="user in selectedUsers"
                :key="user.unionUserUuid"
                type="primary"
                closable
                @close="handleRemoveSelected(user)"
                size="small"
            >
              {{ user.name }}
            </n-tag>
          </div>
        </div>
      </div>

      <!-- 表格区域 -->
      <div class="flex-1 px-6 overflow-hidden mt-2">
        <n-data-table
            :columns="columns"
            :data="userList"
            :loading="loading"
            :pagination="false"
            :bordered="false"
            striped
            :max-height="430"
            :single-line="false"
            :row-props="rowProps"
            :row-class-name="getRowClassName"
            class="user-select-table"
        />
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && userList.length === 0" class="flex flex-col items-center justify-center py-12">
        <Icon icon="fluent:folder-open-20-regular" class="text-gray-400 mb-3" :width="48" :height="48"/>
        <p class="text-gray-500">暂无用户数据</p>
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

    <template #footer>
      <div class="flex justify-between items-center">
        <span class="text-sm text-gray-500">已选择 {{ selectedUsers.length }} 人</span>
        <div class="flex gap-3">
          <n-button size="large" @click="handleCancel">
            取消
          </n-button>
          <n-button
              type="primary"
              size="large"
              @click="handleConfirm"
              :disabled="selectedUsers.length === 0"
          >
            确定选择
          </n-button>
        </div>
      </div>
    </template>
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
  NCheckbox,
  useNotification,
  type DataTableColumns
} from 'naive-ui'
import {
  apiGetWebUserByIdList,
  apiGetWebUserPage,
  type WebUserDetail, WebUserListParams,
  type WebUserPageParams
} from '@/api/webUserApi.ts'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts"

const notification = useNotification()
const emit = defineEmits(['selected'])

// 状态
const selectType = ref()
const visible = ref(false)
const loading = ref(false)
const userList = ref<WebUserDetail[]>([])
const total = ref(0)
const selectedUsers = ref<WebUserDetail[]>([])

// 分页参数
const params = ref<WebUserPageParams>({
  pageSize: 20,
  pageIndex: 1,
  search: null,
  nameSort: null,
  roleCodeList: ['SUPER_ADMIN', 'ADMIN', 'WEB_USER'],
  searchFields: []
})

// 计算属性
const pageCount = computed(() => Math.ceil(total.value / params.value.pageSize))

// 表格列定义
const columns: DataTableColumns<WebUserDetail> = [
  {
    title: '选择',
    key: 'select',
    width: 30,
    align: 'center',
    render(row) {
      const isSelected = selectedUsers.value.some(u => u.unionUserUuid === row.unionUserUuid)
      return h(NCheckbox, {
        checked: isSelected,
        onUpdateChecked: (checked: boolean) => {
          if (checked) {
            handleSelectUser(row)
          } else {
            handleUnselectUser(row)
          }
        }
      })
    }
  },
  {
    title: '用户信息',
    key: 'name',
    width: 165,
    render(row) {
      return h('div', {class: 'flex items-center gap-3'}, [
        h('div', {
          class: `w-10 h-10 rounded-lg ${
              row.enabled
                  ? 'bg-gradient-to-br from-indigo-500 to-purple-600'
                  : 'bg-gray-400'
          } flex items-center justify-center text-white text-sm font-bold`
        }, row.name.substring(0, 2)),
        h('div', [
          h('div', {class: 'font-medium text-gray-800'}, row.name),
          h('div', {class: 'text-xs text-gray-500'}, row.unionUserUuid),
          h('div', {class: 'text-xs text-gray-400'}, row.email || row.mobile || '-')
        ])
      ])
    }
  },
  {
    title: '角色',
    key: 'roles',
    width: 50,
    render(row) {
      if (!row.roleList || row.roleList.length === 0) {
        return h('span', {class: 'text-gray-400'}, '-')
      }

      return h('div', {class: 'flex flex-wrap gap-1'},
          row.roleList.slice(0, 2).map(role =>
              h(NTag, {
                type: 'info',
                size: 'small',
                round: true
              }, {
                default: () => role.roleName
              })
          ).concat(
              row.roleList.length > 2 ? [
                h('span', {class: 'text-xs text-gray-400'}, `+${row.roleList.length - 2}`)
              ] : []
          )
      )
    }
  },
  {
    title: '部门',
    key: 'dept',
    width: 250,
    ellipsis: {
      tooltip: true
    },
    render(row) {
      if (row.deptList && row.deptList.length > 0) {
        let nameStr = ''
        for (const [idx, dept] of row.deptList.entries()) {
          if (idx > 0) {
            nameStr += '\n'
          }
          nameStr += dept.nameList.join('/')
        }
        return h('span', {class: 'text-sm'}, nameStr)
      }
      return h('span', {class: 'text-gray-400'}, '-')
    }
  },
  {
    title: '状态',
    key: 'enabled',
    width: 40,
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
const getRowClassName = (row: WebUserDetail) => {
  const isSelected = selectedUsers.value.some(u => u.unionUserUuid === row.unionUserUuid)
  if (isSelected) return 'selected-row'
  return ''
}

// 行属性配置
const rowProps = (row: WebUserDetail) => {
  return {
    style: 'cursor: pointer;',
    onClick: (e: MouseEvent) => {
      // 阻止点击复选框时的冒泡
      const target = e.target as HTMLElement
      if (target.closest('.n-checkbox')) {
        return
      }

      const isSelected = selectedUsers.value.some(u => u.unionUserUuid === row.unionUserUuid)
      if (isSelected) {
        handleUnselectUser(row)
      } else {
        handleSelectUser(row)
      }
    }
  }
}

// 打开弹窗
const open = (selectTypeInit: string, selectedIdList: string[]) => {
  selectType.value = selectTypeInit
  visible.value = true
  selectedUsers.value = []
  getWebUserByIdList(selectedIdList)
  getUserPage()
}

const getWebUserByIdList = (userIdList: string[]) => {
  if (!userIdList) {
    return
  }
  if (userIdList.length <= 0) {
    return
  }
  const params: WebUserListParams = {
    userIdList: userIdList
  }
  apiGetWebUserByIdList(params).then((res) => {
    if (res.code === 200) {
      selectedUsers.value = res.data
    } else {
      notification.error({
        title: '获取用户列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取用户列表失败',
      content: err,
      duration: 3000
    })
  })
}

// 关闭弹窗
const close = () => {
  visible.value = false
}

// 获取用户列表
const getUserPage = () => {
  loading.value = true
  apiGetWebUserPage(params.value).then((res) => {
    if (res.code === 200) {
      total.value = res.data.filterCount
      userList.value = res.data.data
    } else {
      notification.error({
        title: '获取用户列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取用户列表失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 搜索处理
const handleSearch = () => {
  params.value.searchFields = params.value.search ? ['name', 'email', 'mobile'] : []
  params.value.pageIndex = 1
  getUserPage()
}

const handleClearSearch = () => {
  params.value.search = null
  params.value.searchFields = []
  params.value.pageIndex = 1
  getUserPage()
}

// 分页处理
const handlePageChange = (page: number) => {
  params.value.pageIndex = page
  getUserPage()
}

const handlePageSizeChange = (pageSize: number) => {
  params.value.pageSize = pageSize
  params.value.pageIndex = 1
  getUserPage()
}

// 选择用户
const handleSelectUser = (user: WebUserDetail) => {
  if (!user.unionUserUuid) return

  const userInfo = user
  const exists = selectedUsers.value.some(u => u.unionUserUuid === user.unionUserUuid)
  if (!exists) {
    selectedUsers.value.push(userInfo)
  }
}

// 取消选择用户
const handleUnselectUser = (user: WebUserDetail) => {
  if (!user.unionUserUuid) return

  const index = selectedUsers.value.findIndex(u => u.unionUserUuid === user.unionUserUuid)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  }
}

// 移除已选用户
const handleRemoveSelected = (user: WebUserDetail) => {
  const index = selectedUsers.value.findIndex(u => u.unionUserUuid === user.unionUserUuid)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  }
}

// 清空选择
const handleClearSelected = () => {
  selectedUsers.value = []
}

// 取消
const handleCancel = () => {
  close()
}

// 确认选择
const handleConfirm = () => {
  if (selectedUsers.value.length === 0) {
    notification.warning({
      title: '提示',
      content: '请至少选择一个用户',
      duration: 2000
    })
    return
  }

  emit('selected', {selectType: selectType.value, selectedUsers: selectedUsers.value})
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

  .n-card__footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #f3f4f6;
    background: #fafafa;
  }
}

// 已选择用户区域样式
.selected-users-container {
  height: 75px;
  display: flex;
  flex-direction: column;
}

.selected-users-scroll {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;

  &::-webkit-scrollbar {
    height: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;

    &:hover {
      background: #a8a8a8;
    }
  }

  > div {
    min-width: min-content;
  }
}

// 数据表格样式优化
:deep(.user-select-table) {
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
  white-space: nowrap;
  flex-shrink: 0;

  &.n-tag--success-type {
    background: rgba(16, 185, 129, 0.1);
    color: #059669;
    border-color: rgba(16, 185, 129, 0.2);
  }

  &.n-tag--info-type {
    background: rgba(59, 130, 246, 0.1);
    color: #2563eb;
    border-color: rgba(59, 130, 246, 0.2);
  }

  &.n-tag--primary-type {
    background: rgba(139, 92, 246, 0.1);
    color: #7c3aed;
    border-color: rgba(139, 92, 246, 0.2);
  }
}

// 复选框样式 - 方形
:deep(.n-checkbox) {
  .n-checkbox-box {
    border-radius: 4px; // 方形圆角

    &.n-checkbox-box--checked {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      border-color: #6366f1;
    }
  }
}
</style>