<template>
  <n-modal
      v-model:show="visible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :style="{ width: '600px' }"
      :bordered="false"
      segmented
      :on-after-leave="resetForm"
      class="menu-edit-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon :icon="modalCategory === 'EDIT' ? 'fluent:edit-20-filled' : 'fluent:add-circle-20-filled'" :width="20"
                :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">{{ title }}</span>
      </div>
    </template>
    <div class="custom-form-modal-content">
      <div class="custom-form-content">
        <n-spin :show="loading">
          <n-form
              ref="formRef"
              :model="formData"
              :rules="formRules"
              label-placement="left"
              label-width="100px"
          >
            <n-form-item label="父节点" v-if="formDisplay.parentName">
              <n-input
                  :value="formDisplay.parentName"
                  disabled
                  placeholder="父节点"
              />
            </n-form-item>

            <n-form-item label="名称" path="name">
              <n-input
                  v-model:value="formData.name"
                  placeholder="请输入名称"
                  clearable
                  maxlength="500"
                  show-count
              />
            </n-form-item>

            <n-form-item label="编码" path="code">
              <n-input
                  v-model:value="formData.code"
                  placeholder="请输入编码"
                  clearable
                  maxlength="500"
                  show-count
              />
            </n-form-item>

            <n-form-item label="类型" path="type">
              <n-select
                  v-model:value="formData.type"
                  placeholder="请选择类型"
                  :options="typeOptions"
              />
            </n-form-item>

            <n-form-item label="图标" path="icon">
              <n-input-group>
                <n-input
                    v-model:value="formData.icon"
                    placeholder="请输入图标名称（如：fluent:home-20-filled）"
                    clearable
                    maxlength="500"
                    show-count
                />
                <n-button type="primary" @click="showIconPreview">
                  <template #icon>
                    <Icon :icon="formData.icon || 'fluent:eye-20-regular'"/>
                  </template>
                  预览
                </n-button>
              </n-input-group>
            </n-form-item>

            <n-form-item label="URL" path="url">
              <n-input
                  v-model:value="formData.url"
                  placeholder="请输入菜单路径"
                  clearable
                  maxlength="500"
                  show-count
              />
            </n-form-item>

            <n-form-item label="启用状态" path="enabled">
              <div class="flex items-center gap-4">
                <n-switch v-model:value="formData.enabled" size="medium">
                  <template #checked>
                    启用
                  </template>
                  <template #unchecked>
                    禁用
                  </template>
                </n-switch>
                <span class="text-sm text-gray-500">
              {{ formData.enabled ? '菜单启用后将在系统中显示' : '菜单禁用后将在系统中隐藏' }}
            </span>
              </div>
            </n-form-item>

            <!-- 图标预览区域 -->
            <n-form-item label="图标预览" v-if="formData.icon">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
                  <Icon :icon="formData.icon" :width="24" :height="24" class="text-gray-700"/>
                </div>
                <div class="w-12 h-12 bg-indigo-500 rounded-xl flex items-center justify-center">
                  <Icon :icon="formData.icon" :width="24" :height="24" class="text-white"/>
                </div>
                <div class="w-12 h-12 bg-gray-800 rounded-xl flex items-center justify-center">
                  <Icon :icon="formData.icon" :width="24" :height="24" class="text-white"/>
                </div>
              </div>
            </n-form-item>
          </n-form>
        </n-spin>
      </div>
    </div>
    <template #footer>
      <div class="flex gap-3 justify-end">
        <n-button size="large" @click="handleCancel">
          取消
        </n-button>
        <n-button type="primary" size="large" @click="handleSubmit" :loading="loading">
          <template #icon>
            <Icon icon="fluent:save-20-regular"/>
          </template>
          提交
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputGroup,
  NSelect,
  NSwitch,
  NButton,
  NSpin,
  useNotification,
  useMessage,
  type FormInst,
  type FormRules,
  type FormItemRule
} from 'naive-ui'
import {
  apiEditMenu,
  apiGetMenuDetail,
  type MenuDetail
} from '@/api/menuApi.ts'
import {dialogMaskClosable, dialogDraggable} from "@/config/dialogConfig.ts"

const notification = useNotification()
const message = useMessage()
const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 状态
const visible = ref(false)
const loading = ref(false)
const modalCategory = ref<'ADD' | 'EDIT'>('ADD')
const menuDetailData = ref<MenuDetail | null>(null)

// 计算属性
const title = computed(() => modalCategory.value === 'ADD' ? '添加菜单' : '编辑菜单')

// 表单数据
const formData = ref<MenuDetail>({
  id: null,
  name: null,
  code: null,
  enabled: true,
  url: null,
  icon: null,
  type: 'NORMAL',
  parentId: null,
  seq: null,
  nameList: null,
})

// 表单显示数据
const formDisplay = ref({
  parentName: null as string | null,
})

// 类型选项
const typeOptions = ref([
  {value: 'AGGREGATION', label: '聚合菜单节点'},
  {value: 'NORMAL', label: '普通菜单节点'},
])

