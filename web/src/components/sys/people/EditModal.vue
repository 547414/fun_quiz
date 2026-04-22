<template>
  <n-modal
      v-model:show="dialogVisible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      preset="card"
      :bordered="false"
      segmented
      :style="{ width: '700px', padding: '0'  }"
      :on-after-leave="resetForm"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <div
            class="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl flex items-center justify-center text-white shadow-md">
          <Icon :icon="modalCategory === 'ADD' ? 'fluent:person-add-20-filled' : 'fluent:edit-20-filled'"
                :width="20" :height="20"/>
        </div>
        <span class="text-lg font-semibold text-gray-800">{{ title }}</span>
      </div>
    </template>
    <div class="custom-form-modal-content" style="max-height: 660px;">
      <div class="custom-form-content">
        <n-spin :show="loading">
          <div class="modal-content">
            <div class="form-wrapper">
              <n-form
                  ref="formRef"
                  :model="form"
                  :rules="rules"
                  label-placement="left"
                  label-width="100px"
                  size="medium"
              >
                <n-form-item label="用户名" path="name">
                  <n-input
                      v-model:value="form.name"
                      placeholder="请输入用户名"
                      maxlength="50"
                      show-count
                  >
                    <template #prefix>
                      <Icon icon="fluent:person-20-regular" class="text-gray-400"/>
                    </template>
                  </n-input>
                </n-form-item>

                <n-form-item label="角色" path="roleCodeList" required>
                  <n-select
                      v-model:value="form.roleCodeList"
                      placeholder="请选择角色"
                      :options="roleOptions"
                      multiple
                      :disabled="userInfo?.unionUserUserId === userDetailData?.id && userDetailData !== null"
                  />
                </n-form-item>

                <n-form-item label="密码" path="password" v-if="modalCategory === 'ADD'">
                  <n-input
                      v-model:value="form.password"
                      type="password"
                      placeholder="请输入密码（8-16位，包含大小写字母和数字）"
                      show-password-on="click"
                  >
                    <template #prefix>
                      <Icon icon="fluent:lock-closed-20-regular" class="text-gray-400"/>
                    </template>
                  </n-input>
                </n-form-item>

                <n-form-item label="重复密码" path="passwordRepeat" v-if="modalCategory === 'ADD'">
                  <n-input
                      v-model:value="form.passwordRepeat"
                      type="password"
                      placeholder="请重复密码"
                      show-password-on="click"
                  >
                    <template #prefix>
                      <Icon icon="fluent:checkmark-lock-20-regular" class="text-gray-400"/>
                    </template>
                  </n-input>
                </n-form-item>

                <n-form-item label="手机号" path="mobile">
                  <n-input
                      v-model:value="form.mobile"
                      placeholder="请输入手机号"
                      maxlength="11"
                  >
                    <template #prefix>
                      <Icon icon="fluent:phone-20-regular" class="text-gray-400"/>
                    </template>
                  </n-input>
                </n-form-item>

                <n-form-item label="邮箱" path="email">
                  <n-input
                      v-model:value="form.email"
                      placeholder="请输入邮箱"
                  >
                    <template #prefix>
                      <Icon icon="fluent:mail-20-regular" class="text-gray-400"/>
                    </template>
                  </n-input>
                </n-form-item>

                <!-- 组织选择 -->
                <n-form-item label="所属组织" path="organizationList">
                  <div class="w-full">
                    <div class="flex items-center gap-2 mb-2">
                      <n-button
                          type="primary"
                          size="small"
                          @click="openOrganizationSelector"
                          :disabled="loading"
                      >
                        <template #icon>
                          <Icon icon="fluent:organization-20-regular"/>
                        </template>
                        选择组织
                      </n-button>
                      <span class="text-sm text-gray-500">
                        已选择 {{ selectedOrganizations.length }} 个组织
                      </span>
                    </div>

                    <div v-if="selectedOrganizations.length > 0" class="space-y-2 max-h-32 overflow-y-auto">
                      <div
                          v-for="org in selectedOrganizations"
                          :key="org.id"
                          class="flex items-center justify-between p-2 bg-gray-50 rounded-lg border"
                      >
                        <div class="flex items-center gap-2 flex-1 min-w-0">
                          <Icon icon="fluent:building-20-regular" class="text-purple-500 flex-shrink-0" :width="16"
                                :height="16"/>
                          <span class="text-sm text-gray-700 truncate">{{ org.name }}</span>
                        </div>
                        <n-button
                            size="tiny"
                            text
                            @click="removeOrganization(org.id)"
                            class="text-gray-400 hover:text-red-500"
                        >
                          <Icon icon="fluent:dismiss-12-regular" :width="12" :height="12"/>
                        </n-button>
                      </div>
                    </div>

                    <div v-else
                         class="text-center py-4 text-gray-500 text-sm bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
                      暂未选择任何组织
                    </div>
                  </div>
                </n-form-item>

                <!-- 部门选择 -->
                <n-form-item label="所属部门" path="deptList">
                  <div class="w-full">
                    <div class="flex items-center gap-2 mb-2">
                      <n-button
                          type="primary"
                          size="small"
                          @click="openDeptSelector"
                          :disabled="loading"
                      >
                        <template #icon>
                          <Icon icon="fluent:people-team-20-regular"/>
                        </template>
                        选择部门
                      </n-button>
                      <span class="text-sm text-gray-500">
                        已选择 {{ selectedDeptList.length }} 个部门
                      </span>
                    </div>

                    <div v-if="selectedDeptList.length > 0" class="space-y-2 max-h-32 overflow-y-auto">
                      <div
                          v-for="dept in selectedDeptList"
                          :key="dept.id"
                          class="flex items-center justify-between p-2 bg-blue-50 rounded-lg border"
                          style="min-height: 54px"
                      >
                        <div class="flex items-center gap-2 flex-1 min-w-0">
                          <Icon
                              icon="fluent:people-team-20-regular"
                              class="flex-shrink-0 text-blue-500"
                              :width="16"
                              :height="16"
                          />
                          <div class="flex-1 min-w-0">
                            <div class="text-sm text-gray-700 truncate">{{ dept.name }}</div>
                            <div v-if="dept.nameList && dept.nameList.length > 1"
                                 class="text-xs text-gray-500 truncate">
                              {{ dept.nameList.slice(0, -1).join(' > ') }}
                            </div>
                          </div>
                        </div>
                        <n-button
                            size="tiny"
                            text
                            @click="removeDept(dept.id)"
                            class="text-gray-400 hover:text-red-500"
                        >
                          <Icon icon="fluent:dismiss-12-regular" :width="12" :height="12"/>
                        </n-button>
                      </div>
                    </div>

                    <div v-else
                         class="text-center py-4 text-gray-500 text-sm bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
                      暂未选择任何部门
                    </div>
                  </div>
                </n-form-item>

                <n-form-item label="头像" path="avatarFileId">
                  <div class="avatar-container">
                    <!-- 头像上传/预览统一区域 -->
                    <div class="avatar-area">
                      <!-- 未上传状态 -->
                      <div v-if="!form.avatarFileInfo?.url" class="avatar-upload-zone">
                        <n-upload
                            :max="1"
                            :default-upload="false"
                            @before-upload="beforeAvatarUpload"
                            accept="image/png,image/jpeg"
                            :show-file-list="false"
                        >
                          <n-upload-dragger class="upload-custom">
                            <div class="upload-content">
                              <div class="upload-icon-container">
                                <Icon icon="fluent:image-add-20-regular" :width="32" :height="32"
                                      class="text-gray-400"/>
                              </div>
                              <span class="upload-text">点击或拖拽上传头像</span>
                              <span class="upload-hint">支持 JPG/PNG 格式，最大 10MB</span>
                            </div>
                          </n-upload-dragger>
                        </n-upload>
                      </div>

                      <!-- 已上传状态 -->
                      <div v-else class="avatar-preview-zone">
                        <div class="preview-content">
                          <div class="image-container" @mouseenter="showChangeBtn = true"
                               @mouseleave="showChangeBtn = false">
                            <n-image
                                :src="form.avatarFileInfo.url"
                                :width="200"
                                :height="200"
                                object-fit="cover"
                                class="preview-image"
                            />
                            <!-- 悬浮更换按钮 -->
                            <div v-show="showChangeBtn" class="hover-overlay" @click.stop="changeAvatar">
                              <div class="change-btn">
                                <Icon icon="material-symbols:close-rounded" style="font-size: 20px"/>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </n-form-item>

                <n-form-item label="可用状态" path="enabled">
                  <div class="flex items-center gap-4">
                    <n-switch
                        v-model:value="form.enabled"
                        :disabled="userInfo?.unionUserUserId === userDetailData?.id && userDetailData !== null"
                        size="medium"
                    >
                      <template #checked>
                        启用
                      </template>
                      <template #unchecked>
                        禁用
                      </template>
                    </n-switch>
                    <span class="text-sm text-gray-500">
                {{ form.enabled ? '账号可用后可正常登录使用' : '账号禁用后无法登录系统' }}
              </span>
                  </div>
                </n-form-item>
              </n-form>
            </div>
          </div>
        </n-spin>
      </div>
    </div>
    <template #footer>
      <div class="flex gap-3 justify-end">
        <n-button size="large" @click="dialogVisible = false">
          取消
        </n-button>
        <n-button type="primary" size="large" @click="checkFormData" :loading="loading">
          <template #icon>
            <Icon icon="fluent:save-20-regular"/>
          </template>
          {{ modalCategory === 'ADD' ? '创建人员' : '保存修改' }}
        </n-button>
      </div>
    </template>
  </n-modal>

  <!-- 组织选择弹窗 -->
  <OrganizationSelectModal
      ref="organizationSelectModalRef"
      @confirm="handleOrganizationConfirm"
  />

  <!-- 部门选择弹窗 -->
  <DeptSelectModal
      ref="deptSelectModalRef"
      @confirm="handleDeptConfirm"
  />
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NSwitch,
  NButton,
  NUpload,
  NUploadDragger,
  NImage,
  NSpin,
  useNotification,
  useDialog,
  type FormInst,
  type FormRules,
  type FormItemRule,
  type UploadFileInfo
} from 'naive-ui'
import {apiUploadFile, type UploadParams, type UploadResponse} from "@/api/storageApi.ts"
import {
  type AddWebUserParams,
  apiAddWebUser,
  apiEditWebUser,
  apiGetWebUserDetail,
  type EditWebUserParams, UserListInfo, UserListItemDept, UserListItemOrganization,
  type WebUserDetail,
  type WebUserDetailResponse
} from "@/api/webUserApi.ts"
import {getUserInfo} from "@/utils/userUtil.ts"
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts"
import OrganizationSelectModal from '@/components/sys/organization/SelectModal.vue'
import DeptSelectModal from '@/components/sys/dept/SelectModal.vue'

