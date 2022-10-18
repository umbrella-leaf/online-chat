<template>
  <a-layout class="background">
    <div>
      <a-card class="entrance-card" :tab-list="tabList" @tabChange="onTabChange" :active-tab-key="ActiveTabKey">
        <template #title>
          <p class="title">Online Chat System</p>
        </template>
        <router-view />
      </a-card>
    </div>
  </a-layout>
</template>

<script setup>
import {onUnmounted, ref} from "vue";
import {onBeforeRouteUpdate, useRouter} from "vue-router";
import {useStore} from "vuex";
import Bus from "@/utils/EventBus";


const router = useRouter();
const store = useStore();
Bus.$on('updateRememberMe', (value) => {
  store.commit('entrance/updateRememberMe', value);
})
Bus.$on('updateLastCodeVerify', (value) => {
  store.commit('entrance/updateLastCodeVerify', value);
})
Bus.$on('clearLastCodeVerify', (value) => {
  store.commit('entrance/clearLastCodeVerify', value);
})


const ActiveTabKey = ref('sign-in');
const tabList = ref([
  {
    key: 'sign-in',
    tab: '登录'
  },
  {
    key: 'sign-up',
    tab: '注册'
  }
]);


const onTabChange = (key) => {
  ActiveTabKey.value = key;
  if (key === 'sign-in') {
    router.push('/sign-in');
  } else {
    router.push('/sign-up');
  }
}
const resetActiveTab = (route) => {
  if (route === '/sign-in') {
    ActiveTabKey.value = 'sign-in';
  } else {
    ActiveTabKey.value = 'sign-up';
  }
}


// 重置TabActiveKey
const route = router.currentRoute.value.fullPath;
resetActiveTab(route);
// 监听路由变化
onBeforeRouteUpdate((to) => {
  resetActiveTab(to.path);
});
onUnmounted(() => {
  Bus.$off('updateRememberMe');
  Bus.$off('updateLastCodeVerify');
  Bus.$off('clearLastCodeVerify');
})

</script>

<style scoped>

</style>
