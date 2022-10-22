<template>
  <div class="message">
    <div class="message-wrapper" ref="msg_list">
      <ul>
        <li v-for="(item, i) in FilterMessageList" class="message-item">
          <div class="time" v-if="item.type === 'showTime'"><span v-html="item.show"></span></div>
          <div class="main" :class="{self: IsSelfSend(item)}" v-else :key="item.id">
            <a-avatar class="avatar" :src="item.sender_avatar"  alt=""/>
            <span v-if="IsSelfSend(item)" class="unread">{{ IsRead(item) ? "已读" : "未读" }}</span>
            <div class="content" v-if="item.type === 0">
              <div class="text" v-html="emojiParse(item.content)"></div>
            </div>
            <a-dropdown :trigger="['contextmenu']" v-else >
              <template #overlay>
                <a-menu>
                  <a-menu-item @click="downloadImage(item.content)">
                    <DownloadOutlined />
                    保存到本地
                  </a-menu-item>
                </a-menu>
              </template>
              <img :src="item.content" alt="" class="emoji"/>
            </a-dropdown>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {computed, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {useStore} from "vuex";
import {msgTimeShowFilter} from "@/utils/time/msgTimeShowFilter";
import {emojiParse} from "@/utils/emojis/emojiParse";
import {DownloadOutlined} from "@ant-design/icons-vue";
import {downloadFile} from "@/utils/emojis/download";


const store = useStore();
const props = defineProps({
  MessageList: {
    type: Array,
    default: []
  }
})


// 获取当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 判断消息是否是自己发的
const IsSelfSend = (item) => {
  return item.sender_id === cur_id.value;
}
// 判断是否已读
const IsRead = (item) => {
  return item.status === 1;
}

// 按照时间过滤消息
const FilterMessageList = computed(() => {
  return msgTimeShowFilter(props.MessageList);
})

const downloadImage = (fileUrl) => {
  const imgSrc = fileUrl;
  const fileName = imgSrc.slice(imgSrc.lastIndexOf('/') + 1); // 下载文件的名字
  console.log(imgSrc, fileName);
  downloadFile(imgSrc, fileName);
}

// 获取消息框组件
const msg_list = ref();
// 消息框拉到底
const msg_list_to_bottom = () => {
  msg_list.value.scrollTop = msg_list.value.scrollHeight;
}
Bus.$on('MessageToBottom', msg_list_to_bottom);
onUnmounted(() => {
  Bus.$off('MessageToBottom');
})
</script>

<style scoped>

</style>
