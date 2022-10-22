<template>
  <div>
    <a-empty v-if="SearchResults.length === 0" class="search-empty">
      <template #description>
        <span>未搜索到用户</span>
      </template>
    </a-empty>
    <a-spin :spinning="loading" tip="搜索中……" v-else>
      <div class="search-result" ref="search_results">
        <a-list item-layout="horizontal"
                :data-source="SearchResults"
                split>
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
      </div>
      <a-pagination show-quick-jumper
                    show-less-items
                    show-size-changer
                    :current="SearchState.currentPage"
                    :page-size="SearchState.pageSize"
                    :page-size-options="paginationProps.pageSizeOptions"
                    :total="paginationProps.total"
                    :show-total="paginationProps.showTotal"
                    @change="paginationProps.onChange">
      </a-pagination>
    </a-spin>
  </div>
</template>

<script setup>
import {computed, nextTick, onUnmounted, ref} from "vue";
import Bus from "@/utils/EventBus";


const props = defineProps({
  SearchResults: {
    type: Array,
    default: []
  },
  loading: {
    type: Boolean,
    default: false
  },
  total: {
    type: Number,
    default: 0
  },
  SearchState: {
    type: Object,
    default: {}
  }
})


// 用户名称显示文本
const DisplayName = (item) => {
  return item.nickname || item.username;
}
// 列表分页配置
const paginationProps = computed(() => {
  return {
    pageSizeOptions: ['5', '10', '15'],
    total: props.total,
    showTotal : (total, range) => {
      return `共${total}条结果，当前第${range[0]}-${range[1]}条`
    },
    onChange (page, page_size) {
      Bus.$emit('updateCurrentPage', page);
      Bus.$emit('updatePageSize', page_size)
      // 提交新的分页查询
      Bus.$emit('searchUsers', {btn: false})
    }
  }
})
// 发送好友申请
const SendFriendApply = (item) => {
  Bus.$emit('sendApply', item);
}

// 滚动条设置
const search_results = ref();
// 按钮搜索时滚动条到最上
Bus.$on('resultDisplayToTop', () => {
  // console.log(search_results.value);
  nextTick(() => {search_results.value.scrollTop = 0;})
})
// 页面销毁时卸载
onUnmounted(() => {
  Bus.$off('resultDisplayToTop');
})

</script>

<style scoped>

</style>
