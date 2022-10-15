<template>
  <a-card class="friend-manage" :tab-list="tabList" :active-tab-key="key" @tabChange="onTabChange">
    <template #title>
      <span>好友管理</span>
    </template>
    <template #extra>
      <a-button type="link" @click="RefreshFriendList">刷新</a-button>
    </template>
    <ListManage :ListFriends="ListFriends" v-if="key === 'list'" :loading="loading"/>
    <ApplyManage :ApplyFriends="ApplyFriends" :loading="loading" v-else/>
  </a-card>
</template>

<script setup>
import {computed, ref} from "vue";
import {useStore} from "vuex";
import Bus from "@/utils/EventBus";
import ListManage from "@/components/Widgets/UserProfile/FriendsManage/ListManage";
import ApplyManage from "@/components/Widgets/UserProfile/FriendsManage/ApplyManage";



const store = useStore();
const props = defineProps({
  FriendList: {
    type: Array,
    default: []
  },
  loading: {
    type: Boolean,
    default: false
  }
})
// tab-list
const key = ref('list')
const tabList = ref([
  {
    key: 'list',
    tab: '列表管理'
  },
  {
    key: 'apply',
    tab: '申请管理'
  }
])
const onTabChange = function (value) {
  key.value = value;
}
// 细分好友列表
const AllFriends = computed(() => {
  return props.FriendList;
})
// 未接受好友（包括反向，下同）
const ApplyFriends = computed(() => {
  return AllFriends.value.filter((friend, index) => friend.status === 0);
})
// 列表好友
const ListFriends = computed(() => {
  return AllFriends.value.filter((friend, index) => friend.status !== 0);
})

// 刷新好友列表
const RefreshFriendList = () => {
  Bus.$emit('updateFriendList');
}




</script>

<style scoped>

</style>
