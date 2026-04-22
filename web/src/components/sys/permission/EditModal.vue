<template>
  <n-modal
      v-model:show="visible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :style="{ width: '900px' }"
      :bordered="false"
      segmented
      :on-after-leave="resetForm"
      class="permission-edit-modal"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon :icon="isEdit ? 'fluent:edit-20-filled' : 'fluent:add-circle-20-filled'" :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">{{ isEdit ? '编辑权限' : '新增权限' }}</span>
      </div>
    </template>
    <div class="custom-form-modal-content">
      <div class="custom-form-content">
        <n-spin :show="detailLoading">
          <n-form
              ref="formRef"
              :model="formData"
              :rules="formRules"
              label-placement="left"
              label-width="120px"
              class="py-4"
          >
            <n-form-item label="权限名称" path="name">
              <n-input
                  v-model:value="formData.name"
                  placeholder="请输入权限名称"
                  clearable
                  maxlength="50"
                  show-count
              />
            </n-form-item>

            <n-form-item label="权限编码" path="code">
              <n-input
                  v-model:value="formData.code"
                  placeholder="请输入权限编码"
                  clearable
                  maxlength="50"
                  show-count
              />
            </n-form-item>

            <n-form-item label="权限类型" path="resourceCategory">
              <n-select
                  v-model:value="formData.resourceCategory"
                  :options="categoryOptions"
                  placeholder="请选择权限类型"
                  :disabled="isEdit"
              />
            </n-form-item>

            <n-form-item label="关联资源" path="resourceId" v-if="formData.resourceCategory">
              <n-input
                  :value="resourceName"
                  placeholder="点击选择关联资源"
                  readonly
                  @click="openResourceSelectModal"
                  style="cursor: pointer"
              >
                <template #suffix>
                  <Icon icon="fluent:chevron-down-20-regular" class="text-gray-400"/>
                </template>
              </n-input>
            </n-form-item>

            <n-form-item label="授权配置" path="assignList">
              <div class="w-full">
                <!-- 授权列表 -->
                <div class="space-y-3 mb-4" v-if="formData.assignList && formData.assignList.length > 0">
                  <transition-group name="list" tag="div">
                    <div
                        v-for="(assign, idx) in formData.assignList"
                        :key="'assign-' + idx"
                        class="group relative bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                          <div :class="[
                        'w-10 h-10 rounded-lg flex items-center justify-center',
                        assign.policy === 'ALLOW' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                      ]">
                            <Icon
                                :icon="assign.policy === 'ALLOW' ? 'fluent:checkmark-circle-20-filled' : 'fluent:dismiss-circle-20-filled'"
                                :width="20"
                                :height="20"
                            />
                          </div>
                          <div>
                            <div class="font-medium text-gray-800">
                              {{
                                assign.policy === 'ALLOW' ? formatAllowAssignText(assign) : formatDenyAssignText(assign)
                              }}
                            </div>
                            <div class="text-sm text-gray-500 mt-1">
                          <span v-if="assign.startTime">
                            生效时间：{{ dayjs(assign.startTime).format('YYYY-MM-DD HH:mm') }}
                          </span>
                              <span v-if="assign.endTime" class="ml-3">
                            失效时间：{{ dayjs(assign.endTime).format('YYYY-MM-DD HH:mm') }}
                          </span>
                              <span v-if="!assign.endTime" class="ml-3 text-amber-600">永久有效</span>
                            </div>
                          </div>
                        </div>
                        <n-button
                            type="error"
                            text
                            size="small"
                            @click="removeAssign(idx)"
                            class="opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <template #icon>
                            <Icon icon="fluent:delete-20-regular"/>
                          </template>
                        </n-button>
                      </div>
                    </div>
                  </transition-group>
                </div>

                <!-- 空状态 -->
                <div v-else class="flex flex-col items-center justify-center py-8 bg-gray-50 rounded-lg mb-4">
                  <Icon icon="fluent:people-32-regular" class="text-gray-400 mb-2" :width="32" :height="32"/>
                  <p class="text-sm text-gray-500">暂未配置授权</p>
                </div>

                <!-- 添加授权按钮 -->
                <n-button type="primary" block @click="openAssignModal">
                  <template #icon>
                    <Icon icon="fluent:add-circle-20-regular"/>
                  </template>
                  添加授权配置
                </n-button>
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
                    formData.enabled ? '权限启用后可正常使用' : '权限禁用后无法生效'
                  }}</span>
              </div>
            </n-form-item>
          </n-form>

          <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <div class="flex items-start gap-2">
              <Icon icon="fluent:info-16-filled" class="text-amber-600 mt-0.5" :width="16" :height="16"/>
              <p class="text-sm text-amber-700">授权分配结束时间不选择则为永久授权</p>
            </div>
          </div>
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
          {{ isEdit ? '保存修改' : '创建权限' }}
        </n-button>
      </div>
    </template>
  </n-modal>

  <!-- 授权配置弹窗 -->
  <SelectAssignModal
      ref="selectAssignModalRef"
      @success="handleAssignSuccess"
  />

  <!-- 菜单选择弹窗 -->
  <MenuSelectModal
      ref="menuSelectModalRef"
      @selected="handleMenuSelected"
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
  NSwitch,
  NButton,
  NSelect,
  NSpin,
  useNotification,
  type FormInst,
  type FormRules
} from 'naive-ui'
import {
  apiEditPermission,
  apiGetPermissionDetail,
  type PermissionDetail,
  type PermissionAssign
} from '@/api/permissionApi.ts'
import {formatAllowAssignText, formatDenyAssignText} from '@/utils/format.ts'
import SelectAssignModal from '@/components/sys/permission/SelectAssignModal.vue'
import MenuSelectModal from '@/components/sys/menu/SelectModal.vue'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts"
import dayjs from 'dayjs'
import type {MenuDetail} from '@/api/menuApi.ts'
import type {BackendApiDetail} from '@/api/backendApiApi.ts'

