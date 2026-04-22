<template>
  <div class="flex-1 flex flex-col min-h-0 bg-gradient-to-br from-gray-50 to-gray-100/50">
    <!-- 页面头部 -->
    <div class="px-6 py-5 bg-white shadow-sm border-b border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div
                class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 transform rotate-3 transition-transform hover:rotate-6">
              <Icon icon="fluent:navigation-20-filled" :width="24" :height="24"/>
            </div>
            <div
                class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
              <Icon icon="fluent:checkmark-12-filled" class="text-white" :width="12" :height="12"/>
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
              菜单管理
            </h1>
            <p class="text-sm text-gray-500 mt-1">管理系统菜单结构及权限配置</p>
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
                    placeholder="搜索菜单名称"
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
                  @click="handleSaveSeqAndParent"
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
                添加根节点
              </n-button>
            </div>
          </div>

          <div class="flex-1 px-6 pb-6 overflow-auto">
            <n-spin :show="loading">
              <n-tree
                  :data="menuTreeData"
                  :pattern="searchValue"
                  :selected-keys="selectedKeys"
                  :expanded-keys="expandedKeys"
                  :on-update:selected-keys="handleSelectKeys"
                  :on-update:expanded-keys="handleExpandedKeys"
                  :node-props="nodeProps"
                  :render-label="renderLabel"
                  :render-prefix="renderPrefix"
                  :render-switcher-icon="renderSwitcherIcon"
                  block-line
                  :draggable="isDraggable"
                  expand-on-click
                  @drop="handleDrop"
                  class="menu-tree"
              />
            </n-spin>
          </div>
        </div>

        <!-- 右侧详情 -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Icon icon="fluent:info-20-filled" class="text-indigo-500"/>
              菜单详情
            </h3>

            <div v-if="selectedNode" class="space-y-4">
              <!-- 基本信息 -->
              <div class="bg-gray-50 rounded-xl p-4 space-y-3">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">菜单名称</label>
                    <div class="text-gray-800 font-medium">{{ selectedNode.name }}</div>
                  </div>
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">菜单编码</label>
                    <div class="text-gray-800 font-medium">{{ selectedNode.code }}</div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="text-sm text-gray-500 block mb-1">菜单类型</label>
                    <n-tag :type="selectedNode.type === 'AGGREGATION' ? 'warning' : 'info'" size="small">
                      {{ selectedNode.type === 'AGGREGATION' ? '聚合菜单' : '普通菜单' }}
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
                  <label class="text-sm text-gray-500 block mb-1">菜单路径</label>
                  <div class="text-gray-800">{{ selectedNode.url || '-' }}</div>
                </div>

                <div>
                  <label class="text-sm text-gray-500 block mb-1">菜单图标</label>
                  <div class="flex items-center gap-2">
                    <Icon :icon="selectedNode.icon || 'fluent:document-20-regular'" :width="20" :height="20"
                          class="text-gray-600"/>
                    <span class="text-gray-800">{{ selectedNode.icon || '-' }}</span>
                  </div>
                </div>
              </div>

              <!-- 操作提示 -->
              <div class="bg-blue-50 rounded-xl p-4 space-y-2">
                <h4 class="text-sm font-semibold text-blue-800 mb-2">操作提示</h4>
                <div class="space-y-1.5 text-sm text-blue-700">
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>点击菜单节点查看详情</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>右击菜单节点可编辑、删除、添加菜单</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>拖动菜单节点可排序、更改父子关系</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <Icon icon="fluent:info-16-filled" class="mt-0.5 flex-shrink-0"/>
                    <span>只有聚合类菜单节点可以添加子节点</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="flex flex-col items-center justify-center py-16">
              <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <Icon icon="fluent:navigation-unread-20-regular" class="text-gray-400" :width="40" :height="40"/>
              </div>
              <p class="text-gray-500">请选择一个菜单查看详情</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <MenuEditModal
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
import {ref, computed, h, nextTick, watch} from 'vue'
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
  apiGetMenuTree,
  apiDeleteMenu,
  apiSaveMenuSeqAndParent,
  type MenuTreeDetail,
  type MenuTreeParams,
  type DeleteMenuParams,
  type SaveMenuSeqAndParentParams
} from '@/api/menuApi.ts'
import MenuEditModal from '@/components/sys/menu/EditModal.vue'

