<template>
  <div>
    <a-input-search enter-button placeholder="输入关键字来搜索" v-model:value="keyword"></a-input-search>
    <a-spin :spinning="loading" tip="加载中……">
      <a-list item-layout="horizontal" :data-source="searching ? FilterFriendList : ApplyFriends">
        <template #renderItem="{ item }">
          <a-list-item :key="item['user']?.id">
            <a-list-item-meta>
              <template #avatar>
                <a-avatar shape="circle" :src="item['user']?.avatar_url" />
              </template>
              <template #title>
                <span class="friend-nickname">{{ DisplayName(item) }}</span>
              </template>
              <template #description>
                <span>{{ dayjs(`${item.start}+8`).fromNow() + (PositiveApply(item) ? '发出' : '接收') }}</span>
              </template>
            </a-list-item-meta>
            <template #extra>
              <a-popconfirm :title='`确定要撤销对"${DisplayName(item)}"的好友申请吗？`'
                            v-if="PositiveApply(item)"
                            @confirm="CancelFriendApply(item)">
                <a-button type="link" danger>撤销</a-button>
              </a-popconfirm>
              <div v-else>
                <a-popconfirm :title='`确定要同意"${DisplayName(item)}"的好友申请吗？`'
                              @confirm="AcceptFriendApply(item)">
                  <a-button type="link">同意</a-button>
                </a-popconfirm>
                <a-popconfirm :title='`确定要拒绝"${DisplayName(item)}"的好友申请吗？`'
                              @confirm="RefuseFriendApply(item)">
                  <a-button type="link" danger>拒绝</a-button>
                </a-popconfirm>
              </div>
            </template>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>
  </div>
</template>

<script setup>
import dayjs from "dayjs";
import {computed, ref} from "vue";
import {useStore} from "vuex";
import {apiAcceptFriendApply} from "@/apis/friend/accept-friend-apply";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/message";
import Bus from "@/utils/EventBus";
import {apiRefuseFriendApply} from "@/apis/friend/refuse-friend-apply";
import {apiCancelFriendApply} from "@/apis/friend/cancel-friend-apply";
import {chat_socket} from "@/utils/WebSocket";


const store = useStore();
const props = defineProps({
  ApplyFriends: {
    type: Array,
    default: []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// 获取当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 用户名称显示文本
const DisplayName = (item) => {
  return item['user']?.nickname || item['user']?.username;
}
// 判断申请是当前用户发出的还是接收的（主动发出的话cur_id应该等于好友关系中的pos_id）
const PositiveApply = (item) => {
  return item.pos_id === cur_id.value;
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
// 接受好友申请
const AcceptFriendApply = (item) => {
  apiAcceptFriendApply({friendship_id: item.id})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        Bus.$emit('updateFriendList');
        chat_socket.emit("alterFriendship",
          {
            type: "accept",
            cur_id: cur_id.value,
            receiver_id: item['user']?.id
          });
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}
// 拒绝好友申请
const RefuseFriendApply = (item) => {
  apiRefuseFriendApply({friendship_id: item.id})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        Bus.$emit('updateFriendList');
        chat_socket.emit("alterFriendship",
          {
            type: "refuse",
            cur_id: cur_id.value,
            receiver_id: item['user']?.id
          });
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}
// 撤销好友申请
const CancelFriendApply = (item) => {
  apiCancelFriendApply({friendship_id: item.id})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        Bus.$emit('updateFriendList');
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}

</script>

<style scoped>

</style>
