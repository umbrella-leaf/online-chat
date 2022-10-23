<template>
  <component :is="navbarFixed ? 'a-affix' : 'div'" :offset-top="top">
    <a-layout-header>
      <a-row type="flex">
        <a-col :span="24" :md="6">
          <a-breadcrumb>
            <a-breadcrumb-item>
              <router-link to="/chat-room">Pages</router-link>
            </a-breadcrumb-item>
            <a-breadcrumb-item>{{ route.name }}</a-breadcrumb-item>
          </a-breadcrumb>
          <div class="ant-page-header-heading">
            <span class="ant-page-header-heading-title">{{ route.name }}</span>
          </div>
        </a-col>

        <a-col :span="24" :md="18" class="header-control">
          <a-button type="link" ref="secondarySidebarTriggerBtn" @click="openSettingsDrawer">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M11.4892 3.17094C11.1102 1.60969 8.8898 1.60969 8.51078 3.17094C8.26594 4.17949 7.11045 4.65811 6.22416 4.11809C4.85218 3.28212 3.28212 4.85218 4.11809 6.22416C4.65811 7.11045 4.17949 8.26593 3.17094 8.51078C1.60969 8.8898 1.60969 11.1102 3.17094 11.4892C4.17949 11.7341 4.65811 12.8896 4.11809 13.7758C3.28212 15.1478 4.85218 16.7179 6.22417 15.8819C7.11045 15.3419 8.26594 15.8205 8.51078 16.8291C8.8898 18.3903 11.1102 18.3903 11.4892 16.8291C11.7341 15.8205 12.8896 15.3419 13.7758 15.8819C15.1478 16.7179 16.7179 15.1478 15.8819 13.7758C15.3419 12.8896 15.8205 11.7341 16.8291 11.4892C18.3903 11.1102 18.3903 8.8898 16.8291 8.51078C15.8205 8.26593 15.3419 7.11045 15.8819 6.22416C16.7179 4.85218 15.1478 3.28212 13.7758 4.11809C12.8896 4.65811 11.7341 4.17949 11.4892 3.17094ZM10 13C11.6569 13 13 11.6569 13 10C13 8.34315 11.6569 7 10 7C8.34315 7 7 8.34315 7 10C7 11.6569 8.34315 13 10 13Z" fill="#111827"/>
            </svg>
          </a-button>
          <a-button type="link" class="sidebar-toggler" @click="toggleSideBar">
            <svg width="20" height="20" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
              <path d="M16 132h416c8.837 0 16-7.163 16-16V76c0-8.837-7.163-16-16-16H16C7.163 60 0 67.163 0 76v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16z"/>
            </svg>
          </a-button>
          <router-link class="btn-sign-in" @click="e => e.preventDefault()" to>
            <a-dropdown :trigger="['hover', 'click']"
                        :get-popup-container="() => wrapper">
              <a-avatar shape="circle" :src="avatar_url">
              </a-avatar>
              <template #overlay>
                <a-menu>
                  <a-menu-item><a href="#" @click="SignOut">登出</a></a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </router-link>

          <a-input-search class="header-search"
                          :class="searchLoading ? 'loading' : ''"
                          placeholder="Type here…"
                          @search="onSearch"
                          :loading="searchLoading">
            <svg slot="prefix" width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M8 4C5.79086 4 4 5.79086 4 8C4 10.2091 5.79086 12 8 12C10.2091 12 12 10.2091 12 8C12 5.79086 10.2091 4 8 4ZM2 8C2 4.68629 4.68629 2 8 2C11.3137 2 14 4.68629 14 8C14 9.29583 13.5892 10.4957 12.8907 11.4765L17.7071 16.2929C18.0976 16.6834 18.0976 17.3166 17.7071 17.7071C17.3166 18.0976 16.6834 18.0976 16.2929 17.7071L11.4765 12.8907C10.4957 13.5892 9.29583 14 8 14C4.68629 14 2 11.3137 2 8Z" fill="#111827"/>
            </svg>
          </a-input-search>
        </a-col>
      </a-row>
    </a-layout-header>
  </component>
</template>

<script setup>
import {computed, createVNode, ref} from "vue";
import {onMounted, onUnmounted} from "vue";
import {useRoute, useRouter} from 'vue-router';
import {useStore} from "vuex";
import Bus from '@/utils/EventBus';
import {Modal} from "ant-design-vue";
import {ExclamationCircleOutlined} from "@ant-design/icons-vue"

const route = useRoute();
const store = useStore();
const router = useRouter();

const avatar_url = computed(() => {
  return store.state.user.info.avatar_url;
});


const props = defineProps({
  // Header固定状态
  navbarFixed: {
    type: Boolean,
    default: false
  },
  // SideBar折叠状态
  sidebarCollapsed: {
    type: Boolean,
    default: false
  }
})


// Header和顶端距离
const top = ref(0);
// 搜索输入框加载状态
const searchLoading = ref(false);
// 包裹元素
const wrapper = ref(document.body);
const sidebarCollapsed = computed(() => props.sidebarCollapsed);


const resizeEventHandler = () => {
  top.value = top.value ? 0 : -0.01;
};
const onSearch = (value) =>  {

}
const openSettingsDrawer = () => {
  Bus.$emit('toggleSettingsDrawer', true);
}
const toggleSideBar = () => {
  Bus.$emit('toggleSidebar', !sidebarCollapsed.value);
  resizeEventHandler();
}
// 登出
const SignOut = (e) => {
  e.preventDefault();
  Modal.confirm({
    title: "登出确认",
    icon: createVNode(ExclamationCircleOutlined),
    content: "您确定要注销登录吗？",
    okText: "确认",
    cancelText: "取消",
    onOk() {
      // chat_socket.disconnect();
      store.commit('user/deleteToken');
      store.commit('user/deleteUserInfo');
      router.push('/sign-in');
    },
    onCancel() {}
  })
}


window.addEventListener('resize', resizeEventHandler);
onMounted(() => {
  // 设置wrapper
  wrapper.value = document.getElementById('layout-dashboard');
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeEventHandler);
})
</script>

<style scoped>

</style>
