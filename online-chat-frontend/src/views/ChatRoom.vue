<template>
  <div>
    <a-card bordered class="chatroom">
      <a-row type="flex">
        <a-col :span="24" :md="9" class="chatroom-left">
          <UserInfoLeft :UserInfo="UserInfo" />
          <a-input-search class="search-input" placeholder="搜索联系人" v-model:value="keyword" enter-button />
          <SessionsList :FilterChatList="FilterChatList" :loading="loading" :total="ChatList.length"/>
        </a-col>
        <a-col :span="24" :md="15" class="chatroom-right">
          <a-card >
            <a-card-grid style="width: 100%;" :hoverable="false">
              <UserInfoRight :ChatUserInfo="ChatUserInfo"/>
            </a-card-grid>
            <a-card-grid style="width: 100%" :hoverable="false">
              <MessageFrame :MessageList="MessageList" />
            </a-card-grid>
            <a-card-grid style="width: 100%" :hoverable="false">
              <InputFrame :ChatUserInfo="ChatUserInfo"/>
            </a-card-grid>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import {computed, onUnmounted, ref, watch} from "vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import Bus from "@/utils/EventBus";
import {chat_socket} from "@/utils/WebSocket";
import MessageFrame from '../components/Widgets/ChatRoom/MessageFrame';
import InputFrame from '../components/Widgets/ChatRoom/InputFrame';
import {apiGetInfo} from "@/apis/user/get-info";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";
import UserInfoLeft from "@/components/Widgets/ChatRoom/UserInfoLeft";
import SessionsList from "@/components/Widgets/ChatRoom/SessionsList";
import UserInfoRight from "@/components/Widgets/ChatRoom/UserInfoRight";
import {apiGetChatList} from "@/apis/chat/get-chat-list";
import {apiGetMessageList} from "@/apis/chat/get-message-list";


const router = useRouter();
const store = useStore();
// 用户信息
const UserInfo = computed(() => {
  return store.state.user.info;
})
// 初始化时获取用户信息
const GetUserInfo = () => {
  apiGetInfo()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        store.commit('user/updateUserInfo', response.data.data);
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}
GetUserInfo();

// 搜索关键字
const keyword = ref('');
// 获取聊天列表
const ChatList = ref([]);
// 搜索过滤
const FilterChatList = computed(() => {
  return ChatList.value.filter((item) => {
    const DisplayName = item["friend"].nickname || item["friend"].username;
    return DisplayName.includes(keyword.value);
  })
})

// 当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 获取聊天列表
const loading = ref(false);
const GetChatList = () => {
  loading.value = true;
  apiGetChatList()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        ChatList.value = response.data.data;
      }
      loading.value = false;
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
      loading.value = false;
    })
}
GetChatList();


// 当前聊天ID
const chat_id = computed(() => store.state.chat.chat_id);
// 聊天者信息
const ChatUserInfo = computed(() => {
  return store.state.chat.user_info;
});


// 刷新消息框和输入框状态
const RefreshFrame = () => {
  Bus.$emit('InputFocus');
  Bus.$emit('MessageToBottom');
}
// 消息列表
const MessageList = ref([]);
// 获取消息列表
const GetMessageList = (chat_id) => {
  apiGetMessageList({chat_id: chat_id})
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        MessageList.value = response.data.data;
      }
      RefreshFrame();
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
      RefreshFrame();
    })
}


// chat_socket监听
// 重载页面时，如果当前在聊天页面就加入
chat_socket.on("connect", () => {
  if (chat_id.value) {
    chat_socket.emit("join", {chat_id: chat_id.value, sender_id: cur_id.value, receiver_id: ChatUserInfo.value.id});
  }
})
// 收到消息列表更新推送
chat_socket.on("updateMessageList", (data) => {
  if (data["force"] && chat_id.value) {
    GetMessageList(chat_id.value);
    return;
  }
  if (chat_id.value && chat_id.value === data["chat_id"]) {
    GetMessageList(chat_id.value);
  }
})
// 收到聊天列表更新推送
chat_socket.on("updateChatList", (data) => {
  GetChatList();
})
// 强制退出聊天室
chat_socket.on("out_of_chat", (data) => {
  if (chat_id.value === data["chat_id"]) {
    router.push("/chat-room");
    MessageList.value = [];
  }
})


// 聊天室id改变时重新获取消息
watch(() => chat_id.value, (newVal, oldVal) => {
  // 之前是聊天窗口，就离开
  if (oldVal) {
    chat_socket.emit("leave", {cur_id: cur_id.value});
    const url = `${store.state.urls.backend_url}/chat/close/${oldVal}`;
    navigator.sendBeacon(url);
  }
  // 进入新的聊天窗口就加入
  if (newVal) {
    // 清空输入
    Bus.$emit('ClearInput');
    chat_socket.emit("join", {chat_id: newVal, sender_id: cur_id.value, receiver_id: ChatUserInfo.value.id});
  }
})
// 加一个setInterval，每天0点更新一次聊天列表和消息列表（如果此时正在聊天室里）
const updateDataWhenZeroClock = setInterval(() => {
    const now_date = new Date();
    if (now_date.getHours() === 0 && now_date.getMinutes() === 0 && now_date.getSeconds() === 0) {
      GetChatList();
      if (chat_id.value) GetMessageList(chat_id.value);
    }
  }, 1000);

if (chat_id.value) {
  GetMessageList(chat_id.value);
}
const final = () => {
  // 聊天窗口关闭/隐藏时退出聊天
  if (document.visibilityState === "hidden") {
    if (chat_id.value) {
      const url = `${store.state.urls.backend_url}/chat/close/${chat_id.value}`;
      navigator.sendBeacon(url);
      chat_socket.emit("leave", {cur_id: cur_id.value});
    }
  }
  // 聊天窗口可见时加入聊天
  if (document.visibilityState === "visible") {
    if (chat_id.value) {
      chat_socket.emit("join", {chat_id: chat_id.value, sender_id: cur_id.value, receiver_id: ChatUserInfo.value.id});
    }
  }
}

document.addEventListener('visibilitychange', final);
onUnmounted(() => {
  chat_socket.off("updateMessageList");
  chat_socket.off("updateChatList");
  chat_socket.off("out_of_chat");
  clearInterval(updateDataWhenZeroClock);
  document.removeEventListener("visibilitychange", final);
})

</script>

<style scoped>

</style>
