<template>
  <div>
    <a-card bordered class="chatroom">
      <a-row type="flex">
        <a-col :span="24" :md="9" class="chatroom-left">
          <a-card class="userinfo">
            <a-card-meta>
              <template #avatar>
                <a-avatar src="https://joeschmoe.io/api/v1/random"></a-avatar>
              </template>
              <template #title>
                伤心太平洋
              </template>
              <template #description>
                <span>我只爱你，You R My Super Star</span>
              </template>
            </a-card-meta>
          </a-card>
          <a-input-search class="search-input" placeholder="搜索联系人" v-model:value="keyword" enter-button />

          <a-list bordered item-layout="horizontal" :data-source="sessions" class="sessions-list">
            <template #renderItem="{item}">
              <a-list-item>
                <a-list-item-meta>
                  <template #avatar>
                    <a-avatar :src="item.avatar"></a-avatar>
                  </template>
                  <template #title>
                    {{ item.name }}
                  </template>
                  <template #description>
                    <span>{{ item.latest_msg }}</span>
                  </template>
                </a-list-item-meta>
                <template #actions>
                  <div class="session-right">
                    <a-avatar class="msg_read" v-if="!item.latest_unread">✔</a-avatar>
                    <a-avatar class="msg_unread" v-else></a-avatar>
                    <span>{{item.latest_msg_time}}</span>
                  </div>
                </template>
              </a-list-item>
            </template>
          </a-list>
        </a-col>
        <a-col :span="24" :md="15" class="chatroom-right">
          <a-card >
            <a-card-grid style="width: 100%;" :hoverable="false">
              <a-card class="userinfo">
                <a-card-meta>
                  <template #avatar>
                    <a-avatar src="https://joeschmoe.io/api/v1/random"></a-avatar>
                  </template>
                  <template #title>
                    夕阳的刻痕
                    <div class="userinfo-right">
                      <FontIcons type="icon--MaleUser" />
                      <FontIcons type="icon-settings" />
                    </div>
                  </template>
                  <template #description>
                    <span>路明泽不会发现我是他表哥吧</span>
                  </template>
                </a-card-meta>
              </a-card>
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
import {ref} from "vue";
import {createFromIconfontCN} from '@ant-design/icons-vue';
import {useStore} from "vuex";
import MessageFrame from '../components/Widgets/MessageFrame';
import InputFrame from '../components/Widgets/InputFrame';

const store = useStore();
const FontIcons = createFromIconfontCN({
  scriptUrl: store.state.urls.icon_font_url
})

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

</script>

<style scoped>

</style>
