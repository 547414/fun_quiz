<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div
                class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:organization-20-filled" :width="24" :height="24"/>
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:checkmark-12-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              组织管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">管理组织架构及部门层级关系</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 px-6 pb-6 pt-4 overflow-hidden">
      <div class="h-full grid grid-cols-2 gap-4">
        <!-- 左侧树形结构 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
          <div class="p-6 pb-0">
            <!-- 搜索框和操作按钮行 -->
            <div class="flex items-center gap-3 mb-4">
              <div class="flex-1">
                <n-input
                    v-model:value="searchValue"
                    placeholder="搜索组织名称"
                    clearable
                    size="large"
                    @update:value="handleSearch"
                    @clear="handleSearchClear"
                >
                  <template #suffix>
                    <Icon icon="fluent:search-20-regular" class="text-gray-400"/>
                  </template>
                </n-input>
              </div>
              <n-button
                  type="primary"
                  size="large"
                  @click="doSaveSeqAndParent"
              >
                <template #icon>
                  <Icon icon="fluent:save-20-regular"/>
                </template>
                保存结构
              </n-button>
              <n-button
                  type="success"
                  size="large"
                  @click="handleAddRoot"
              >
                <template #icon>
                  <Icon icon="fluent:add-circle-20-filled"/>
                </template>
                添加根组织
              </n-button>
            </div>
          </div>

          <div class="flex-1 px-6 pb-6 overflow-auto">
            <n-spin :show="loading">
              <n-tree
                  :data="organizationTreeData"
                  :pattern="searchValue"
                  :selected-keys="selectedKeys"
                  :expanded-keys="expandedKeys"
                  :on-update:selected-keys="handleSelectKeys"
                  :on-update:expanded-keys="handleExpandedKeys"
                  :on-load="handleLoadChildren"
                  :node-props="nodeProps"
                  :render-label="renderLabel"
                  :render-prefix="renderPrefix"
                  :render-switcher-icon="renderSwitcherIcon"
                  block-line
                  :draggable="isDraggable"
                  expand-on-click
                  @drop="handleDrop"
                  class="organization-tree"
              />
            </n-spin>
          </div>
        </div>

        <!-- 右侧详情 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Icon icon="fluent:info-20-filled" class="text-indigo-500"/>
              组织详情
            </h3>

            <div v-if="selectedNode" class="space-y-4">
              <!-- 基本信息 -->
              <div class="bg-gray-50 rounded-xl p-4 space-y-3">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">组织名称</label>
                    <div class="text-gray-800 font-medium">{{ selectedNode.name }}</div>
                  </div>
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">组织编码</label>
                    <div class="text-gray-800 font-medium">{{ selectedNode.code || '-' }}</div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">组织类别</label>
                    <n-tag :type="getCategoryTagType(selectedNode.category)" size="small">
                      {{ getCategoryLabel(selectedNode.category) }}
                    </n-tag>
                  </div>
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">启用状态</label>
                    <n-switch
                        v-model:value="selectedNode.enabled"
                        disabled
                        size="small"
                    >
                      <template #checked>
                        启用
                      </template>
                      <template #unchecked>
                        禁用
                      </template>
                    </n-switch>
                  </div>
                </div>

                <div>
                  <label class="text-sm text-gray-500 block mb-1">组织地址</label>
                  <div class="text-gray-800">{{ selectedNode.address || '-' }}</div>
                </div>

                <div>
                  <label class="text-sm text-gray-500 block mb-1">组织路径</label>
                  <div class="flex items-center gap-1 flex-wrap">
                    <template v-if="selectedNode.nameList && selectedNode.nameList.length > 0">
                      <template v-for="(name, index) in selectedNode.nameList" :key="index">
                        <span class="text-gray-600">{{ name }}</span>
                        <Icon v-if="index < selectedNode.nameList.length - 1"
                              icon="fluent:chevron-right-12-regular"
                              class="text-gray-400"
                              :width="12" :height="12"/>
                      </template>
                    </template>
                    <span v-else class="text-gray-600">{{ selectedNode.name }}</span>
                  </div>
                </div>
              </div>

              <!-- 操作提示 -->
              <div class="bg-blue-50 rounded-xl p-4 space-y-2">
                <h4 class="text-sm font-semibold text-blue-800 mb-2">操作提示</h4>
                <div class="space-y-1.5 text-sm text-blue-700">
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>点击组织节点查看详情</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>右击组织节点可编辑、删除、添加下级组织</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>拖动组织节点可排序、更改上下级关系</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>点击展开图标加载下级组织数据</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="flex flex-col items-center justify-center py-16">
              <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <Icon icon="fluent:organization-20-regular" class="text-gray-400" :width="40" :height="40"/>
              </div>
              <p class="text-gray-500">请选择一个组织查看详情</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <OrganizationEditModal
        ref="editModalRef"
        @success="handleEditSuccess"
    />

    <!-- 右键菜单 -->
    <n-dropdown
        placement="bottom-start"
        trigger="manual"
        :x="xRef"
        :y="yRef"
        :options="dropdownOptions"
        :show="showDropdown"
        :on-clickoutside="handleClickoutside"
        @select="handleSelect"
    />
  </div>
