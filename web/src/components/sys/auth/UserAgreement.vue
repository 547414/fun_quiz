<template>
  <n-modal
      v-model:show="dialogVisible"
      :mask-closable="dialogMaskClosable"
      :draggable="dialogDraggable"
      :closable="false"
      preset="card"
      class="agreement-modal"
      :style="{ maxWidth: '800px', maxHeight: '90vh' }"
  >
    <template #header>
      <div class="flex items-center">
        <Icon icon="fluent:document-text-20-filled" class="text-indigo-500 text-xl mr-2"/>
        <span class="text-lg font-semibold text-gray-800">用户服务协议</span>
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

    <div class="agreement-content">
      <div class="update-info flex items-center mb-6 p-3 bg-gray-50 rounded-lg">
        <Icon icon="fluent:calendar-20-regular" class="mr-2 text-gray-600"/>
        <span class="text-sm text-gray-600">更新日期：2024年1月1日 | 生效日期：2024年1月1日</span>
      </div>

      <div class="space-y-6">
        <!-- 协议接受 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:handshake-20-filled" class="mr-2 text-indigo-500"/>
            协议接受
          </h3>
          <div class="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-lg">
            <p class="text-gray-700 leading-relaxed">
              欢迎使用玄测后台管理系统！在使用本服务前，请您仔细阅读并充分理解本协议的各项条款。您通过注册、登录或使用本服务，即表示您已完全同意并接受本协议的全部条款。
            </p>
          </div>
        </section>

        <!-- 服务说明 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:apps-20-filled" class="mr-2 text-indigo-500"/>
            服务说明
          </h3>
          <div class="space-y-3">
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:ticket-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">玄测后台管理：</span>
                <span class="text-gray-600">提供工单创建、跟踪、处理的全流程管理</span>
              </div>
            </div>
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:people-team-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">团队协作：</span>
                <span class="text-gray-600">支持多用户协作处理和工单分配功能</span>
              </div>
            </div>
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:clock-alarm-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">实时通知：</span>
                <span class="text-gray-600">工单状态变更及时通知相关人员</span>
              </div>
            </div>
            <div class="flex items-start p-3 bg-blue-50 rounded-lg">
              <Icon icon="fluent:chart-multiple-20-regular" class="mr-2 text-indigo-500 mt-0.5"/>
              <div>
                <span class="font-medium text-gray-800">数据统计：</span>
                <span class="text-gray-600">提供工单处理效率和质量分析报告</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 用户权利义务 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:person-accounts-20-filled" class="mr-2 text-indigo-500"/>
            用户权利与义务
          </h3>
          <div class="grid grid-cols-1 gap-4">
            <div class="bg-green-50 p-4 rounded-lg">
              <h4 class="flex items-center font-medium text-green-800 mb-2">
                <Icon icon="fluent:shield-checkmark-20-filled" class="mr-2"/>
                您的权利
              </h4>
              <ul class="space-y-1 text-green-700 text-sm">
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  享受系统功能和技术支持
                </li>
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  对个人数据享有控制权
                </li>
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  随时停止使用服务
                </li>
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  获得及时的客户服务
                </li>
              </ul>
            </div>
            <div class="bg-orange-50 p-4 rounded-lg">
              <h4 class="flex items-center font-medium text-orange-800 mb-2">
                <Icon icon="fluent:warning-20-filled" class="mr-2"/>
                您的义务
              </h4>
              <ul class="space-y-1 text-orange-700 text-sm">
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  遵守法律法规和本协议条款
                </li>
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  保护账户信息和密码安全
                </li>
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  真实填写工单信息
                </li>
                <li class="flex items-center">
                  <Icon icon="fluent:circle-small-20-filled" class="mr-1"/>
                  合理使用系统资源
                </li>
              </ul>
            </div>
          </div>
        </section>

        <!-- 使用规范 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:book-exclamation-mark-20-filled" class="mr-2 text-indigo-500"/>
            使用规范
          </h3>
          <div class="bg-red-50 border border-red-200 p-4 rounded-lg">
            <h4 class="font-medium text-red-800 mb-3">禁止行为包括但不限于：</h4>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex items-center text-red-700">
                <Icon icon="fluent:prohibited-20-filled" class="mr-2"/>
                <span class="text-sm">恶意创建虚假工单</span>
              </div>
              <div class="flex items-center text-red-700">
                <Icon icon="fluent:prohibited-20-filled" class="mr-2"/>
                <span class="text-sm">攻击系统安全</span>
              </div>
              <div class="flex items-center text-red-700">
                <Icon icon="fluent:prohibited-20-filled" class="mr-2"/>
                <span class="text-sm">盗用他人账户</span>
              </div>
              <div class="flex items-center text-red-700">
                <Icon icon="fluent:prohibited-20-filled" class="mr-2"/>
                <span class="text-sm">泄露他人信息</span>
              </div>
              <div class="flex items-center text-red-700">
                <Icon icon="fluent:prohibited-20-filled" class="mr-2"/>
                <span class="text-sm">发布违法内容</span>
              </div>
              <div class="flex items-center text-red-700">
                <Icon icon="fluent:prohibited-20-filled" class="mr-2"/>
                <span class="text-sm">商业化滥用</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 数据保护 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:shield-globe-20-filled" class="mr-2 text-indigo-500"/>
            数据保护
          </h3>
          <div class="bg-blue-50 p-4 rounded-lg">
            <div class="space-y-3">
              <div class="flex items-start">
                <Icon icon="fluent:shield-lock-20-filled" class="text-blue-600 text-xl mr-3 mt-0.5"/>
                <div>
                  <p class="font-medium text-blue-800">数据安全</p>
                  <p class="text-blue-700 text-sm">所有数据采用加密存储，确保信息安全</p>
                </div>
              </div>
              <div class="flex items-start">
                <Icon icon="fluent:cloud-sync-20-filled" class="text-blue-600 text-xl mr-3 mt-0.5"/>
                <div>
                  <p class="font-medium text-blue-800">数据备份</p>
                  <p class="text-blue-700 text-sm">定期备份用户数据，防止意外丢失</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 责任限制 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:shield-error-20-filled" class="mr-2 text-indigo-500"/>
            责任限制
          </h3>
          <div class="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
            <p class="text-yellow-800 text-sm leading-relaxed">
              在法律允许的最大范围内，我们对因不可抗力、黑客攻击、系统故障等原因导致的服务中断或数据丢失不承担责任。建议用户定期导出重要数据。我们会尽最大努力保障服务稳定性和数据安全。
            </p>
          </div>
        </section>

        <!-- 服务中断 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:warning-20-filled" class="mr-2 text-indigo-500"/>
            服务中断说明
          </h3>
          <div class="space-y-3">
            <div class="p-3 bg-purple-50 rounded-lg">
              <div class="flex items-start">
                <Icon icon="fluent:wrench-screwdriver-20-filled" class="text-purple-600 text-lg mr-3 mt-0.5"/>
                <div>
                  <p class="font-medium text-purple-800">计划维护</p>
                  <p class="text-purple-700 text-sm">系统维护期间会提前通知，尽量安排在低峰时段</p>
                </div>
              </div>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
              <div class="flex items-start">
                <Icon icon="fluent:flash-20-filled" class="text-purple-600 text-lg mr-3 mt-0.5"/>
                <div>
                  <p class="font-medium text-purple-800">紧急情况</p>
                  <p class="text-purple-700 text-sm">遇到紧急情况导致的服务中断，我们会尽快恢复服务</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 协议修改 -->
        <section>
          <h3 class="flex items-center text-lg font-semibold text-gray-800 mb-3">
            <Icon icon="fluent:document-edit-20-filled" class="mr-2 text-indigo-500"/>
            协议修改与终止
          </h3>
          <div class="space-y-3">
            <div class="p-3 bg-cyan-50 rounded-lg">
              <p class="text-cyan-800 text-sm">
                <Icon icon="fluent:edit-20-filled" class="mr-2"/>
                我们保留随时修改本协议的权利，修改后的协议将在系统内公布并立即生效。
              </p>
            </div>
            <div class="p-3 bg-cyan-50 rounded-lg">
              <p class="text-cyan-800 text-sm">
                <Icon icon="fluent:door-arrow-right-20-filled" class="mr-2"/>
                用户可随时停止使用服务，我们也可在用户违反协议时暂停或终止服务。
              </p>
            </div>
          </div>
        </section>

        <!-- 联系方式 -->
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
              <span class="text-gray-700">service@minsheng-pharma.com</span>
            </div>
            <div class="flex items-center">
              <Icon icon="fluent:phone-20-regular" class="mr-2 text-gray-600"/>
              <span class="text-gray-700">400-123-4567</span>
            </div>
            <div class="flex items-center">
              <Icon icon="fluent:clock-20-regular" class="mr-2 text-gray-600"/>
              <span class="text-gray-700">服务时间：工作日 9:00-18:00</span>
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
  message.success('您已同意用户协议')
  emit('accept')
  closeModal()
}

const handleDecline = () => {
  message.warning('您已拒绝用户协议')
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

.agreement-content {
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