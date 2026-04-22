<template>
  <n-modal
      v-model:show="dialogVisible"
      :mask-closable="true"
      :draggable="true"
      preset="card"
      :bordered="false"
      segmented
      :style="{ width: '800px', padding: '0' }"
      :on-after-leave="resetModal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon icon="fluent:organization-20-filled" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">选择组织</span>
      </div>
    </template>

    <div class="organization-select-modal-content" style="max-height: 600px;">
      <div class="flex h-full">
        <!-- 左侧组织树 -->
        <div class="flex-1 border-r border-gray-100">
          <div class="p-4">
            <div class="mb-4">
              <n-input
                  v-model:value="searchValue"
                  placeholder="搜索组织名称"
                  clearable
                  size="medium"
                  @update:value="handleSearch"
                  @clear="handleSearchClear"
              >
                <template #suffix>
                  <Icon icon="fluent:search-20-regular" class="text-gray-400"/>
                </template>
              </n-input>
            </div>

            <div class="tree-container" style="height: 480px; overflow-y: auto;">
              <n-spin :show="loading">
                <n-tree
                    ref="treeRef"
                    :data="organizationTreeData"
                    :pattern="searchValue"
                    :checked-keys="checkedKeys"
                    :expanded-keys="expandedKeys"
                    :on-update:checked-keys="handleCheckedKeys"
                    :on-update:expanded-keys="handleExpandedKeys"
                    :on-load="handleLoadChildren"
                    :render-label="renderLabel"
                    :render-prefix="renderPrefix"
                    :render-switcher-icon="renderSwitcherIcon"
                    allow-checking-not-loaded
                    block-line
                    checkable
                    cascade
                    expand-on-click
                    class="organization-tree"
                />
              </n-spin>
            </div>
          </div>
        </div>

        <!-- 右侧已选择列表 -->
        <div class="w-80 bg-gray-50">
          <div class="p-4">
            <h4 class="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
              <Icon icon="fluent:checkmark-circle-20-filled" class="text-green-500"/>
              已选择组织 ({{ selectedOrganizations.length }})
            </h4>

            <div class="space-y-2 overflow-y-auto" style="max-height: 516px">
              <div
                  v-for="org in selectedOrganizations"
                  :key="org.id"
                  class="flex items-center justify-between p-2 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
              >
                <div class="flex items-center gap-2 flex-1 min-w-0">
                  <Icon icon="fluent:building-20-regular" class="text-blue-500 flex-shrink-0" :width="16" :height="16"/>
                  <span class="text-sm text-gray-700 truncate">{{ org.name }}</span>
                </div>
                <n-button
                    size="tiny"
                    text
                    @click="removeOrganization(org.id)"
                    class="text-gray-400 hover:text-red-500"
                >
                  <Icon icon="fluent:dismiss-12-regular" :width="12" :height="12"/>
                </n-button>
              </div>

              <div v-if="selectedOrganizations.length === 0" class="text-center py-8">
                <Icon icon="fluent:organization-20-regular" class="text-gray-300 mb-2" :width="32" :height="32"/>
                <p class="text-sm text-gray-500">暂未选择任何组织</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex gap-3 justify-end">
        <n-button size="large" @click="dialogVisible = false">
          取消
        </n-button>
        <n-button type="primary" size="large" @click="confirmSelection">
          <template #icon>
            <Icon icon="fluent:checkmark-20-regular"/>
          </template>
          确认选择 ({{ selectedOrganizations.length }})
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import {ref, computed, h} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NModal,
  NTree,
  NInput,
  NButton,
  NSpin,
  useNotification,
  type TreeOption
} from 'naive-ui'
import {
  apiGetOrganizationTree,
  type OrganizationTreeDetail,
  type OrganizationTreeParams
} from '@/api/organizationApi.ts'

// 组织选项类型
interface OrganizationTreeOption extends TreeOption, Omit<OrganizationTreeDetail, 'children'> {
  key: string
  label: string
  children?: OrganizationTreeOption[]
  isLeaf?: boolean
  hasLoaded?: boolean
}

interface SelectedOrganization {
  id: string
  name: string
  nameList?: string[]
}

const emit = defineEmits(['confirm'])

const notification = useNotification()

// 状态管理
const dialogVisible = ref(false)
const loading = ref(false)
const organizationTreeData = ref<OrganizationTreeOption[]>([])
const checkedKeys = ref<string[]>([])
const expandedKeys = ref<string[]>([])
const searchValue = ref('')

// 已选择的组织
const selectedOrganizations = ref<SelectedOrganization[]>([])

