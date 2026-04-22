<template>
  <ResetSelfPassword ref="resetPasswordRef"/>
  <aside class="sidebar-container" :class="{ 'sidebar-collapsed': isCollapsed }">
    <div ref="sidebarRootRef" class="w-70 h-screen bg-white flex flex-col relative overflow-hidden sidebar-custom">
      <!-- 背景装饰 -->
      <div
          class="absolute -top-25 -right-25 w-75 h-75 bg-gradient-radial from-indigo-500/8 to-transparent pointer-events-none"></div>
      <div
          class="absolute -bottom-37.5 -left-25 w-87.5 h-87.5 bg-gradient-radial from-blue-500/6 to-transparent pointer-events-none"></div>

      <!-- Logo区域 -->
      <div class="pl-8 pb-3 pt-5 relative z-1">
        <div class="flex items-center gap-3.5">
          <div
              class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-14 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 relative overflow-hidden logo-shine">
            <Icon icon="fluent:cube-24-filled" :width="28" :height="28"/>
            <div
                class="absolute -top-1/2 -right-1/2 w-full h-full bg-gradient-to-br from-transparent via-white/30 to-transparent animate-shine"></div>
          </div>
          <span
              class="text-xl font-extrabold bg-gradient-to-br from-indigo-500 to-purple-600 bg-clip-text text-transparent tracking-tight logo-text">玄测后台管理</span>
        </div>
      </div>

      <!-- 主导航区域（中段滚动） -->
      <div
          class="flex-1 flex flex-col px-6 pr-3 mr-3 overflow-y-auto overflow-x-hidden relative z-1 min-h-0 custom-scrollbar">
        <nav class="flex-1">
          <template v-for="section in menuSections" :key="section.id">
            <div class="flex flex-col gap-1.5">
              <template v-for="item in section.items" :key="item.id">
                <!-- 父菜单项 -->
                <div v-if="item.children" class="relative">
                  <SidebarItem
                      :icon="item.icon"
                      :label="item.label"
                      :active="isParentActive(item)"
                      :badge="item.badge"
                      :has-children="true"
                      :expanded="expandedItems.includes(item.id)"
                      :collapsed="isCollapsed"
                      @click="toggleMenuItem(item)"
                  />
                  <n-collapse-transition :show="expandedItems.includes(item.id)">
                    <div class="mt-1.5 ml-4 pl-7 relative submenu-custom">
                      <div
                          class="absolute left-2 -top-1.5 bottom-1.5 w-0.5 bg-gradient-to-b from-gray-200/80 to-gray-200/30 rounded-sm"></div>
                      <SidebarItem
                          v-for="child in item.children"
                          :key="child.id"
                          :icon="child.icon"
                          :label="child.label"
                          :active="activeItem === child.id"
                          :badge="child.badge"
                          :collapsed="isCollapsed"
                          class="opacity-85 scale-96 hover:opacity-100 hover:scale-98 transition-all"
                          @click="handleItemClick(child.id, child.path)"
                      />
                    </div>
                  </n-collapse-transition>
                </div>
                <!-- 普通菜单项 -->
                <SidebarItem
                    v-else
                    :icon="item.icon"
                    :label="item.label"
                    :active="activeItem === item.id"
                    :badge="item.badge"
                    @click="handleItemClick(item.id, item.path)"
                />
              </template>
            </div>
            <div v-if="section.divider" class="h-px bg-gray-100 my-6"></div>
          </template>
        </nav>
      </div>
      <!-- 用户槽位（使用 out-in，且保留展开态测量 ref） -->
      <div class="slot user-slot">
        <Transition name="slot-fade" mode="out-in">
          <!-- 改动：slot-content 不再 absolute -->
          <div :key="isCollapsed ? 'mini' : 'full'" class="slot-content">
            <!-- 展开态：用于显示 + 测量高度 -->
            <div v-if="!isCollapsed" ref="userMeasureRef" class="p-4 px-6 pb-6 relative z-1">
              <n-card class="bg-gradient-to-br from-gray-50 to-gray-100 border border-black/4 custom-card-content"
                      :bordered="false">
                <div class="flex items-center gap-3.5">
                  <div class="relative">
                    <n-avatar size="large" :src="webUserDetail?.avatarFileInfo?.url"
                              class="w-11 h-11 rounded-3 shadow-md"/>
                  </div>
                  <div class="flex-1">
                    <h4 class="text-sm font-semibold text-gray-800 mb-0.5 overflow-hidden text-ellipsis whitespace-nowrap"
                        style="width: 74px;" :title="userName">{{ userName }}</h4>
                    <p class="text-xs text-gray-500 font-medium overflow-hidden text-ellipsis whitespace-nowrap"
                       style="width: 74px;" :title="userRoleLabel">{{ userRoleLabel }}</p>
                  </div>
                  <n-dropdown :options="userOptions" placement="top-end" :show-arrow="true"
                              @select="handleOptionSelect">
                    <n-button size="small" quaternary circle
                              class="w-9 h-9 text-gray-500 hover:bg-indigo-500 hover:text-white hover:-translate-y-0.5 hover:shadow-md hover:shadow-indigo-500/20 active:translate-y-0 transition-all">
                      <Icon icon="fluent:more-horizontal-20-regular" :width="20" :height="20"/>
                    </n-button>
                  </n-dropdown>
                </div>
              </n-card>
            </div>

            <!-- 折叠态微头像 -->
            <div v-else class="p-4 relative z-1 flex justify-center">
              <n-dropdown :options="userOptions" placement="right" :show-arrow="true" @select="handleOptionSelect">
                <n-avatar size="large" :src="webUserDetail?.avatarFileInfo?.url"
                          class="w-11 h-11 rounded-3 shadow-md cursor-pointer hover:scale-105 transition-transform"/>
              </n-dropdown>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- 折叠按钮 -->
    <button class="collapse-toggle-btn" :class="{ 'collapsed': isCollapsed }" @click="toggleSidebar">
      <Icon :icon="isCollapsed ? 'fluent:chevron-right-20-regular' : 'fluent:chevron-left-20-regular'" :width="16"
            :height="16"/>
    </button>
  </aside>
