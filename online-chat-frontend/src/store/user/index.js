export const user = {
  namespaced: true,
  state: () => ({
    token: null,
    info: {}
  }),
  getters: {

  },
  mutations: {
    updateToken(state, value) {
      state.token = value;
    },
    deleteToken(state) {
      state.token = null;
    },
    updateUserInfo(state, info) {
      state.info = info;
    },
    deleteUserInfo(state) {
      state.info = {};
    }
  },
  actions: {

  }
}
