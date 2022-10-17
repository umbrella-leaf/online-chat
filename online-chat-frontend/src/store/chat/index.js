export const chat = {
  namespaced: true,
  state: () => ({
    curChatID: 0
  }),
  getters: {

  },
  mutations: {
    changeCurChatID(state, chat_id) {
      state.curChatID = chat_id;
    },
    QuitAllChat(state) {
      state.curChatID = 0;
    }
  },
  actions: {

  }
}