</template>

<script setup lang="ts">
import {h, ref, watch} from 'vue'
import {NAvatar, NButton, NCard, NCollapseTransition, NDropdown, useDialog, useNotification} from 'naive-ui'
import {Icon} from '@iconify/vue'
import SidebarItem from './SidebarItem.vue'
import {
  apiChangeCurrentUserRole,
  apiGetWebUserDetail,
  ChangeCurrentUserRoleParams,
  UserRoleListInfo,
  WebUserDetail,
  WebUserLoginDetail
} from "@/api/webUserApi.ts";
import {userRoleEnum} from "@/enum/common.ts";
import {apiUnionUserLogout} from "@/api/unionUserApi.ts";
import {useRoute, useRouter} from "vue-router";
import ResetSelfPassword from "@/components/sys/auth/ResetSelfPassword.vue";
import {cloneDeep} from 'lodash-es'
import {MenuTreeDetail} from "@/api/menuApi.ts";
import {getUnionUserInfo} from "@/utils/userUtil.ts";

const props = defineProps({menuTree: {type: Array, default: () => []}})
const emit = defineEmits(['sidebar-toggle'])

/** 折叠状态 */
const isCollapsedLocalStorage = localStorage.getItem('sidebarCollapsed')
const isCollapsed = ref(isCollapsedLocalStorage === 'true')
emit('sidebar-toggle', isCollapsed.value)
const toggleSidebar = async () => {
  isCollapsed.value = !isCollapsed.value
  localStorage.setItem('sidebarCollapsed', isCollapsed.value ? 'true' : 'false')
  emit('sidebar-toggle', isCollapsed.value)
}

const notification = useNotification()
const dialog = useDialog()
const webUserDetail = ref<WebUserDetail>()
const userName = ref()
const userRoleLabel = ref()
const userRoleCode = ref()
const router = useRouter()
const route = useRoute()
const resetPasswordRef = ref()

/** 菜单类型 */
interface MenuItem {
  id: string;
  icon: string;
  label: string;
  badge?: string | number | null;
  path?: string | null;
  children?: MenuItem[]
}

interface MenuSection {
  id: string;
  items: MenuItem[];
  divider?: boolean
}

const activeItem = ref('ticket-list')
const expandedItems = ref<string[]>(['ticket'])
const menuSections = ref<MenuSection[]>([{id: 'primary', items: []}])

