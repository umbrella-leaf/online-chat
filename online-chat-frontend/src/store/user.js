export const user = {
  namespaced: true,
  state: () => ({
    token: null
  }),
  getters: {

  },
  mutations: {
    updateToken(state, value) {
      state.token = value;
    },
    deleteToken(state, value) {
      state.token = null;
    }
  },
  actions: {

  }
}
