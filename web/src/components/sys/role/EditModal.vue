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
      class="role-edit-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon :icon="isEdit ? 'fluent:edit-20-filled' : 'fluent:add-circle-20-filled'" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">{{ isEdit ? '编辑角色' : '新增角色' }}</span>
      </div>
    </template>
    <div class="custom-form-modal-content">
      <div class="custom-form-content">
        <n-form
            ref="formRef"
            :model="formData"
            :rules="formRules"
            label-placement="left"
            label-width="100px"
            class="py-4"
        >
          <n-form-item label="角色名称" path="name">
            <n-input
                v-model:value="formData.name"
                placeholder="请输入角色名称"
                clearable
                maxlength="50"
                show-count
            />
          </n-form-item>

          <n-form-item label="角色编码" path="code">
            <n-input
                v-model:value="formData.code"
                placeholder="请输入角色编码（如：ADMIN）"
                :disabled="isEdit"
                clearable
                maxlength="30"
                show-count
            />
          </n-form-item>

          <n-form-item label="角色描述" path="brief">
            <n-input
                v-model:value="formData.brief"
                type="textarea"
                placeholder="请输入角色描述信息"
                :rows="4"
                maxlength="200"
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
              <span class="text-sm text-gray-500">{{
                  formData.enabled ? '角色启用后可正常使用' : '角色禁用后无法分配给用户'
                }}</span>
            </div>
          </n-form-item>

          <!-- 权限预览（可选） -->
          <n-form-item label="权限预览" v-if="isEdit">
            <div class="w-full p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-medium text-gray-700">已分配权限</span>
                <n-button type="info" :secondary="true" size="small" round>
                  <template #icon>
                    <Icon icon="fluent:settings-20-regular"/>
                  </template>
                  配置权限
                </n-button>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div v-for="permission in mockPermissions" :key="permission"
                     class="flex items-center gap-2 text-sm text-gray-600">
                  <Icon icon="fluent:checkmark-circle-16-filled" class="text-green-500"/>
                  {{ permission }}
                </div>
              </div>
            </div>
          </n-form-item>
        </n-form>
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
          {{ isEdit ? '保存修改' : '创建角色' }}
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSwitch,
  NButton,
  useNotification,
  type FormInst,
  type FormRules,
  type FormItemRule
} from 'naive-ui'
import {apiEditRole, RoleDetail} from '@/api/roleApi.ts'
import {dialogMaskClosable, dialogDraggable} from "@/config/dialogConfig.ts";

const notification = useNotification()
const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 状态
const visible = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const editingId = ref<string>('')

// 表单数据
const formData = ref<RoleDetail>({
  id: null,
  name: null,
  code: null,
  brief: null,
  enabled: true,
  createdAt: null,
  updatedAt: null,
})

// 模拟权限数据
const mockPermissions = ref([
  '用户管理',
  '角色管理',
  '菜单管理',
  '部门管理',
  '工单查看',
  '工单创建'
])

// 表单验证规则
const validateCode = (_rule: FormItemRule, value: string) => {
  if (!value) {
    return new Error('请输入角色编码')
  } else if (!/^[A-Z_]+$/.test(value)) {
    return new Error('角色编码只能包含大写字母和下划线')
  }
  return true
}

const formRules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入角色名称',
      trigger: ['blur', 'input']
    },
    {
      min: 2,
      max: 50,
      message: '角色名称长度应在2-50个字符之间',
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
  brief: [
    {
      max: 500,
      message: '描述长度不能超过500个字符',
      trigger: ['blur']
    }
  ]
}

// 打开弹窗
const open = (role?: RoleDetail) => {
  visible.value = true
  if (role) {
    isEdit.value = true
    editingId.value = role.id
    formData.value = role
  } else {
    isEdit.value = false
    editingId.value = null
  }
}

// 关闭弹窗
const close = () => {
  visible.value = false
}

// 重置表单
const resetForm = () => {
  formData.value = {
    id: null,
    name: null,
    code: null,
    brief: null,
    enabled: true,
    createdAt: null,
    updatedAt: null
  }
  formRef.value?.restoreValidation()
}

// 取消
const handleCancel = () => {
  close()
}

// 提交
const handleSubmit = () => {
  formRef.value?.validate().then(() => {
    editRole()
  })
}

const editRole = () => {
  loading.value = true
  apiEditRole(formData.value).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: isEdit.value ? '角色信息已更新' : '角色已创建',
        duration: 3000
      })
      resetForm()
      emit('success')
      close()
    } else {
      notification.error({
        title: '操作失败',
        content: res.message || '请稍后重试'
      })
    }
  }).catch((error) => {
    notification.error({
      title: '操作失败',
      content: error.message
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
    resize: none;
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

// 权限预览区域
.permission-preview {
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  border: 1px solid #e5e7eb;
}
</style>