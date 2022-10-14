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
        <router-link :to="kvMap[1]">
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
        <router-link :to="kvMap[2]">
            <span class="icon">
              <svg t="1665721623232" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2495" width="20" height="20">
                <path d="M512 74.666667C270.933333 74.666667 74.666667 270.933333 74.666667 512S270.933333 949.333333 512 949.333333 949.333333 753.066667 949.333333 512 753.066667 74.666667 512 74.666667zM288 810.666667c0-123.733333 100.266667-224 224-224S736 686.933333 736 810.666667c-61.866667 46.933333-140.8 74.666667-224 74.666666s-162.133333-27.733333-224-74.666666z m128-384c0-53.333333 42.666667-96 96-96s96 42.666667 96 96-42.666667 96-96 96-96-42.666667-96-96z m377.6 328.533333c-19.2-96-85.333333-174.933333-174.933333-211.2 32-29.866667 51.2-70.4 51.2-117.333333 0-87.466667-72.533333-160-160-160s-160 72.533333-160 160c0 46.933333 19.2 87.466667 51.2 117.333333-89.6 36.266667-155.733333 115.2-174.933334 211.2-55.466667-66.133333-91.733333-149.333333-91.733333-243.2 0-204.8 168.533333-373.333333 373.333333-373.333333S885.333333 307.2 885.333333 512c0 93.866667-34.133333 177.066667-91.733333 243.2z" p-id="2496"></path>
              </svg>
						</span>
          <span class="label">个人中心</span>
        </router-link>
      </a-menu-item>
      <a-menu-item key="3">
        <router-link :to="kvMap[3]">
            <span class="icon">
              <svg t="1665721717574" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2646" width="20" height="20">
                <path d="M678.3 642.4c24.2-13 51.9-20.4 81.4-20.4h0.1c3 0 4.4-3.6 2.2-5.6-30.8-27.6-65.6-49.7-103.7-65.8-0.4-0.2-0.8-0.3-1.2-0.5C719.2 505 759.6 431.7 759.6 349c0-137-110.8-248-247.5-248S264.7 212 264.7 349c0 82.7 40.4 156 102.6 201.1-0.4 0.2-0.8 0.3-1.2 0.5-44.7 18.9-84.8 46-119.3 80.6-34.5 34.5-61.5 74.7-80.4 119.5C147.9 794.5 138 841 137 888.8c-0.1 4.5 3.5 8.2 8 8.2h59.9c4.3 0 7.9-3.5 8-7.8 2-77.2 32.9-149.5 87.6-204.3C357 628.2 432.2 597 512.2 597c56.7 0 111.1 15.7 158 45.1 2.5 1.5 5.5 1.7 8.1 0.3zM512.2 521c-45.8 0-88.9-17.9-121.4-50.4-32.4-32.5-50.3-75.7-50.3-121.6 0-45.9 17.9-89.1 50.3-121.6S466.3 177 512.2 177s88.9 17.9 121.4 50.4c32.4 32.5 50.3 75.7 50.3 121.6 0 45.9-17.9 89.1-50.3 121.6C601.1 503.1 558 521 512.2 521zM880 759h-84v-84c0-4.4-3.6-8-8-8h-56c-4.4 0-8 3.6-8 8v84h-84c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h84v84c0 4.4 3.6 8 8 8h56c4.4 0 8-3.6 8-8v-84h84c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8z" p-id="2647"></path>
              </svg>
						</span>
          <span class="label">添加好友</span>
        </router-link>
      </a-menu-item>
    </a-menu>
  </a-layout-sider>

</template>

<script setup>
import {computed, ref} from "vue";
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
  1: '/chat-room',
  2: '/user-profile',
  3: '/user-add'
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