const notification = useNotification()
const dialog = useDialog()

// 扩展TreeOption类型，直接继承MenuTreeDetail的结构
interface MenuTreeOption extends TreeOption, Omit<MenuTreeDetail, 'children'> {
  key: string
  label: string
  children?: MenuTreeOption[]
  isLeaf?: boolean
}

// 组件引用
const editModalRef = ref()

// 数据状态
const loading = ref(false)
const menuTreeData = ref<MenuTreeOption[]>([])
const selectedKeys = ref<string[]>([])
const expandedKeys = ref<string[]>([])
const searchValue = ref('')
const selectedNode = ref<MenuTreeDetail | null>(null)
const allExpandedKeys = ref<string[]>([]) // 存储所有可展开的keys
const isDraggable = ref(true) // 控制拖拽功能

// 右键菜单相关
const showDropdown = ref(false)
const xRef = ref(0)
const yRef = ref(0)
const currentContextNode = ref<MenuTreeDetail | null>(null)

// 下拉菜单选项
const dropdownOptions = computed((): DropdownOption[] => {
  const options: DropdownOption[] = [
    {
      label: '编辑',
      key: 'edit',
      icon: () => h(Icon, {icon: 'fluent:edit-20-regular'})
    },
    {
      label: '删除',
      key: 'delete',
      icon: () => h(Icon, {icon: 'fluent:delete-20-regular'})
    }
  ]

  if (currentContextNode.value?.type === 'AGGREGATION') {
    options.push({
      label: '添加子节点',
      key: 'add',
      icon: () => h(Icon, {icon: 'fluent:add-circle-20-regular'})
    })
  }

  return options
})

// 转换菜单数据为树形结构
const transformMenuToTree = (menus: MenuTreeDetail[]): MenuTreeOption[] => {
  return menus.map(menu => {
    const hasChildren = menu.children && menu.children.length > 0
    return {
      ...menu,
      key: menu.id,
      label: menu.name,
      children: hasChildren ? transformMenuToTree(menu.children) : undefined,
      isLeaf: !hasChildren
    } as MenuTreeOption
  })
}

