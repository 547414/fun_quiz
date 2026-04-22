<template>
  <n-modal
      v-model:show="dialogVisible"
      :mask-closable="true"
      :draggable="true"
      preset="card"
      :bordered="false"
      segmented
      :style="{ width: '900px', padding: '0' }"
      :on-after-leave="resetModal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon icon="fluent:people-team-20-filled" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">选择部门</span>
      </div>
    </template>

    <div class="dept-select-modal-content" style="max-height: 600px;">
      <div class="flex h-full">
        <!-- 左侧筛选和树 -->
        <div class="flex-1 border-r border-gray-100">
          <div class="p-4">
            <!-- 组织筛选 -->
            <div class="mb-4">
              <div class="flex items-center gap-2 mb-2">
                <Icon icon="fluent:organization-20-regular" class="text-gray-600" :width="16" :height="16"/>
                <span class="text-sm text-gray-600 font-medium">选择组织:</span>
              </div>
              <n-select
                  v-model:value="organizationId"
                  :options="organizationOptions"
                  placeholder="请选择组织"
                  size="medium"
                  @update:value="handleOrganizationChange"
                  clearable
              >
                <template #arrow>
                  <Icon icon="fluent:chevron-down-12-regular" class="text-gray-400"/>
                </template>
              </n-select>
            </div>

            <!-- 搜索框 -->
            <div class="mb-4">
              <n-input
                  v-model:value="searchValue"
                  placeholder="搜索部门名称"
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

            <div class="tree-container" style="height: 420px; overflow-y: auto;">
              <n-spin :show="loading">
                <n-tree
                    ref="treeRef"
                    :data="deptTreeData"
                    :pattern="searchValue"
                    :selected-keys="selectedKeys"
                    :expanded-keys="expandedKeys"
                    :on-update:selected-keys="handleSelectedKeys"
                    :on-update:expanded-keys="handleExpandedKeys"
                    :on-load="handleLoadChildren"
                    :render-label="renderLabel"
                    :render-prefix="renderPrefix"
                    :render-switcher-icon="renderSwitcherIcon"
                    block-line
                    selectable
                    expand-on-click
                    class="dept-tree"
                />
              </n-spin>
            </div>
          </div>
        </div>

        <!-- 右侧已选择列表 -->
        <div class="w-80 bg-gray-50">
          <div class="p-4">
            <h4 class="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
              <Icon icon="fluent:checkmark-circle-20-filled" class="text-blue-500"/>
              已选择部门
            </h4>

            <div class="space-y-2 overflow-y-auto" style="max-height: 516px">
              <div
                  v-if="selectedDept"
                  class="flex items-center justify-between p-2 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
              >
                <div class="flex items-center gap-2 flex-1 min-w-0">
                  <Icon
                      :icon="getDeptIcon(selectedDept.category)"
                      :class="getDeptIconColor(selectedDept.category)"
                      class="flex-shrink-0"
                      :width="16"
                      :height="16"
                  />
                  <div class="flex-1 min-w-0">
                    <div class="text-sm text-gray-700 truncate">{{ selectedDept.name }}</div>
                    <div v-if="selectedDept.nameList && selectedDept.nameList.length > 1"
                         class="text-xs text-gray-500 truncate">
                      {{ selectedDept.nameList.slice(0, -1).join(' > ') }}
                    </div>
                  </div>
                </div>
                <n-button
                    size="tiny"
                    text
                    @click="clearSelection"
                    class="text-gray-400 hover:text-red-500"
                >
                  <Icon icon="fluent:dismiss-12-regular" :width="12" :height="12"/>
                </n-button>
              </div>

              <div v-if="!selectedDept" class="text-center py-8">
                <Icon icon="fluent:people-team-20-regular" class="text-gray-300 mb-2" :width="32" :height="32"/>
                <p class="text-sm text-gray-500">暂未选择任何部门</p>
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
        <n-button type="primary" size="large" @click="confirmSelection" :disabled="!selectedDept">
          <template #icon>
            <Icon icon="fluent:checkmark-20-regular"/>
          </template>
          确认选择
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import {computed, h, ref} from 'vue'
import {Icon} from '@iconify/vue'
import {NButton, NInput, NModal, NSelect, NSpin, NTree, type TreeOption, useNotification} from 'naive-ui'
import {apiGetDeptTree, type DeptTreeDetail, type DeptTreeParams} from '@/api/deptApi.ts'
import {UserListInfo} from "@/api/webUserApi.ts"
import {getUserInfo} from "@/utils/userUtil.ts"

