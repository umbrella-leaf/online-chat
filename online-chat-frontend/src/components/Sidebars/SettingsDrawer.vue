<template>
  <a-drawer
    class="settings-drawer"
    :class="[rtl ? 'index-drawer-rtl' : '']"
    :placement="rtl ? 'left' : 'right'"
    :closable="false"
    :visible="showSettingsDrawer"
    width="360"
    :get-container="() => wrapper"
    @close="closeSettingsDrawer">
    <!-- Settings Drawer Close Button -->
    <a-button type="link" class="btn-close" @click="closeSettingsDrawer">
      <svg xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 9 9">
        <g id="close" transform="translate(0.75 0.75)">
          <path id="Path" d="M7.5,0,0,7.5" fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5"/>
          <path id="Path-2" data-name="Path" d="M0,0,7.5,7.5" fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5"/>
        </g>
      </svg>
    </a-button>
    <!-- / Settings Drawer Close Button -->

    <!-- Settings Drawer Content -->
    <div class="drawer-content">
      <h6>界面主题配置</h6>
      <p>您可以在此配置以下选项</p>
      <hr>
      <div class="sidebar-color">
        <h6>侧边栏颜色设置</h6>
        <a-radio-group v-model:value="sidebarColorModel" @change="updateSidebarColor" defaultValue="primary">
          <a-radio-button value="primary" class="bg-primary"></a-radio-button>
          <a-radio-button value="secondary" class="bg-secondary"></a-radio-button>
          <a-radio-button value="success" class="bg-success"></a-radio-button>
          <a-radio-button value="danger" class="bg-danger"></a-radio-button>
          <a-radio-button value="warning" class="bg-warning"></a-radio-button>
          <a-radio-button value="black" class="bg-dark"></a-radio-button>
        </a-radio-group>
      </div>
      <div class="sidenav-type">
        <h6>侧边栏主题设置</h6>
        <p>在两种不同的主题背景之中切换</p>
        <a-radio-group button-style="solid" v-model:value="sidebarThemeModel" @change="updateSidebarTheme" defaultValue="primary">
          <a-radio-button value="light">透明背景</a-radio-button>
          <a-radio-button value="white">白色背景</a-radio-button>
        </a-radio-group>
      </div>
      <div class="navbar-fixed">
        <h6>顶栏固定设置</h6>
        <a-switch default-checked v-model:checked="navbarFixedModel" @change="toggleNavbarPosition" />
      </div>
    </div>
    <!-- / Settings Drawer Content -->
  </a-drawer>

</template>

<script setup>
import {ref} from "vue";
import {onMounted} from "vue";
import Bus from "@/utils/EventBus";

const props = defineProps({
  // Settings drawer visibility status.
  showSettingsDrawer: {
    type: Boolean,
    default: false
  },
  // Main sidebar color.
  sidebarColor: {
    type: String,
    default: "primary"
  },
  // Main sidebar theme : light, white, dark.
  sidebarTheme: {
    type: String,
    default: "light"
  },
  // Header fixed status.
  navbarFixed: {
    type: Boolean,
    default: false
  },
  // Drawer direction.
  rtl: {
    type: Boolean,
    default: false
  }
})

// The wrapper element to attach dropdowns to.
const wrapper = ref(document.body);
// Main sidebar color.
const sidebarColorModel = ref(props.sidebarColor);
// Main sidebar theme : light, white, dark.
const sidebarThemeModel = ref(props.sidebarTheme);
// Header fixed status.
const navbarFixedModel = ref(props.navbarFixed);


const closeSettingsDrawer = () => {
  Bus.$emit('toggleSettingsDrawer', false)
};
const updateSidebarTheme = (e) => {
  Bus.$emit('updateSidebarTheme', e.target.value)
};
const toggleNavbarPosition = () => {
  Bus.$emit('toggleNavbarPosition', navbarFixedModel.value);
};
const updateSidebarColor = (e) => {
  Bus.$emit('updateSidebarColor', e.target.value)
}


onMounted(() => {
  // Set the wrapper to the proper element, layout wrapper.
  wrapper.value = document.getElementById('layout-dashboard') ;
})

</script>

<style scoped>

</style>