const notification = useNotification()
const emit = defineEmits(['success'])

// 表单引用
const formRef = ref<FormInst | null>(null)

// 弹窗引用
const selectAssignModalRef = ref()
const menuSelectModalRef = ref()
const backendApiSelectModalRef = ref()

// 状态
const visible = ref(false)
const loading = ref(false)
const detailLoading = ref(false)
const isEdit = ref(false)
const editingId = ref<string>('')

// 表单数据
const formData = ref<PermissionDetail>({
  id: null,
  name: null,
  code: null,
  resourceCategory: 'MENU',
  resourceId: null,
  enabled: true,
  assignList: [],
  assignNameList: [],
  ignoreAuth: null,
})

// 资源名称
const resourceName = ref<string>('')

// 类别选项
const categoryOptions = [
  {label: '菜单节点', value: 'MENU'},
  {label: '后端接口', value: 'BACKEND_API'}
]

// 表单验证规则
const formRules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入权限名称',
      trigger: ['blur', 'input']
    },
    {
      min: 1,
      max: 50,
      message: '权限名称长度应在1-50个字符之间',
      trigger: ['blur']
    }
  ],
  code: [
    {
      required: true,
      message: '请输入权限编码',
      trigger: ['blur', 'input']
    },
    {
      min: 1,
      max: 50,
      message: '权限编码长度应在1-50个字符之间',
      trigger: ['blur']
    }
  ],
  resourceCategory: [
    {
      required: true,
      message: '请选择权限类型',
      trigger: 'change'
    }
  ],
  resourceId: [
    {
      required: true,
      message: '请选择关联资源',
      trigger: 'change'
    }
  ]
}

// 打开弹窗
const open = (permissionId?: string) => {
  visible.value = true
  if (permissionId) {
    isEdit.value = true
    editingId.value = permissionId
    getPermissionDetail(permissionId)
  } else {
    isEdit.value = false
    editingId.value = ''
    resetForm()
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
    resourceCategory: 'MENU',
    resourceId: null,
    enabled: true,
    assignList: [],
    assignNameList: [],
    ignoreAuth: null,
  }
  resourceName.value = ''
  formRef.value?.restoreValidation()
}

// 获取权限详情
const getPermissionDetail = (permissionId: string) => {
  detailLoading.value = true
  apiGetPermissionDetail(permissionId).then((res) => {
    if (res.code === 200) {
      formData.value = res.data
      // 设置资源名称
      if (res.data.resourceCategory === 'MENU' && res.data.resourceId) {
        resourceName.value = '菜单资源'
      } else if (res.data.resourceCategory === 'BACKEND_API' && res.data.resourceId) {
        resourceName.value = '接口资源'
      }
    } else {
      notification.error({
        title: '获取权限详情失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    notification.error({
      title: '获取权限详情失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    detailLoading.value = false
  })
}

// 打开资源选择弹窗
const openResourceSelectModal = () => {
  if (formData.value.resourceCategory === 'MENU') {
    menuSelectModalRef.value?.open()
  } else if (formData.value.resourceCategory === 'BACKEND_API') {
    backendApiSelectModalRef.value?.open()
  }
}

// 打开授权配置弹窗
const openAssignModal = () => {
  selectAssignModalRef.value?.open()
}

// 移除授权
const removeAssign = (index: number) => {
  formData.value.assignList?.splice(index, 1)
}

// 授权配置成功回调
const handleAssignSuccess = (assign: PermissionAssign) => {
  if (!formData.value.assignList) {
    formData.value.assignList = []
  }
  const newAssign = {
    ...assign
  }
  newAssign.grantType = formData.value.resourceCategory
  newAssign.grantObjectId = formData.value.resourceId
  newAssign.permissionId = formData.value.id
  formData.value.assignList.push(newAssign)
}

// 菜单选择回调
const handleMenuSelected = (menu: MenuDetail) => {
  formData.value.resourceId = menu.id
  resourceName.value = menu.name
}

// 后端接口选择回调
// @ts-ignore
const handleBackendApiSelected = (api: BackendApiDetail) => {
  formData.value.resourceId = api.id
  resourceName.value = api.url
}

// 取消
const handleCancel = () => {
  close()
}

// 提交
const handleSubmit = () => {
  formRef.value?.validate().then(() => {
    editPermission()
  })
}

const editPermission = () => {
  loading.value = true
  apiEditPermission(formData.value).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '操作成功',
        content: isEdit.value ? '权限信息已更新' : '权限已创建',
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
    max-height: 600px;
    overflow-y: auto;
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
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    border: none;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    }
  }
}

// 列表动画
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-move {
  transition: transform 0.3s ease;
}
</style>