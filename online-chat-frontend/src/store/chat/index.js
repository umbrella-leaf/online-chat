export const chat = {
  namespaced: true,
  state: () => ({
    chat_id: 0
  }),
  getters: {

  },
  mutations: {
    updateChatID(state, chat_id) {
      state.chat_id = chat_id;
    },
    resetChatID(state) {
      state.chat_id = 0;
    }
  },
  actions: {

  }
}
