<template>
  <n-modal
      v-model:show="visible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :style="{ width: '750px' }"
      :bordered="false"
      segmented
      class="menu-select-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon icon="fluent:navigation-20-filled" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">选择菜单</span>
      </div>
    </template>

    <div class="flex flex-col h-[600px]">
      <!-- 搜索栏 -->
      <div class="px-6 py-4 border-b border-gray-100">
        <n-input-group>
          <n-input
              v-model:value="params.search"
              placeholder="请输入菜单名称"
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

      <!-- 树形表格区域 -->
      <div class="flex-1 px-6 py-4 overflow-auto">
        <n-spin :show="loading">
          <n-tree
              :data="menuTree"
              :pattern="params.search"
              :show-irrelevant-nodes="false"
              :selectable="true"
              :selected-keys="selectedKeys"
              :on-update:selected-keys="handleUpdateSelectedKeys"
              :node-props="nodeProps"
              :render-label="renderLabel"
              :render-prefix="renderPrefix"
              block-line
              class="menu-tree"
          />
        </n-spin>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && menuTree.length === 0" class="flex flex-col items-center justify-center py-12">
        <Icon icon="fluent:folder-open-20-regular" class="text-gray-400 mb-3" :width="48" :height="48"/>
        <p class="text-gray-500">暂无菜单数据</p>
      </div>

      <!-- 底部选中信息 -->
      <div class="px-6 py-4 border-t border-gray-100 bg-gray-50" v-if="selectedMenu">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <Icon icon="fluent:checkmark-circle-20-filled" class="text-green-600"/>
            <span class="text-sm text-gray-700">
              已选择：<span class="font-medium">{{ selectedMenu.name }}</span>
              <span class="text-gray-500 ml-2">({{ selectedMenu?.nameList?.join('/') }})</span>
            </span>
          </div>
          <n-button type="primary" size="small" @click="handleConfirm">
            确认选择
          </n-button>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import {h, ref} from 'vue'
import {Icon} from '@iconify/vue'
import {NButton, NInput, NInputGroup, NModal, NSpin, NTag, NTree, type TreeOption, useNotification} from 'naive-ui'
import {apiGetMenuTree, type MenuTreeDetail, MenuTreeParams,} from '@/api/menuApi.ts'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts"

const notification = useNotification()
const emit = defineEmits(['selected'])

// 状态
const visible = ref(false)
const loading = ref(false)
const menuTree = ref<TreeOption[]>([])
const selectedKeys = ref<string[]>([])
const selectedMenu = ref<MenuTreeDetail | null>(null)

// 搜索参数
const params = ref({
  search: ''
})

// 将菜单树转换为 NTree 需要的格式
const transformMenuTree = (nodes: MenuTreeDetail[]): TreeOption[] => {
  const data = nodes.map(node => ({
    key: node.id,
    label: node.name,
    nameList: node.nameList,
    icon: node.icon,
    type: node.type,
    enabled: node.enabled,
    children: node.children ? transformMenuTree(node.children) : undefined,
    isLeaf: !node.children || node.children.length === 0,
    _raw: node // 保存原始数据
  }))
  console.log('transformMenuTree ...')
  console.log(data)
  return data
}

// 渲染节点标签
const renderLabel = (data: any) => {
  const option: TreeOption = data.option as TreeOption
  console.log('option ...')
  console.log(option)
  return h('div', {class: 'flex items-center gap-2'}, [
    h('span', {class: option?.enabled ? '' : 'text-gray-400'}, option?.label),
    option.type === 'EXTERNAL' && h(NTag, {
      type: 'info',
      size: 'tiny',
      round: true
    }, {
      default: () => '外链'
    })
  ])
}

// 渲染节点前缀图标
const renderPrefix = ({ option }: { option: TreeOption }) => {
  const iconMap = {
    'home': 'fluent:home-20-regular',
    'user': 'fluent:person-20-regular',
    'setting': 'fluent:settings-20-regular',
    'menu': 'fluent:navigation-20-regular',
    'document': 'fluent:document-20-regular',
    'folder': 'fluent:folder-20-regular',
  }

  const iconName = option.icon || (option.isLeaf ? 'document' : 'folder')
  const icon = iconMap[iconName as string] || iconMap['menu']

  return h('div', {
    class: `w-8 h-8 rounded-lg flex items-center justify-center ${
        option.enabled
            ? 'bg-gradient-to-br from-teal-100 to-cyan-100 text-teal-600'
            : 'bg-gray-100 text-gray-400'
    }`
  }, h(Icon, {icon, width: 16, height: 16}))
}

// 节点属性
const nodeProps = ({option}: { option: TreeOption }) => {
  return {
    onClick() {
      if (option.key) {
        handleSelectMenu(option)
      }
    }
  }
}

// 更新选中的键
const handleUpdateSelectedKeys = (keys: string[]) => {
  selectedKeys.value = keys
}

// 选择菜单
const handleSelectMenu = (option: TreeOption) => {
  selectedKeys.value = [option.key as string]
  selectedMenu.value = {
    id: option.key as string,
    name: option.label as string,
    nameList: (option.nameList || []) as string[],
    icon: option.icon as string,
    type: option.type as string,
    enabled: option.enabled as boolean,
  }
}

// 确认选择
const handleConfirm = () => {
  if (selectedMenu.value) {
    emit('selected', selectedMenu.value)
    close()
  }
}

// 打开弹窗
const open = () => {
  visible.value = true
  selectedKeys.value = []
  selectedMenu.value = null
  getMenuTree()
}

// 关闭弹窗
const close = () => {
  visible.value = false
}

// 获取菜单树
const getMenuTree = () => {
  loading.value = true
  const params: MenuTreeParams = {
    parentId: null
  }
  apiGetMenuTree(params).then((res) => {
    if (res.code === 200) {
      menuTree.value = transformMenuTree(res.data)
    } else {
      notification.error({
        title: '获取菜单列表失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取菜单列表失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 搜索处理
const handleSearch = () => {
  // NTree 组件内置了搜索功能，通过 pattern 属性实现
}

const handleClearSearch = () => {
  params.value.search = ''
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

// 树形组件样式
:deep(.menu-tree) {
  .n-tree-node {
    padding: 4px 0;

    &.n-tree-node--selected {
      background: linear-gradient(to right, #e0f2fe, #cffafe);

      .n-tree-node-content {
        background: transparent;
      }
    }

    .n-tree-node-content {
      padding: 8px 12px;
      border-radius: 8px;
      transition: all 0.2s ease;

      &:hover {
        background: #f3f4f6;
      }

      &__text {
        font-size: 14px;
      }
    }

    .n-tree-node-indent {
      width: 24px;
    }
  }
}

// 输入框样式
:deep(.n-input) {
  &.n-input--focus {
    border-color: #06b6d4;
    box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.1);
  }
}

// 按钮样式
:deep(.n-button) {
  &.n-button--primary-type {
    background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
    border: none;

    &:hover {
      background: linear-gradient(135deg, #0f766e 0%, #0891b2 100%);
    }
  }
}

// 标签样式
:deep(.n-tag) {
  &.n-tag--info-type {
    background: rgba(6, 182, 212, 0.1);
    color: #0891b2;
    border-color: rgba(6, 182, 212, 0.2);
  }
}

// 加载状态
:deep(.n-spin-content) {
  min-height: 300px;
}
</style>