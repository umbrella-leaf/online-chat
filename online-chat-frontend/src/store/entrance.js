export const entrance = {
  namespaced: true,
  state: () => ({
    rememberMe: false,
    lastCodeVerify: {}
  }),
  getters: {

  },
  mutations: {
    updateRememberMe(state, value) {
      state.rememberMe = value;
    },
    updateLastCodeVerify(state, {phone, code, time}) {
      state.lastCodeVerify[phone] = {code, time};
    },
    clearLastCodeVerify(state, phone) {
      delete state.lastCodeVerify[phone];
    }
  },
  actions: {

  }
}
