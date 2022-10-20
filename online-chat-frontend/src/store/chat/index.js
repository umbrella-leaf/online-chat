export const chat = {
  namespaced: true,
  state: () => ({
    chat_id: 0,
    user_info: {}
  }),
  getters: {

  },
  mutations: {
    updateChatID(state, chat_id) {
      state.chat_id = chat_id;
    },
    resetChatID(state) {
      state.chat_id = 0;
    },
    updateChatUserInfo(state, info) {
      state.user_info = info;
    },
    resetChatUserInfo(state) {
      state.user_info = {};
    }
  },
  actions: {

  }
}
