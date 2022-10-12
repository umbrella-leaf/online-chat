<template>
  <div>
    <a-input-search enter-button placeholder="输入关键字来搜索" v-model:value="keyword"></a-input-search>
    <a-list item-layout="horizontal" :data-source="searching ? FilterFriendList : ApplyFriends">
      <template #renderItem="{ item }">
        <a-list-item>
          <a-list-item-meta>
            <template #avatar>
              <a-avatar shape="circle" :src="item.avatar_url" />
            </template>
            <template #title>
              <span class="friend-nickname">{{ DisplayName(item) }}</span>
            </template>
            <template #description>
              <span>{{ dayjs(`${item.start}+8`).fromNow() }}</span>
            </template>
          </a-list-item-meta>
          <template #actions>
            <div>
              <a-popconfirm :title='`确定要同意"${DisplayName(item)}"的好友申请吗？`'
                            ok-text="确定"
                            cancel-text="取消">
                <a-button type="link">同意</a-button>
              </a-popconfirm>
              <a-popconfirm :title='`确定要拒绝"${DisplayName(item)}"的好友申请吗？`'
                            ok-text="确定"
                            cancel-text="取消">
                <a-button type="link" danger>拒绝</a-button>
              </a-popconfirm>
            </div>
          </template>
        </a-list-item>
      </template>
    </a-list>
  </div>
</template>

<script setup>
import dayjs from "@/utils/time"
import {computed, ref} from "vue";

const props = defineProps({
  ApplyFriends: {
    type: Array,
    default: []
  }
})
// 用户名称显示文本
const DisplayName = (item) => {
  return item.nickname || item.username;
}

// 搜索关键字
const keyword = ref('');
// 过滤列表
const FilterFriendList = computed(() => {
  return props.ApplyFriends.filter((friend) => {
    return DisplayName(friend).includes(keyword.value.trim());
  })
})
// 搜索状态
const searching = computed(() => {
  return keyword.value.trim() !== '';
})

</script>

<style scoped>

</style>
