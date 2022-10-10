<template>
  <div class="input">
    <div class="emoji">
      <div class="operations" style="width: 11%;">
        <FontIcons type="icon-EMOTION" />
        <FontIcons type="icon-organicsearch" />
      </div>
    </div>
    <a-textarea ref="textarea" v-model:value="content" @keyup="onKeyup" placeholder="输入信息，按enter发送"></a-textarea>
    <div class="send" @click="send">
      <span>发送（R）</span>
    </div>
    <transition name="appear">
      <div class="warn" v-show="warn">
        <div class="description">不能发送空白信息</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {createFromIconfontCN} from '@ant-design/icons-vue';
import {useStore} from "vuex";


const store = useStore();
const FontIcons = createFromIconfontCN({
  scriptUrl: store.state.urls.icon_font_url
})
const textarea = ref();
const textarea_focus = () => {
  textarea.value.focus();
}
Bus.$on('SendMessage', textarea_focus);


const content = ref('');
const warn = ref(false);


const onKeyup = (e) => {
  if (e.keyCode === 13) {
    send();
  }
}
const send = () => {
  if (content.value.replace(/(^\s*)|(\s*$)/g, "").length === 0) {
    warn.value = true;
    content.value = '';
    setTimeout(() => {
      warn.value = false;
    }, 1000)
  } else {
    content.value = '';
    Bus.$emit("SendMessage");
  }
}


onMounted(() => {
  textarea_focus();
})
onUnmounted(() => {
  Bus.$off('SendMessage');
})

</script>

<style scoped>

</style>