</template>

<script setup lang="ts">
import {ref, computed, h, nextTick} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NTree,
  NInput,
  NButton,
  NSpin,
  NTag,
  NSwitch,
  NDropdown,
  useNotification,
  useDialog,
  type TreeOption,
  type TreeDropInfo,
  type DropdownOption
} from 'naive-ui'
import {
  apiGetOrganizationTree,
  apiDeleteOrganization,
  apiSaveOrganizationSeqAndParent,
  type OrganizationTreeDetail,
  type OrganizationTreeParams,
  type DeleteOrganizationParams,
  type SaveOrganizationSeqAndParentParams
} from '@/api/organizationApi.ts'
import OrganizationEditModal from '@/components/sys/organization/EditModal.vue'

const notification = useNotification()
const dialog = useDialog()

// 扩展TreeOption类型
interface OrganizationTreeOption extends TreeOption, Omit<OrganizationTreeDetail, 'children'> {
  key: string
  label: string
  children?: OrganizationTreeOption[]
  isLeaf?: boolean
  hasLoaded?: boolean // 标记是否已加载子节点
}

// 组件引用
const editModalRef = ref()

// 数据状态
const loading = ref(false)
const organizationTreeData = ref<OrganizationTreeOption[]>([])
const selectedKeys = ref<string[]>([])
const expandedKeys = ref<string[]>([])
const searchValue = ref('')
const selectedNode = ref<OrganizationTreeDetail | null>(null)
const isDraggable = ref(true)

// 右键菜单相关
const showDropdown = ref(false)
const xRef = ref(0)
const yRef = ref(0)
const currentContextNode = ref<OrganizationTreeDetail | null>(null)

// 下拉菜单选项
const dropdownOptions = computed((): DropdownOption[] => {
  return [
    {
      label: '编辑',
      key: 'edit',
      icon: () => h(Icon, {icon: 'fluent:edit-20-regular'})
    },
    {
      label: '删除',
      key: 'delete',
      icon: () => h(Icon, {icon: 'fluent:delete-20-regular'})
    },
    {
      label: '添加下级',
      key: 'add',
      icon: () => h(Icon, {icon: 'fluent:add-circle-20-regular'})
    }
  ]
})

// 组织类别配置
const categoryConfig = {
  COMPANY: {label: '公司', type: 'primary'},
  OTHER: {label: '其他', type: 'default'}
}

// 获取类别标签
const getCategoryLabel = (category: string | null) => {
  if (!category) return '未分类'
  return categoryConfig[category]?.label || category
}

// 获取类别标签类型
const getCategoryTagType = (category: string | null) => {
  if (!category) return 'default'
  return categoryConfig[category]?.type || 'default'
}

