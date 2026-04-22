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
      class="organization-edit-modal"
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
            <n-form-item label="上级组织" v-if="formDisplay.parentName">
              <n-input
                  :value="formDisplay.parentName"
                  disabled
                  placeholder="上级组织"
              />
            </n-form-item>

            <n-form-item label="组织名称" path="name">
              <n-input
                  v-model:value="formData.name"
                  placeholder="请输入组织名称"
                  clearable
                  maxlength="100"
                  show-count
              />
            </n-form-item>

            <n-form-item label="组织编码" path="code">
              <n-input
                  v-model:value="formData.code"
                  placeholder="请输入组织编码"
                  clearable
                  maxlength="50"
                  show-count
              />
            </n-form-item>

            <n-form-item label="组织类别" path="category">
              <n-select
                  v-model:value="formData.category"
                  placeholder="请选择组织类别"
                  :options="categoryOptions"
              />
            </n-form-item>

            <n-form-item label="组织地址" path="address">
              <n-input
                  v-model:value="formData.address"
                  type="textarea"
                  placeholder="请输入组织地址"
                  clearable
                  maxlength="500"
                  show-count
                  :autosize="{
                    minRows: 2,
                    maxRows: 4
                  }"
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
                  {{ formData.enabled ? '组织启用后将在系统中正常显示' : '组织禁用后将在系统中隐藏' }}
                </span>
              </div>
            </n-form-item>

            <!-- 组织信息预览 -->
            <n-form-item label="组织预览" v-if="formData.name || formData.code">
              <div class="w-full bg-gray-50 rounded-xl p-4">
                <div class="flex items-start gap-3">
                  <div
                      class="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon :icon="getOrgIcon()" :width="20" :height="20" class="text-white"/>
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-gray-800">
                      {{ formData.name || '未命名组织' }}
                    </div>
                    <div class="text-sm text-gray-500 mt-1">
                      <span v-if="formData.code">编码：{{ formData.code }}</span>
                      <span v-if="formData.code && formData.category" class="mx-2">·</span>
                      <span v-if="formData.category">{{ getCategoryLabel(formData.category) }}</span>
                    </div>
                    <div v-if="formData.address" class="text-sm text-gray-600 mt-2">
                      <Icon icon="fluent:location-16-regular" class="inline-block mr-1"/>
                      {{ formData.address }}
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
  apiEditOrganization,
  apiGetOrganizationDetail,
  type OrganizationDetail
} from '@/api/organizationApi.ts'
import {dialogMaskClosable, dialogDraggable} from "@/config/dialogConfig.ts"

const notification = useNotification()
const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 状态
const visible = ref(false)
const loading = ref(false)
const modalCategory = ref<'ADD' | 'EDIT'>('ADD')
const organizationDetailData = ref<OrganizationDetail | null>(null)

// 计算属性
const title = computed(() => modalCategory.value === 'ADD' ? '添加组织' : '编辑组织')

// 表单数据
const formData = ref<OrganizationDetail>({
  id: null,
  name: '',
  code: null,
  category: null,
  address: null,
  parentId: null,
  seq: 1,
  enabled: true,
  nameList: []
})

// 表单显示数据
const formDisplay = ref({
  parentName: null as string | null,
})

// 组织类别选项
const categoryOptions = ref([
  {value: 'COMPANY', label: '公司'},
  {value: 'OTHER', label: '其他'},
])

// 获取组织类别标签
const getCategoryLabel = (category: string | null) => {
  if (!category) return ''
  const option = categoryOptions.value.find(opt => opt.value === category)
  return option ? option.label : category
}

// 获取组织图标
const getOrgIcon = () => {
  switch (formData.value.category) {
    case 'COMPANY':
      return 'fluent:building-bank-20-filled'
    default:
      return 'fluent:building-20-filled'
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
      message: '请输入组织名称',
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
      message: '请选择组织类别',
      trigger: ['blur', 'change']
    }
  ],
  address: [
    {
      max: 500,
      message: '地址长度不能超过500个字符',
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
const open = (organization?: OrganizationDetail | null, parent?: OrganizationDetail | null) => {
  visible.value = true

  if (organization) {
    // 编辑模式
    modalCategory.value = 'EDIT'
    organizationDetailData.value = organization
    getOrganizationDetail(organization.id!)
  } else {
    // 新增模式
    modalCategory.value = 'ADD'
    clearForm()

    if (parent) {
      // 添加子组织
      formDisplay.value.parentName = parent.nameList ? parent.nameList.join(' / ') : parent.name
      formData.value.parentId = parent.id
    } else {
      // 添加根组织
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
    address: null,
    parentId: null,
    seq: 1,
    enabled: true,
    nameList: []
  }
  formDisplay.value.parentName = null
}

// 重置表单
const resetForm = () => {
  clearForm()
  organizationDetailData.value = null
  formRef.value?.restoreValidation()
}

// 获取组织详情
const getOrganizationDetail = (organizationId: string) => {
  loading.value = true
  apiGetOrganizationDetail(organizationId).then((res) => {
    if (res.code === 200) {
      formData.value = res.data

      // 设置父组织名称
      if (res.data.nameList && res.data.nameList.length > 1) {
        formDisplay.value.parentName = res.data.nameList.slice(0, -1).join(' / ')
      } else {
        formDisplay.value.parentName = null
      }

      organizationDetailData.value = res.data
    } else {
      notification.error({
        title: '获取组织详情失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取组织详情失败',
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
// 新增提交
const doSubmitAdd = () => {
  loading.value = true
  const submitData = {
    ...formData.value,
    id: null
  }

  apiEditOrganization(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '添加成功',
        content: '组织已成功添加',
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
    id: organizationDetailData.value?.id
  }

  apiEditOrganization(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '编辑成功',
        content: '组织已成功更新',
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
    border-color: #a78bfa;
  }

  .n-input.n-input--focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
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

// 组织预览区域样式
.organization-preview {
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