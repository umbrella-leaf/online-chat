<template>
  <a-card class="userinfo">
    <a-card-meta>
      <template #avatar>
        <a-avatar :src="ChatUserInfo['avatar_url']"></a-avatar>
      </template>
      <template #title>
        {{ DisplayName }}
        <div class="userinfo-right">
          <FontIcons type="icon--MaleUser" />
          <FontIcons type="icon-index" />
        </div>
      </template>
      <template #description>
        <span>{{ ChatUserInfo['signature'] }}</span>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script setup>
import {useStore} from "vuex";
import {createFromIconfontCN} from "@ant-design/icons-vue";
import {computed} from "vue";

const store = useStore();
const props = defineProps({
  ChatUserInfo: {
    type: Object,
    default: {}
  }
})

// 展示名字
const DisplayName = computed(() => {
  return props.ChatUserInfo['nickname'] || props.ChatUserInfo['username'];
})

const FontIcons = createFromIconfontCN({
  scriptUrl: store.state.urls.icon_font_url
})
</script>

<style scoped>

</style>
