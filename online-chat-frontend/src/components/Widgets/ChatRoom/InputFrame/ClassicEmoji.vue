<template>
  <ul class="emojiBox">
    <template v-for="item in Object.keys(EmojiMap)" :key="EmojiMap[item]">
      <li>
        <span class="emoji" @click="insertEmotion(item)">{{ item }}</span>
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

const insertEmotion = (item) => {
  Bus.$emit('InsertDefaultEmoji',item);
  Bus.$emit('InputFocus');
  Bus.$emit('ChangePickerVisible', false);
}
</script>

<style scoped>

</style>
