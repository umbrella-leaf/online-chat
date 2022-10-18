<template>
  <div>
    <a-input-search enter-button placeholder="输入关键字来搜索" v-model:value="keyword">输入关键字来搜索</a-input-search>
    <a-spin :spinning="loading" tip="加载中……">
      <a-list item-layout="horizontal" :data-source="searching ? FilterFriendList : ListFriends">
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
                <span v-if="PositiveBlack(item)">已屏蔽</span>
                <span v-else-if="NegativeBlack(item)">已被屏蔽</span>
                <span v-else>正常</span>
              </template>
            </a-list-item-meta>
            <template #extra>
              <div>
                <a-popconfirm :title='`确定要屏蔽"${DisplayName(item)}"吗？`'
                              v-if="NoBlack(item)"
                              @confirm="BlackFriend(item)">
                  <a-button type="link">屏蔽</a-button>
                </a-popconfirm>
                <a-popconfirm :title='`确定要解除对"${DisplayName(item)}"的屏蔽吗？`'
                              v-if="PositiveBlack(item)"
                              @confirm="WhiteFriend(item)">
                  <a-button type="link">解除</a-button>
                </a-popconfirm>
                <a-popconfirm :title='`确定要删除"${DisplayName(item)}"的好友吗？`'
                              @confirm="DeleteFriend(item)">
                  <a-button type="link" danger>删除</a-button>
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
import {computed, ref} from "vue";
import {useStore} from "vuex";
import {apiBlackFriend} from "@/apis/friend/black-friend";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/message";
import Bus from "@/utils/EventBus";
import {apiWhiteFriend} from "@/apis/friend/white-friend";
import {apiDeleteFriend} from "@/apis/friend/delete-friend";
import {chat_socket} from "@/utils/WebSocket";


const store = useStore();
const props = defineProps({
  ListFriends: {
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
// 判断关系状态
// 未屏蔽
const NoBlack = (item) => {
  return item.status === 1;
}
// 当前用户主动屏蔽
const PositiveBlack = (item) => {
  return (item.status === -1 && item.pos_id === cur_id.value) || (item.status === -2 && item.neg_id === cur_id.value);
}
// 当前用户被动屏蔽
const NegativeBlack = (item) => {
  return (item.status === -1 && item.neg_id === cur_id.value) || (item.status === -2 && item.pos_id === cur_id.value);
}

// 搜索关键字
const keyword = ref('');
// 过滤列表
const FilterFriendList = computed(() => {
  return props.ListFriends.filter((friend) => {
    return DisplayName(friend).includes(keyword.value.trim());
  })
})
// 搜索状态
const searching = computed(() => {
  return keyword.value.trim() !== '';
})


// 屏蔽好友
const BlackFriend = (item) => {
  apiBlackFriend({friendship_id: item.id})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        Bus.$emit('updateFriendList');
        chat_socket.emit("alterFriendship",
          {
            type: "black",
            cur_id: cur_id.value,
            receiver_id: item['user']?.id,
            friendship_id: item.id
          });
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}
// 解除屏蔽
const WhiteFriend = (item) => {
  apiWhiteFriend({friendship_id: item.id})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        Bus.$emit('updateFriendList');
        chat_socket.emit("alterFriendship",
          {
            type: "white",
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
// 删除好友
const DeleteFriend = (item) => {
  apiDeleteFriend({friendship_id: item.id})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        // 获取删除的聊天ID
        const chat_id = response.data.data["chat_id"];
        Bus.$emit('updateFriendList');
        chat_socket.emit("alterFriendship",
          {
            type: "delete",
            cur_id: cur_id.value,
            receiver_id: item['user']?.id,
            chat_id: chat_id
          });
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