// 计算已选择的组织
const computedSelectedOrganizations = computed(() => {
  const result: SelectedOrganization[] = []

  const findOrganizations = (nodes: OrganizationTreeOption[], keys: string[]) => {
    for (const node of nodes) {
      if (keys.includes(node.key)) {
        result.push({
          id: node.id || '',
          name: node.name,
          nameList: node.nameList
        })
      }
      if (node.children) {
        findOrganizations(node.children, keys)
      }
    }
  }

  findOrganizations(organizationTreeData.value, checkedKeys.value)
  return result
})

// 监听选中状态变化
const handleCheckedKeys = (keys: string[]) => {
  checkedKeys.value = keys
  selectedOrganizations.value = computedSelectedOrganizations.value
}

// 转换组织数据为树形结构
const transformOrganizationToTree = (organizations: OrganizationTreeDetail[]): OrganizationTreeOption[] => {
  if (!organizations || organizations.length === 0) {
    return []
  }
  return organizations.map(org => {
    const hasChildren = org.children && org.children.length > 0
    return {
      ...org,
      key: org.id || '',
      label: org.name,
      children: hasChildren ? transformOrganizationToTree(org.children) : undefined,
      isLeaf: !org.hasChild,
      hasLoaded: hasChildren
    } as OrganizationTreeOption
  })
}

