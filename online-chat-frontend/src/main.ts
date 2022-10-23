import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './App.vue'
import 'ant-design-vue/dist/antd.css'
import router from './router'
import store from './store'
import '@/utils/time';

import './scss/app.scss';

router.beforeEach((to, from, next) => {
  if (to.fullPath) {
    if (to.fullPath.includes("chat-room")) {
      if (to.fullPath.match(/\d+/g)) {
        // @ts-ignore
        store.commit("chat/updateChatID" ,parseInt(to.fullPath.match(/\d+/g)[0]));
      }
      else {
        store.commit("chat/resetChatID");
        store.commit("chat/resetChatUserInfo");
      }
    } else {
      store.commit("chat/resetChatID");
      store.commit("chat/resetChatUserInfo");
    }
  } else {
    store.commit("chat/resetChatID");
    store.commit("chat/resetChatUserInfo");
  }
  next();
})

router.afterEach((to, from) => {
  window.scrollTo(0, 0);
  if (to.fullPath && to.fullPath.includes("chat-room")) {
    window.scrollBy(0, 20);
  }
})


createApp(App)
  .use(store)
  .use(router)
  .use(Antd)
  .mount('#app')
