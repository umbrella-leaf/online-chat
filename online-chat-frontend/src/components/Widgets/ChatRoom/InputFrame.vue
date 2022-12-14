<template>
  <div class="input">
    <div class="emoji-blank" id="emoji-blank">
      <keep-alive>
        <EmojiPicker>
          <FontIcons type="icon-emotion-line" title="表情"/>
        </EmojiPicker>
      </keep-alive>
      <a-popover trigger="click" @visibleChange="MessageSearchVisibleChange" :get-popup-container="() => wrapper">
        <template #content>
          <a-input-search enter-button ref="message_search" v-model:value="search_keyword" @change="SearchMessageByKeyword"/>
        </template>
        <FontIcons type="icon-search" title="搜索聊天记录"/>
      </a-popover>
    </div>
    <ContentEditor class="textarea"/>
    <div class="input-btn send" @click="Bus.$emit('SendMessageByBtn')" title="按enter键发送，按shift+enter换行">
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
import {computed, nextTick, onMounted, onUnmounted, ref} from "vue";
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
        // console.log(error);
        ReportErrorMessage(error);
      })
  }
}
const send = (param) => {
  const { content, html } = param;
  // 消息为空判断
  const MessageEmpty = (content) => {
    return content.replace(/&nbsp;/g, "").trim().length === 0;
  }
  // 在聊天室内才发送
  if (chat_id.value) {
    // 如果消息为空
    if (MessageEmpty(content)) {
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

// 历史消息搜索关键字
const search_keyword = ref('');
const message_search = ref();
// 历史消息搜索popover可见性改变事件
const MessageSearchVisibleChange = (visible) => {
  if (visible) {
    // 搜索框聚焦
    nextTick(() => {
      setTimeout(() => {
        message_search.value.focus();
      });
    })
  } else {
    // 关闭popover时清空搜索框
    message_search.value.blur();
    search_keyword.value = '';
    SearchMessageByKeyword();
  }
}
// 搜索历史消息（通过关键字）
const SearchMessageByKeyword = () => {
  Bus.$emit("SearchMessage", search_keyword.value);
  Bus.$emit("MessageToBottom");
}
// 搜索框包裹组件
const wrapper = ref(document.body);


// 发送文本消息
Bus.$on('SendText', (param) => {
  send(param);
})
// 发送消息事件（用于直接发送用户表情包）
Bus.$on('SendUserEmoji', (param) => {
  SendNewMessage(param, 1)
})
onMounted(() => {
  wrapper.value = document.getElementById("emoji-blank");
})
onUnmounted(() => {
  Bus.$off('SendText');
  Bus.$off('SendUserEmoji');
})

</script>

<style scoped>

</style>
