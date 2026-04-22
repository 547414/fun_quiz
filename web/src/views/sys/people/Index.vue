<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div
                class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-blue-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:people-20-filled" :width="24" :height="24"/>
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:person-add-16-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              人员管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">管理系统用户账户和权限</p>
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
                placeholder="搜索名称/手机号/邮箱"
                clearable
                @clear="getWebUserPage"
                @keyup.enter="onSearch"
                size="large"
                :style="{ width: '320px'}"
            />
          </div>

          <n-button
              type="primary"
              size="large"
              @click="openAddModal"
              class="shadow-md hover:shadow-lg transition-all duration-200"
          >
            <template #icon>
              <Icon icon="fluent:person-add-20-filled"/>
            </template>
            添加人员
          </n-button>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 px-6 pb-6 pt-4 overflow-hidden">
      <div class="h-full bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <!-- 表格区域 -->
        <div class="p-6 pb-0">
          <n-data-table
              :columns="columns"
              :data="webUserList"
              :loading="loading"
              :pagination="false"
              :bordered="false"
              striped
              :max-height="tableHeight"
              :scroll-x="1000"
          />
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && webUserList.length === 0" class="flex flex-col items-center justify-center py-16">
          <div class="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Icon icon="fluent:people-20-regular" class="text-gray-400" :width="48" :height="48"/>
          </div>
          <p class="text-gray-500 text-lg">暂无人员数据</p>
          <p class="text-gray-400 text-sm mt-2">点击上方"添加人员"按钮创建第一个用户</p>
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
              :item-count="total"
              :page-sizes="[10, 20, 50, 100]"
              show-size-picker
              @update:page="pageChange"
              @update:page-size="handleSizeChange"
          />
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <EditWebUserModal ref="EditWebUserModalRef" @operateSuccess="refreshPage"/>
  </div>
</template>

<script setup lang="tsx">
import {ref, onMounted, h, onUnmounted} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NDataTable,
  NButton,
  NInput,
  NPagination,
  NSwitch,
  NTag,
  NImage,
  NSpace,
  NTooltip,
  useNotification,
  useDialog,
  type DataTableColumns
} from 'naive-ui'
import EditWebUserModal from "@/components/sys/people/EditModal.vue"
import commonResource from "@/resource/commonResource.ts"
import {
  apiGetWebUserPage,
  type WebUserPageParams,
  type WebUserPageResponse,
  type WebUserDetail,
  type ChangeWebUserEnabledParams,
  apiChangeWebUserEnabled,
  type ResetPasswordParams,
  apiResetPassword, UserListInfo
} from "@/api/webUserApi.ts"
import {cloneDeep} from "lodash"
import {getUserInfo} from "@/utils/userUtil.ts"
import {apiDeleteUnionUser, DeleteUnionUserParams} from "@/api/unionUserApi.ts";

const notification = useNotification()
const dialog = useDialog()
const EditWebUserModalRef = ref()
const loading = ref(false)
const tableHeight = ref(400)

const userInfo = ref<UserListInfo>(cloneDeep(getUserInfo()))
const webUserList = ref<WebUserDetail[]>([])

// 角色选项
const roleOptionList = ref([
  {text: '超级管理员', value: 'SUPER_ADMIN'},
  {text: '工会管理员', value: 'TRADE_UNION_ADMIN'},
  {text: '总管理员', value: 'TOTAL_ADMIN'},
  {text: '普通用户', value: 'WEB_USER'},
])

