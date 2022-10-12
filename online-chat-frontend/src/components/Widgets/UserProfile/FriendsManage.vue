<template>
  <a-card class="friend-manage" :tab-list="tabList" :active-tab-key="key" @tabChange="onTabChange">
    <template #title>
      <span>好友管理</span>
    </template>
    <ListManage :ListFriends="ListFriends" v-if="key === 'list'"/>
    <ApplyManage :ApplyFriends="ApplyFriends" v-else/>
  </a-card>
</template>

<script setup>
import {computed, ref} from "vue";
import {useStore} from "vuex";
import ListManage from "@/components/Widgets/UserProfile/FriendsManage/ListManage";
import ApplyManage from "@/components/Widgets/UserProfile/FriendsManage/ApplyManage";


const store = useStore();
const props = defineProps({
  FriendList: {
    type: Array,
    default: []
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




</script>

<style scoped>

</style>
