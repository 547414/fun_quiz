<template>
  <div class="flex flex-wrap gap-2 items-center">
    <n-image-group>
      <div v-for="(img, i) in safeList" :key="i" class="relative group w-16 h-16 flex-shrink-0">
        <n-image
          :src="img.url ?? ''"
          width="64"
          height="64"
          object-fit="cover"
          class="rounded-lg border border-gray-200 block"
        />
        <button
          type="button"
          @click.stop="remove(i)"
          class="absolute -top-1.5 -right-1.5 w-4 h-4 bg-red-500 rounded-full text-white text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity leading-none z-10"
        >×</button>
      </div>
    </n-image-group>
    <label
      v-if="!max || safeList.length < max"
      class="w-16 h-16 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center cursor-pointer hover:border-violet-400 transition-colors flex-shrink-0"
    >
      <input type="file" accept="image/*" class="hidden" @change="handleFile"/>
      <n-spin v-if="uploading" size="small"/>
      <span v-else class="text-gray-400 text-2xl leading-none">+</span>
    </label>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { apiUploadFile, UploadFileInfo } from '@/api/storageApi.ts'

const props = defineProps<{
  modelValue: UploadFileInfo[] | null | undefined
  max?: number
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: UploadFileInfo[]): void
}>()

const message = useMessage()
const uploading = ref(false)
const safeList = computed<UploadFileInfo[]>(() => props.modelValue ?? [])

const remove = (i: number) => {
  const next = [...safeList.value]
  next.splice(i, 1)
  emit('update:modelValue', next)
}

const handleFile = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  apiUploadFile({ file, fileName: file.name, fileSize: file.size }).then(res => {
    if (res.code === 200) {
      const d = res.data
      const info: UploadFileInfo = {
        fileInfoId: d.fileInfoId,
        fileName: d.fileName,
        fileType: d.fileType,
        fileSize: d.fileSize,
        bucketName: d.bucketName,
        objectName: d.objectName,
        fileObjectName: d.fileObjectName,
        url: d.url,
      }
      emit('update:modelValue', [...safeList.value, info])
    } else {
      message.error(res.message || '上传失败')
    }
  }).catch((err) => {
    message.error(typeof err === 'string' ? err : '上传失败')
  }).finally(() => {
    uploading.value = false
    ;(e.target as HTMLInputElement).value = ''
  })
}
</script>
