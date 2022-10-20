<template>
  <div class="input">
    <div class="emoji-blank">
      <EmojiPicker>
        <FontIcons type="icon-emotion-line" />
      </EmojiPicker>
      <FontIcons type="icon-search" />
    </div>
    <a-textarea ref="textarea" v-model:value="content" @keyup="onKeyup" placeholder="输入信息，按enter发送"></a-textarea>
    <div class="send" @click="send">
      <span>发送（R）</span>
    </div>
    <transition name="appear">
      <div class="warn" v-show="warn">
        <div class="description">不能发送空白信息</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {computed, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {createFromIconfontCN} from '@ant-design/icons-vue';
import {useStore} from "vuex";
import {apiSendNewMessage} from "@/apis/chat/send-new-message";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/message";
import {chat_socket} from "@/utils/WebSocket";
import EmojiPicker from "@/components/Widgets/ChatRoom/InputFrame/EmojiPicker";


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


const onKeyup = (e) => {
  if (e.keyCode === 13) {
    send();
  }
}
// 发送消息
const SendNewMessage = (content) => {
  const params = {
    chat_id: chat_id.value,
    content: content,
    sender_id: cur_id.value
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
const send = () => {
  if (chat_id.value) {
    if (content.value.replace(/(^\s*)|(\s*$)/g, "").length === 0) {
      warn.value = true;
      content.value = '';
      setTimeout(() => {
        warn.value = false;
      }, 1000)
    } else {
      SendNewMessage(content.value);
    }
  } else {
    content.value = "";
  }
}


const textarea = ref();
const textarea_focus = () => {
  textarea.value.focus();
}
Bus.$on('InputFocus', textarea_focus);
Bus.$on('ClearInput', () => {
  content.value = '';
})
// 添加表情事件
Bus.$on('InsertDefaultEmoji', (emoji) => {
  content.value += emoji;
})
onUnmounted(() => {
  Bus.$off('InputFocus');
  Bus.$off('ClearInput');
  Bus.$off('InsertDefaultEmoji');
})

</script>

<style scoped>

</style>
