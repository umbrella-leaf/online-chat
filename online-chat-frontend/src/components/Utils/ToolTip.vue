<template>
  <a-tooltip>
    <template #title>
      <span v-if="content !== undefined">{{content}}</span>
      <slot name="content" v-else></slot>
    </template>
    <info-circle-outlined style="color: rgba(0, 0, 0, 0.45)" />
  </a-tooltip>
</template>

<script setup>
import {InfoCircleOutlined} from "@ant-design/icons-vue";
import {computed} from "vue";

const props = defineProps({
  content: {
    type: String
  }
})


const content = computed(() => props.content);

</script>

<style scoped>

</style>