/** 查找菜单 */
const findMenuItemByPath = (items: MenuItem[], targetPath: string): string | null => {
  for (const item of items) {
    if (item.path === targetPath) return item.id
    if (item.children?.length) for (const child of item.children) if (child.path === targetPath) return child.id
  }
  return null
}
const findParentMenuItem = (items: MenuItem[], targetId: string): MenuItem | null => {
  for (const item of items) {
    if (item.children?.length) for (const child of item.children) if (child.id === targetId) return item
  }
  return null
}
const initActiveMenuItem = () => {
  const currentPath = route.path
  for (const section of menuSections.value) {
    const foundItemId = findMenuItemByPath(section.items, currentPath)
    if (foundItemId) {
      activeItem.value = foundItemId
      const matchedParentItem = section.items.find(item => item.id === foundItemId)
      if (matchedParentItem?.children) {
        if (!expandedItems.value.includes(foundItemId)) expandedItems.value.push(foundItemId)
      } else {
        const parentItem = findParentMenuItem(section.items, foundItemId)
        if (parentItem && !expandedItems.value.includes(parentItem.id)) expandedItems.value.push(parentItem.id)
      }
      return
    }
  }
}
const convertMenuTree = (menuTree: MenuTreeDetail[]) =>
    menuTree.map(item => ({
      id: item.code, icon: item.icon, label: item.label, path: item.path,
      children: item.children?.map(child => ({id: child.code, icon: child.icon, label: child.label, path: child.path}))
    }))

if (props.menuTree && (props.menuTree as any[]).length > 0) {
  menuSections.value = [{id: 'primary', items: convertMenuTree(props.menuTree as MenuTreeDetail[])}]
}

/** 用户菜单 */
const defaultUserOptions = [
  {type: 'divider', props: {style: 'min-width: 120px; min-height: 40px;padding: 2px 4px;'}, key: 'd1'},
  {
    label: '重置密码',
    key: 'reset-password',
    props: {style: 'min-width: 120px; min-height: 40px;padding: 2px 4px;'},
    icon: () => h(Icon, {icon: 'fluent:key-20-regular', width: 16, height: 16})
  },
  {
    label: '偏好设置',
    key: 'preferences',
    props: {style: 'min-width: 120px; min-height: 40px;padding: 2px 4px;'},
    icon: () => h(Icon, {icon: 'fluent:options-20-regular', width: 16, height: 16})
  },
  {type: 'divider', props: {style: 'min-width: 120px; min-height: 40px;padding: 2px 4px;'}, key: 'd2'},
  {
    label: '退出登录',
    key: 'logout',
    props: {style: 'min-width: 120px; min-height: 40px;padding: 2px 4px;'},
    icon: () => h(Icon, {icon: 'fluent:sign-out-20-regular', width: 16, height: 16})
  }
]
const userOptions = ref(defaultUserOptions as any[])

const toggleMenuItem = (item: MenuItem) => {
  if (item.children?.length) {
    const idx = expandedItems.value.indexOf(item.id)
    if (idx > -1) expandedItems.value.splice(idx, 1)
    else expandedItems.value.push(item.id)
  } else {
    handleItemClick(item.id)
  }
}
const isParentActive = (parent: MenuItem) => parent.id === activeItem.value || !!parent.children?.some(c => c.id === activeItem.value)
const handleItemClick = (itemId: string, itemPath: string = null) => {
  activeItem.value = itemId
  if (itemPath) router.push(`${itemPath}`)
}

