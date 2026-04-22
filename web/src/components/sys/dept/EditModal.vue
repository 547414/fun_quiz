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
      class="dept-edit-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center text-white shadow-md">
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
            <n-form-item label="上级部门" v-if="formDisplay.parentName">
              <n-input
                  :value="formDisplay.parentName"
                  disabled
                  placeholder="上级部门"
              />
            </n-form-item>

            <n-form-item label="部门名称" path="name">
              <n-input
                  v-model:value="formData.name"
                  placeholder="请输入部门名称"
                  clearable
                  maxlength="100"
                  show-count
              />
            </n-form-item>

            <n-form-item label="部门编码" path="code">
              <n-input
                  v-model:value="formData.code"
                  placeholder="请输入部门编码"
                  clearable
                  maxlength="50"
                  show-count
              />
            </n-form-item>

            <n-form-item label="部门类别" path="category">
              <n-select
                  v-model:value="formData.category"
                  placeholder="请选择部门类别"
                  :options="categoryOptions"
              />
            </n-form-item>

            <n-form-item label="部门简介" path="brief">
              <n-input
                  v-model:value="formData.brief"
                  type="textarea"
                  placeholder="请输入部门简介"
                  clearable
                  maxlength="500"
                  show-count
                  :autosize="{
                    minRows: 2,
                    maxRows: 4
                  }"
              />
            </n-form-item>

            <n-form-item label="来源类别" path="sourceCategory" v-if="showSourceFields">
              <n-select
                  v-model:value="formData.sourceCategory"
                  placeholder="请选择来源类别"
                  :options="sourceCategoryOptions"
                  clearable
              />
            </n-form-item>

            <n-form-item label="来源ID" path="sourceId" v-if="showSourceFields && formData.sourceCategory">
              <n-input
                  v-model:value="formData.sourceId"
                  placeholder="请输入来源ID"
                  clearable
                  maxlength="50"
                  show-count
              />
            </n-form-item>

            <n-form-item label="排序号" path="seq">
              <n-input-number
                  v-model:value="formData.seq"
                  placeholder="请输入排序号"
                  :min="1"
                  :max="9999"
                  clearable
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
                  {{ formData.enabled ? '部门启用后将在系统中正常显示' : '部门禁用后将在系统中隐藏' }}
                </span>
              </div>
            </n-form-item>

            <!-- 部门信息预览 -->
            <n-form-item label="部门预览" v-if="formData.name || formData.code">
              <div class="w-full bg-gray-50 rounded-xl p-4">
                <div class="flex items-start gap-3">
                  <div
                      class="w-10 h-10 bg-gradient-to-br from-blue-400 to-cyan-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon :icon="getDeptIcon()" :width="20" :height="20" class="text-white"/>
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-gray-800">
                      {{ formData.name || '未命名部门' }}
                    </div>
                    <div class="text-sm text-gray-500 mt-1">
                      <span v-if="formData.code">编码：{{ formData.code }}</span>
                      <span v-if="formData.code && formData.category" class="mx-2">·</span>
                      <span v-if="formData.category">{{ getCategoryLabel(formData.category) }}</span>
                    </div>
                    <div v-if="formData.brief" class="text-sm text-gray-600 mt-2">
                      <Icon icon="fluent:text-description-16-regular" class="inline-block mr-1"/>
                      {{ formData.brief }}
                    </div>
                    <div v-if="formData.sourceCategory" class="text-sm text-gray-500 mt-1">
                      <Icon icon="fluent:link-16-regular" class="inline-block mr-1"/>
                      来源：{{ getSourceCategoryLabel(formData.sourceCategory) }}
                      <span v-if="formData.sourceId">（{{ formData.sourceId }}）</span>
                    </div>
                  </div>
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
  NInputNumber,
  NSelect,
  NSwitch,
  NButton,
  NSpin,
  useNotification,
  type FormInst,
  type FormRules,
  type FormItemRule
} from 'naive-ui'
import {
  apiEditDept,
  apiGetDeptDetail,
  type DeptDetail,
  type DeptTreeDetail
} from '@/api/deptApi.ts'
import {dialogMaskClosable, dialogDraggable} from "@/config/dialogConfig.ts"

const notification = useNotification()
const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 状态
const visible = ref(false)
const loading = ref(false)
const modalCategory = ref<'ADD' | 'EDIT'>('ADD')
const deptDetailData = ref<DeptDetail | null>(null)
const showSourceFields = ref(false) // 控制是否显示来源字段

// 计算属性
const title = computed(() => modalCategory.value === 'ADD' ? '添加部门' : '编辑部门')

// 表单数据
const formData = ref<DeptDetail>({
  id: null,
  name: '',
  code: null,
  category: null,
  brief: null,
  parentId: null,
  sourceCategory: null,
  sourceId: null,
  nameList: [],
  seq: 1,
  enabled: true
})

// 表单显示数据
const formDisplay = ref({
  parentName: null as string | null,
})

// 部门类别选项
const categoryOptions = ref([
  {value: 'DEPARTMENT', label: '部门'},
  {value: 'OTHER', label: '其他'},
])

