<template>
  <ul class="emojiBox">
    <template v-for="(item, index) in Object.keys(EmojiMap)" :key="EmojiMap[item]">
      <li>
        <img :src="emotion_src(index)"  alt="" class="emoji" @click="insertEmotion(item)"/>
      </li>
    </template>
  </ul>
</template>

<script setup>
import Bus from "@/utils/EventBus";

const props = defineProps({
  EmojiMap: {
    type: Object,
    default: {}
  }
})

const emotion_src = (index) => {
  return `https://res.wx.qq.com/mpres/htmledition/images/icon/emotion/${index}.gif`;
};
const insertEmotion = (item) => {
  Bus.$emit('InsertDefaultEmoji',`[${item}]`);
  Bus.$emit('InputFocus');
}

</script>

<style scoped>

</style>
