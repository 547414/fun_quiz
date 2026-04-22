<template>
  <n-modal
      v-model:show="visible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :style="{ width: '700px' }"
      :bordered="false"
      segmented
      :on-after-leave="resetForm"
      class="assign-select-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon icon="fluent:people-add-20-filled" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">授权配置</span>
      </div>
    </template>
    <div class="custom-form-modal-content">
      <div class="custom-form-content">
        <n-form
            ref="formRef"
            :model="formData"
            :rules="formRules"
            label-placement="left"
            label-width="120px"
            class="py-4"
        >
          <n-form-item label="被授权对象" path="granteeObjectId">
            <n-input-group>
              <n-input
                  :value="formData.granteeObjectName"
                  placeholder="点击选择角色"
                  readonly
                  @click="openRoleSelectModal"
                  style="cursor: pointer"
              >
                <template #prefix>
                  <Icon icon="fluent:people-team-20-regular" class="text-gray-400"/>
                </template>
              </n-input>
              <n-button type="primary" @click="openRoleSelectModal">
                选择角色
              </n-button>
            </n-input-group>
          </n-form-item>

          <n-form-item label="生效时间" path="startTime">
            <n-date-picker
                v-model:value="formData.startTime"
                type="datetime"
                placeholder="请选择授权生效时间"
                clearable
                style="width: 100%"
                :default-time="defaultTime"
            />
          </n-form-item>

          <n-form-item label="失效时间" path="endTime">
            <n-date-picker
                v-model:value="formData.endTime"
                type="datetime"
                placeholder="请选择授权失效时间（不选则永久有效）"
                clearable
                style="width: 100%"
                :is-date-disabled="dateDisabled"
            />
          </n-form-item>

          <n-form-item label="授权策略" path="policy">
            <n-radio-group v-model:value="formData.policy" size="medium">
              <n-space>
                <n-radio-button value="ALLOW" class="allow-radio">
                  <div class="flex items-center gap-2">
                    <Icon icon="fluent:checkmark-circle-20-filled" class="text-green-600"/>
                    <span>允许</span>
                  </div>
                </n-radio-button>
                <n-radio-button value="DENY" class="deny-radio">
                  <div class="flex items-center gap-2">
                    <Icon icon="fluent:dismiss-circle-20-filled" class="text-red-600"/>
                    <span>拒绝</span>
                  </div>
                </n-radio-button>
              </n-space>
            </n-radio-group>
          </n-form-item>
        </n-form>
      </div>
      <!-- 授权说明 -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div class="flex items-start gap-3">
          <Icon icon="fluent:info-16-filled" class="text-blue-600 mt-0.5" :width="16" :height="16"/>
          <div class="text-sm text-blue-700 space-y-1">
            <p>• 允许策略：授予角色访问该权限的能力</p>
            <p>• 拒绝策略：明确禁止角色访问该权限（优先级高于允许）</p>
            <p>• 不设置失效时间则表示永久授权</p>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex gap-3 justify-end">
        <n-button size="large" @click="handleCancel">
          取消
        </n-button>
        <n-button type="primary" size="large" @click="handleSubmit" :loading="loading">
          <template #icon>
            <Icon icon="fluent:checkmark-20-regular"/>
          </template>
          确认配置
        </n-button>
      </div>
    </template>
  </n-modal>

  <!-- 角色选择弹窗 -->
  <RoleSelectModal
      ref="roleSelectModalRef"
      @selected="handleRoleSelected"
  />
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputGroup,
  NButton,
  NRadioGroup,
  NRadioButton,
  NSpace,
  NDatePicker,
  type FormInst,
  type FormRules
} from 'naive-ui'
import {type PermissionAssign} from '@/api/permissionApi.ts'
import RoleSelectModal from '@/components/sys/role/SelectModal.vue'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts"
import type {RoleDetail} from '@/api/roleApi.ts'

const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 弹窗引用
const roleSelectModalRef = ref()

// 状态
const visible = ref(false)
const loading = ref(false)

// 默认时间
const defaultTime = "00:00:00"

// 修改接口类型，使用时间戳
interface FormData extends Omit<PermissionAssign, 'startTime' | 'endTime'> {
  startTime: number | null
  endTime: number | null
}

// 表单数据 - 使用时间戳
const formData = ref<FormData>({
  id: null,
  grantType: 'MENU',
  grantObjectId: null,
  granteeType: 'ROLE',
  granteeObjectId: null,
  grantObjectName: null,
  granteeObjectName: null,
  granteeObjectCode: null,
  permissionId: null,
  startTime: Date.now(), // 使用时间戳
  endTime: null,
  policy: 'ALLOW',
  ignoreAuth: null,
})

// 表单验证规则
const formRules: FormRules = {
  granteeObjectId: [
    {
      required: true,
      message: '请选择被授权的角色',
      trigger: 'change'
    }
  ],
  startTime: [
    {
      required: true,
      message: '请选择授权生效时间',
      trigger: ['change', 'blur'],
      validator: (_rule, value) => {
        if (!value) {
          return new Error('请选择授权生效时间')
        }
        return true
      }
    }
  ],
  policy: [
    {
      required: true,
      message: '请选择授权策略',
      trigger: 'change'
    }
  ]
}

// 禁用日期函数
const dateDisabled = (timestamp: number) => {
  // 如果有开始时间，结束时间不能早于开始时间
  if (formData.value.startTime) {
    return timestamp < formData.value.startTime
  }
  return false
}

// 打开弹窗
const open = () => {
  visible.value = true
  resetForm()
}

// 关闭弹窗
const close = () => {
  visible.value = false
}

// 重置表单
const resetForm = () => {
  formData.value = {
    id: null,
    grantType: 'MENU',
    grantObjectId: null,
    granteeType: 'ROLE',
    granteeObjectId: null,
    grantObjectName: null,
    granteeObjectName: null,
    granteeObjectCode: null,
    permissionId: null,
    startTime: Date.now(), // 使用时间戳
    endTime: null,
    policy: 'ALLOW',
    ignoreAuth: null,
  }
  formRef.value?.restoreValidation()
}

// 打开角色选择弹窗
const openRoleSelectModal = () => {
  roleSelectModalRef.value?.open()
}

// 角色选择回调
const handleRoleSelected = (role: RoleDetail) => {
  formData.value.granteeObjectId = role.id
  formData.value.granteeObjectName = role.name
  formData.value.granteeObjectCode = role.code
}

// 取消
const handleCancel = () => {
  close()
}

// 提交
const handleSubmit = () => {
  formRef.value?.validate().then(() => {
    // 提交时转换数据格式
    const submitData: PermissionAssign = {
      ...formData.value,
      startTime: formData.value.startTime ? new Date(formData.value.startTime) : null,
      endTime: formData.value.endTime ? new Date(formData.value.endTime) : null,
    }
    emit('success', submitData)
    close()
  }).catch(err => {
    console.error('表单验证失败:', err)
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
}

// 单选按钮样式
:deep(.n-radio-button) {
  &.allow-radio {
    &.n-radio-button--checked {
      background: linear-gradient(135deg, #acecd6 0%, #93dfc8 100%);
      border-color: #059669;
    }
  }

  &.deny-radio {
    &.n-radio-button--checked {
      background: linear-gradient(135deg, #f3adad 0%, #efa6a6 100%);
      border-color: #dc2626;
    }
  }

  &.n-button--primary-type {
    border: none;
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

.n-time-picker-panel {
  .n-button {
    background-color: #93dfc8 !important;
  }
}
</style>