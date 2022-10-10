<template>
  <a-list bordered item-layout="horizontal" :data-source="sessions" class="sessions-list">
    <template #renderItem="{item}">
      <a-list-item>
        <a-list-item-meta>
          <template #avatar>
            <a-avatar :src="item.avatar"></a-avatar>
          </template>
          <template #title>
            {{ item.name }}
          </template>
          <template #description>
            <span>{{ item.latest_msg }}</span>
          </template>
        </a-list-item-meta>
        <template #actions>
          <div class="session-right">
            <a-avatar class="msg_read" v-if="!item.latest_unread">✔</a-avatar>
            <a-avatar class="msg_unread" v-else></a-avatar>
            <span>{{item.latest_msg_time}}</span>
          </div>
        </template>
      </a-list-item>
    </template>
  </a-list>
</template>

<script setup>

const props = defineProps({
  sessions: {
    type: Object,
    default: {}
  }
})
</script>

<style scoped>

</style>
