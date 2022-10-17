import { createStore } from 'vuex'
import {settings} from "@/store/settings";
import {urls} from "@/store/urls";
import {entrance} from "@/store/entrance";
import {user} from "@/store/user";
import createPersistedState from 'vuex-persistedstate';

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    settings,
    urls,
    entrance,
    user
  },
  plugins: [
    createPersistedState({
      // storage: window.sessionStorage,
      key: 'online-chat-client',
      path: ['settings', 'urls', 'entrance', 'user']
    })
  ]
})