// 部门选项类型
interface DeptTreeOption extends TreeOption, Omit<DeptTreeDetail, 'children'> {
  key: string
  label: string
  children?: DeptTreeOption[]
  isLeaf?: boolean
  hasLoaded?: boolean
  hasChildren?: boolean
}

interface SelectedDept {
  id: string
  name: string
  category?: string
  nameList?: string[]
}

const emit = defineEmits(['confirm'])

const notification = useNotification()
const userInfo = ref<UserListInfo>(getUserInfo())

// 状态管理
const dialogVisible = ref(false)
const loading = ref(false)
const deptTreeData = ref<DeptTreeOption[]>([])
const selectedKeys = ref<string[]>([])
const expandedKeys = ref<string[]>([])
const searchValue = ref('')
const organizationId = ref(null)

// 已选择的部门（单选）
const selectedDept = ref<SelectedDept | null>(null)

// 组织选项
const organizationOptions = computed(() => {
  if (!userInfo.value?.organizationList) return []
  return userInfo.value.organizationList.map(org => ({
    label: org.name,
    value: org.id
  }))
})

// 监听选中状态变化（单选）
const handleSelectedKeys = (keys: string[]) => {
  selectedKeys.value = keys
  if (keys.length > 0) {
    const key = keys[0]
    const dept = findDeptByKey(deptTreeData.value, key)
    if (dept) {
      selectedDept.value = {
        id: dept.id || '',
        name: dept.name,
        category: dept.category,
        nameList: dept.nameList
      }
    }
  } else {
    selectedDept.value = null
  }
}

// 根据key查找部门
const findDeptByKey = (nodes: DeptTreeOption[], key: string): DeptTreeOption | null => {
  for (const node of nodes) {
    if (node.key === key) {
      return node
    }
    if (node.children) {
      const found = findDeptByKey(node.children, key)
      if (found) return found
    }
  }
  return null
}

// 处理组织切换
const handleOrganizationChange = (value: string | null) => {
  organizationId.value = value
  searchValue.value = ''
  selectedKeys.value = []
  expandedKeys.value = []
  selectedDept.value = null
  getDeptTree()
}

// 转换部门数据为树形结构（允许根节点可选）
const transformDeptToTree = (deptList: DeptTreeDetail[]): DeptTreeOption[] => {
  if (!deptList?.length) return []
  return deptList.map((dept) => {
    const hasChildrenArray = Array.isArray(dept.children)
    const transformedChildren = hasChildrenArray
        ? (dept.children!.length > 0 ? transformDeptToTree(dept.children!) : [])
        : undefined

    const hasLoaded = hasChildrenArray && dept.children!.length > 0
    const option: DeptTreeOption = {
      ...dept,
      key: dept.id || '',
      label: dept.name,
      children: transformedChildren,
      isLeaf: !dept.hasChild,
      hasLoaded,
      hasChildren: dept.hasChild
      // 移除 checkboxDisabled，允许所有节点可选
    }
    return option
  })
}

