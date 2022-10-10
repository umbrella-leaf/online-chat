<template>
  <div>
    <a-card bordered class="chatroom">
      <a-row type="flex">
        <a-col :span="24" :md="9" class="chatroom-left">
          <UserInfoLeft :UserInfo="UserInfo" />
          <a-input-search class="search-input" placeholder="搜索联系人" v-model:value="keyword" enter-button />
          <SessionsList :sessions="sessions" />
        </a-col>
        <a-col :span="24" :md="15" class="chatroom-right">
          <a-card >
            <a-card-grid style="width: 100%;" :hoverable="false">
              <UserInfoRight />
            </a-card-grid>
            <a-card-grid style="width: 100%" :hoverable="false">
              <MessageFrame />
            </a-card-grid>
            <a-card-grid style="width: 100%" :hoverable="false">
              <InputFrame />
            </a-card-grid>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>
import {computed, ref} from "vue";
import {useStore} from "vuex";
import MessageFrame from '../components/Widgets/ChatRoom/MessageFrame';
import InputFrame from '../components/Widgets/ChatRoom/InputFrame';
import {apiGetInfo} from "@/apis/user/get-info";
import {ResponseToMessage, ReportErrorMessage} from "@/utils/message";
import UserInfoLeft from "@/components/Widgets/ChatRoom/UserInfoLeft";
import SessionsList from "@/components/Widgets/ChatRoom/SessionsList";
import UserInfoRight from "@/components/Widgets/ChatRoom/UserInfoRight";


const store = useStore();
const keyword = ref('');
const sessions = ref([
  {
    avatar: 'https://joeschmoe.io/api/v1/random',
    name: '夕阳的刻痕',
    latest_msg: '你要好好上课啊。',
    latest_unread: true,
    latest_msg_time: '12: 39'
  },
  {
    avatar: 'https://joeschmoe.io/api/v1/random',
    name: '路明非',
    latest_msg: '喂，帮我自学签到一下',
    latest_unread: false,
    latest_msg_time: '12: 38'
  },
  {
    avatar: 'https://joeschmoe.io/api/v1/random',
    name: '数学老师',
    latest_msg: '你今天怎么不来上课？',
    latest_unread: false,
    latest_msg_time: '10: 07'
  },
  {
    avatar: 'https://joeschmoe.io/api/v1/random',
    name: '妈妈',
    latest_msg: '你就好好学习就可以了。',
    latest_unread: false,
    latest_msg_time: '昨天'
  },
  {
    avatar: 'https://joeschmoe.io/api/v1/random',
    name: '妈妈',
    latest_msg: '你就好好学习就可以了。',
    latest_unread: false,
    latest_msg_time: '昨天'
  },
  {
    avatar: 'https://joeschmoe.io/api/v1/random',
    name: '数学老师',
    latest_msg: '你今天怎么不来上课？',
    latest_unread: false,
    latest_msg_time: '10: 07'
  }
])


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
      console.log(error);
      ReportErrorMessage(error);
    })

}
GetUserInfo();

</script>

<style scoped>

</style>