// 获取菜单树
const getMenuTree = () => {
  const params: MenuTreeParams = {
    parentId: null
  }
  loading.value = true
  apiGetMenuTree(params).then((res) => {
    if (res.code === 200) {
      menuTreeData.value = transformMenuToTree(res.data)
      // 获取所有可展开的节点keys
      allExpandedKeys.value = getAllKeys(menuTreeData.value)
      // 默认展开所有节点
      expandedKeys.value = [...allExpandedKeys.value]
    } else {
      notification.error({
        title: '获取菜单失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取菜单失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 获取所有节点的key
const getAllKeys = (nodes: MenuTreeOption[]): string[] => {
  const keys: string[] = []
  const traverse = (node: MenuTreeOption) => {
    keys.push(node.key as string)
    if (node.children) {
      node.children.forEach(traverse)
    }
  }
  nodes.forEach(traverse)
  return keys
}

// 搜索处理
const handleSearch = (value: string) => {
  if (value.trim()) {
    // 搜索时自动展开所有节点
    expandedKeys.value = [...allExpandedKeys.value]
  }
}

// 清空搜索处理
const handleSearchClear = () => {
  // 清空搜索时保持当前展开状态
  // 如果想要收起所有节点，可以取消下面这行的注释
  // expandedKeys.value = []
}

// 监听搜索值变化，自动展开匹配节点的父节点
watch(searchValue, (newValue) => {
  if (newValue.trim()) {
    // 搜索时展开所有节点以显示匹配结果
    expandedKeys.value = [...allExpandedKeys.value]
  }
})

// 节点选择处理
const handleSelectKeys = (keys: string[]) => {
  selectedKeys.value = keys
  if (keys.length > 0) {
    const node = findNodeByKey(menuTreeData.value, keys[0])
    if (node) {
      // 直接使用节点数据，因为MenuTreeOption已经包含了所有需要的属性
      selectedNode.value = {
        id: node.id,
        parentId: node.parentId,
        seq: node.seq,
        name: node.name,
        code: node.code,
        enabled: node.enabled,
        url: node.url,
        icon: node.icon,
        type: node.type,
        children: node.children as MenuTreeDetail[] | undefined,
        typeDisplay: node.typeDisplay,
        nameList: node.nameList
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
const findNodeByKey = (nodes: MenuTreeOption[], key: string): MenuTreeOption | null => {
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

// 渲染节点标签
const renderLabel = (info: { option: TreeOption }) => {
  return h('span', {class: 'tree-node-label text-gray-700'}, info.option.label as string)
}

// 渲染节点前缀图标
const renderPrefix = (info: { option: TreeOption }) => {
  const node = info.option as MenuTreeOption
  return h(Icon, {
    icon: node.icon || 'fluent:document-20-regular',
    width: 18,
    height: 18,
    class: node.type === 'AGGREGATION' ? 'text-orange-500' : 'text-blue-500'
  })
}

// 渲染折叠图标
const renderSwitcherIcon = (info: { option: TreeOption, expanded: boolean }) => {
  const node = info.option
  // 如果是叶子节点，返回空
  if (node.isLeaf) {
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
    // @ts-ignore - onContextmenu 是有效的事件属性
    onContextmenu: (e: MouseEvent) => {
      e.preventDefault()
      const node = option as MenuTreeOption
      currentContextNode.value = {
        ...node,
        children: node.children as MenuTreeDetail[] | undefined
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
const handleCommand = (command: string, node: MenuTreeDetail) => {
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

// 添加根节点
const handleAddRoot = () => {
  editModalRef.value?.open()
}

// 添加子节点
const handleAdd = (parent: MenuTreeDetail) => {
  editModalRef.value?.open(null, parent)
}

// 编辑节点
const handleEdit = (node: MenuTreeDetail) => {
  editModalRef.value?.open(node)
}

// 删除节点
const handleDelete = (node: MenuTreeDetail) => {
  dialog.warning({
    title: '删除确认',
    content: `确定要删除菜单【${node.name}】吗？删除后不可恢复。`,
    positiveText: '确定删除',
    negativeText: '取消',
    onPositiveClick: () => {
      doDeleteMenu(node)
    }
  })
}

// 执行删除
const doDeleteMenu = (node: MenuTreeDetail) => {
  const params: DeleteMenuParams = {
    menuId: node.id
  }
  loading.value = true
  apiDeleteMenu(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '删除成功',
        content: `菜单【${node.name}】已删除`,
        duration: 3000
      })
      getMenuTree()
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

    const dragNodeData = dragNode as MenuTreeOption
    const dropNodeData = node as MenuTreeOption

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
const canDrop = (dragNode: MenuTreeOption, dropNode: MenuTreeOption): boolean => {
  // 不能拖拽到自身
  if (dragNode.key === dropNode.key) {
    return false
  }

  // 不能拖拽到自己的子节点
  const isChildNode = (parent: MenuTreeOption, child: MenuTreeOption): boolean => {
    if (!parent.children) return false

    for (const node of parent.children) {
      if (node.key === child.key) return true
      if (isChildNode(node, child)) return true
    }
    return false
  }

  return !isChildNode(dragNode, dropNode)
}

// 更新树形结构
const updateTreeStructure = (dragNode: MenuTreeOption, dropNode: MenuTreeOption, dropPosition: string) => {
  // 深拷贝菜单树数据
  const newTreeData = JSON.parse(JSON.stringify(menuTreeData.value))

  // 从原位置移除拖拽节点
  const removeNode = (nodes: MenuTreeOption[], targetKey: string): MenuTreeOption | null => {
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

  // 插入节点到新位置
  const insertNode = (nodes: MenuTreeOption[], targetKey: string, insertedNode: MenuTreeOption, position: string) => {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].key === targetKey) {
        if (position === 'inside') {
          // 插入为子节点
          if (!nodes[i].children) {
            nodes[i].children = []
          }
          nodes[i].children!.push(insertedNode)
          nodes[i].isLeaf = false
        } else if (position === 'before') {
          // 插入到目标节点之前
          nodes.splice(i, 0, insertedNode)
        } else if (position === 'after') {
          // 插入到目标节点之后
          nodes.splice(i + 1, 0, insertedNode)
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

  // 执行移动
  const draggedNode = removeNode(newTreeData, dragNode.key)
  if (draggedNode) {
    let position = 'inside'
    if (dropPosition === 'before') position = 'before'
    else if (dropPosition === 'after') position = 'after'

    insertNode(newTreeData, dropNode.key, draggedNode, position)

    // 更新数据
    menuTreeData.value = newTreeData

    notification.info({
      title: '拖拽成功',
      content: '菜单结构已更新，请点击保存按钮提交更改',
      duration: 3000
    })
  }
}

// 保存排序和父子关系
const handleSaveSeqAndParent = () => {
  dialog.info({
    title: '保存确认',
    content: '确定要保存当前的排序和父子关系吗？',
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: () => {
      doSaveSeqAndParent()
    }
  })
}

// 执行保存
const doSaveSeqAndParent = () => {
  // 收集树形数据并转换为扁平结构
  const collectMenuData = (nodes: MenuTreeOption[], parentId: string | null = null): any[] => {
    const result: any[] = []
    nodes.forEach((node, index) => {
      const menuData = {
        id: node.key,
        parentId: parentId,
        seq: index + 1,
        name: node.name,
        code: node.code,
        enabled: node.enabled,
        url: node.url,
        icon: node.icon,
        type: node.type
      }
      result.push(menuData)

      if (node.children && node.children.length > 0) {
        result.push(...collectMenuData(node.children, node.key as string))
      }
    })
    return result
  }

  const params: SaveMenuSeqAndParentParams = {
    menuTree: collectMenuData(menuTreeData.value)
  }

  loading.value = true
  apiSaveMenuSeqAndParent(params).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '保存成功',
        content: '菜单结构已更新',
        duration: 3000
      })
      getMenuTree()
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

// 编辑成功回调
const handleEditSuccess = () => {
  getMenuTree()
}
// 初始化
getMenuTree()
</script>

<style scoped lang="scss">
// 树形组件样式
:deep(.menu-tree) {
  .n-tree-node {
    padding: 0;
    margin: 2px 0;

    // 确保节点的 wrapper 不干扰背景样式
    .n-tree-node-wrapper {
      background-color: transparent !important; // 去除 wrapper 背景
      padding: 0 !important;
      margin: 0 !important;
    }

    // 清除节点本身背景，确保只通过 .n-tree-node-content 控制
    background-color: transparent !important;

    // 确保背景色只应用于 .n-tree-node-content
    .n-tree-node-content {
      width: 100%;
      padding: 8px 12px;
      border-radius: 8px;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      min-height: 36px;
      margin: 0;
      background-color: transparent; // 初始透明背景

      &:hover {
        background-color: #e5e8ec; // hover 背景色
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

    // 选中状态背景
    &.n-tree-node--selected {
      .n-tree-node-content {
        background-color: #ede9fe; // 选中背景色

        .tree-node-label {
          color: #6366f1;
          font-weight: 500;
        }
      }
    }

    // hover 状态背景
    &:hover:not(.n-tree-node--selected) {
      .n-tree-node-content {
        background-color: #e5e8ec;
      }
    }
  }

  .n-tree-node-indent {
    width: 1.5rem;
  }

  // 折叠图标垂直居中
  .n-tree-node-switcher {
    display: flex;
    align-items: center;
    justify-content: center;
    align-self: center;
    width: 24px;
    height: 24px;
  }

  // 确保搜索高亮显示正常
  .n-tree-node--highlight {
    .n-tree-node-content {
      background-color: #fef3c7;

      .tree-node-label {
        color: #d97706;
        font-weight: 500;
      }
    }
  }

  // 搜索匹配节点的特殊样式
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