const modalCategory = ref('ADD')
const dialogVisible = ref(false)
const loading = ref(false)
const formRef = ref<FormInst | null>(null)
const title = ref('添加人员')
const notification = useNotification()
const dialog = useDialog()
const showChangeBtn = ref(false) // 控制更换按钮显示

// 弹窗引用
const organizationSelectModalRef = ref()
const deptSelectModalRef = ref()

// 选择的组织和部门
const selectedOrganizations = ref<UserListItemOrganization[]>([])
const selectedDeptList = ref<UserListItemDept[]>([])

const emit = defineEmits(['operateSuccess'])

const form = ref<AddWebUserParams>({
  name: '',
  roleCodeList: [],
  password: null,
  passwordRepeat: null,
  mobile: null,
  email: null,
  wxUserId: null,
  wecomUserUuid: null,
  unionUserUuid: null,
  avatarFileInfo: null,
  enabled: true,
  companyId: null,
  company: null,
  dept: null,
  position: null,
})

const userDetailData = ref<WebUserDetail>(null)

const roleOptions = ref([
  {label: '超级管理员', value: 'SUPER_ADMIN'},
  {label: '工会管理员', value: 'TRADE_UNION_ADMIN'},
  {label: '总管理员', value: 'TOTAL_ADMIN'},
  {label: '普通用户', value: 'WEB_USER'},
])

