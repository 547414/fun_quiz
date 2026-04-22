<template>
  <n-modal
      v-model:show="dialogVisible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      :closable="false"
      preset="card"
      class="policy-modal"
      :style="{ maxWidth: '800px', maxHeight: '90vh' }"
  >
    <template #header>
      <div class="flex items-center">
        <Icon icon="fluent:shield-lock-20-filled" class="text-indigo-500 text-xl mr-2"/>
        <span class="text-lg font-semibold text-gray-800">隐私政策</span>
        <n-button
            text
            class="ml-auto -mr-2"
            @click="closeModal"
        >
          <Icon
              icon="fluent:dismiss-circle-20-regular"
              class="text-xl text-gray-400 hover:text-gray-600 transition-colors"
          />
        </n-button>
      </div>
    </template>

    <div class="policy-content">
      <div class="update-info flex items-center mb-6 p-3 bg-gray-50 rounded-lg">
        <Icon icon="fluent:calendar-20-regular" class="mr-2 text-gray-600"/>
        <span class="text-sm text-gray-600">更新日期：2024年1月1日 | 生效日期：2024年1月1日</span>
      </div>

      <div class="space-y-6">
        <!-- 引言 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:info-20-filled" class="mr-2 text-indigo-500"/>
            引言
          </h3>
          <p class="text-gray-600 leading-relaxed">
            欢迎使用玄测后台管理系统。我们深知个人信息对您的重要性，并会尽全力保护您的个人信息安全可靠。我们致力于维持您对我们的信任，恪守权责一致、目的明确、选择同意、最小必要、确保安全、主体参与、公开透明等原则。
          </p>
        </section>

        <!-- 信息收集 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:database-20-filled" class="mr-2 text-indigo-500"/>
            我们收集的信息
          </h3>
          <div class="space-y-3">
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:person-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">账户信息：</span>
                <span class="text-gray-600">用户名、密码、邮箱地址等注册信息</span>
              </div>
            </div>
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:ticket-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">工单信息：</span>
                <span class="text-gray-600">创建的工单内容、状态、处理记录</span>
              </div>
            </div>
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:history-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">使用记录：</span>
                <span class="text-gray-600">登录时间、操作记录、访问日志</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 信息使用 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:target-20-filled" class="mr-2 text-indigo-500"/>
            信息使用目的
          </h3>
          <div class="grid grid-cols-2 gap-3">
            <div class="p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg text-center">
              <Icon icon="fluent:service-bell-20-filled" class="text-2xl text-indigo-600 mb-2"/>
              <p class="font-medium text-gray-800">提供服务</p>
            </div>
            <div class="p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg text-center">
              <Icon icon="fluent:shield-20-filled" class="text-2xl text-indigo-600 mb-2"/>
              <p class="font-medium text-gray-800">安全保障</p>
            </div>
            <div class="p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg text-center">
              <Icon icon="fluent:star-20-filled" class="text-2xl text-indigo-600 mb-2"/>
              <p class="font-medium text-gray-800">改善体验</p>
            </div>
            <div class="p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg text-center">
              <Icon icon="fluent:mail-20-filled" class="text-2xl text-indigo-600 mb-2"/>
              <p class="font-medium text-gray-800">服务通知</p>
            </div>
          </div>
        </section>

        <!-- 信息保护 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:lock-closed-20-filled" class="mr-2 text-indigo-500"/>
            信息保护措施
          </h3>
          <div class="grid grid-cols-2 gap-3">
            <div class="flex items-center p-3 border border-gray-200 rounded-lg">
              <Icon icon="fluent:key-20-filled" class="mr-3 text-indigo-500"/>
              <span class="text-gray-700">加密传输存储</span>
            </div>
            <div class="flex items-center p-3 border border-gray-200 rounded-lg">
              <Icon icon="fluent:person-lock-20-filled" class="mr-3 text-indigo-500"/>
              <span class="text-gray-700">严格访问控制</span>
            </div>
            <div class="flex items-center p-3 border border-gray-200 rounded-lg">
              <Icon icon="fluent:shield-task-20-filled" class="mr-3 text-indigo-500"/>
              <span class="text-gray-700">定期安全审计</span>
            </div>
            <div class="flex items-center p-3 border border-gray-200 rounded-lg">
              <Icon icon="fluent:database-arrow-down-20-filled" class="mr-3 text-indigo-500"/>
              <span class="text-gray-700">数据备份恢复</span>
            </div>
          </div>
        </section>

        <!-- 您的权利 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:person-settings-20-filled" class="mr-2 text-indigo-500"/>
            您的权利
          </h3>
          <div class="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg">
            <div class="grid grid-cols-2 gap-3">
              <div class="flex items-center">
                <Icon icon="fluent:eye-20-filled" class="mr-2 text-green-600"/>
                <span class="text-gray-700">查看个人信息</span>
              </div>
              <div class="flex items-center">
                <Icon icon="fluent:edit-20-filled" class="mr-2 text-green-600"/>
                <span class="text-gray-700">更正错误信息</span>
              </div>
              <div class="flex items-center">
                <Icon icon="fluent:delete-20-filled" class="mr-2 text-green-600"/>
                <span class="text-gray-700">删除个人信息</span>
              </div>
              <div class="flex items-center">
                <Icon icon="fluent:arrow-download-20-filled" class="mr-2 text-green-600"/>
                <span class="text-gray-700">导出数据副本</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 第三方共享 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:people-20-filled" class="mr-2 text-indigo-500"/>
            信息共享说明
          </h3>
          <div class="bg-amber-50 border border-amber-200 p-4 rounded-lg">
            <div class="flex items-start">
              <Icon icon="fluent:warning-20-filled" class="text-amber-600 text-xl mr-3 mt-0.5"/>
              <div>
                <p class="text-amber-800 font-medium mb-2">我们不会向第三方出售、出租您的个人信息，除非：</p>
                <ul class="text-amber-700 text-sm space-y-1">
                  <li class="flex items-center">
                    <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                    事先获得您的明确同意
                  </li>
                  <li class="flex items-center">
                    <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                    根据法律法规要求
                  </li>
                  <li class="flex items-center">
                    <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                    保护您或他人合法权益的紧急情况
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- Cookie使用 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:cookies-20-filled" class="mr-2 text-indigo-500"/>
            Cookie使用说明
          </h3>
          <div class="bg-purple-50 p-4 rounded-lg">
            <p class="text-purple-800 mb-3">我们使用Cookie和类似技术来：</p>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex items-center text-purple-700">
                <Icon icon="fluent:person-circle-20-filled" class="mr-2"/>
                <span class="text-sm">记住登录状态</span>
              </div>
              <div class="flex items-center text-purple-700">
                <Icon icon="fluent:chart-multiple-20-filled" class="mr-2"/>
                <span class="text-sm">分析使用情况</span>
              </div>
              <div class="flex items-center text-purple-700">
                <Icon icon="fluent:settings-20-filled" class="mr-2"/>
                <span class="text-sm">提供个性化体验</span>
              </div>
              <div class="flex items-center text-purple-700">
                <Icon icon="fluent:shield-globe-20-filled" class="mr-2"/>
                <span class="text-sm">提高安全性</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 联系我们 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:call-20-filled" class="mr-2 text-indigo-500"/>
            联系我们
          </h3>
          <div class="bg-gray-50 p-4 rounded-lg space-y-2">
            <div class="flex items-center">
              <Icon icon="fluent:building-20-regular" class="mr-2 text-gray-600"/>
              <span class="text-gray-700">民生医药科技有限公司</span>
            </div>
            <div class="flex items-center">
              <Icon icon="fluent:mail-20-regular" class="mr-2 text-gray-600"/>
              <span class="text-gray-700">privacy@minsheng-pharma.com</span>
            </div>
            <div class="flex items-center">
              <Icon icon="fluent:phone-20-regular" class="mr-2 text-gray-600"/>
              <span class="text-gray-700">400-123-4567</span>
            </div>
          </div>
        </section>
      </div>

      <!-- 操作按钮 -->
      <div class="flex gap-3 mt-6 pt-4 border-t border-gray-200">
        <n-button size="large" @click="handleDecline" class="flex-1">
          拒绝
        </n-button>
        <n-button type="primary" size="large" @click="handleAccept" class="flex-1">
          <template #icon>
            <Icon icon="fluent:checkmark-circle-20-filled"/>
          </template>
          同意并继续
        </n-button>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {NModal, NButton, useMessage} from 'naive-ui'
import {Icon} from '@iconify/vue'
import {dialogDraggable, dialogMaskClosable} from "@/config/dialogConfig.ts";

const message = useMessage()
const dialogVisible = ref(false)

const emit = defineEmits(['accept', 'decline'])

const openModal = () => {
  dialogVisible.value = true
}

const closeModal = () => {
  dialogVisible.value = false
}

const handleAccept = () => {
  message.success('您已同意隐私政策')
  emit('accept')
  closeModal()
}

const handleDecline = () => {
  message.warning('您已拒绝隐私政策')
  emit('decline')
  closeModal()
}

defineExpose({
  openModal,
  closeModal
})
</script>

<style scoped lang="scss">
:deep(.n-card) {
  border-radius: 1.5rem;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

:deep(.n-card-header) {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

:deep(.n-card__content) {
  padding: 0;
}

.policy-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 1.5rem 1.5rem 1.5rem 1.5rem;
  margin-right: -1.5rem;

  &::-webkit-scrollbar {
    width: 8px;
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

:deep(.n-button) {
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;

  &.n-button--large-type {
    height: 44px;
  }
}

:deep(.n-button--primary-type) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #5a67d8 0%, #6b5b95 100%);
  }
}
</style>