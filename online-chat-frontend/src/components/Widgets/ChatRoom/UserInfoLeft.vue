<template>
  <a-card class="userinfo" @click="JumpToUserProfile">
    <a-card-meta>
      <template #avatar>
        <a-avatar :src="UserInfo.avatar_url"></a-avatar>
      </template>
      <template #title>
        <span>{{ UserInfo.nickname || UserInfo.username }}</span>
      </template>
      <template #description>
        <span>{{ UserInfo.signature }}</span>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script setup>
import {useRouter} from "vue-router";


const router = useRouter();
const props = defineProps({
  UserInfo: {
    type: Object,
    default: {}
  }
})
// 点击名字跳转进入个人中心
const JumpToUserProfile = () => {
  router.push('/user-profile');
}
</script>

<style scoped>

</style>
