<template>
  <div>
    <a-card bordered class="chatroom">
      <a-row type="flex">
        <a-col :span="24" :md="9" class="chatroom-left">
          <UserInfoLeft :UserInfo="UserInfo" />
          <a-input-search class="search-input" placeholder="搜索联系人" v-model:value="keyword" enter-button />
          <SessionsList :FilterChatList="FilterChatList" :loading="loading"/>
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
              <InputFrame />
            </a-card-grid>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import {computed, ref, watch} from "vue";
import {useStore} from "vuex";
import {useRoute} from "vue-router";
import Bus from "@/utils/EventBus";
import MessageFrame from '../components/Widgets/ChatRoom/MessageFrame';
import InputFrame from '../components/Widgets/ChatRoom/InputFrame';
import {apiGetInfo} from "@/apis/user/get-info";
import {ResponseToMessage, ReportErrorMessage} from "@/utils/message";
import UserInfoLeft from "@/components/Widgets/ChatRoom/UserInfoLeft";
import SessionsList from "@/components/Widgets/ChatRoom/SessionsList";
import UserInfoRight from "@/components/Widgets/ChatRoom/UserInfoRight";
import {apiGetChatList} from "@/apis/chat/get-chat-list";
import {apiGetMessageList} from "@/apis/chat/get-message-list";


const route = useRoute();
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
    const DisplayName = item.friend?.nickname || item.friend?.username;
    return DisplayName.includes(keyword.value);
  })
})
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
const chat_id = computed(() => route.params.chat_id)
// 聊天者信息
const ChatUserInfo = computed(() => {
  const cur_chat =  ChatList.value.filter((item) => {
    return item["chat"]?.id.toString() === chat_id.value?.toString();
  });
  if (cur_chat.length) return cur_chat[0]["friend"];
  return {};
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
// 刷新页面时重置消息列表
if (chat_id.value) {
  GetMessageList(chat_id.value);
}
// 聊天室id改变时重新获取消息
watch(() => chat_id.value, (newVal, oldVal) => {
  if (newVal) {
    const chat_id = parseInt(newVal);
    GetMessageList(chat_id);
  }
})


</script>

<style scoped>

</style>
