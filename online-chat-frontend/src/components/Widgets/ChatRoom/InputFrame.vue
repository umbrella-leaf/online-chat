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
    <a-textarea ref="textarea" v-model:value="content" class="textarea"
                @keydown="onKeyDown" placeholder="输入信息，按enter发送，按shift+enter换行"
                v-show="MsgReviewing === false"/>
    <div v-show="MsgReviewing === true" class="textarea review" v-html="emojiParse(content)"/>
    <div class="input-btn review" v-if="MsgReviewing === false" @click="review" title="预览发送内容, 预览状态下无法按enter发送">
      <span>预览</span>
    </div>
    <div class="input-btn edit" v-else @click="edit"  title="回到编辑状态">
      <span>编辑</span>
    </div>
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
import {emojiParse} from "@/utils/emojis/emojiParse";


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


// 按回车发送
// 按Shift+Enter换行
const onKeyDown = (e) => {
  if (e.shiftKey && e.keyCode === 13) {
    return;
  }
  if (e.keyCode === 13) {
    e.preventDefault();
    send();
  }
}

// 预览消息
const MsgReviewing = ref(false);
// 预览
const review = () => {
  MsgReviewing.value = true;
}
// 编辑（取消预览）
const edit = () => {
  MsgReviewing.value = false;
  textarea_focus();
}

// 发送消息
const SendNewMessage = (content, type=0) => {
  if (chat_id.value) {
    const params = {
      chat_id: chat_id.value,
      content: content,
      sender_id: cur_id.value,
      type: type
    }
    apiSendNewMessage(params)
      .then(response => {
        ResponseToMessage(response, false);
        if (response.data.status === 200) {
          // 清空输入
          Bus.$emit('ClearInput');
          // 恢复编辑
          edit();
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
  nextTick(() => {textarea.value.focus();})
}
Bus.$on('InputFocus', textarea_focus);
Bus.$on('ClearInput', () => {
  content.value = '';
})
// 添加表情事件
Bus.$on('InsertDefaultEmoji', (emoji) => {
  content.value += emoji;
})
// 发送消息事件（用于直接发送用户表情包）
Bus.$on('SendUserEmoji', (emoji_url) => {
  SendNewMessage(emoji_url, 1)
})
onUnmounted(() => {
  Bus.$off('InputFocus');
  Bus.$off('ClearInput');
  Bus.$off('InsertDefaultEmoji');
  Bus.$off('SendUserEmoji');
})

</script>

<style scoped>

</style>
