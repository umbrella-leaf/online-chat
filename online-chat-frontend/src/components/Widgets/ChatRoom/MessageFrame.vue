<template>
  <div class="message">
    <div class="message-wrapper" ref="msg_list">
      <ul>
        <li v-for="(item, i) in DisplayMessageList" class="message-item">
          <div class="time" v-if="item.type === 'showTime'"><span v-html="item.show"></span></div>
          <div class="main" :class="{self: IsSelfSend(item)}" v-else :key="item.id">
            <a-avatar class="avatar" :src="item.sender_avatar"  alt=""/>
            <span v-if="IsSelfSend(item)" class="unread">{{ IsRead(item) ? "已读" : "未读" }}</span>
            <div class="content" v-if="item.type === 0">
              <div class="text" v-html="item.html" :class="SentimentStyle(item)"></div>
            </div>
            <a-dropdown :trigger="['contextmenu']" v-else >
              <template #overlay>
                <a-menu>
                  <a-menu-item @click="downloadImage(item.html)">
                    <DownloadOutlined />
                    保存到本地
                  </a-menu-item>
                </a-menu>
              </template>
              <img :src="item.html" alt="" class="emoji"/>
            </a-dropdown>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {computed, nextTick, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {useStore} from "vuex";
import {msgTimeShowFilter} from "@/utils/time/msgTimeShowFilter";
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
// 历史消息搜索关键字
const search_keyword = ref('');
// 历史消息搜索结果
const SearchMessageList = computed(() => {
  return msgTimeShowFilter(props.MessageList.filter((message) => {
    return message.content.includes(search_keyword.value);
  }))
})
// 最终展示的消息列表
const DisplayMessageList = computed(() => {
  if (search_keyword.value === '') return FilterMessageList.value;
  return SearchMessageList.value;
})


// 下载表情图片
const downloadImage = (fileUrl) => {
  const imgSrc = fileUrl;
  const fileName = imgSrc.slice(imgSrc.lastIndexOf('/') + 1); // 下载文件的名字
  downloadFile(imgSrc, fileName);
}

// 消息情感样式
const SentimentStyle = (item) => {
  return {
    positive_02: item["sentiment"] === 1 && item["degree"] <= 0.2,
    positive_04: item["sentiment"] === 1 && item["degree"] <= 0.4 && item["degree"] > 0.2,
    positive_06: item["sentiment"] === 1 && item["degree"] <= 0.6 && item["degree"] > 0.4,
    positive_08: item["sentiment"] === 1 && item["degree"] <= 0.8 && item["degree"] > 0.6,
    positive_10: item["sentiment"] === 1 && item["degree"] > 0.8,
    negative_02: item["sentiment"] === -1 && item["degree"] <= 0.2,
    negative_04: item["sentiment"] === -1 && item["degree"] <= 0.4 && item["degree"] > 0.2,
    negative_06: item["sentiment"] === -1 && item["degree"] <= 0.6 && item["degree"] > 0.4,
    negative_08: item["sentiment"] === -1 && item["degree"] <= 0.8 && item["degree"] > 0.6,
    negative_10: item["sentiment"] === -1 && item["degree"] > 0.8,
    neutral_05: item["sentiment"] === 0 && item["degree"] <= 0.5,
    neutral_10: item["sentiment"] === 0 && item["degree"] > 0.5,
    sentimental: true
  }
}

// 获取消息框组件
const msg_list = ref();
// 消息框拉到底
const msg_list_to_bottom = () => {
  nextTick(() => {msg_list.value.scrollTop = msg_list.value.scrollHeight;})
}
// Bus挂载消息框滚动到底部事件
Bus.$on('MessageToBottom', msg_list_to_bottom);
// Bus挂载历史消息搜索事件
Bus.$on('SearchMessage', (keyword) => {
  search_keyword.value = keyword;
});
onUnmounted(() => {
  Bus.$off('MessageToBottom');
  Bus.$off('SearchMessage');
})
</script>

<style scoped>

</style>