if (userInfo.value.currentRoleCode === 'SUPER_ADMIN') {
  roleOptionList.value = [
    {text: '超级管理员', value: 'SUPER_ADMIN'},
    {text: '工会管理员', value: 'TRADE_UNION_ADMIN'},
    {text: '总管理员', value: 'TOTAL_ADMIN'},
    {text: '普通用户', value: 'WEB_USER'},
  ]
} else if (userInfo.value.currentRoleCode === 'TOTAL_ADMIN') {
  roleOptionList.value = [
    {text: '工会管理员', value: 'TRADE_UNION_ADMIN'},
    {text: '总管理员', value: 'TOTAL_ADMIN'},
    {text: '普通用户', value: 'WEB_USER'},
  ]
} else if (userInfo.value.currentRoleCode === 'TRADE_UNION_ADMIN') {
  roleOptionList.value = [
    {text: '工会管理员', value: 'TRADE_UNION_ADMIN'},
    {text: '普通用户', value: 'WEB_USER'},
  ]
}

// 计算表格高度
const calculateTableHeight = () => {
  const windowHeight = window.innerHeight
  tableHeight.value = windowHeight - 300
}

onMounted(() => {
  calculateTableHeight()
  window.addEventListener('resize', calculateTableHeight)
  getWebUserPage()
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateTableHeight)
})

// 表格列定义
// 在现有的 columns 数组中添加组织和部门列
// 找到现有的 columns 定义，在合适位置添加以下两列

// 在现有的 columns 数组中添加组织和部门列
// 找到现有的 columns 定义，在合适位置添加以下两列