const userInfo = ref<UserListInfo>(getUserInfo())
if (userInfo.value.currentRoleCode === 'SUPER_ADMIN') {
  roleOptions.value = [
    {label: '超级管理员', value: 'SUPER_ADMIN'},
    {label: '工会管理员', value: 'TRADE_UNION_ADMIN'},
    {label: '总管理员', value: 'TOTAL_ADMIN'},
    {label: '普通用户', value: 'WEB_USER'},
  ]
} else if (userInfo.value.currentRoleCode === 'TOTAL_ADMIN') {
  roleOptions.value = [
    {label: '工会管理员', value: 'TRADE_UNION_ADMIN'},
    {label: '总管理员', value: 'TOTAL_ADMIN'},
    {label: '普通用户', value: 'WEB_USER'},
  ]
} else if (userInfo.value.currentRoleCode === 'TRADE_UNION_ADMIN') {
  roleOptions.value = [
    {label: '工会管理员', value: 'TRADE_UNION_ADMIN'},
    {label: '普通用户', value: 'WEB_USER'},
  ]
} else if (userInfo.value.currentRoleCode === 'WEB_USER') {
  roleOptions.value = [
    {label: '普通用户', value: 'WEB_USER'},
  ]
}

// 打开组织选择器
const openOrganizationSelector = () => {
  organizationSelectModalRef.value?.open(selectedOrganizations.value)
}

