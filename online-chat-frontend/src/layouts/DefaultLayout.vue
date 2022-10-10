<template>
  <div>
    <a-layout class="layout-dashboard"
              id="layout-dashboard"
              :class="[navbarFixed ? 'navbar-fixed' : '',
              !sidebarCollapsed ? 'has-sidebar' : '', layoutClass]">
      <SidePart :sidebarCollapsed="sidebarCollapsed"
                :sidebarColor="sidebarColor"
                :sidebarTheme="sidebarTheme">
      </SidePart>
      <a-layout>
        <HeaderPart :sidebarCollapsed="sidebarCollapsed"
                    :navbarFixed="navbarFixed">
        </HeaderPart>
        <a-layout-content>
          <router-view />
        </a-layout-content>
        <FooterPart></FooterPart>

        <!-- Floating Action Button For Toggling Settings Drawer -->
        <a-button class="fab" shape="circle" @click="Bus.$emit('toggleSettingsDrawer', true)">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M11.4892 3.17094C11.1102 1.60969 8.8898 1.60969 8.51078 3.17094C8.26594 4.17949 7.11045 4.65811 6.22416 4.11809C4.85218 3.28212 3.28212 4.85218 4.11809 6.22416C4.65811 7.11045 4.17949 8.26593 3.17094 8.51078C1.60969 8.8898 1.60969 11.1102 3.17094 11.4892C4.17949 11.7341 4.65811 12.8896 4.11809 13.7758C3.28212 15.1478 4.85218 16.7179 6.22417 15.8819C7.11045 15.3419 8.26594 15.8205 8.51078 16.8291C8.8898 18.3903 11.1102 18.3903 11.4892 16.8291C11.7341 15.8205 12.8896 15.3419 13.7758 15.8819C15.1478 16.7179 16.7179 15.1478 15.8819 13.7758C15.3419 12.8896 15.8205 11.7341 16.8291 11.4892C18.3903 11.1102 18.3903 8.8898 16.8291 8.51078C15.8205 8.26593 15.3419 7.11045 15.8819 6.22416C16.7179 4.85218 15.1478 3.28212 13.7758 4.11809C12.8896 4.65811 11.7341 4.17949 11.4892 3.17094ZM10 13C11.6569 13 13 11.6569 13 10C13 8.34315 11.6569 7 10 7C8.34315 7 7 8.34315 7 10C7 11.6569 8.34315 13 10 13Z" fill="#111827"/>
          </svg>
        </a-button>
        <!-- / Floating Action Button For Toggling Settings Drawer -->
        <!-- Sidebar Overlay -->
        <div class="sidebar-overlay" @click="Bus.$emit('toggleSidebar', true)" v-show="! sidebarCollapsed"></div>
        <!-- / Sidebar Overlay -->
      </a-layout>
      <SettingsDrawer
        :sidebarColor="sidebarColor"
        :showSettingsDrawer="showSettingsDrawer"
        :navbarFixed="navbarFixed"
        :sidebarTheme="sidebarTheme">
      </SettingsDrawer>
    </a-layout>
  </div>
</template>

<script setup>
import {computed, onMounted, onUnmounted, ref} from "vue";
import {useRoute} from "vue-router";
import {useStore} from 'vuex';
import {useState} from "@/utils/hooks/useState";
import Bus from '@/utils/EventBus';
import SidePart from '../components/Sidebars/SidePart';
import HeaderPart from '../components/Headers/HeaderPart';
import FooterPart from "../components/Footers/FooterPart";
import SettingsDrawer from "../components/Sidebars/SettingsDrawer";


Bus.$on('toggleSidebar', (value) => {
  store.commit('settings/toggleSidebar', value);
});
Bus.$on('toggleSettingsDrawer', (value) => {
  store.commit('settings/toggleSettingsDrawer', value);
});
Bus.$on('toggleNavbarPosition', (value) => {
  store.commit('settings/toggleNavbarPosition', value);
});
Bus.$on('updateSidebarTheme', (value) => {
  store.commit('settings/updateSidebarTheme', value);
});
Bus.$on('updateSidebarColor', (value) => {
  store.commit('settings/updateSidebarColor', value);
});


const router = useRoute();
const store = useStore();

// // Sidebar collapsed status.
// const sidebarCollapsed = computed(() => store.state.settings.sidebarCollapsed);
// // Main sidebar color.
// const sidebarColor = computed(() => store.state.settings.sidebarColor);
// // Main sidebar theme : light, white, dark.
// const sidebarTheme = computed(() => store.state.settings.sidebarTheme);
// // Header fixed status.
// const navbarFixed = computed(() => store.state.settings.navbarFixed);
// // Settings drawer visibility status.
// const showSettingsDrawer = computed(() => store.state.settings.showSettingsDrawer);
const {sidebarCollapsed, sidebarColor, sidebarTheme, navbarFixed, showSettingsDrawer}
  = useState("settings",
  ["sidebarCollapsed",
    "sidebarColor",
    "sidebarTheme",
    "navbarFixed",
    "showSettingsDrawer"]);


// Sets layout's element's class based on route's meta data.
const layoutClass = computed(() => router.meta.layoutClass);
onUnmounted(() => {
  Bus.$off('toggleSidebar');
  Bus.$off('toggleSettingsDrawer');
  Bus.$off('toggleNavbarPosition');
  Bus.$off('updateSidebarTheme');
  Bus.$off('updateSidebarColor');
})

</script>

<style scoped>

</style>
