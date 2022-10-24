<template>
  <div>
    <a-card class="user-search">
      <a-row>
        <a-col :span="24" :md="24">
          <a-card>
            <template #title>
              <span>用户搜索</span>
            </template>
            <a-row>
              <a-col :span="24" :md="{offset: 1, span: 22}">
                <SearchInput />
                <ResultShow :loading="loading" :SearchResults="SearchResults" :total="total" :SearchState="SearchState"/>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup>

// 关键字
import {computed, onUnmounted, ref} from "vue";
import {apiSearchUser} from "@/apis/user/search-user";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";
import {apiAddFriend} from "@/apis/friend/add-friend";
import {useStore} from "vuex";
import Bus from "@/utils/EventBus";
import SearchInput from "@/components/Widgets/UserSearch/SearchInput";
import ResultShow from "@/components/Widgets/UserSearch/ResultShow";
import {chat_socket} from "@/utils/WebSocket";


const store = useStore();
// 搜索状态，包括页码、页大小、查询方式和关键字
const SearchState = ref({
  search_by: 'id',
  keyword: '',
  currentPage: 1,
  pageSize: 5
})


// 加载中标识
const loading = ref(false);
// 搜索结果用户列表
const SearchResults = ref([]);
const total = ref(0);
const SearchUsers = (search_source) => {
  loading.value = true;
  apiSearchUser(SearchState.value)
    .then(response => {
      ResponseToMessage(response, false);
      loading.value = false;
      if (response.data.status === 200) {
        SearchResults.value = response.data.data.user_list;
        total.value = response.data.data.total;
        // 若是按钮引起的获取列表，就将页码设置为1
        if (search_source.btn) {
          SearchState.value.currentPage = 1;
        }
        // 若不是添加好友引起的获取列表，就将滚动条移动到最上
        if (!search_source.add) {
          Bus.$emit('resultDisplayToTop');
        }
      } else {
        SearchResults.value = [];
        total.value = 0;
      }
    })
    .catch(error => {
      // console.log(error);
      ReportErrorMessage(error);
      loading.value = false;
    })
}


// 获取当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 发出好友申请
const SendFriendApply = (item) => {
  const param = {
    pos_id: cur_id.value,
    neg_id: item.id
  }
  apiAddFriend(param)
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        SearchUsers({btn: false, add: true});
        chat_socket.emit("alterFriendship",
          {
            type: "apply",
            cur_id: cur_id.value,
            receiver_id: item.id
          });
      }
    })
    .catch(error => {
      // console.log(error);
      ReportErrorMessage(error);
    })
}


// 给Bus挂载事件
Bus.$on('searchUsers', (params) => {
  SearchUsers(params);
})
Bus.$on('sendApply', (item) => {
  SendFriendApply(item);
})
Bus.$on('updateSearchBy', (search_by) => {
  SearchState.value.search_by  = search_by;
})
Bus.$on('updateKeyword', (keyword) => {
  SearchState.value.keyword  = keyword;
})
Bus.$on('updateCurrentPage', (currentPage) => {
  SearchState.value.currentPage  = currentPage;
})
Bus.$on('updatePageSize', (pageSize) => {
  SearchState.value.pageSize  = pageSize;
})

// 销毁时卸载
onUnmounted(() => {
  Bus.$off('searchUsers');
  Bus.$off('sendApply');
  Bus.$off('updateSearchBy');
  Bus.$off('updateKeyword');
  Bus.$off('updateCurrentPage');
  Bus.$off('updatePageSize');
})


</script>

<style scoped>

</style>
