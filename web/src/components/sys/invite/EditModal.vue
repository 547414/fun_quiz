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
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon :icon="isEdit ? 'fluent:edit-20-filled' : 'fluent:add-circle-20-filled'" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">{{ isEdit ? '编辑邀请码' : '新增邀请码' }}</span>
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
          <n-form-item label="邀请码" path="code" v-if="isEdit">
            <n-input
                v-model:value="formData.code"
                placeholder="邀请码"
                disabled
                class="font-mono"
            >
              <template #prefix>
                <Icon icon="fluent:key-20-regular" class="text-gray-400"/>
              </template>
            </n-input>
          </n-form-item>

          <n-form-item label="备注" path="brief">
            <n-input
                v-model:value="formData.brief"
                type="textarea"
                placeholder="请输入备注信息，方便识别邀请码用途"
                :rows="3"
                maxlength="500"
                show-count
            />
          </n-form-item>

          <n-form-item label="注册数量" path="maxLimit">
            <div class="w-full space-y-3">
              <div class="flex items-center gap-4">
                <n-input-number
                    v-model:value="formData.maxLimit"
                    :min="0"
                    :max="100"
                    :disabled="unlimitedRegistration"
                    placeholder="最大注册数量"
                    :style="{ width: '200px' }"
                >
                  <template #suffix>
                    <span class="text-gray-500">人</span>
                  </template>
                </n-input-number>
                <n-checkbox
                    v-model:checked="unlimitedRegistration"
                    @update:checked="handleUnlimitedChange"
                >
                  无限制
                </n-checkbox>
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-500" v-if="isEdit && formData.registerNum > 0">
                <Icon icon="fluent:info-16-regular"/>
                <span>已使用：{{ formData.registerNum }} 人</span>
              </div>
            </div>
          </n-form-item>

          <n-form-item label="有效期" path="deadline">
            <div class="w-full space-y-3">
              <n-date-picker
                  v-model:value="deadlineTimestamp"
                  type="date"
                  placeholder="选择有效期"
                  :is-date-disabled="dateDisabled"
                  clearable
                  :style="{ width: '100%' }"
              />
              <div class="flex items-center gap-2">
                <n-button
                    v-for="quick in quickDeadlines"
                    :key="quick.label"
                    size="small"
                    quaternary
                    @click="setQuickDeadline(quick.days)"
                >
                  {{ quick.label }}
                </n-button>
              </div>
            </div>
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
                  formData.enabled ? '邀请码启用后可正常使用' : '邀请码禁用后无法用于注册'
                }}</span>
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
          {{ isEdit ? '保存修改' : '创建邀请码' }}
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue'
import {Icon} from '@iconify/vue'
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NSwitch,
  NButton,
  NDatePicker,
  NCheckbox,
  useNotification,
  type FormInst,
  type FormRules,
  type FormItemRule
} from 'naive-ui'
import {
  apiEditInviteCode,
  apiGetInviteCodeDetail,
  type EditInviteCodeParams,
  type InviteCodeDetailResponse
} from '@/api/inviteCodeApiApi.ts'
import {dialogMaskClosable, dialogDraggable} from "@/config/dialogConfig.ts";
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import duration from 'dayjs/plugin/duration';

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(duration);

const notification = useNotification()
const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 状态
const visible = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const editingId = ref<string>('')
const unlimitedRegistration = ref(false)

// 表单数据
const formData = ref<EditInviteCodeParams>({
  id: null,
  code: null,
  brief: null,
  deadline: null,
  deleted: false,
  maxLimit: 20,
  enabled: true,
  registerNum: 0
})

// 有效期时间戳（用于日期选择器）
const deadlineTimestamp = ref<number | null>(null)

// 快速选择有效期
const quickDeadlines = [
  {label: '7天', days: 7},
  {label: '30天', days: 30},
  {label: '90天', days: 90},
  {label: '半年', days: 180},
  {label: '一年', days: 365}
]

// 监听有效期时间戳变化
watch(deadlineTimestamp, (newVal) => {
  if (newVal) {
    formData.value.deadline = new Date(dayjs(newVal).format('YYYY-MM-DD'))
  } else {
    formData.value.deadline = null
  }
})

// 表单验证规则
const validateDeadline = (_rule: FormItemRule, value: string) => {
  if (!value) {
    return new Error('请选择有效期')
  }
  const selectedDate = dayjs(value)
  if (selectedDate.isBefore(dayjs(), 'day')) {
    return new Error('有效期不能早于今天')
  }
  return true
}

const formRules: FormRules = {
  brief: [
    {
      max: 500,
      message: '备注长度不能超过500个字符',
      trigger: ['blur']
    }
  ],
  maxLimit: [
    {
      required: true,
      type: 'number',
      message: '请设置最大注册数量',
      trigger: ['blur', 'change']
    }
  ],
  deadline: [
    {
      required: true,
      validator: validateDeadline,
      trigger: ['blur', 'change']
    }
  ],
  enabled: [
    {
      required: true,
      type: 'boolean',
      message: '请选择是否启用',
      trigger: ['blur', 'change']
    }
  ]
}

// 处理无限制复选框
const handleUnlimitedChange = (checked: boolean) => {
  if (checked) {
    formData.value.maxLimit = 0
  } else {
    formData.value.maxLimit = 20
  }
}

// 设置快速有效期
const setQuickDeadline = (days: number) => {
  const deadline = dayjs().add(days, 'day')
  deadlineTimestamp.value = deadline.valueOf()
}

// 禁用过去的日期
const dateDisabled = (ts: number) => {
  return dayjs(ts).isBefore(dayjs(), 'day')
}

// 打开弹窗
const open = (inviteCode?: EditInviteCodeParams) => {
  visible.value = true
  if (inviteCode) {
    isEdit.value = true
    editingId.value = inviteCode.id
    getDetailData(inviteCode.id)
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
    code: null,
    brief: null,
    deadline: null,
    deleted: false,
    maxLimit: 20,
    enabled: true,
    registerNum: 0
  }
  deadlineTimestamp.value = null
  unlimitedRegistration.value = false
  formRef.value?.restoreValidation()
}

// 获取详情数据
const getDetailData = (dataId: string) => {
  loading.value = true
  apiGetInviteCodeDetail(dataId).then((res: InviteCodeDetailResponse) => {
    if (res.code === 200) {
      formData.value = res.data
      // 设置有效期时间戳
      if (res.data.deadline) {
        deadlineTimestamp.value = dayjs(res.data.deadline).valueOf()
      }
      // 设置无限制复选框
      unlimitedRegistration.value = res.data.maxLimit === 0
    } else {
      notification.error({
        title: '获取邀请码详情失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '获取邀请码详情失败',
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
    doSubmit()
  })
}

const doSubmit = () => {
  loading.value = true
  const submitData = {...formData.value}

  // 新增时设置生成的邀请码
  if (!isEdit.value) {
    submitData.id = null
  }

  apiEditInviteCode(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: isEdit.value ? '邀请码信息已更新' : '邀请码已创建',
        duration: 3000
      })
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
    resize: none;
  }
}

// 数字输入框样式
:deep(.n-input-number) {
  &.n-input-number--focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
}

// 日期选择器样式
:deep(.n-date-picker) {
  width: 100%;

  .n-input {
    &.n-input--focus {
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
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
    background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
    border: none;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
    }
  }
}

// 复选框样式
:deep(.n-checkbox) {
  .n-checkbox-box {
    &.n-checkbox-box--checked {
      background-color: #3b82f6;
      border-color: #3b82f6;
    }
  }
}

// 预览区域
.code-preview {
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  border: 1px solid #e5e7eb;
}
</style>