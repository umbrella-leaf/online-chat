<template>
  <div class="sessions-list" >
    <a-spin :spinning="loading" tip="加载中……">
      <a-empty v-if="FilterChatList.length === 0" class="search-empty">
        <template #description>
          <span>未搜索到好友</span>
        </template>
      </a-empty>
      <a-list bordered item-layout="horizontal" :data-source="FilterChatList" class="search-result" v-else>
        <template #renderItem="{item}">
          <a-list-item @click="JumpIntoChat(item)" :class="{'chat-selected': ChatSelected(item)}" :key="ChatID(item)">
            <a-popover>
              <template #content>
                <a-card style="width: 200px;">
                  <a-card-meta>
                    <template #title>{{ DisplayName(item) }}</template>
                    <template #avatar>
                      <a-avatar :src="AvatarUrl(item)" />
                    </template>
                  </a-card-meta>
                  <a-descriptions :column="1">
                    <a-descriptions-item label="手机号">{{ Telephone(item) }}</a-descriptions-item>
                    <a-descriptions-item label="邮箱">{{ Email(item) }}</a-descriptions-item>
                    <a-descriptions-item label="签名">{{ Signature(item) }}</a-descriptions-item>
                  </a-descriptions>
                </a-card>
              </template>
              <a-list-item-meta>
                <template #avatar>
                  <a-avatar :src="AvatarUrl(item)"></a-avatar>
                </template>
                <template #title>
                  <span>{{ DisplayName(item) }}</span>
                </template>
                <template #description>
                  <span>{{ LatestMsgContent(item) }}</span>
                </template>
              </a-list-item-meta>
            </a-popover>
            <template #actions>
              <div class="session-right">
                <a-avatar class="msg_read" v-if="!LatestMsgUnread(item)">✔</a-avatar>
                <a-avatar class="msg_unread" v-else></a-avatar>
                <span>{{LatestMsgTime(item)}}</span>
              </div>
            </template>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>
  </div>
</template>

<script setup>
import {useStore} from "vuex";
import {useRouter, useRoute} from "vue-router";
import {computed} from "vue";
import dayjs from "dayjs";


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
  return item["latest_msg"]?.content
}
// 最新消息时间
const LatestMsgTime = (item) => {
  if (item["latest_msg"]?.send_time) {
    return dayjs(`${item["latest_msg"]?.send_time}+8`).fromNow();
  }
  return '';
}
// 最新消息是否未读
const LatestMsgUnread = (item) => {
  return item["latest_msg"]?.sender_id !== cur_id.value && item["latest_msg"]?.status === 0;
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
}
// 选中的聊天颜色样式
const ChatSelected = (item) => {
  return item.chat?.id?.toString() === route.params.chat_id;
}
</script>

<style scoped>

</style>