const columns: DataTableColumns<WebUserDetail> = [
  {
    title: '名称',
    key: 'name',
    width: 200,
    fixed: 'left',
    sorter: true,
    render(row) {
      return h('div', {class: 'flex items-center gap-3'}, [
        h(NImage, {
          src: row?.avatarFileInfo?.url || commonResource.DefaultAvatar,
          width: 40,
          height: 40,
          lazy: true,
          class: 'rounded-full border border-gray-200'
        }),
        h('div', [
          h('div', {class: 'font-medium text-gray-800'}, row.name),
          h('div', {class: 'text-xs text-gray-500 mt-0.5'}, row.mobile || '暂无手机号')
        ])
      ])
    }
  },
  {
    title: '邮箱',
    key: 'email',
    width: 200,
    ellipsis: {
      tooltip: true
    },
    render(row) {
      return h('span', {class: 'text-gray-600'}, row.email || '-')
    }
  },
  // 新增：组织列
  {
    title: '组织',
    key: 'organizationList',
    width: 200,
    render(row) {
      if (!row.organizationList || row.organizationList.length === 0) {
        return h('span', {class: 'text-gray-400'}, '-')
      }

      // 如果有多个组织，显示第一个并提示总数
      const firstOrg = row.organizationList[0]
      const displayName = firstOrg.name
      const tooltipContent = row.organizationList.map(org =>
          org.nameList?.join(' / ') || org.name
      ).join('\n')

      if (row.organizationList.length === 1) {
        return h(NTooltip, {
          style: {'--n-color': '#374151'}
        }, {
          trigger: () => h('span', {class: 'text-gray-600 cursor-pointer'}, displayName),
          default: () => h('div', {
            class: 'text-white whitespace-pre-line',
            style: {color: 'white'}
          }, tooltipContent)
        })
      } else {
        return h('div', {class: 'flex items-center'}, [
          h(NTooltip, {
            style: {'--n-color': '#374151'}
          }, {
            trigger: () => h('span', {class: 'text-gray-600 cursor-pointer'}, displayName),
            default: () => h('div', {
              class: 'text-white whitespace-pre-line',
              style: {color: 'white'}
            }, tooltipContent)
          }),
          h('span', {class: 'text-xs text-blue-500 ml-2'}, `+${row.organizationList.length - 1}`)
        ])
      }
    }
  },
  // 新增：部门列
  {
    title: '部门',
    key: 'deptList',
    width: 200,
    render(row) {
      if (!row.deptList || row.deptList.length === 0) {
        return h('span', {class: 'text-gray-400'}, '-')
      }

      // 如果有多个部门，显示第一个并提示总数
      const firstDept = row.deptList[0]
      const displayName = firstDept.name
      const tooltipContent = row.deptList.map(dept =>
          dept.nameList?.join(' / ') || dept.name
      ).join('\n')

      if (row.deptList.length === 1) {
        return h(NTooltip, {
          style: {'--n-color': '#374151'}
        }, {
          trigger: () => h('span', {class: 'text-gray-600 cursor-pointer'}, displayName),
          default: () => h('div', {
            class: 'text-white whitespace-pre-line',
            style: {color: 'white'}
          }, tooltipContent)
        })
      } else {
        return h('div', {class: 'flex items-center'}, [
          h(NTooltip, {
            style: {'--n-color': '#374151'}
          }, {
            trigger: () => h('span', {class: 'text-gray-600 cursor-pointer'}, displayName),
            default: () => h('div', {
              class: 'text-white whitespace-pre-line',
              style: {color: 'white'}
            }, tooltipContent)
          }),
          h('span', {class: 'text-xs text-blue-500 ml-2'}, `+${row.deptList.length - 1}`)
        ])
      }
    }
  },
  {
    title: '启用状态',
    key: 'enabled',
    width: 120,
    align: 'center',
    render(row) {
      return h('div', {class: 'flex items-center justify-center'}, [
        h(NSwitch, {
          value: row.enabled,
          disabled: userInfo.value.unionUserUserId === row.id,
          size: 'medium',
          onUpdateValue: (value: boolean) => {
            row.enabled = value
            changeEnabled(row)
          }
        }, {
          checked: () => '启用',
          unchecked: () => '禁用'
        })
      ])
    }
  },
  {
    title: '角色',
    key: 'roleList',
    width: 200,
    filterOptions: roleOptionList.value.map(item => ({
      label: item.text,
      value: item.value
    })),
    filter: true,
    render(row) {
      return h(NSpace, {size: 8}, {
        default: () => row.roleList?.map(role =>
            h(NTag, {
              type: 'info',
              bordered: false,
              round: true
            }, {default: () => role.roleName})
        )
      })
    }
  },
  {
    title: '微信用户',
    key: 'unionUserName',
    width: 150,
    render(row) {
      return h('span', {class: 'text-gray-600'}, row.unionUserName || '-')
    }
  },
  {
    title: '操作',
    key: 'operate',
    width: 240,
    fixed: 'right',
    align: 'center',
    render(row) {
      return h(NSpace, {size: 'small', justify: 'center'}, () => [
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'primary',
            ghost: false,
            circle: true,
            onClick: () => openEditModal(row)
          }, {
            icon: () => h(Icon, {icon: 'fluent:edit-20-regular'})
          }),
          default: () => '编辑'
        }),
        h(NTooltip, {}, {
          trigger: () => h(NButton, {
            size: 'small',
            type: 'warning',
            secondary: true,
            circle: true,
            disabled: userInfo.value.unionUserUserId === row.id,
            onClick: () => resetPassword(row)
          }, {
            icon: () => h(Icon, {icon: 'fluent:key-reset-20-regular'})
          }),
          default: () => '重置密码'
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

// 参数和分页
const params = ref<WebUserPageParams>({
  pageSize: 20,
  pageIndex: 1,
  search: null,
  nameSort: null,
  roleCodeList: ['SUPER_ADMIN', 'ADMIN', 'WEB_USER'],
  searchFields: []
})
const total = ref(0)

// 获取人员列表
const getWebUserPage = () => {
  loading.value = true
  apiGetWebUserPage(params.value).then((res: WebUserPageResponse) => {
    if (res.code === 200) {
      total.value = res.data.filterCount
      webUserList.value = res.data.data
    } else {
      notification.error({
        title: '获取人员列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '获取人员列表失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 页面变化
const pageChange = (currentPage: number) => {
  params.value.pageIndex = currentPage
  getWebUserPage()
}

// 页面大小变化
const handleSizeChange = (pageSize: number) => {
  params.value.pageSize = pageSize
  params.value.pageIndex = 1
  getWebUserPage()
}

// 改变启用状态
const changeEnabled = (user: WebUserDetail) => {
  dialog.warning({
    title: '确认操作',
    content: `是否确认${user.enabled ? '启用' : '禁用'}【${user.name}】?`,
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      const params: ChangeWebUserEnabledParams = {
        id: user.id,
        enabled: user.enabled
      }
      doChangeEnabled(params, user)
    },
    onNegativeClick: () => {
      user.enabled = !user.enabled
    }
  })
}

const doChangeEnabled = (params: ChangeWebUserEnabledParams, user: WebUserDetail) => {
  loading.value = true
  apiChangeWebUserEnabled(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '修改人员启用状态成功',
        duration: 3000
      })
      getWebUserPage()
    } else {
      notification.error({
        title: '修改人员启用状态失败',
        content: res.message,
        duration: 3000
      })
      user.enabled = !user.enabled
    }
  }).catch((err: string) => {
    notification.error({
      title: '修改人员启用状态失败',
      content: err,
      duration: 3000
    })
    user.enabled = !user.enabled
  }).finally(() => {
    loading.value = false
  })
}

// 重置密码
const resetPassword = (user: WebUserDetail) => {
  dialog.warning({
    title: '确认重置密码',
    content: `是否确认重置【${user.name}】的密码?`,
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      doResetPassword(user)
    }
  })
}

const doResetPassword = (user: WebUserDetail) => {
  const params: ResetPasswordParams = {
    userId: user.id
  }
  apiResetPassword(params).then((res) => {
    if (res.code === 200) {
      dialog.success({
        title: '重置成功',
        content: () => h('div', [
          h('div', '【' + user.name + '】的密码已重置为'),
          h('div', {class: 'text-blue-600 font-mono mt-2 text-lg'}, res.data)
        ]),
        positiveText: '复制密码',
        negativeText: '我知道了',
        onPositiveClick: () => {
          copyPassword(res.data)
        }
      })
    } else {
      notification.error({
        title: '重置密码失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '重置密码失败',
      content: err,
      duration: 3000
    })
  })
}

// 复制密码
const copyPassword = (text: string) => {
  navigator.clipboard.writeText(text).then(() => {
    notification.success({
      title: '复制密码成功',
      duration: 2000
    })
  }).catch((err) => {
    notification.error({
      title: '复制密码失败',
      content: err,
      duration: 3000
    })
  })
}

const handleDelete = (user: WebUserDetail) => {
  dialog.warning({
    title: '确认删除',
    content: `是否确认删除${user.name}？`,
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      deleteUnionUser(user)
    }
  })
}

const deleteUnionUser = (user: WebUserDetail) => {
  const deleteParams: DeleteUnionUserParams = {
    unionUserId: user.unionUserUuid
  }
  loading.value = true
  apiDeleteUnionUser(deleteParams).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '删除成功',
        duration: 3000
      })
      params.value.pageIndex = 1
      getWebUserPage()
    } else {
      notification.error({
        title: '删除失败',
        content: res.message,
        duration: 3000
      })
      loading.value = false
    }
  }).catch((err: string) => {
    notification.error({
      title: '删除失败',
      content: err,
      duration: 3000
    })
    loading.value = false
  }).finally(() => {

  })
}

// 打开编辑弹窗
const openEditModal = (user: WebUserDetail) => {
  EditWebUserModalRef.value.openModal('EDIT', user.id)
}

// 打开添加弹窗
const openAddModal = () => {
  EditWebUserModalRef.value.openModal('ADD')
}

// 刷新页面
const refreshPage = () => {
  getWebUserPage()
}

// 搜索
const onSearch = () => {
  params.value.pageIndex = 1
  getWebUserPage()
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
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
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

// 分页样式
:deep(.n-pagination) {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>