// 获取组织树
const getOrganizationTree = (searchValue: string | null = null) => {
  const params: OrganizationTreeParams = {
    level: null,
    parentId: null,
    searchValue: searchValue
  }
  loading.value = true
  apiGetOrganizationTree(params).then((res) => {
    if (res.code === 200) {
      organizationTreeData.value = transformOrganizationToTree(res.data)
    } else {
      notification.error({
        title: '获取组织失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取组织失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 懒加载子节点
const handleLoadChildren = (node: TreeOption) => {
  return new Promise<void>((resolve) => {
    const orgNode = node as OrganizationTreeOption

    if (orgNode.hasLoaded) {
      resolve()
      return
    }

    const params: OrganizationTreeParams = {
      level: null,
      parentId: orgNode.id
    }

    apiGetOrganizationTree(params).then((res) => {
      if (res.code === 200) {
        if (res.data && res.data.length > 0) {
          orgNode.children = transformOrganizationToTree(res.data)
          orgNode.isLeaf = false
        } else {
          orgNode.isLeaf = true
          orgNode.children = undefined
        }
        orgNode.hasLoaded = true
        resolve()
      } else {
        notification.error({
          title: '加载失败',
          content: res.message,
          duration: 3000
        })
        resolve()
      }
    }).catch((err) => {
      notification.error({
        title: '加载失败',
        content: err,
        duration: 3000
      })
      resolve()
    })
  })
}

// 搜索处理
const handleSearch = (value: string) => {
  if (value.trim()) {
    expandedKeys.value = []
    getOrganizationTree(searchValue.value)
  }
}

// 清空搜索处理
const handleSearchClear = () => {
  searchValue.value = ''
  expandedKeys.value = []
  getOrganizationTree(null)
}

// 展开节点处理
const handleExpandedKeys = (keys: string[]) => {
  expandedKeys.value = keys
}

// 移除组织
const removeOrganization = (orgId: string) => {
  checkedKeys.value = checkedKeys.value.filter(key => key !== orgId)
  selectedOrganizations.value = selectedOrganizations.value.filter(org => org.id !== orgId)
}

// 渲染节点标签
const renderLabel = (info: { option: TreeOption }) => {
  return h('span', {class: 'tree-node-label text-gray-700'}, info.option.label as string)
}

// 渲染节点前缀图标
const renderPrefix = (info: { option: TreeOption }) => {
  const node = info.option as OrganizationTreeOption
  let icon = 'fluent:building-20-regular'
  let colorClass = 'text-blue-500'

  if (node.category === 'COMPANY') {
    icon = 'fluent:building-bank-20-regular'
    colorClass = 'text-purple-500'
  }

  return h(Icon, {
    icon: icon,
    width: 18,
    height: 18,
    class: colorClass
  })
}

// 渲染折叠图标
const renderSwitcherIcon = (info: { option: TreeOption, expanded: boolean }) => {
  const node = info.option as OrganizationTreeOption

  if (node.isLeaf && node.hasLoaded) {
    return null
  }

  return h(Icon, {
    icon: info.expanded ? 'fluent:chevron-down-12-filled' : 'fluent:chevron-right-12-filled',
    width: 12,
    height: 12,
    class: 'text-gray-500'
  })
}

// 确认选择
const confirmSelection = () => {
  emit('confirm', selectedOrganizations.value)
  dialogVisible.value = false
}

// 重置弹窗
const resetModal = () => {
  searchValue.value = ''
  checkedKeys.value = []
  expandedKeys.value = []
  selectedOrganizations.value = []
}

// 打开弹窗
const open = (preSelected: SelectedOrganization[] = []) => {
  dialogVisible.value = true
  selectedOrganizations.value = [...preSelected]
  checkedKeys.value = preSelected.map(org => org.id)
  getOrganizationTree()
}

defineExpose({
  open
})
</script>

<style scoped lang="scss">
// 组织选择弹窗样式
.organization-select-modal {
  // 居中显示
  :deep(.n-modal) {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

.organization-select-modal-content {
  padding: 0;

  .tree-container {
    &::-webkit-scrollbar {
      width: 6px;
    }

    &::-webkit-scrollbar-track {
      background: #f5f5f5;
      border-radius: 3px;
    }

    &::-webkit-scrollbar-thumb {
      background: #d1d5db;
      border-radius: 3px;

      &:hover {
        background: #9ca3af;
      }
    }
  }
}

:deep(.organization-tree) {
  .n-tree-node {
    padding: 0;
    margin: 2px 0;
    align-items: center;

    // 移除所有默认背景色
    .n-tree-node-wrapper {
      background-color: transparent !important;
      padding: 0 !important;
      margin: 0 !important;

      &:hover {
        background-color: transparent !important;
      }

      &.n-tree-node-wrapper--selected {
        background-color: transparent !important;
      }
    }

    // 统一的节点内容样式
    .n-tree-node-content {
      width: 100%;
      padding: 6px 8px;
      border-radius: 6px;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      min-height: 32px;
      margin: 0;
      background-color: transparent;

      // 悬浮效果只在这里控制
      &:hover {
        background-color: #e5e8ec !important;
      }

      &__prefix {
        display: flex;
        align-items: center;
        margin-right: 8px;
      }

      &__text {
        flex: 1;
        display: flex;
        align-items: center;
      }
    }

    // 选中状态样式
    &.n-tree-node--selected {
      .n-tree-node-content {
        background-color: #ede9fe !important;

        .tree-node-label {
          color: #6366f1;
          font-weight: 500;
        }

        // 选中状态下的悬浮效果
        &:hover {
          background-color: #ddd6fe !important;
        }
      }
    }

    // 复选框样式
    .n-tree-node-checkbox {
      margin-right: 8px;
      display: flex;
      align-items: center;

      // 确保复选框垂直居中
      .n-checkbox {
        background-color: transparent !important;
        display: flex;
        align-items: center;
        height: 32px; // 与节点高度一致
      }
    }

    // 移除任何其他可能的背景色
    &:hover {
      background-color: transparent !important;
    }

    &.n-tree-node--pending {
      background-color: transparent !important;
    }

    &.n-tree-node--disabled {
      background-color: transparent !important;
    }
  }

  .n-tree-node-indent {
    width: 1.2rem;
  }

  .n-tree-node-switcher {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    background-color: transparent !important;

    &:hover {
      background-color: transparent !important;
    }
  }

  // 移除树根级别的任何背景
  &.n-tree {
    background-color: transparent !important;
  }
}

:deep(.n-card) {
  .n-card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .n-modal-card__content {
    padding: 0 !important;
    border-bottom: 1px solid #e5e7eb;
  }

  .n-card__footer {
    padding: 1rem 1.5rem;
    background: linear-gradient(to bottom, #fafafa, #f5f5f5);
  }
}

:deep(.n-button) {
  font-weight: 500;
  transition: all 0.3s ease;

  &:not(:disabled) {
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    &:active {
      transform: translateY(0);
    }
  }

  &.n-button--primary-type {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border: none;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #5558e3 0%, #7c4ce3 100%);
    }
  }
}

/* ✅ 让树上的复选框呈方形（0px 圆角） */
:deep(.organization-tree .n-tree-node-checkbox .n-checkbox .n-checkbox-box) {
  border-radius: 0 !important;
}

/* ✅ 已选中 / 半选中状态下也保持方形 */
:deep(.organization-tree .n-tree-node-checkbox .n-checkbox.n-checkbox--checked .n-checkbox-box),
:deep(.organization-tree .n-tree-node-checkbox .n-checkbox.n-checkbox--indeterminate .n-checkbox-box) {
  border-radius: 0 !important;
}
</style>