// 转换组织数据为树形结构
const transformOrganizationToTree = (organizations: OrganizationTreeDetail[]): OrganizationTreeOption[] => {
  if (organizations?.length === 0) {
    return []
  }
  return organizations.map(org => {
    const hasChildren = org.children && org.children.length > 0
    return {
      ...org,
      key: org.id || '',
      label: org.name,
      children: hasChildren ? transformOrganizationToTree(org.children) : undefined,
      isLeaf: !org.hasChild, // 默认都可能有子节点，通过懒加载确定
      hasLoaded: hasChildren // 如果已有子节点数据，标记为已加载
    } as OrganizationTreeOption
  })
}

// 获取组织树（只加载第一层）
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

    // 如果已经加载过，直接返回
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
  // 搜索时需要加载所有数据或使用后端搜索接口
  if (value.trim()) {
    expandedKeys.value = []
    selectedKeys.value = []
    selectedNode.value = null
    getOrganizationTree(searchValue.value)
  }
}

// 清空搜索处理
const handleSearchClear = () => {
  searchValue.value = ''
  expandedKeys.value = []
  selectedKeys.value = []
  selectedNode.value = null
  getOrganizationTree(null)
}

// 节点选择处理
const handleSelectKeys = (keys: string[]) => {
  selectedKeys.value = keys
  if (keys.length > 0) {
    const node = findNodeByKey(organizationTreeData.value, keys[0])
    if (node) {
      selectedNode.value = {
        id: node.id,
        parentId: node.parentId,
        seq: node.seq,
        name: node.name,
        code: node.code,
        category: node.category,
        address: node.address,
        enabled: node.enabled,
        children: node.children as OrganizationTreeDetail[] | undefined,
        nameList: node.nameList,
        organizationIdList: node.organizationIdList,
        hasChild: node.hasChild
      }
    }
  } else {
    selectedNode.value = null
  }
}

// 展开节点处理
const handleExpandedKeys = (keys: string[]) => {
  expandedKeys.value = keys
}

// 通过key查找节点
const findNodeByKey = (nodes: OrganizationTreeOption[], key: string): OrganizationTreeOption | null => {
  for (const node of nodes) {
    if (node.key === key) {
      return node
    }
    if (node.children) {
      const found = findNodeByKey(node.children, key)
      if (found) return found
    }
  }
  return null
}

// 从树中删除节点
const removeNodeFromTree = (nodes: OrganizationTreeOption[], targetKey: string): boolean => {
  for (let i = 0; i < nodes.length; i++) {
    if (nodes[i].key === targetKey) {
      nodes.splice(i, 1)
      return true
    }
    if (nodes[i].children) {
      const removed = removeNodeFromTree(nodes[i].children, targetKey)
      if (removed) {
        // 如果子节点被删除后，父节点没有子节点了，更新父节点状态
        if (nodes[i].children.length === 0) {
          nodes[i].children = undefined
          nodes[i].isLeaf = true
        }
        return true
      }
    }
  }
  return false
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
  } else if (node.category === 'DEPARTMENT') {
    icon = 'fluent:people-team-20-regular'
    colorClass = 'text-blue-500'
  } else if (node.category === 'TEAM') {
    icon = 'fluent:people-20-regular'
    colorClass = 'text-orange-500'
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

  // 如果确定是叶子节点，返回空
  if (node.isLeaf && node.hasLoaded) {
    return null
  }

  // 返回折叠图标
  return h(Icon, {
    icon: info.expanded ? 'fluent:chevron-down-12-filled' : 'fluent:chevron-right-12-filled',
    width: 12,
    height: 12,
    class: 'text-gray-500'
  })
}

// 节点属性
const nodeProps = ({option}: { option: TreeOption }) => {
  return {
    onContextmenu: (e: MouseEvent) => {
      e.preventDefault()
      const node = option as OrganizationTreeOption
      currentContextNode.value = {
        ...node,
        children: node.children as OrganizationTreeDetail[] | undefined
      }
      showDropdown.value = false
      nextTick().then(() => {
        showDropdown.value = true
        xRef.value = e.clientX
        yRef.value = e.clientY
      })
    }
  } as Record<string, any>
}

