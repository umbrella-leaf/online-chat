<template>
  <a-layout-sider
    collapsible
    class="sider-primary"
    breakpoint="lg"
    collapsed-width="0"
    width="250px"
    :collapsed="sidebarCollapsed"
    @collapse="toggleSidebar"
    :trigger="null"
    :class="[`ant-layout-sider-${sidebarColor}`, `ant-layout-sider-${sidebarTheme}`]"
    theme="light"
    :style="{ backgroundColor: 'transparent' }">
    <div class="brand">
      <img src="images/logo-ct-black.png" alt="">
      <span>Online Chat</span>
    </div>
    <hr>
    <a-menu theme="light" mode="inline" selectable :selected-keys="selectedKeys">
      <a-menu-item key="1">
        <router-link to="/chatroom">
            <span class="icon">
              <svg t="1664800243743" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1651" width="20" height="20">
                <path d="M896 128H128a32 32 0 0 0-32 32v576a32 32 0 0 0 32 32h288v-64H160V192h704v512h-256c-8.832 0-16.832 3.584-22.656 9.376l-159.968 160 45.248 45.248L621.248 768H896a32 32 0 0 0 32-32V160a32 32 0 0 0-32-32" fill="#181818" p-id="1652"></path>
                <path d="M560 448a48 48 0 1 0-95.968-0.032A48 48 0 0 0 560 448M240 448a48 48 0 1 0 95.968 0.032A48 48 0 0 0 240 448M784 448a48 48 0 1 0-95.968-0.032A48 48 0 0 0 784 448" fill="#181818" p-id="1653"></path>
              </svg>
						</span>
          <span class="label">聊天室</span>
        </router-link>
      </a-menu-item>
      <a-menu-item key="2">
        <router-link to="/profile">
            <span class="icon">
              <svg t="1664800243743" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1651" width="20" height="20">
                <path d="M896 128H128a32 32 0 0 0-32 32v576a32 32 0 0 0 32 32h288v-64H160V192h704v512h-256c-8.832 0-16.832 3.584-22.656 9.376l-159.968 160 45.248 45.248L621.248 768H896a32 32 0 0 0 32-32V160a32 32 0 0 0-32-32" fill="#181818" p-id="1652"></path>
                <path d="M560 448a48 48 0 1 0-95.968-0.032A48 48 0 0 0 560 448M240 448a48 48 0 1 0 95.968 0.032A48 48 0 0 0 240 448M784 448a48 48 0 1 0-95.968-0.032A48 48 0 0 0 784 448" fill="#181818" p-id="1653"></path>
              </svg>
						</span>
          <span class="label">存档</span>
        </router-link>
      </a-menu-item>
    </a-menu>
  </a-layout-sider>

</template>

<script setup>
import {computed, onMounted, ref} from "vue";
import Bus from '@/utils/EventBus';
import {useRouter, onBeforeRouteUpdate} from "vue-router";

const props = defineProps({
  // Sidebar折叠状态
  sidebarCollapsed: {
    type: Boolean,
    default: false
  },
  // Sidebar颜色设置
  sidebarColor: {
    type: String,
    default: "primary"
  },
  // Sidebar主题设置
  sidebarTheme: {
    type: String,
    default: 'light'
  }
})


const selectedKeys = ref(['1'])
const sidebarCollapsed = computed(() => {
  return props.sidebarCollapsed;
})
const kvMap = {
  1: '/chatroom',
  2: '/profile'
}
const router = useRouter();


const toggleSidebar = () => {
  Bus.$emit('toggleSidebar', !sidebarCollapsed.value);
}
// 根据路由变化重置sidebar
const resetSelected = (route) => {
  for (const [key, value] of Object.entries(kvMap)) {
    if (route === value) {
      selectedKeys.value = [key];
    }
  }
}
// 监听路由变化
onBeforeRouteUpdate((to) => {
  resetSelected(to.path);
});
// 初始化时正确设置sidebar
// 通过onMounted时对菜单初始值进行初始化操作来解决url直接访问跳转错误
let currentPath = router.currentRoute.value.fullPath;
resetSelected(currentPath);

</script>

<style scoped>

</style>
