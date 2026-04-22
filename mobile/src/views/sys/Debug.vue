<template>
  <van-nav-bar
      title="Debug"
      left-arrow
      @click-left="onClickLeft"
  />
  <div class="page-content">
    <van-divider class="divider">local storage item
    </van-divider>
    <van-cell-group inset>
      <van-field
          v-model="localStorageKey"
          clearable
          label="key"
          placeholder="key"
      >
      </van-field>
      <van-field
          v-model="localStorageKey"
          clearable
          label="value"
          placeholder="value"
      >
      </van-field>
      <van-field
          v-model="localStorageValueShow"
          clearable
          label="localStorageValueShow"
          placeholder="localStorageValueShow"
          type="textarea"
          rows="4"
          autosize
      >
      </van-field>
    </van-cell-group>
    <div style="padding: 0 16px" class="mt-4">
      <van-button type="primary" block @click="setLocalStorage">set local storage</van-button>
    </div>
    <div style="padding: 0 16px" class="mt-4">
      <van-button type="primary" block @click="getLocalStorage">get local storage</van-button>
    </div>
    <van-divider class="divider">local storage</van-divider>
    <div style="padding: 0 16px" class="mt-4">
      <van-button type="primary" block @click="clearAllLocalStorage">clear all local storage</van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from "vue-router";
import {notifyError} from "@/utils/notify.ts";
import {showConfirmDialog} from "vant";

const localStorageKey = ref('testA')
const localStorageValue = ref('testValue')
const localStorageValueShow = ref('')
const router = useRouter()
const setLocalStorage = () => {
  if (localStorageKey.value && localStorageValue.value) {
    localStorage.setItem(localStorageKey.value, localStorageValue.value)
  } else {
    notifyError('请填写key和value')
  }
}

const getLocalStorage = () => {
  if (localStorageKey.value) {
    const value = localStorage.getItem(localStorageKey.value)
    if (value) {
      localStorageValueShow.value = JSON.stringify(value)
    } else {
      notifyError('找不到key')
    }
  } else {
    notifyError('请填写key')
  }
}
const onClickLeft = () => {
  router.push('/?back=mine')
}

const clearAllLocalStorage = () => {
  showConfirmDialog({
    title: '提示',
    width: '80vw',
    message:
        '是否确认清楚全部缓存？',
  }).then(() => {
    localStorage.clear()
  }).catch(() => {

  });
}
</script>

<style scoped lang="scss">
.page-content {
  padding: 0 0 16px 0;
  width: 100%;
  height: calc(100vh - 46px);
  background-color: #efefef;
  overflow-y: auto;
}

.divider {
  color: #696969;
  border-color: #b9b9b9;
  padding: 0 16px;
}
</style>