// 处理下拉菜单选择
const handleSelect = (key: string) => {
  showDropdown.value = false
  if (currentContextNode.value) {
    handleCommand(key, currentContextNode.value)
  }
}

// 点击外部关闭下拉菜单
const handleClickoutside = () => {
  showDropdown.value = false
}

// 处理命令
const handleCommand = (command: string, node: OrganizationTreeDetail) => {
  switch (command) {
    case 'edit':
      handleEdit(node)
      break
    case 'delete':
      handleDelete(node)
      break
    case 'add':
      handleAdd(node)
      break
  }
}

// 添加根组织
const handleAddRoot = () => {
  editModalRef.value?.open(null, null, (savedData: OrganizationTreeDetail) => {
    handleEditSuccess(savedData, true, null)
  })
}

// 添加子组织
const handleAdd = (parent: OrganizationTreeDetail) => {
  editModalRef.value?.open(null, parent, (savedData: OrganizationTreeDetail) => {
    handleEditSuccess(savedData, true, parent)
  })
}

// 编辑节点
const handleEdit = (node: OrganizationTreeDetail) => {
  editModalRef.value?.open(node, null, (savedData: OrganizationTreeDetail) => {
    handleEditSuccess(savedData, false, null)
  })
}

// 删除节点
const handleDelete = (node: OrganizationTreeDetail) => {
  dialog.warning({
    title: '删除确认',
    content: `确定要删除组织【${node.name}】吗？删除后不可恢复。`,
    positiveText: '确定删除',
    negativeText: '取消',
    onPositiveClick: () => {
      doDeleteOrganization(node)
    }
  })
}