// 打开部门选择器
const openDeptSelector = () => {
  deptSelectModalRef.value?.open(selectedDeptList.value)
}

// 处理组织选择确认
const handleOrganizationConfirm = (organizations: UserListItemOrganization[]) => {
  selectedOrganizations.value = organizations
}

// 处理部门选择确认
const handleDeptConfirm = (deptList: UserListItemDept[]) => {
  selectedDeptList.value = deptList
}

// 移除组织
const removeOrganization = (orgId: string) => {
  selectedOrganizations.value = selectedOrganizations.value.filter(org => org.id !== orgId)
}

// 移除部门
const removeDept = (deptId: string) => {
  selectedDeptList.value = selectedDeptList.value.filter(dept => dept.id !== deptId)
}

const validatePasswordRepeat = (_rule: FormItemRule, value: string) => {
  if (value !== form.value.password) {
    return new Error('两次输入密码不一致')
  }
  return true
}

const rules: FormRules = {
  name: [
    {required: true, message: '请填写名称', trigger: 'blur'},
    {min: 1, max: 50, message: '最短1个字符，最长50个字符', trigger: 'blur'},
  ],
  roleCodeList: [
    {required: true, message: '请选择角色', trigger: 'change', type: 'array'},
  ],
  password: [
    {required: true, message: '请填写密码', trigger: 'blur'},
    {min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur'},
    {pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/, message: '密码必须包含大小写字母和数字', trigger: 'blur'},
  ],
  passwordRepeat: [
    {required: true, message: '请填写重复密码', trigger: 'blur'},
    {min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur'},
    {pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/, message: '密码必须包含大小写字母和数字', trigger: 'blur'},
    {validator: validatePasswordRepeat, trigger: 'blur'}
  ],
  mobile: [
    {pattern: /^1[3456789]\d{9}$/, message: '手机号格式不正确', trigger: 'blur'},
  ],
  email: [
    {type: 'email', message: '邮箱格式不正确', trigger: 'blur'},
  ],
}

const onSubmit = () => {
  dialog.warning({
    title: '确认提交',
    content: '是否确认提交当前信息？',
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      if (modalCategory.value === 'ADD') {
        doSubmitAdd()
      } else {
        doSubmitEdit()
      }
    }
  })
}

const checkFormData = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      onSubmit()
    }
  })
}

