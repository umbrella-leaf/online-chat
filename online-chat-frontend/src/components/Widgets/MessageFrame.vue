<template>
  <div class="message">
    <div class="message-wrapper" ref="msg_list">
      <ul>
        <li v-for="(item, i) in messages" class="message-item" :key="item.time">
          <div class="time"><span>{{item.time}}</span></div>
          <div class="main" :class="{self: item.self}">
            <a-avatar class="avatar" :src="item.img"  alt=""/>
            <div class="content">
              <div class="text">{{item.content}}</div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import Bus from "@/utils/EventBus";


const msg_list = ref();
const msg_list_to_bottom = () => {
  msg_list.value.scrollTop = msg_list.value.scrollHeight;
}
Bus.$on('SendMessage', msg_list_to_bottom);


const messages = ref([
  {
    time: '2022/10/05 18:21',
    self: true,
    img: 'https://joeschmoe.io/api/v1/random',
    content: '你好！'
  },
  {
    time: '2022/10/05 18:22',
    self: false,
    img: 'https://joeschmoe.io/api/v1/random',
    content: '嗯，你好！111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
  },
  {
    time: '2022/10/05 18:23',
    self: true,
    img: 'https://joeschmoe.io/api/v1/random',
    content: '你好！'
  },
  {
    time: '2022/10/05 18:24',
    self: false,
    img: 'https://joeschmoe.io/api/v1/random',
    content: '嗯，你好！'
  }
])


onMounted(() => {
  msg_list_to_bottom();
})
</script>

<style scoped>

</style>
