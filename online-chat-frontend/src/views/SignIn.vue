<template>
  <a-form name="sign-in"
          :model="FormState"
          :wrapper-col="{offset: 3, span: 18}"
          :rules="rules"
          @finish="SignIn"
          @finishFailed="validFailed"
          ref="formRef">
    <a-form-item name="telephone" validate-first has-feedback>
      <a-input v-model:value="FormState.telephone" placeholder="请输入电话号码" :autocomplete="remember">
        <template #prefix><UserOutlined /></template>
        <template #suffix>
          <ToolTip>
            <template #content>
              ① 手机号不能为空 <br>
              ② 密码必须包含数字、字母、字符其中任意两种及以上，中间不能包含空格，且长度在8-20之间
            </template>
          </ToolTip>
        </template>
      </a-input>
    </a-form-item>
    <a-form-item name="password" validate-first has-feedback>
      <a-input-password v-model:value="FormState.password" placeholder="请输入密码" :autocomplete="remember">
        <template #prefix><LockOutlined /></template>
      </a-input-password>
    </a-form-item>
    <a-form-item name="remember" :wrapper-col="{offset: 4, span: 16}">
      <a-checkbox v-model:checked="rememberMe">记住我</a-checkbox>
    </a-form-item>
    <a-form-item :wrapper-col="{offset: 3, span: 18}">
      <a-button type="primary" html-type="submit">登录</a-button>
      <a-button type="primary" danger @click="resetForm">重置</a-button>
    </a-form-item>
  </a-form>
</template>

<script setup>
import {computed, reactive, ref} from "vue";
import {UserOutlined, LockOutlined} from '@ant-design/icons-vue';
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {message} from "ant-design-vue";
import Bus from '@/utils/EventBus';
import ToolTip from '@/components/Utils/ToolTip';
import {apiSignIn} from "@/apis/entrance/sign-in";
import md5 from 'js-md5';
import {ResponseToMessage, ReportErrorMessage} from "@/utils/notice";
import {chat_socket} from "@/utils/WebSocket";


const store = useStore();
const router = useRouter();
const rememberMe = computed({
  get() {
    return store.state.entrance.rememberMe;
  },
  set(value) {
    Bus.$emit('updateRememberMe', value);
  }
})
const remember = computed(() => {
  return rememberMe.value ? 'on' : 'new-password';
})


// 获取表单
const formRef = ref();
const FormState = reactive({
  telephone: '',
  password: ''
})
// 验证规则
const rules = {
  // 手机号验证规则
  telephone: [{required: true, whitespace: true, message: '手机号不能为空！'},
    {pattern: /^1((34[0-8])|(8\d{2})|(([35][0-35-9]|4[579]|66|7[35678]|9[1389])\d))\d{7}$/, message: '手机号格式不正确'}],
  // 密码验证规则，必须包含数字、字母、字符两种及以上，且在8-20位之间
  password: [{required: true, whitespace: true, message: '密码不能为空！'},
    {pattern: /^(?![0-9]+$)(?![a-zA-Z]+$)(?!([^(0-9a-zA-Z)])+$)\S{8,20}$/, message: '密码格式不正确'}],
}


const resetForm = () => {
  formRef.value.resetFields();
}
const SignIn = (value) => {
  const params = {
    username: FormState.telephone.toString(),
    password: md5(FormState.password).toUpperCase()
  };
  apiSignIn(params)
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        store.commit('user/updateToken', response.data.data['token']);
        router.push('/chat-room');
        chat_socket.emit("join_self", {cur_id: response.data.data['user_id']});
      }
    })
    .catch(error => {
      ReportErrorMessage(error);
    })
}
const validFailed = ({values, errorFields, outOfDate}) => {
  message.error('请检查输入！');
}

</script>

<style scoped>

</style>
