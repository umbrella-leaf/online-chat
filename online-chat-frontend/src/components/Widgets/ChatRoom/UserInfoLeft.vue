<template>
  <a-card class="userinfo">
    <a-card-meta>
      <template #avatar>
        <a-avatar :src="UserInfo.avatar_url"></a-avatar>
      </template>
      <template #title>
        {{ UserInfo.nickname || UserInfo.username }}
      </template>
      <template #description>
        <span>{{ UserInfo.signature }}</span>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script setup>

const props = defineProps({
  UserInfo: {
    type: Object,
    default: {}
  }
})
</script>

<style scoped>

</style>