// 表单验证规则
const validateCode = (_rule: FormItemRule, value: string) => {
  if (!value) {
    return new Error('请输入编码')
  } else if (!/^[A-Za-z0-9_]+$/.test(value)) {
    return new Error('编码只能包含字母、数字和下划线')
  }
  return true
}

const formRules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入菜单名称',
      trigger: ['blur', 'input']
    },
    {
      min: 1,
      max: 500,
      message: '名称长度应在1-500个字符之间',
      trigger: ['blur']
    }
  ],
  code: [
    {
      required: true,
      validator: validateCode,
      trigger: ['blur', 'input']
    }
  ],
  type: [
    {
      required: true,
      message: '请选择菜单类型',
      trigger: ['blur', 'change']
    }
  ],
  icon: [
    {
      required: true,
      message: '请输入图标名称',
      trigger: ['blur', 'input']
    }
  ],
  url: [
    {
      required: true,
      message: '请输入菜单路径',
      trigger: ['blur', 'input']
    }
  ]
}

// 打开弹窗
const open = (menu?: MenuDetail | null, parent?: MenuDetail | null) => {
  visible.value = true

  if (menu) {
    // 编辑模式
    modalCategory.value = 'EDIT'
    menuDetailData.value = menu
    getMenuDetail(menu.id)
  } else {
    // 新增模式
    modalCategory.value = 'ADD'
    clearForm()

    if (parent) {
      // 添加子节点
      formDisplay.value.parentName = parent.nameList ? parent.nameList.join(' / ') : parent.name
      formData.value.parentId = parent.id
    } else {
      // 添加根节点
      formDisplay.value.parentName = null
      formData.value.parentId = null
    }
  }
}

// 关闭弹窗
const close = () => {
  visible.value = false
}

// 清空表单
const clearForm = () => {
  formData.value = {
    id: null,
    name: null,
    code: null,
    enabled: true,
    url: null,
    icon: null,
    type: 'NORMAL',
    parentId: null,
    seq: null,
    nameList: null,
  }
  formDisplay.value.parentName = null
}

// 重置表单
const resetForm = () => {
  clearForm()
  menuDetailData.value = null
  formRef.value?.restoreValidation()
}

// 获取菜单详情
const getMenuDetail = (menuId: string) => {
  loading.value = true
  apiGetMenuDetail(menuId).then((res) => {
    if (res.code === 200) {
      formData.value = res.data

      // 设置父节点名称
      if (res.data.nameList && res.data.nameList.length > 1) {
        formDisplay.value.parentName = res.data.nameList.slice(0, -1).join(' / ')
      } else {
        formDisplay.value.parentName = null
      }

      menuDetailData.value = res.data
    } else {
      notification.error({
        title: '获取菜单详情失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取菜单详情失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 显示图标预览
const showIconPreview = () => {
  if (!formData.value.icon) {
    message.warning('请先输入图标名称')
    return
  }
  message.info('图标预览已显示在下方')
}

// 取消
const handleCancel = () => {
  close()
}

// 提交
const handleSubmit = () => {
  formRef.value?.validate().then(() => {
    if (modalCategory.value === 'ADD') {
      doSubmitAdd()
    } else {
      doSubmitEdit()
    }
  })
}

// 新增提交
const doSubmitAdd = () => {
  loading.value = true
  const submitData = {
    ...formData.value,
    id: null
  }

  apiEditMenu(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '添加成功',
        content: '菜单已成功添加',
        duration: 3000
      })
      emit('success')
      close()
    } else {
      notification.error({
        title: '添加失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '添加失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 编辑提交
const doSubmitEdit = () => {
  loading.value = true
  const submitData = {
    ...formData.value,
    id: menuDetailData.value?.id
  }

  apiEditMenu(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '编辑成功',
        content: '菜单已成功更新',
        duration: 3000
      })
      emit('success')
      close()
    } else {
      notification.error({
        title: '编辑失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '编辑失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
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
    padding: 1.5rem;
  }

  .n-card__footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #f3f4f6;
    background: #fafafa;
  }
}

// 表单样式
:deep(.n-form) {
  .n-form-item {
    margin-bottom: 8px;

    &:last-child {
      margin-bottom: 0;
    }

    .n-form-item-label {
      font-weight: 500;
      color: #374151;
    }
  }
}

// 输入框样式
:deep(.n-input) {
  &:not(.n-input--disabled) {
    &:hover {
      border-color: #a78bfa;
    }

    &.n-input--focus {
      border-color: #8b5cf6;
      box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
    }
  }

  &.n-input--disabled {
    background-color: #f9fafb;

    .n-input__input-el {
      color: #6b7280;
    }
  }
}

// 选择器样式
:deep(.n-select) {
  .n-base-selection:hover {
    border-color: #a78bfa;
  }

  .n-base-selection--active {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  }
}

// 开关样式增强
:deep(.n-switch) {
  &.n-switch--active {
    .n-switch__rail {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
  }

  &:not(.n-switch--active) {
    .n-switch__rail {
      background: #e5e7eb;
    }
  }

  .n-switch__button {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
}

// 按钮样式
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

// 图标预览区域样式
.icon-preview {
  .preview-box {
    transition: all 0.2s ease;

    &:hover {
      transform: scale(1.05);
    }
  }
}
</style>