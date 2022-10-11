<template>
  <div>
    <a-card bordered class="user-profile">
      <a-row :gutter="16">
        <a-col :span="24" :md="8">
          <UserInfoModify :UserInfo="UserInfo" />
        </a-col>
        <a-col :span="24" :md="8">
          <a-card class="friend-manage">
            <template #title>
              <span>好友管理</span>
            </template>
          </a-card>
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

const store = useStore();

const UserInfo = computed(() => {
  return store.state.user.info;
})
const GetUserInfo = () => {
  apiGetInfo()
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        store.commit('user/updateUserInfo', response.data.data);
      }
    })
    .catch(error => {
      ReportErrorMessage(error);
    })
}
GetUserInfo();


Bus.$on('updateUserInfo', () => {
  GetUserInfo();
})
onUnmounted(() => {
  Bus.$off('updateUserInfo');
})

</script>

<style scoped>

</style>
