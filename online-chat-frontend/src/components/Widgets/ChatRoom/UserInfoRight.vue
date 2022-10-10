<template>
  <a-card class="userinfo">
    <a-card-meta>
      <template #avatar>
        <a-avatar src="https://joeschmoe.io/api/v1/random"></a-avatar>
      </template>
      <template #title>
        夕阳的刻痕
        <div class="userinfo-right">
          <FontIcons type="icon--MaleUser" />
          <FontIcons type="icon-settings" />
        </div>
      </template>
      <template #description>
        <span>路明泽不会发现我是他表哥吧</span>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script setup>
import {useStore} from "vuex";
import {createFromIconfontCN} from "@ant-design/icons-vue";

const store = useStore();
const FontIcons = createFromIconfontCN({
  scriptUrl: store.state.urls.icon_font_url
})
</script>

<style scoped>

</style>
