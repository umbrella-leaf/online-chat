export const settings = {
  namespaced: true,
  state: () => ({
    sidebarCollapsed: false,
    sidebarColor: "primary",
    sidebarTheme: "light",
    navbarFixed: false,
    showSettingsDrawer: false
  }),
  getters: {

  },
  mutations: {
    toggleSidebar(state, value) {
      state.sidebarCollapsed = value;
    },
    toggleSettingsDrawer(state, value) {
      state.showSettingsDrawer = value;
    },
    toggleNavbarPosition(state, value) {
      state.navbarFixed = value;
    },
    updateSidebarTheme(state, value) {
      state.sidebarTheme = value;
    },
    updateSidebarColor(state, value) {
      state.sidebarColor = value;
    }
  },
  actions: {

  }
}
