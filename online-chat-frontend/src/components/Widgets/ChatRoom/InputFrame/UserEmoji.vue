<template>
  <ul class="emojiBox">
    <li>
      <div class="emoji user user-upload" @click="showEmojiUploader">
        <PlusOutlined />
      </div>
    </li>
    <template v-for="emoji in EmojiMap" :key="emoji.id">
      <li>
        <span class="emoji user" >
          <img :src="emoji.url" alt="" @click="SendUserEmoji(emoji)"/>
        </span>
      </li>
    </template>
  </ul>
  <EmojiUploader :visible="visible"/>
</template>

<script setup>
import {PlusOutlined} from "@ant-design/icons-vue"
import EmojiUploader from "@/components/Widgets/ChatRoom/InputFrame/EmojiUploader";
import {onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";

const props = defineProps({
  EmojiMap: {
    type: Array,
    default: []
  }
})

// 用户表情上传框可见
const visible = ref(false);
// 显示上传框
const showEmojiUploader = () => {
  visible.value = true;
  Bus.$emit("ChangePickerVisible", false);
}

// 发送用户表情
const SendUserEmoji = (emoji) => {
  Bus.$emit('SendUserEmoji', emoji.url);
  // 关闭表情选择框
  Bus.$emit('ChangePickerVisible', false);
}

// Bus挂载上传框状态改变事件
Bus.$on("ChangeUploaderVisible", (value) => {
  visible.value = value;
})

onUnmounted(() => {
  Bus.$off("ChangeUploaderVisible");
})

</script>

<style scoped>

</style>
