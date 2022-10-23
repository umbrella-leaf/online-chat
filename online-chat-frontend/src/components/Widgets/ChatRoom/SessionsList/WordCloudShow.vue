<template>
  <a-modal :visible="visible" title="聊天记录词云" @cancel="CloseWordCloudImg" :footer="null">
    <div style="height: 330px;">
      <a-spin :spinning="WordCloudLoading" tip="词云图片生成中，请稍等" :indicator="indicator">
        <a-image style="width: 100%;" :src="WordCloudBase64" />
      </a-spin>
    </div>
  </a-modal>
</template>

<script setup>
import {computed, h, onUnmounted, ref} from "vue";
import {useStore} from "vuex";
import {apiGenWordCloud} from "@/apis/chat/gen-word-cloud";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";
import {LoadingOutlined} from "@ant-design/icons-vue";
import Bus from "@/utils/EventBus";

const store = useStore();
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})


const chat_id = computed(() => store.state.chat.chat_id);
// 词云图片加载中
const WordCloudLoading = ref(false);
// 词云图片base64地址（来自后端）
const WordCloudBase64 = ref('');
// 生成词云图片
const GenWordCloudImg = () => {
  WordCloudLoading.value = true;
  apiGenWordCloud({chat_id: chat_id.value})
    .then(response => {
      ResponseToMessage(response);
      WordCloudLoading.value = false;
      if (response.data.status === 200) {
        WordCloudBase64.value = response.data.data;
      }
    })
    .catch(error => {
      WordCloudLoading.value = false;
      console.log(error);
      ReportErrorMessage(error);
    })
}

// 关闭展示框
const CloseWordCloudImg = () => {
  Bus.$emit("CloseWordCloud");
}

// 加载图标
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '24px',
  },
  spin: true,
});

// Bus挂载词云图片获取事件
Bus.$on("GenWordCloud", () => {
  GenWordCloudImg();
})
onUnmounted(() => {
  Bus.$off("GenWordCloud");
})

</script>

<style scoped lang="scss">
.ant-spin-nested-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: inherit;
}

</style>
