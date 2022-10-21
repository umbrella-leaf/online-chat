<template>
  <a-popover trigger="click" overlayClassName="emoji-popover" v-model:visible="visible">
    <template #content>
      <component :is="curEmojis.component" :EmojiMap="curEmojis.map" />
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
import {onUnmounted, ref, shallowRef} from "vue";
import Bus from "@/utils/EventBus";

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
Bus.$on("ChangePickerVisible", (value) => {
  visible.value = value;
})

onUnmounted(() => {
  Bus.$off("ChangePickerVisible");
})

</script>

<style scoped lang="scss">

</style>