// 执行删除
const doDeleteOrganization = (node: OrganizationTreeDetail) => {
  const params: DeleteOrganizationParams = {
    organizationId: node.id || ''
  }
  loading.value = true
  apiDeleteOrganization(params).then((res) => {
    if (res.code === 200) {
      // 从树中删除节点
      const nodeKey = node.id || ''
      const removed = removeNodeFromTree(organizationTreeData.value, nodeKey)

      if (removed) {
        // 如果删除的是当前选中的节点，清空选中状态
        if (selectedKeys.value.includes(nodeKey)) {
          selectedKeys.value = []
          selectedNode.value = null
        }

        // 如果删除的节点在展开列表中，移除它
        const expandedIndex = expandedKeys.value.indexOf(nodeKey)
        if (expandedIndex > -1) {
          expandedKeys.value.splice(expandedIndex, 1)
        }

        notification.success({
          title: '删除成功',
          content: `组织【${node.name}】已删除`,
          duration: 3000
        })
      } else {
        // 如果从本地数据删除失败，回退到重新获取数据
        console.warn('从本地数据删除节点失败，重新获取数据')
        getOrganizationTree()
        notification.success({
          title: '删除成功',
          content: `组织【${node.name}】已删除`,
          duration: 3000
        })
      }
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

// 处理拖拽
const handleDrop = (info: TreeDropInfo) => {
  try {
    const {node, dragNode, dropPosition} = info

    if (!node || !dragNode) {
      console.error('拖拽节点信息不完整')
      return
    }

    const dragNodeData = dragNode as OrganizationTreeOption
    const dropNodeData = node as OrganizationTreeOption

    // 防止拖拽到自身或子节点
    if (!canDrop(dragNodeData, dropNodeData)) {
      notification.warning({
        title: '操作无效',
        content: '不能将节点拖拽到自身或其子节点中',
        duration: 3000
      })
      return
    }

    // 更新树形结构逻辑
    updateTreeStructure(dragNodeData, dropNodeData, dropPosition)
  } catch (error) {
    console.error('拖拽操作失败:', error)
    notification.error({
      title: '拖拽失败',
      content: '请刷新页面后重试',
      duration: 3000
    })
  }
}

// 检查是否可以拖拽
const canDrop = (dragNode: OrganizationTreeOption, dropNode: OrganizationTreeOption): boolean => {
  // 不能拖拽到自身
  if (dragNode.key === dropNode.key) {
    return false
  }

  // 不能拖拽到自己的子节点
  const isChildNode = (parent: OrganizationTreeOption, child: OrganizationTreeOption): boolean => {
    if (!parent.children) return false

    for (const node of parent.children) {
      if (node.key === child.key) return true
      if (isChildNode(node, child)) return true
    }
    return false
  }

  return !isChildNode(dragNode, dropNode)
}

// 更新树形结构 - 修复版本
const updateTreeStructure = (dragNode: OrganizationTreeOption, dropNode: OrganizationTreeOption, dropPosition: string) => {
  // 深拷贝组织树数据
  const newTreeData = JSON.parse(JSON.stringify(organizationTreeData.value))

  // 从原位置移除拖拽节点
  const removeNode = (nodes: OrganizationTreeOption[], targetKey: string): OrganizationTreeOption | null => {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].key === targetKey) {
        return nodes.splice(i, 1)[0]
      }
      if (nodes[i].children) {
        const removed = removeNode(nodes[i].children, targetKey)
        if (removed) return removed
      }
    }
    return null
  }

  // 查找节点的父节点
  const findParentNode = (nodes: OrganizationTreeOption[], targetKey: string, parent: OrganizationTreeOption | null = null): OrganizationTreeOption | null => {
    for (const node of nodes) {
      if (node.key === targetKey) {
        return parent
      }
      if (node.children) {
        const found = findParentNode(node.children, targetKey, node)
        if (found !== null) return found
      }
    }
    return null
  }

  // 插入节点到新位置并更新parentId
  const insertNode = (nodes: OrganizationTreeOption[], targetKey: string, insertedNode: OrganizationTreeOption, position: string): boolean => {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].key === targetKey) {
        if (position === 'inside') {
          // 插入为子节点 - 更新parentId为目标节点的id
          insertedNode.parentId = nodes[i].id

          if (!nodes[i].children) {
            nodes[i].children = []
          }
          nodes[i].children!.push(insertedNode)
          nodes[i].isLeaf = false
          nodes[i].hasChild = true

          // 递归更新插入节点的所有子节点的parentId链
          updateChildrenParentInfo(insertedNode)
        } else if (position === 'before' || position === 'after') {
          // 插入到目标节点的同级 - parentId应该与目标节点的parentId相同
          insertedNode.parentId = nodes[i].parentId

          if (position === 'before') {
            nodes.splice(i, 0, insertedNode)
          } else {
            nodes.splice(i + 1, 0, insertedNode)
          }

          // 递归更新插入节点的所有子节点的parentId链
          updateChildrenParentInfo(insertedNode)
        }
        return true
      }
      if (nodes[i].children) {
        const inserted = insertNode(nodes[i].children, targetKey, insertedNode, position)
        if (inserted) return true
      }
    }
    return false
  }

  // 递归更新子节点的parent信息
  const updateChildrenParentInfo = (node: OrganizationTreeOption) => {
    if (node.children && node.children.length > 0) {
      node.children.forEach(child => {
        child.parentId = node.id
        updateChildrenParentInfo(child)
      })
    }
  }

  // 处理根级别的插入（当拖动到树的最外层时）
  const handleRootLevelInsert = (draggedNode: OrganizationTreeOption, position: string, targetKey: string) => {
    // 如果是拖到根级别（before或after某个根节点）
    const targetIndex = newTreeData.findIndex((n: OrganizationTreeOption) => n.key === targetKey)
    if (targetIndex !== -1) {
      // 设置parentId为null（根节点）
      draggedNode.parentId = null

      if (position === 'before') {
        newTreeData.splice(targetIndex, 0, draggedNode)
      } else if (position === 'after') {
        newTreeData.splice(targetIndex + 1, 0, draggedNode)
      }

      // 递归更新子节点
      updateChildrenParentInfo(draggedNode)
      return true
    }
    return false
  }

  // 执行移动
  const draggedNode = removeNode(newTreeData, dragNode.key)
  if (draggedNode) {
    let insertPosition = 'inside'
    if (dropPosition === 'before') insertPosition = 'before'
    else if (dropPosition === 'after') insertPosition = 'after'

    // 先尝试在子树中插入
    let inserted = insertNode(newTreeData, dropNode.key, draggedNode, insertPosition)

    // 如果没有成功插入，可能是拖到了根级别
    if (!inserted && (insertPosition === 'before' || insertPosition === 'after')) {
      inserted = handleRootLevelInsert(draggedNode, insertPosition, dropNode.key)
    }

    if (inserted) {
      // 更新数据
      organizationTreeData.value = newTreeData

      notification.info({
        title: '拖拽成功',
        content: '组织结构已更新，请点击保存按钮提交更改',
        duration: 3000
      })
    } else {
      notification.error({
        title: '拖拽失败',
        content: '无法完成拖拽操作，请重试',
        duration: 3000
      })
      // 如果插入失败，重新加载数据
      getOrganizationTree()
    }
  }
}

