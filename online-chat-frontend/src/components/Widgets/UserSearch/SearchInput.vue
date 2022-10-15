<template>
  <a-input-search
    v-model:value="FormState.keyword"
    @search="SearchUsers"
    @keyup="onKeyup"
    size="large"
    enter-button placeholder="输入关键字来搜索用户">
    <template #addonBefore>
      <a-select v-model:value="FormState.search_by">
        <a-select-option value="id">按ID搜索</a-select-option>
        <a-select-option value="name">按名称搜索</a-select-option>
      </a-select>
    </template>
  </a-input-search>
</template>

<script setup>
import {onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";

const FormState = ref({
  search_by: 'id',
  keyword: ''
})


// 搜索用户
const SearchUsers = () => {
  // 在搜索框按下后才修改父组件中的search_by和关键字参数
  Bus.$emit('updateSearchBy', FormState.value.search_by);
  Bus.$emit('updateKeyword', FormState.value.keyword);
  // 按钮查询时页码要置1
  Bus.$emit('updateCurrentPage', 1);
  Bus.$emit('searchUsers', {btn: true});
}
// 按回车搜索
const onKeyup = (e) => {
  if (e.keyCode === 13) {
    SearchUsers();
  }
}

</script>

<style scoped>

</style>
