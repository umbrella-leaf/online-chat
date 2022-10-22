<template>
  <a-popover trigger="click" overlayClassName="emoji-popover" v-model:visible="visible">
    <template #content>
      <component :is="curEmojis.component" :EmojiMap="curEmojis.map"/>
      <a-divider />
      <div class="options">
        <template v-for="item in emojiOptions" :key="item.name">
          <span v-html="item.show" class="option" @click="selectEmojis(item)" :class="{selected: isEmojisSelected(item)}"/>
        </template>
      </div>
    </template>
    <slot />
  </a-popover>
</template>

<script setup>
import {WeChatEmojisMap, ClassicEmojisMap, QQEmojisMap} from "@/utils/emojis/default";
import WeChatEmojis from "@/components/Widgets/ChatRoom/InputFrame/WeChatEmoji";
import ClassicEmojis from "@/components/Widgets/ChatRoom/InputFrame/ClassicEmoji";
import QQEmojis from "@/components/Widgets/ChatRoom/InputFrame/QQEmoji";
import UserEmojis from "@/components/Widgets/ChatRoom/InputFrame/UserEmoji";
import {onUnmounted, ref, shallowRef} from "vue";
import Bus from "@/utils/EventBus";
import {apiGetEmojiList} from "@/apis/emoji/get-emoji-list";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";


// 用户表情列表
const UserEmojiList = ref([]);
// 获取用户表情
const getUserEmojiList = () => {
  apiGetEmojiList()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        UserEmojiList.value = response.data.data;
      }
    })
    .catch(error => {
      ReportErrorMessage(error);
      console.log(error);
    })
}
getUserEmojiList();


const emojiOptions = [
  {
    name: "WeChatEmojis",
    component: shallowRef(WeChatEmojis),
    map: WeChatEmojisMap,
    show: `<img src="https://res.wx.qq.com/mpres/htmledition/images/icon/emotion/13.gif"/>`
  },
  {
    name: "ClassicEmojis",
    component: shallowRef(ClassicEmojis),
    map: ClassicEmojisMap,
    show: `<span>😁</span>`
  },
  {
    name: "QQEmojis",
    component: shallowRef(QQEmojis),
    map: QQEmojisMap,
    show: `<img src="https://www.emojiall.com/img/platform/qq/004@2x.gif"/>`
  },
  {
    name: "UserEmojis",
    component: shallowRef(UserEmojis),
    map: UserEmojiList,
    show: `<svg t="1666357395748" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1631" width="25" height="25">
    <path d="M512.002048 872.229888c-82.62144 0-448.510976-259.203072-448.510976-547.059712L63.491072 312.064C62.8224 181.332992 166.3744 73.839616 297.048064 69.632c91.287552-0.022528 174.242816 53.066752 212.452352 135.974912 39.40864-80.579584 121.427968-131.525632 211.125248-131.13344C851.058688 77.101056 956.502016 181.472256 960.512 311.857152l0 13.334528C960.512 613.071872 594.622464 872.229888 512.002048 872.229888z" fill="#d81e06" p-id="1632"></path>
           </svg>`
  }
];
// 当前表情集
const curEmojis = ref(emojiOptions[0]);
// 选定表情集
const selectEmojis = (item) => {
  curEmojis.value = item;
}
// 是否选定当前表情集
const isEmojisSelected = (item) => {
  return curEmojis.value["name"] === item.name;
}


// 表情选择框可见
const visible = ref(false);
// Bus挂载表情选择框可见性改变事件
Bus.$on("ChangePickerVisible", (value) => {
  visible.value = value;
})
// Bus挂载更新用户表情包列表事件
Bus.$on("UpdateUserEmojis", () => {
  getUserEmojiList();
})

onUnmounted(() => {
  Bus.$off("ChangePickerVisible");
  Bus.$off("UpdateUserEmojis");
})

</script>

<style scoped lang="scss">

</style>
