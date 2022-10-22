<template>
  <div>
    <Toolbar
      :editor="editorRef"
      :defaultConfig="toolbarConfig"
      :mode="mode"
    />
    <Editor
      style="height: 85px;"
      v-model="valueHtml"
      :defaultConfig="editorConfig"
      :mode="mode"
      @keydown="onKeyDown"
      @onCreated="handleCreated"
    />
  </div>
</template>

<script setup>
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import {onBeforeUnmount, ref, shallowRef, nextTick} from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import Bus from "@/utils/EventBus";
import {htmlUnParse} from "@/utils/emojis/htmlUnParse";

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef();
// 内容 HTML
const valueHtml = ref('')
const toolbarConfig = {
  toolbarKeys: [
    'bold', 'underline', 'italic', 'through', '|',
    'fontSize', 'fontFamily', '|',
    'color', 'bgColor', '|',
    'clearStyle', 'redo', 'undo'
  ]
};
const editorConfig = {
  placeholder: '请输入消息内容，按enter发送，按shift+enter换行' ,
  hoverbarKeys: {
    'text': {
      menuKeys: []
    },
    'image': {
      menuKeys: []
    }
  }
};

const handleCreated = (editor) => {
  editorRef.value = editor; // 记录 editor 实例，重要！
  editor.clear();
}
// 编辑器模式
const mode = ref('default');

// 按回车发送
// 按Shift+Enter换行
const onKeyDown = (e) => {
  if (e.shiftKey && e.keyCode === 13) {
    return;
  }
  if (e.keyCode === 13) {
    e.preventDefault();
    const editor = editorRef.value;
    if (editor === null) return;
    // 获取纯文本
    const content = htmlUnParse(valueHtml.value);
    const html = valueHtml.value;
    Bus.$emit('SendText', {html, content});
  }
}

// Bus挂载聚焦和清空事件
const textarea_focus = () => {
  nextTick(() => {editorRef.value.focus();})
}
Bus.$on('InputFocus', textarea_focus);
Bus.$on('ClearInput', () => {
  editorRef.value.clear();
})
// Bus挂载添加表情事件
Bus.$on('InsertDefaultEmoji', (emoji) => {
  const editor = editorRef.value;
  if (editor === null) return;
  editor.focus();
  editor.dangerouslyInsertHtml(emoji);
})


// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor == null) return;
  editor.destroy();
  Bus.$off('InputFocus');
  Bus.$off('ClearInput');
  Bus.$off('InsertDefaultEmoji');
})

</script>

<style scoped lang="scss">

</style>
