<template>
  <a-card class="intimacy-rank">
    <template #title>
      <span>亲密度排行</span>
    </template>
    <template #extra>
      <a-button type="link" @click="RefreshIntimacyRank">刷新</a-button>
    </template>
    <a-spin :spinning="loading" tip="加载中">
      <a-list :data-source="IntimacyRankList">
        <template #renderItem="{ item }">
          <a-list-item :key="item.id">
            <a-list-item-meta>
              <template #title>
                <span>{{ DisplayName(item) }}</span>
              </template>
              <template #avatar>
                <a-avatar shape="circle" :src='item["friend"]?.avatar_url' />
              </template>
              <template #description>
                <span>{{ `你们已经认识${RecognizedTime(item)}了` }}</span>
              </template>
            </a-list-item-meta>
            <template #actions>
              <div class="intimacy-right" title="互发消息数">
                <svg t="1664800243743" class="message-cnt" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1651" width="25" height="25">
                  <path d="M896 128H128a32 32 0 0 0-32 32v576a32 32 0 0 0 32 32h288v-64H160V192h704v512h-256c-8.832 0-16.832 3.584-22.656 9.376l-159.968 160 45.248 45.248L621.248 768H896a32 32 0 0 0 32-32V160a32 32 0 0 0-32-32" fill="#181818" p-id="1652"></path>
                  <path d="M560 448a48 48 0 1 0-95.968-0.032A48 48 0 0 0 560 448M240 448a48 48 0 1 0 95.968 0.032A48 48 0 0 0 240 448M784 448a48 48 0 1 0-95.968-0.032A48 48 0 0 0 784 448" fill="#181818" p-id="1653"></path>
                </svg>
                <span>{{ item["message_cnt"] }}</span>
              </div>
              <div class="intimacy-right" title="亲密度">
                <svg t="1666176578093" class="intimacy-rate" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2491" width="25" height="25">
                  <path d="M512 787.392l-212.64-212.64-96.832-96.832-9.12-9.12A127.04 127.04 0 0 1 160 383.36c0-70.624 57.408-128 128-128 32.8 0 62.432 12.704 85.12 33.088l9.76 9.76 96.544 96.512L512 427.36l32.576-32.64 96.544-96.512 9.76-9.76A126.912 126.912 0 0 1 736 255.36c70.592 0 128 57.408 128 128a127.04 127.04 0 0 1-33.408 85.472l-9.12 9.12-96.832 96.832L512 787.392zM736 191.36c-47.584 0-90.944 17.6-124.48 46.272l-0.16-0.16-2.144 2.176-19.232 19.232L512 336.832 434.016 258.88l-19.232-19.2-2.144-2.208-0.16 0.16A190.944 190.944 0 0 0 288 191.36a192 192 0 0 0-192 192c0 58.176 25.984 110.176 66.848 145.408L512 877.888l349.152-349.12A191.488 191.488 0 0 0 928 383.296a192 192 0 0 0-192-192z" fill="#181818" p-id="2492"></path>
                </svg>
                <span>{{ item["intimacy"] }}</span>
              </div>
            </template>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>
  </a-card>
</template>

<script setup>
import dayjs from "dayjs";
import Bus from "@/utils/EventBus";

const props = defineProps({
  IntimacyRankList: {
    type: Array,
    default: []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const DisplayName = (item) => {
  return item["friend"]?.nickname || item["friend"]?.username;
}
// 认识时间
const RecognizedTime = (item) => {
  return dayjs(`${item["start_time"]}+8`).fromNow(true);
}

// 刷新亲密度列表
const RefreshIntimacyRank = () => {
  Bus.$emit("updateIntimacyRank");
}

</script>

<style scoped>

</style>