const doSubmitAdd = () => {
  loading.value = true

  // 准备提交数据，包含选择的组织和部门信息
  const submitData = {
    ...form.value,
    organizationList: selectedOrganizations.value,
    deptList: selectedDeptList.value
  }

  apiAddWebUser(submitData).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '添加人员成功',
        duration: 3000
      })
      dialogVisible.value = false
      emit('operateSuccess')
    } else {
      notification.error({
        title: '添加人员失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '添加人员失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

const doSubmitEdit = () => {
  loading.value = true

  // 准备提交数据，包含选择的组织和部门信息
  const editParams: EditWebUserParams = {
    id: userDetailData.value.id,
    ...form.value,
    organizationList: selectedOrganizations.value,
    deptList: selectedDeptList.value
  }

  apiEditWebUser(editParams).then((res) => {
    if (res.code === 200) {
      notification.success({
        title: '编辑人员成功',
        duration: 3000
      })
      dialogVisible.value = false
      emit('operateSuccess')
    } else {
      notification.error({
        title: '编辑人员失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '编辑人员失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

const openModal = (category: string, userId: string | null = null) => {
  modalCategory.value = category
  userDetailData.value = null
  title.value = category === 'ADD' ? '添加人员' : '编辑人员'
  if (category === 'ADD') {
    clearForm()
  }
  dialogVisible.value = true
  if (userId && category === 'EDIT') {
    getWebUserDetail(userId)
  }
}

const clearForm = () => {
  form.value = {
    name: '',
    roleCodeList: [],
    password: null,
    passwordRepeat: null,
    mobile: null,
    email: null,
    wxUserId: null,
    wecomUserUuid: null,
    unionUserUuid: null,
    avatarFileInfo: null,
    enabled: true,
    companyId: null,
    company: null,
    dept: null,
    position: null,
  }
  selectedOrganizations.value = []
  selectedDeptList.value = []
}

const resetForm = () => {
  clearForm()
  formRef.value?.restoreValidation()
}

const getWebUserDetail = (userId: string) => {
  loading.value = true
  apiGetWebUserDetail(userId).then((res: WebUserDetailResponse) => {
    if (res.code === 200) {
      form.value.avatarFileInfo = res.data.avatarFileInfo
      form.value.email = res.data.email
      form.value.mobile = res.data.mobile
      form.value.name = res.data.name
      form.value.roleCodeList = res.data.roleList.map(item => item.roleCode)
      form.value.enabled = res.data.enabled
      userDetailData.value = res.data

      // 如果有组织和部门信息，也要填充
      if (res.data.organizationList) {
        selectedOrganizations.value = res.data.organizationList
      }

      if (res.data.deptList) {
        selectedDeptList.value = res.data.deptList
      }
    } else {
      notification.error({
        title: '获取人员详情失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '获取人员详情失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

const beforeAvatarUpload = (data: {
  file: UploadFileInfo
  fileList: UploadFileInfo[]
}) => {
  const file = data.file.file!
  const typeList = ['image/jpeg', 'image/png']
  if (!typeList.includes(file.type!)) {
    notification.error({
      title: '上传失败',
      content: '头像图片只能是 JPG 或 PNG 格式!',
      duration: 3000
    })
    return false
  } else if (file.size! / 1024 / 1024 > 10) {
    notification.error({
      title: '上传失败',
      content: '头像图片大小不能超过 10MB!',
      duration: 3000
    })
    return false
  }
  uploadFile(file)
  return false
}

const uploadFile = (file: File) => {
  const params: UploadParams = {
    file: file,
    fileName: null,
    fileSize: null,
  }
  loading.value = true
  apiUploadFile(params).then((res: UploadResponse) => {
    if (res.code === 200) {
      form.value.avatarFileInfo = res.data
      notification.success({
        title: '上传成功',
        duration: 2000
      })
    } else {
      notification.error({
        title: '上传失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err: string) => {
    notification.error({
      title: '上传失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

// 更换头像
const changeAvatar = () => {
  form.value.avatarFileInfo = null
}

defineExpose({
  openModal,
})
</script>

<style scoped lang="scss">
.modal-content {
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

// 添加分割线样式
:deep(.n-card) {
  .n-card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb; // 头部分割线
  }

  .n-modal-card__content {
    padding: 0 !important;
    border-bottom: 1px solid #e5e7eb; // 中间和底部分割线
  }

  .n-card__footer {
    padding: 1rem 1.5rem;
    background: linear-gradient(to bottom, #fafafa, #f5f5f5);
  }
}

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
}

:deep(.n-select) {
  .n-base-selection {
    &:hover {
      border-color: #60a5fa;
    }

    &.n-base-selection--focus {
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
  }
}

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

:deep(.n-switch) {
  &.n-switch--active {
    .n-switch__rail {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
  }
}

.modal-content {
  padding: 0;
  height: auto;
  overflow-y: hidden;

  // 滚动条贴边
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;

    &:hover {
      background: #9ca3af;
    }
  }
}

.form-wrapper {
  padding: 16px 16px 16px 24px; // 左侧正常padding，右侧减少padding让滚动条贴边
}

// 头像容器统一大小
.avatar-container {
  width: 100%;
}

.avatar-area {
  width: 100%;
  min-height: 200px; // 固定最小高度，与图片高度一致
  display: flex;
  align-items: center;
  justify-content: flex-start; // 左对齐
}

// 上传区域样式
.avatar-upload-zone {
  width: 200px; // 与图片宽度一致
  height: 200px; // 与图片高度一致
  display: flex;
  align-items: center;
  justify-content: center;

  .upload-custom {
    width: 200px; // 与图片宽度一致
    height: 200px; // 与图片高度一致
    border: 2px dashed #e5e7eb;
    border-radius: 8px; // 与图片圆角一致
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover {
      border-color: #3b82f6;
      background: linear-gradient(to bottom, #f0f9ff, #e0f2fe);
    }
  }

  .upload-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 8px;
  }

  .upload-icon-container {
    width: 32px;
    height: 32px;
    background: #f3f4f6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
  }

  .upload-text {
    color: #4b5563;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 2px;
    line-height: 1.2;
  }

  .upload-hint {
    color: #9ca3af;
    font-size: 10px;
    line-height: 1.2;
  }
}

// 预览区域样式
.avatar-preview-zone {
  width: 200px; // 与上传区域宽度一致
  height: 200px; // 与上传区域高度一致
  display: flex;
  align-items: center;
  justify-content: center;

  .preview-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0; // 移除间距
  }

  .image-container {
    position: relative;
    display: inline-block;
    width: 200px;
    height: 200px;
    cursor: pointer;

    .preview-image {
      border-radius: 8px;
      border: 2px dashed #e5e7eb;
      transition: all 0.3s ease;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    // 悬浮遮罩层
    .hover-overlay {
      position: absolute;
      top: 0;
      right: 0;
      background: rgba(0, 0, 0, 0.5);
      border-radius: 0 8px 0 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
      cursor: pointer;
      width: 46px;
      height: 46px;

      .change-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        color: white;
        font-size: 20px;
        font-weight: 500;
        top: -1px;
        left: 5px;
        position: relative;

        &:hover {
          transform: scale(1.05);
        }
      }
    }

    &:hover .preview-image {
      border: 2px dashed rgba(59, 130, 246, 0.5);
    }
  }
}
</style>