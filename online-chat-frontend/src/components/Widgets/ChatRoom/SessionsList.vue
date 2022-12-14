<template>
  <div class="sessions-list" >
    <a-spin :spinning="loading" tip="加载中……">
      <a-empty v-if="total === 0" class="search-empty">
        <template #description>
          <span>还没有好友哦，快去添加吧</span>
        </template>
      </a-empty>
      <a-empty v-else-if="FilterChatList.length === 0" class="search-empty">
        <template #description>
          <span>未搜索到好友</span>
        </template>
      </a-empty>
      <a-list bordered item-layout="horizontal" :data-source="FilterChatList" class="search-result" v-else>
        <template #renderItem="{item}">
          <a-list-item @click="JumpIntoChat(item)" :class="{'chat-selected': ChatSelected(item)}" :key="ChatID(item)">
            <a-list-item-meta>
              <template #avatar>
                <a-badge v-if="!LatestMsgUnread(item)" count="✔" :number-style="{ backgroundColor: '#52c41a' }">
                  <a-avatar :src="AvatarUrl(item)" />
                </a-badge>
                <a-badge v-else :count="UnreadMsgCount(item)">
                  <a-avatar :src="AvatarUrl(item)" />
                </a-badge>
              </template>
              <template #title>
                <span>{{ DisplayName(item) }}</span>
              </template>
              <template #description>
                <span v-html="LatestMsgContent(item)" class="message"/>
              </template>
            </a-list-item-meta>
            <template #actions>
              <span v-html="LatestMsgTime(item)"></span>
            </template>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>
    <a-row justify="end" style="background-color: white">
      <a-col :span="4">
        <a-button block type="dashed" :disabled="!WordCloudAble" @click="ShowWordCloudImg">词云</a-button>
      </a-col>
      <a-col :span="4">
        <a-button block type="dashed" @click="router.push('/user-add')"><PlusOutlined /></a-button>
      </a-col>
    </a-row>
    <WordCloudShow :visible="WordCloudImgVisible" />
  </div>
</template>

<script setup>
import {useStore} from "vuex";
import {useRouter, useRoute} from "vue-router";
import {computed, onUnmounted, ref} from "vue";
import {msgTimeFormat} from "@/utils/time/msgTimeFormat";
import {emojiParse} from "@/utils/emojis/emojiParse";
import {PlusOutlined} from '@ant-design/icons-vue';
import WordCloudShow from "@/components/Widgets/ChatRoom/SessionsList/WordCloudShow";
import Bus from "@/utils/EventBus";


const store = useStore();
const route = useRoute();
const router = useRouter();
const props = defineProps({
  FilterChatList: {
    type: Array,
    default: []
  },
  loading: {
    type: Boolean,
    default: false
  },
  total: {
    type: Number,
    default: 0
  }
})
// 当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 头像
const AvatarUrl = (item) => {
  return item["friend"]?.avatar_url;
}
// 展示名字
const DisplayName = (item) => {
  return item["friend"]?.nickname || item["friend"]?.username;
}
// 聊天室ID
const ChatID = (item) => {
  return item["chat"]?.id;
}
// 最新消息内容
const LatestMsgContent = (item) => {
  return emojiParse(item["latest_msg"]?.content);
}
// 最新消息时间
const LatestMsgTime = (item) => {
  return msgTimeFormat(item["latest_msg"]?.send_time, true);
}
// 最新消息是否未读
const LatestMsgUnread = (item) => {
  return item["latest_msg"]?.sender_id !== cur_id.value && item["latest_msg"]?.status === 0;
}
// 未读消息数
const UnreadMsgCount = (item) => {
  return item["chat"]?.unread;
}


// 手机号
const Telephone = (item) => {
  return item["friend"]?.telephone;
}
// 邮箱
const Email = (item) => {
  return item["friend"]?.email
}
// 签名
const Signature = (item) => {
  return item["friend"]?.signature;
}


// 点击会话列表中的名字跳转进入对应聊天室
const JumpIntoChat = (item) => {
  router.push(`/chat-room/${item.chat?.id}`);
  store.commit("chat/updateChatUserInfo", item["friend"]);
}
// 选中的聊天颜色样式
const ChatSelected = (item) => {
  return item.chat?.id?.toString() === route.params.chat_id;
}


const chat_id = computed(() => store.state.chat.chat_id);
// 可生成词云
const WordCloudAble = computed(() => {
  return chat_id.value !== 0;
})
// 词云图片框可见
const WordCloudImgVisible = ref(false);
// 展示词云框图片
const ShowWordCloudImg = () => {
  WordCloudImgVisible.value = true;
  Bus.$emit("GenWordCloud");
}
// 关闭词云图片框
const CloseWordCloudImg = () => {
  WordCloudImgVisible.value = false;
}

// Bus挂载图片框关闭事件
Bus.$on("CloseWordCloud", () => {
  CloseWordCloudImg();
})

onUnmounted(() => {
  Bus.$off("CloseWordCloud");
})

</script>

<style scoped>

</style>
