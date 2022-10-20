<template>
  <a-card class="userinfo">
    <a-card-meta>
      <template #avatar>
        <a-avatar :src="ChatUserInfo['avatar_url']"></a-avatar>
      </template>
      <template #title>
        {{ DisplayName }}
        <div class="userinfo-right">
          <a-popover v-if="ChatUserInfo['id']">
            <template #content>
              <a-card style="width: 250px;">
                <a-card-meta>
                  <template #title>{{ DisplayName }}</template>
                  <template #avatar>
                    <a-avatar :src="ChatUserInfo['avatar_url']" />
                  </template>
                </a-card-meta>
                <a-descriptions :column="1">
                  <a-descriptions-item label="手机号">{{ ChatUserInfo['telephone'] }}</a-descriptions-item>
                  <a-descriptions-item label="邮箱">{{ ChatUserInfo['email'] }}</a-descriptions-item>
                  <a-descriptions-item label="签名">{{ ChatUserInfo['signature'] }}</a-descriptions-item>
                </a-descriptions>
              </a-card>
            </template>
            <FontIcons type="icon--MaleUser" style="cursor: pointer;"/>
          </a-popover>
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
