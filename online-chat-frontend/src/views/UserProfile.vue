<template>
  <div>
    <a-card bordered class="user-profile">
      <a-row :gutter="16">
        <a-col :span="24" :md="8">
          <UserInfoModify :UserInfo="UserInfo" />
        </a-col>
        <a-col :span="24" :md="8">
          <FriendsManage :FriendList="FriendList" :loading="loading"/>
        </a-col>
        <a-col :span="24" :md="8">
          <IntimacyRank :IntimacyRankList="IntimacyRankList" :loading="loading1"/>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import {apiGetInfo} from "@/apis/user/get-info";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";
import {computed, onUnmounted, ref} from "vue";
import {useStore} from "vuex";
import UserInfoModify from "@/components/Widgets/UserProfile/UserInfoModify";
import Bus from "@/utils/EventBus"
import FriendsManage from "@/components/Widgets/UserProfile/FriendsManage";
import {apiGetFriendList} from "@/apis/friend/get-friend-list";
import {chat_socket} from "@/utils/WebSocket";
import IntimacyRank from "@/components/Widgets/UserProfile/IntimacyRank";
import {apiGetIntimacyRank} from "@/apis/friend/get-intimacy-rank";

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


// 好友管理刷新标识
const loading = ref(false);
// 获取好友列表
const FriendList = ref([]);
const GetFriendList = () => {
  loading.value = true;
  apiGetFriendList()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        FriendList.value = response.data.data;
      }
      loading.value = false;
    })
    .catch(error => {
      // console.log(error);
      ReportErrorMessage(error);
      loading.value = false;
    })
}
GetFriendList();


// 亲密度排行列表刷新标识
const loading1 = ref(false);
// 获取亲密度列表
const IntimacyRankList = ref([]);
const GetIntimacyRank = () => {
  loading1.value = true;
  apiGetIntimacyRank()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        IntimacyRankList.value = response.data.data;
      }
      loading1.value = false;
    })
    .catch(error => {
      // console.log(error);
      ReportErrorMessage(error);
    })
}
GetIntimacyRank();


chat_socket.on("updateFriendList", (data) => {
  GetFriendList();
});
chat_socket.on("updateIntimacyRank", (data) => {
  GetIntimacyRank();
})


Bus.$on('updateUserInfo', () => {
  GetUserInfo();
})
Bus.$on('updateFriendList', () => {
  GetFriendList();
})
Bus.$on('updateIntimacyRank', () => {
  GetIntimacyRank();
})
onUnmounted(() => {
  chat_socket.off("updateFriendList");
  chat_socket.off("updateIntimacyRank");
  Bus.$off('updateUserInfo');
  Bus.$off('updateFriendList');
  Bus.$off('updateIntimacyRank');
})

</script>

<style scoped>

</style>
