<template>
  <ul class="emojiBox">
    <template v-for="item in Object.keys(EmojiMap)" :key="EmojiMap[item]">
      <li>
        <img :src="emotion_src(item)"  alt="" class="emoji" @click="insertEmotion(item)"/>
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

const emotion_src = (item) => {
  const name = props.EmojiMap[item];
  const index = name.match(/\d+/g)[0];
  return `https://www.emojiall.com/img/platform/qq/${index}@2x.gif`;
};
const insertEmotion = (item) => {
  Bus.$emit('InsertDefaultEmoji',`[${item}]`);
  Bus.$emit('InputFocus');
  Bus.$emit('ChangePickerVisible', false);
}

</script>

<style scoped>

</style>
