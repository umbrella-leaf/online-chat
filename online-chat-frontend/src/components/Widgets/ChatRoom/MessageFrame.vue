<template>
  <div class="message">
    <div class="message-wrapper" ref="msg_list">
      <ul>
        <li v-for="(item, i) in MessageList" class="message-item">
          <div class="time"><span>{{ TimeDisplay(item) }}</span></div>
          <div class="main" :class="{self: IsSelfSend(item)}">
            <a-avatar class="avatar" :src="item.sender_avatar"  alt=""/>
            <div class="content">
              <div class="text">{{ item.content }}</div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {computed, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {useStore} from "vuex";
import dayjs from "dayjs";
import {msgTimeFormat} from "@/utils/time/msgTimeFormat";


const store = useStore();
const props = defineProps({
  MessageList: {
    type: Array,
    default: []
  }
})


// 获取当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 判断消息是否是自己发的
const IsSelfSend = (item) => {
  return item.sender_id === cur_id.value;
}
// 时间显示格式
const TimeDisplay = (item) => {
  return msgTimeFormat(item.time);
}
// 按照时间过滤消息
const FilterMessageList = computed(() => {

})

const msg_list = ref();
const msg_list_to_bottom = () => {
  msg_list.value.scrollTop = msg_list.value.scrollHeight;
}
Bus.$on('MessageToBottom', msg_list_to_bottom);
onUnmounted(() => {
  Bus.$off('MessageToBottom');
})
</script>

<style scoped>

</style>
