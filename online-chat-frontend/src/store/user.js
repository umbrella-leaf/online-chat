export const user = {
  namespaced: true,
  state: () => ({
    token: null,
    avatar_url: null
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
    updateAvatarUrl(state, value) {
      state.avatar_url = value;
    },
    deleteAvatarUrl(state) {
      state.avatar_url = null;
    }
  },
  actions: {

  }
}
