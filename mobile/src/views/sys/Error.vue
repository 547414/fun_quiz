<template>
  <div>
    <van-empty image="error" :description="EnumErrorCategory[errorCategory.toString()]"/>
  </div>
</template>

<script setup lang="ts">
import {useRoute} from "vue-router";
import {EnumErrorCategory} from "@/enum/errorEnum.ts";

const route = useRoute();
const errorCategory = route.params.errorCategory;
</script>