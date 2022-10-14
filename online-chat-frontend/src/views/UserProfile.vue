<template>
  <div>
    <a-card bordered class="user-profile">
      <a-row :gutter="16">
        <a-col :span="24" :md="8">
          <UserInfoModify :UserInfo="UserInfo" />
        </a-col>
        <a-col :span="24" :md="8">
          <FriendsManage :FriendList="FriendList"/>
        </a-col>
        <a-col :span="24" :md="8">
          <a-card class="intimacy-rank">
            <template #title>
              <span>亲密度排行</span>
            </template>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import {apiGetInfo} from "@/apis/user/get-info";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/message";
import {computed, onUnmounted, ref} from "vue";
import {useStore} from "vuex";
import UserInfoModify from "@/components/Widgets/UserProfile/UserInfoModify";
import Bus from "@/utils/EventBus"
import FriendsManage from "@/components/Widgets/UserProfile/FriendsManage";
import {apiGetFriendList} from "@/apis/friend/get-friend-list";

const store = useStore();

// 获取用户信息
const UserInfo = computed(() => {
  return store.state.user.info;
})
const GetUserInfo = () => {
  apiGetInfo()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        const info = response.data.data;
        info.nickname = info.nickname ? info.nickname : '';
        store.commit('user/updateUserInfo', info);
      }
    })
    .catch(error => {
      ReportErrorMessage(error);
    })
}
GetUserInfo();
// 获取好友列表
// 初始化时获取好友列表
const FriendList = ref([]);
const GetFriendList = () => {
  apiGetFriendList()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        FriendList.value = response.data.data;
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}
GetFriendList();


Bus.$on('updateUserInfo', () => {
  GetUserInfo();
})
Bus.$on('updateFriendList', () => {
  GetFriendList();
})
onUnmounted(() => {
  Bus.$off('updateUserInfo');
  Bus.$off('updateFriendList');
})

</script>

<style scoped>

</style>