// 修改doSaveSeqAndParent中的collectOrganizationData函数
// 确保收集数据时parentId是正确的
const doSaveSeqAndParent = () => {
  // 收集树形数据 - 添加parentId参数以正确设置父ID
  const collectOrganizationData = (nodes: OrganizationTreeOption[], parentId: string | null = null): OrganizationTreeDetail[] => {
    return nodes.map((node, index) => {
      return {
        id: node.id,
        parentId: parentId, // 使用传入的parentId而不是节点自身的parentId
        seq: index + 1,
        name: node.name,
        code: node.code,
        category: node.category,
        address: node.address,
        enabled: node.enabled,
        children: node.children ? collectOrganizationData(node.children, node.id) : [], // 递归时传入当前节点的id作为子节点的parentId
        nameList: node.nameList,
        organizationIdList: node.organizationIdList,
        hasChild: node.hasChild || (node.children && node.children.length > 0),
      }
    })
  }

  const params: SaveOrganizationSeqAndParentParams = {
    organizationTree: collectOrganizationData(organizationTreeData.value, null) // 根节点的parentId为null
  }

  loading.value = true
  apiSaveOrganizationSeqAndParent(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '保存成功',
        content: '组织结构已更新',
        duration: 3000
      })
      getOrganizationTree()
    } else {
      notification.error({
        title: '保存失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '保存失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 刷新指定节点的子节点数据
const refreshNodeChildren = async (parentId: string | null) => {
  if (!parentId) {
    // 如果是根节点，重新获取根级数据
    getOrganizationTree()
    return
  }

  const params: OrganizationTreeParams = {
    level: null,
    parentId: parentId
  }

  try {
    const res = await apiGetOrganizationTree(params)
    if (res.code === 200) {
      // 找到父节点并更新其子节点
      const updateNodeChildren = (nodes: OrganizationTreeOption[], targetId: string): boolean => {
        for (const node of nodes) {
          if (node.id === targetId) {
            // 更新子节点数据
            if (res.data && res.data.length > 0) {
              node.children = transformOrganizationToTree(res.data)
              node.isLeaf = false
              node.hasLoaded = true
              // 确保父节点展开以显示新添加的子节点
              if (!expandedKeys.value.includes(node.key)) {
                expandedKeys.value.push(node.key)
              }
            } else {
              node.children = undefined
              node.isLeaf = true
              node.hasLoaded = true
            }
            return true
          }
          if (node.children) {
            const updated = updateNodeChildren(node.children, targetId)
            if (updated) return true
          }
        }
        return false
      }

      const updated = updateNodeChildren(organizationTreeData.value, parentId)
      if (!updated) {
        // 如果在当前树中找不到父节点，可能是因为父节点还没有加载，重新获取整个树
        console.warn('在当前树中找不到父节点，重新获取整个树')
        getOrganizationTree()
      }
    } else {
      notification.error({
        title: '刷新失败',
        content: res.message,
        duration: 3000
      })
    }
  } catch (err) {
    notification.error({
      title: '刷新失败',
      content: String(err),
      duration: 3000
    })
  }
}

// 编辑成功回调
const handleEditSuccess = (savedData?: OrganizationTreeDetail, isAdd: boolean = false, parentNode?: OrganizationTreeDetail | null) => {
  if (isAdd && savedData) {
    // 如果是添加操作，只刷新父节点的子节点
    const parentId = parentNode?.id || null
    refreshNodeChildren(parentId)

    notification.success({
      title: '添加成功',
      content: `组织【${savedData.name}】已添加`,
      duration: 3000
    })
  } else {
    // 如果是编辑操作，需要更新当前节点信息
    if (savedData && selectedNode.value && selectedNode.value.id === savedData.id) {
      // 更新选中节点的信息
      selectedNode.value = {...savedData}

      // 更新树中对应节点的信息
      const updateNodeInTree = (nodes: OrganizationTreeOption[], targetId: string, newData: OrganizationTreeDetail): boolean => {
        for (const node of nodes) {
          if (node.id === targetId) {
            // 更新节点数据，保留树结构相关属性
            Object.assign(node, {
              ...newData,
              key: node.key,
              label: newData.name,
              children: node.children,
              isLeaf: node.isLeaf,
              hasLoaded: node.hasLoaded
            })
            return true
          }
          if (node.children) {
            const updated = updateNodeInTree(node.children, targetId, newData)
            if (updated) return true
          }
        }
        return false
      }

      updateNodeInTree(organizationTreeData.value, savedData.id || '', savedData)
    }

    notification.success({
      title: '编辑成功',
      content: `组织【${savedData?.name}】已更新`,
      duration: 3000
    })
  }
}

// 初始化
getOrganizationTree()
</script>

<style scoped lang="scss">
// 树形组件样式
:deep(.organization-tree) {
  .n-tree-node {
    padding: 0;
    margin: 2px 0;

    .n-tree-node-wrapper {
      background-color: transparent !important;
      padding: 0 !important;
      margin: 0 !important;
    }

    background-color: transparent !important;

    .n-tree-node-content {
      width: 100%;
      padding: 8px 12px;
      border-radius: 8px;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      min-height: 36px;
      margin: 0;
      background-color: transparent;

      &:hover {
        background-color: #e5e8ec;
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

    &.n-tree-node--selected {
      .n-tree-node-content {
        background-color: #ede9fe;

        .tree-node-label {
          color: #6366f1;
          font-weight: 500;
        }
      }
    }

    &:hover:not(.n-tree-node--selected) {
      .n-tree-node-content {
        background-color: #e5e8ec;
      }
    }
  }

  .n-tree-node-indent {
    width: 1.5rem;
  }

  .n-tree-node-switcher {
    display: flex;
    align-items: center;
    justify-content: center;
    align-self: center;
    width: 24px;
    height: 24px;
  }

  .n-tree-node--highlight {
    .n-tree-node-content {
      background-color: #fef3c7;

      .tree-node-label {
        color: #d97706;
        font-weight: 500;
      }
    }
  }

  .n-tree-node--matched {
    .n-tree-node-content {
      background-color: #fef3c7;
      border: 1px solid #f59e0b;

      .tree-node-label {
        color: #d97706;
        font-weight: 600;
      }
    }
  }
}

// 滚动条样式
.overflow-auto {
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

    &.n-button--success-type {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #0ea55e 0%, #047857 100%);
      }
    }
  }
}

// 搜索框增强样式
:deep(.n-input) {
  .n-input__input-el {
    &::placeholder {
      color: #9ca3af;
    }
  }

  &:hover {
    .n-input__border {
      border-color: #6366f1;
    }
  }

  &.n-input--focus {
    .n-input__border {
      border-color: #6366f1;
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
    }
  }
}
</style>