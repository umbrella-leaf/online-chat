<template>
  <a-popover trigger="click" overlayClassName="emoji-popover">
    <template #content>
      <component :is="curEmojis.component" :EmojiMap="curEmojis.map" />
      <a-divider />
      <div class="options">
        <div class="operations" style="width: 100%;">
          <template v-for="item in emojiOptions" :key="item.name">
            <span v-html="item.show" class="option" @click="selectEmojis(item)" :class="{selected: isEmojisSelected(item)}"/>
          </template>
        </div>
      </div>
    </template>
    <slot />
  </a-popover>
</template>

<script setup>
import {defaultEmojisMap1, defaultEmojisMap2} from "@/utils/emojis/default";
import DefaultEmoji1 from "@/components/Widgets/ChatRoom/InputFrame/DefaultEmoji1";
import DefaultEmoji2 from "@/components/Widgets/ChatRoom/InputFrame/DefaultEmoji2";
import {ref, shallowRef} from "vue";


const emojiOptions = [
  {
    name: "default1",
    component: shallowRef(DefaultEmoji1),
    map: defaultEmojisMap1,
    show: `<img src="https://res.wx.qq.com/mpres/htmledition/images/icon/emotion/13.gif"/>`
  },
  {
    name: "default2",
    component: shallowRef(DefaultEmoji2),
    map: defaultEmojisMap2,
    show: `<span>😁</span>`
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



</script>

<style scoped lang="scss">

</style>
