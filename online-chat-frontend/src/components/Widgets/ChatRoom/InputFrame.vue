<template>
  <div class="input">
    <div class="emoji-blank">
      <keep-alive>
        <EmojiPicker>
          <FontIcons type="icon-emotion-line" title="表情"/>
        </EmojiPicker>
      </keep-alive>
      <FontIcons type="icon-search" title="搜索聊天记录"/>
    </div>
    <ContentEditor class="textarea"/>
    <div class="input-btn send" @click="send" title="按enter键发送，按shift+enter换行">
      <span>发送（S）</span>
    </div>
    <transition name="appear">
      <div class="warn" v-show="warn">
        <div class="description">不能发送空白信息</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {computed, nextTick, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {createFromIconfontCN} from '@ant-design/icons-vue';
import {useStore} from "vuex";
import {apiSendNewMessage} from "@/apis/chat/send-new-message";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";
import {chat_socket} from "@/utils/WebSocket";
import EmojiPicker from "@/components/Widgets/ChatRoom/InputFrame/EmojiPicker";
import ContentEditor from "@/components/Widgets/ChatRoom/InputFrame/ContentEditor";


const store = useStore();
const FontIcons = createFromIconfontCN({
  scriptUrl: store.state.urls.icon_font_url
})
const props = defineProps({
  ChatUserInfo: {
    type: Object,
    default: {}
  }
})


const content = ref('');
const warn = ref(false);
// 当前聊天ID
const chat_id = computed(() => store.state.chat.chat_id);
// 当前用户ID
const cur_id = computed(() => store.state.user.info.id);


// 发送消息
const SendNewMessage = (param, type=0) => {
  if (chat_id.value) {
    const params = {
      chat_id: chat_id.value,
      content: param.content,
      html: param.html,
      sender_id: cur_id.value,
      type: type
    }
    apiSendNewMessage(params)
      .then(response => {
        ResponseToMessage(response, false);
        if (response.data.status === 200) {
          // 清空输入
          Bus.$emit('ClearInput');
          // 推送消息
          chat_socket.emit("send", {chat_id: chat_id.value, sender_id: cur_id.value, receiver_id: props.ChatUserInfo.id});
        }
      })
      .catch(error => {
        console.log(error);
        ReportErrorMessage(error);
      })
  }
}
const send = (param) => {
  const { content, html } = param;
  // 在聊天室内才发送
  if (chat_id.value) {
    // 如果消息为空（文本内容空且html消息无表情）
    if (content.replace(/(^\s*)|(\s*$)/g, "").length === 0 && !html.includes("<img")) {
      warn.value = true;
      Bus.$emit('ClearInput');
      setTimeout(() => {
        warn.value = false;
      }, 1000)
    } else {
      SendNewMessage(param);
    }
  } else {
    Bus.$emit('ClearInput');
  }
}

// 发送文本消息
Bus.$on('SendText', (param) => {
  send(param);
})
// 发送消息事件（用于直接发送用户表情包）
Bus.$on('SendUserEmoji', (param) => {
  SendNewMessage(param, 1)
})
onUnmounted(() => {
  Bus.$off('SendText');
  Bus.$off('SendUserEmoji');
})

</script>

<style scoped>

</style>
