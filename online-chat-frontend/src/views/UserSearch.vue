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
                <a-input-search
                  v-model:value="FormState.keyword"
                  @search="SearchUsers"
                  @keyup="onKeyup"
                  size="large"
                  enter-button placeholder="输入关键字来搜索用户">
                  <template #addonBefore>
                    <a-select v-model:value="FormState.search_by">
                      <a-select-option value="id">按ID搜索</a-select-option>
                      <a-select-option value="name">按名称搜索</a-select-option>
                    </a-select>
                  </template>
                </a-input-search>
                <a-empty v-if="SearchResults.length === 0" class="search-empty">
                  <template #description>
                    <span>未搜索到用户</span>
                  </template>
                </a-empty>
                <a-list item-layout="horizontal"
                        :data-source="SearchResults"
                        class="search-result"
                        split v-else>
                  <template #renderItem="{ item }">
                    <a-list-item>
                      <a-list-item-meta>
                        <template #title>
                          <span>{{ DisplayName(item) }}</span>
                        </template>
                        <template #avatar>
                          <a-avatar shape="circle" :src="item.avatar_url" />
                        </template>
                        <template #description>
                          <span>{{ item.signature }}</span>
                        </template>
                      </a-list-item-meta>
                      <template #actions>
                        <a-popconfirm
                          :title='`确定要向用户"${DisplayName(item)}"发出好友申请吗？`'
                          @confirm="SendFriendApply(item)">
                          <a-button type="link">发出好友申请</a-button>
                        </a-popconfirm>
                      </template>
                    </a-list-item>
                  </template>
                </a-list>
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
import {computed, ref} from "vue";
import {apiSearchUser} from "@/apis/user/search-user";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/message";
import {apiAddFriend} from "@/apis/friend/add-friend";
import {useStore} from "vuex";


const store = useStore();
const FormState = ref({
  search_by: 'id',
  keyword: ''
})

// 搜索结果用户列表
const SearchResults = ref([]);
const SearchUsers = () => {
  apiSearchUser(FormState.value)
    .then(response => {
      ResponseToMessage(response, false);
      if (response.data.status === 200) {
        SearchResults.value = response.data.data;
      }
    })
    .catch(error => {
      console.log(error);
      ReportErrorMessage(error);
    })
}
// 获取当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 用户名称显示文本
const DisplayName = (item) => {
  return item.nickname || item.username;
}
// 按回车搜索
const onKeyup = (e) => {
  if (e.keyCode === 13) {
    SearchUsers();
  }
}

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
        // 重置搜索结果
        FormState.value.keyword = '';
        SearchResults.value = SearchResults.value.filter((user) => {
          return user.id !== item.id;
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