// 获取部门树
const getDeptTree = (searchValue: string | null = null) => {
  const params: DeptTreeParams = {
    level: null,
    parentId: null,
    searchValue: searchValue,
    organizationId: organizationId.value
  }
  loading.value = true
  apiGetDeptTree(params).then((res) => {
    if (res.code === 200) {
      deptTreeData.value = transformDeptToTree(res.data)
    } else {
      notification.error({
        title: '获取部门失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取部门失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 处理展开节点
const handleExpandedKeys = (keys: string[]) => {
  expandedKeys.value = keys
}

// 懒加载子节点
const handleLoadChildren = (node: TreeOption) => {
  return new Promise<void>((resolve) => {
    const deptNode = node as DeptTreeOption
    if (!deptNode.hasChildren || deptNode.hasLoaded) {
      resolve()
      return
    }

    const params: DeptTreeParams = {
      level: null,
      parentId: deptNode.id,
      searchValue: null,
      organizationId: organizationId.value
    }

    apiGetDeptTree(params).then((res) => {
      if (res.code === 200 && res.data.length > 0) {
        deptNode.children = transformDeptToTree(res.data)
        deptNode.hasLoaded = true
        deptNode.isLeaf = false
      } else {
        deptNode.isLeaf = true
      }
      resolve()
    }).catch(() => {
      deptNode.isLeaf = true
      resolve()
    })
  })
}

// 搜索处理
const handleSearch = (value: string) => {
  if (value && value.trim()) {
    getDeptTree(value)
  }
}

// 清除搜索
const handleSearchClear = () => {
  searchValue.value = ''
  getDeptTree()
}

// 清除选择
const clearSelection = () => {
  selectedKeys.value = []
  selectedDept.value = null
}

// 获取部门图标
const getDeptIcon = (category?: string | null) => {
  switch (category) {
    case 'COMPANY':
      return 'fluent:building-20-filled'
    case 'DEPARTMENT':
      return 'fluent:people-team-20-filled'
    case 'TEAM':
      return 'fluent:people-20-filled'
    default:
      return 'fluent:building-20-filled'
  }
}

// 获取部门图标颜色
const getDeptIconColor = (category?: string | null) => {
  switch (category) {
    case 'COMPANY':
      return 'text-purple-500'
    case 'DEPARTMENT':
      return 'text-blue-500'
    case 'TEAM':
      return 'text-orange-500'
    default:
      return 'text-blue-500'
  }
}

// 渲染节点标签
const renderLabel = (info: { option: TreeOption }) => {
  return h('span', {class: 'tree-node-label text-gray-700'}, info.option.label as string)
}

// 渲染节点前缀图标
const renderPrefix = (info: { option: TreeOption }) => {
  const node = info.option as DeptTreeOption
  return h(Icon, {
    icon: getDeptIcon(node.category),
    width: 18,
    height: 18,
    class: getDeptIconColor(node.category)
  })
}

// 渲染折叠图标
const renderSwitcherIcon = (info: { option: TreeOption, expanded: boolean }) => {
  const node = info.option as DeptTreeOption

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
  if (selectedDept.value) {
    emit('confirm', [selectedDept.value])
    dialogVisible.value = false
  }
}

// 重置弹窗
const resetModal = () => {
  searchValue.value = ''
  selectedKeys.value = []
  expandedKeys.value = []
  selectedDept.value = null
  organizationId.value = null
}

// 打开弹窗
const open = (preSelected: SelectedDept[] = []) => {
  dialogVisible.value = true
  if (preSelected.length > 0) {
    selectedDept.value = preSelected[0]
    selectedKeys.value = [preSelected[0].id]
  }

  // 设置默认组织
  if (userInfo.value?.organizationList?.length > 0) {
    organizationId.value = userInfo.value.organizationList[0].id
  }

  getDeptTree()
}

defineExpose({
  open
})
</script>

<style scoped lang="scss">
// 部门选择弹窗样式
.dept-select-modal {
  // 居中显示
  :deep(.n-modal) {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

.dept-select-modal-content {
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

:deep(.dept-tree) {
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
      cursor: pointer;

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
        background-color: #eff6ff !important;

        .tree-node-label {
          color: #2563eb;
          font-weight: 500;
        }

        // 选中状态下的悬浮效果
        &:hover {
          background-color: #dbeafe !important;
        }
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
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    border: none;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
    }
  }
}

:deep(.n-select) {
  .n-base-selection {
    border-radius: 8px;

    &:hover {
      border-color: #2563eb;
    }

    &.n-base-selection--focus {
      border-color: #2563eb;
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
    }
  }

  .n-base-selection-label {
    color: #374151;
    font-weight: 500;
  }

  .n-base-selection-placeholder {
    color: #9ca3af;
  }
}
</style>