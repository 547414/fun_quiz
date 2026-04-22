<template>
  <div class="app-container" v-if="menuTree.length !== 0 && !loading">
    <SideBar :menuTree="menuTree" @sidebar-toggle="handleSidebarToggle"/>
    <main class="main-content" :class="{ 'main-content--expanded': sidebarCollapsed }">
      <router-view/>
    </main>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import SideBar from '@/components/sys/sideBar/SideBar.vue'
import {apiGetAllowMenuTree, MenuTreeDetail, MenuTreeParams} from "@/api/menuApi.ts";
import {useNotification} from "naive-ui";

const notification = useNotification()
const menuTree = ref<MenuTreeDetail[]>([])
const loading = ref(false)
const sidebarCollapsed = ref(false)

const handleSidebarToggle = (collapsed: boolean) => {
  sidebarCollapsed.value = collapsed
}

const getAllowMenu = () => {
  const params: MenuTreeParams = {
    parentId: null,
  }
  loading.value = true
  apiGetAllowMenuTree(params).then((res) => {
    if (res.code === 200) {
      menuTree.value = res.data || []
    } else {
      menuTree.value = []
      notification.error({
        title: '获取菜单失败',
        content: res.message,
        duration: 3000
      })
    }
  }).catch((err) => {
    menuTree.value = []
    notification.error({
      title: '获取菜单失败',
      content: err,
      duration: 3000
    })
  }).finally(() => {
    loading.value = false
  })
}

getAllowMenu()
</script>

<style lang="scss" scoped>
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: #f5f6fb;
  overflow: hidden;
}

.main-content {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  padding: 14px 2rem;
  margin-left: 0;
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &--expanded {
    margin-left: -280px;
  }

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: #e1e4e8;
    border-radius: 3px;

    &:hover {
      background: #d1d5db;
    }
  }
}
</style>