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
import {onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";
import {createFromIconfontCN} from '@ant-design/icons-vue';
import {useStore} from "vuex";


const store = useStore();
const FontIcons = createFromIconfontCN({
  scriptUrl: store.state.urls.icon_font_url
})


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
    Bus.$emit("SendNewMessage", content.value);
    // content.value = '';
    // Bus.$emit("InputFocus");
    // Bus.$emit("MessageToBottom");
  }
}


const textarea = ref();
const textarea_focus = () => {
  textarea.value.focus();
}
Bus.$on('InputFocus', textarea_focus);
Bus.$on('ClearInput', () => {
  content.value = '';
})
onUnmounted(() => {
  Bus.$off('InputFocus');
  Bus.$off('ClearInput');
})

</script>

<style scoped>

</style>