const addChangeRoleOption = (list: UserRoleListInfo[], current: string) => {
  for (let i = list.length - 1; i >= 0; i--) {
    const role = list[i];
    const isCur = role.roleCode === current
    userOptions.value.unshift({
      label: role.roleName, key: `ROLE_${role.roleCode}`,
      props: {
        style: `
        min-width:120px; min-height:40px; padding:2px 12px; margin:4px; border-radius:8px; transition:all .2s; position:relative;
        ${isCur
            ? 'background:linear-gradient(135deg,rgba(99,102,241,.12) 0%, rgba(139,92,246,.08) 100%); border:1px solid rgba(99,102,241,.2); color:#4f46e5; font-weight:600; box-shadow:0 2px 8px rgba(99,102,241,.15);'
            : 'background:rgba(244,241,254,1); border:1px solid transparent; color:#374151; font-weight:500;'}
      `
      },
      icon: () => h(Icon, {
        icon: isCur ? 'fluent:checkmark-circle-20-filled' : '',
        width: 16,
        height: 16,
        style: {color: isCur ? '#4f46e5' : '#6b7280'}
      })
    })
  }
}
const initUserOptions = () => {
  userOptions.value = cloneDeep(defaultUserOptions)
  const local = localStorage.getItem('unionUserInfo')
  if (!local) return
  const info: WebUserLoginDetail = JSON.parse(local)
  let webUserId: string
  for (const user of info.unionUserInfo.userList) {
    if (user.unionUserUserCategory === 'WEB_USER') {
      webUserId = user.unionUserUserId
      userName.value = user.unionUserUserName
      userRoleLabel.value = userRoleEnum[user.currentRoleCode]
      userRoleCode.value = user.currentRoleCode
      addChangeRoleOption(user.unionUserUserRoleList, user.currentRoleCode)
      break
    }
  }
  return webUserId
}
const getUserDetail = () => {
  const webUserId = initUserOptions()
  apiGetWebUserDetail(webUserId).then(res => {
    if (res.code === 200) webUserDetail.value = res.data
    else notification.error({title: '错误', content: res.message, duration: 3000})
  }).catch(err => notification.error({title: '错误', content: `${err.message}`, duration: 3000}))
}
const handleOptionSelect = (key: string) => {
  if (key === 'logout') logout()
  else if (key === 'reset-password') resetPasswordRef.value?.openModal()
  else if (key.includes('ROLE_')) changeRole(key.replace('ROLE_', ''))
}
const changeRole = (roleCode: string) => {
  if (roleCode === userRoleCode.value) return
  dialog.info({
    title: '切换角色',
    content: `确定要切换到角色【${userRoleEnum[roleCode]}】吗？`,
    positiveText: '确定', negativeText: '取消', draggable: true,
    onPositiveClick: () => doChangeRole(roleCode)
  })
}
const doChangeRole = (roleCode: string) => {
  const params: ChangeCurrentUserRoleParams = {roleCode}
  apiChangeCurrentUserRole(params).then(res => {
    if (res.code === 200) {
      userRoleCode.value = roleCode
      userRoleLabel.value = userRoleEnum[roleCode]
      changeStorage(roleCode, res.data.accessToken)
      initUserOptions()
      notification.success({title: '成功', content: '切换角色成功', duration: 1000})
      setTimeout(() => {
        window.location.href = window.location.origin + '/'
        const unionUserInfo: WebUserLoginDetail = getUnionUserInfo()
        if (!unionUserInfo) {
          window.location.href = window.location.origin + '/'
        } else {
          for (const [_idx, user] of unionUserInfo?.unionUserInfo?.userList?.entries()) {
            if (user.unionUserUserCategory === 'WEB_USER') {
              if (user.currentRoleCode === 'WEB_USER') {
                window.location.href = window.location.origin + '/sys/people'
                break
              } else {
                window.location.href = window.location.origin + '/quiz/list'
                break
              }
            }
          }
        }
      }, 1000)
    } else notification.error({title: '错误', content: res.message, duration: 3000})
  }).catch(err => notification.error({title: '错误', content: `${err.message}`, duration: 3000}))
}
const changeStorage = (roleCode: string, accessToken: string) => {
  const local = localStorage.getItem('unionUserInfo')
  if (local) {
    const info: WebUserLoginDetail = JSON.parse(local)
    for (const u of info.unionUserInfo.userList) if (u.unionUserUserCategory === 'WEB_USER') {
      u.currentRoleCode = roleCode;
      break
    }
    info.accessToken = accessToken
    localStorage.setItem('unionUserInfo', JSON.stringify(info))
  }
  const session = sessionStorage.getItem('unionUserInfo')
  if (session) {
    const info: WebUserLoginDetail = JSON.parse(session)
    for (const u of info.unionUserInfo.userList) if (u.unionUserUserCategory === 'WEB_USER') {
      u.currentRoleCode = roleCode;
      break
    }
    info.accessToken = accessToken
    sessionStorage.setItem('unionUserInfo', JSON.stringify(info))
  }
}
const logout = () => {
  dialog.warning({
    title: '警告', content: '确定要退出登录吗？', positiveText: '确定', negativeText: '取消', draggable: true,
    onPositiveClick: () => doLogout()
  })
}
const doLogout = () => {
  apiUnionUserLogout().then(res => {
    if (res.code === 200) {
      localStorage.clear();
      sessionStorage.clear()
      notification.success({title: '成功', content: '退出登录成功', duration: 3000})
      router.push('/login')
    } else notification.error({title: '错误', content: res.message, duration: 3000})
  }).catch(err => notification.error({title: '错误', content: `${err}`, duration: 3000}))
}

getUserDetail()

watch(() => route.path, () => initActiveMenuItem())
watch(() => props.menuTree, (newTree) => {
  if (newTree && (newTree as any[]).length > 0) {
    menuSections.value = [{id: 'primary', items: convertMenuTree(newTree as MenuTreeDetail[])}]
    setTimeout(() => initActiveMenuItem(), 0)
  }
}, {immediate: true, deep: true})
</script>

<style lang="scss" scoped>
.sidebar-container {
  position: relative;
  transition: all .3s cubic-bezier(.4, 0, .2, 1);

  &.sidebar-collapsed {
    transform: translateX(-280px);
  }
}