// 来源类别选项
const sourceCategoryOptions = ref([
  {value: 'SYSTEM', label: '系统'},
  {value: 'IMPORT', label: '导入'},
  {value: 'SYNC', label: '同步'},
  {value: 'MANUAL', label: '手动'},
])

// 获取部门类别标签
const getCategoryLabel = (category: string | null) => {
  if (!category) return ''
  const option = categoryOptions.value.find(opt => opt.value === category)
  return option ? option.label : category
}

// 获取来源类别标签
const getSourceCategoryLabel = (sourceCategory: string | null) => {
  if (!sourceCategory) return ''
  const option = sourceCategoryOptions.value.find(opt => opt.value === sourceCategory)
  return option ? option.label : sourceCategory
}

// 获取部门图标
const getDeptIcon = () => {
  switch (formData.value.category) {
    case 'COMPANY':
      return 'fluent:building-bank-20-filled'
    case 'DEPARTMENT':
      return 'fluent:people-team-20-filled'
    case 'TEAM':
      return 'fluent:people-20-filled'
    default:
      return 'fluent:folder-20-filled'
  }
}

// 表单验证规则
const validateCode = (_rule: FormItemRule, value: string) => {
  if (value && !/^[A-Za-z0-9_-]+$/.test(value)) {
    return new Error('编码只能包含字母、数字、下划线和中划线')
  }
  return true
}

const formRules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入部门名称',
      trigger: ['blur', 'input']
    },
    {
      min: 1,
      max: 100,
      message: '名称长度应在1-100个字符之间',
      trigger: ['blur']
    }
  ],
  code: [
    {
      validator: validateCode,
      trigger: ['blur', 'input']
    },
    {
      max: 50,
      message: '编码长度不能超过50个字符',
      trigger: ['blur']
    }
  ],
  category: [
    {
      required: true,
      message: '请选择部门类别',
      trigger: ['blur', 'change']
    }
  ],
  brief: [
    {
      max: 500,
      message: '简介长度不能超过500个字符',
      trigger: ['blur']
    }
  ],
  sourceId: [
    {
      max: 50,
      message: '来源ID长度不能超过50个字符',
      trigger: ['blur']
    }
  ],
  seq: [
    {
      type: 'number',
      required: true,
      message: '请输入排序号',
      trigger: ['blur', 'change']
    }
  ]
}

// 打开弹窗
const open = (dept?: DeptTreeDetail | null, parent?: DeptTreeDetail | null) => {
  visible.value = true
  showSourceFields.value = false // 默认不显示来源字段，可根据需要调整

  if (dept) {
    // 编辑模式
    modalCategory.value = 'EDIT'
    deptDetailData.value = dept as DeptDetail
    getDeptDetail(dept.id!)
  } else {
    // 新增模式
    modalCategory.value = 'ADD'
    clearForm()

    if (parent) {
      // 添加子部门
      formDisplay.value.parentName = parent.nameList ? parent.nameList.join(' / ') : parent.name
      formData.value.parentId = parent.id
    } else {
      // 添加根部门
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
    name: '',
    code: null,
    category: null,
    brief: null,
    parentId: null,
    sourceCategory: null,
    sourceId: null,
    nameList: [],
    seq: 1,
    enabled: true
  }
  formDisplay.value.parentName = null
}

// 重置表单
const resetForm = () => {
  clearForm()
  deptDetailData.value = null
  formRef.value?.restoreValidation()
}

// 获取部门详情
const getDeptDetail = (deptId: string) => {
  loading.value = true
  apiGetDeptDetail(deptId).then((res) => {
    if (res.code === 200) {
      formData.value = res.data

      // 设置父部门名称
      if (res.data.nameList && res.data.nameList.length > 1) {
        formDisplay.value.parentName = res.data.nameList.slice(0, -1).join(' / ')
      } else {
        formDisplay.value.parentName = null
      }

      // 如果有来源信息，显示来源字段
      if (res.data.sourceCategory || res.data.sourceId) {
        showSourceFields.value = true
      }

      deptDetailData.value = res.data
    } else {
      notification.error({
        title: '获取部门详情失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取部门详情失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
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

  apiEditDept(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '添加成功',
        content: '部门已成功添加',
        duration: 3000
      })
      // 传递保存的数据和操作类型
      emit('success', res.data || submitData, true, formData.value.parentId)
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
    id: deptDetailData.value?.id
  }

  apiEditDept(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '编辑成功',
        content: '部门已成功更新',
        duration: 3000
      })
      // 传递保存的数据和操作类型
      emit('success', res.data || submitData, false, null)
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
      border-color: #60a5fa;
    }

    &.n-input--focus {
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
  }

  &.n-input--disabled {
    background-color: #f9fafb;

    .n-input__input-el {
      color: #6b7280;
    }
  }
}

// 文本域样式
:deep(.n-input--textarea) {
  .n-input__textarea-el {
    scrollbar-width: thin;
    scrollbar-color: #d1d5db #f5f5f5;

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

// 数字输入框样式
:deep(.n-input-number) {
  .n-input:hover {
    border-color: #60a5fa;
  }

  .n-input.n-input--focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
}

// 选择器样式
:deep(.n-select) {
  .n-base-selection:hover {
    border-color: #60a5fa;
  }

  .n-base-selection--active {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
  }
}

// 部门预览区域样式
.dept-preview {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>