/* 折叠按钮 */
.collapse-toggle-btn {
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  width: 16px;
  height: 60px;
  background: rgba(255, 255, 255, .7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(229, 231, 235, .3);
  border-radius: 0 8px 8px 0;
  border-left: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 2px 0 8px rgba(0, 0, 0, .1);
  transition: all .3s cubic-bezier(.4, 0, .2, 1);
  z-index: 10;

  &:hover {
    background: rgba(248, 250, 252, .8);
    border-color: rgba(209, 213, 219, .4);
    box-shadow: 2px 0 12px rgba(0, 0, 0, .15);
    transform: translateY(-50%) scale(1.05);
  }

  &:active {
    transform: translateY(-50%) scale(.95);
  }

  &.collapsed {
    left: 100%;
    background: rgba(255, 255, 255, .9);
    backdrop-filter: blur(10px);
    border-color: rgba(229, 231, 235, .5);
    color: #374151;

    &:hover {
      background: rgba(249, 250, 251, .95);
      box-shadow: 2px 0 12px rgba(0, 0, 0, .2);
    }
  }
}

/* 侧边栏容器 */
.sidebar-custom {
  width: 280px;
  box-shadow: 0 0 60px rgba(0, 0, 0, .05);
}

/* Logo文字过渡 */
.logo-text {
  transition: all .3s cubic-bezier(.4, 0, .2, 1);
  opacity: 1;
  transform: translateX(0);
  max-width: 200px;
  overflow: hidden;

  &--collapsed {
    opacity: 0;
    transform: translateX(-20px);
    max-width: 0;
  }
}

/* 槽位：固定高度（由JS写入变量） */
.slot {
  position: relative;
  display: block;
}

.user-slot {
  height: 120px;
}

/* 改动：槽内内容使用文档流，不再 absolute，避免重叠 */
.slot-content {
  position: static; /* 关键改动 */
  inset: auto; /* 避免任何铺满定位 */
  height: 100%; /* 占满槽位高度，便于内部对齐/动效 */
}

/* 过渡：out-in 先出后进，不重叠不漂移 */
.slot-fade-enter-active, .slot-fade-leave-active {
  transition: opacity .18s ease, transform .18s ease;
}

.slot-fade-enter-from, .slot-fade-leave-to {
  opacity: 0;
  transform: translateX(-6px);
}

/* 自定义滚动条 */
.custom-scrollbar {
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
    margin: 10px 0;
  }

  &::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #e5e7eb, #d1d5db);
    border-radius: 10px;
    transition: all .3s;

    &:hover {
      background: linear-gradient(to bottom, #d1d5db, #9ca3af);
    }
  }

  scrollbar-width: thin;
  scrollbar-color: #e5e7eb transparent;
}

/* 闪光动画 */
@keyframes shine {
  0% {
    transform: translateX(-100%) translateY(-100%);
  }
  100% {
    transform: translateX(200%) translateY(200%);
  }
}

.animate-shine {
  animation: shine 3s infinite;
}

/* 自定义Tailwind类 */
@media (min-width: 1px) {
  .w-70 {
    width: 280px;
  }
  .w-75 {
    width: 300px;
  }
  .w-87\.5 {
    width: 350px;
  }
  .h-75 {
    height: 300px;
  }
  .h-87\.5 {
    height: 350px;
  }
  .-top-25 {
    top: -100px;
  }
  .-right-25 {
    right: -100px;
  }
  .-bottom-37\.5 {
    bottom: -150px;
  }
  .-left-25 {
    left: -100px;
  }
  .w-25 {
    width: 100px;
  }
  .h-25 {
    height: 100px;
  }
  .translate-x-7\.5 {
    transform: translateX(30px);
  }
  .-translate-y-7\.5 {
    transform: translateY(-30px);
  }
  .rounded-14 {
    border-radius: 14px;
  }
  .rounded-2\.5 {
    border-radius: 10px;
  }
  .rounded-3 {
    border-radius: 12px;
  }
  .w-11 {
    width: 44px;
  }
  .h-11 {
    height: 44px;
  }
  .w-9 {
    width: 36px;
  }
  .h-9 {
    height: 36px;
  }
  .-translate-y-0\.5 {
    transform: translateY(-2px);
  }
  .translate-y-0 {
    transform: translateY(0);
  }
  .scale-96 {
    transform: scale(.96);
  }
  .scale-98 {
    transform: scale(.98);
  }
  .z-1 {
    z-index: 1;
  }
}
</style>
