<template>
  <a-form name="sign-up"
          :model="FormState"
          :wrapper-col="{offset: 3, span: 18}"
          :rules="rules"
          @finish="SignUp"
          @finishFailed="validFailed"
          ref="formRef">
    <!--输入用户名-->
    <a-form-item name="username" has-feedback validate-first>
      <a-input v-model:value="FormState.username" placeholder="请输入用户名" autocomplete="new-password">
        <template #prefix><UserOutlined /></template>
        <template #suffix>
          <ToolTip>
            <template #content>
              ① 用户名不能为空，不能包含空格，只能包含汉字、数字、字母及下划线，且长度在2-15之间 <br>
              ② 密码必须包含数字、字母、字符其中任意两种及以上，中间不能包含空格，且长度在8-20之间
            </template>
          </ToolTip>
        </template>
      </a-input>
    </a-form-item>
    <!--输入密码-->
    <a-form-item name="password" has-feedback validate-first>
      <a-input-password v-model:value="FormState.password" placeholder="请输入密码" autocomplete="new-password">
        <template #prefix><LockOutlined /></template>
      </a-input-password>
    </a-form-item>
    <!--输入密码-->
    <a-form-item name="checkPassword" has-feedback validate-first>
      <a-input-password v-model:value="FormState.checkPassword" placeholder="请再次输入密码" autocomplete="new-password">
        <template #prefix><LockOutlined /></template>
      </a-input-password>
    </a-form-item>
    <!--输入邮箱-->
    <a-form-item name="email" has-feedback validate-first>
      <a-input v-model:value="FormState.email" placeholder="请输入邮箱" autocomplete="new-password">
        <template #prefix><MailOutlined /></template>
        <template #suffix>
          <ToolTip content="邮箱不能为空，注册完成并验证后账号方可使用" />
        </template>
      </a-input>
    </a-form-item>
    <!--输入手机号码-->
    <a-form-item name="telephone" has-feedback validate-first>
      <a-input v-model:value="FormState.telephone" placeholder="请输入电话号码" autocomplete="new-password">
        <template #prefix><PhoneOutlined /></template>
        <template #suffix>
          <ToolTip content="手机号码不可为空" />
        </template>
      </a-input>
    </a-form-item>
    <!--输入验证码-->
    <a-form-item name="verifyCode" has-feedback validate-first>
      <a-input-search v-model:value="FormState.verifyCode"
                      placeholder="请输入验证码"
                      autocomplete="new-password"
                      @search="sendVerifyCode">
        <template #prefix><MessageOutlined /></template>
        <template #enterButton>
          <a-button type="primary" :disabled="verifyCodeTimer.disabled">
            {{ verifyCodeMessage }}
          </a-button>
        </template>
      </a-input-search>
    </a-form-item>
    <a-form-item :wrapper-col="{offset: 3, span: 18}">
      <a-button type="primary" html-type="submit">注册</a-button>
      <a-button type="primary" danger @click="resetForm">重置</a-button>
    </a-form-item>
  </a-form>
</template>

<script setup>

import {computed, reactive, ref} from "vue";
import {UserOutlined, LockOutlined, MailOutlined, PhoneOutlined, MessageOutlined} from '@ant-design/icons-vue';
import {useStore} from "vuex";
import Bus from '@/utils/EventBus';
import ToolTip from "@/components/Utils/ToolTip";
import {message} from "ant-design-vue";
import md5 from "js-md5";
import {apiSignUp} from "@/apis/entrance/sign-up";
import {apiSendCode} from "@/apis/entrance/send-code";
import {apiSendEmail} from "@/apis/entrance/send-email";
import {ResponseToMessage, ReportErrorMessage} from "@/utils/notice";
import {useRouter} from "vue-router";


const store = useStore();
const router = useRouter();


// 验证码发送计时器
const verifyCodeTimer = reactive({
  count: 0,
  disabled: false,
  timer: null
})
// 验证码发送按钮显示文本
const verifyCodeMessage = computed(() => {
  return verifyCodeTimer.count ? `${verifyCodeTimer.count}秒后重发` : '发送验证码';
})
// 从vuex获取上次发送验证码的时间和码型
const lastCodeVerifyTime = computed(() => {
  return store.state.entrance.lastCodeVerify[FormState.telephone]?.time;
})
const lastCodeVerifyCode = computed(() => {
  return store.state.entrance.lastCodeVerify[FormState.telephone]?.code;
})


// 获取表单
const formRef = ref();
const FormState = reactive({
  username: '',
  password: '',
  checkPassword: '',
  email: '',
  telephone: '',
  verifyCode: ''
})


// 重置表单
const resetForm = () => {
  formRef.value.resetFields();
}
// 自定义密码验证（这一动作包含了修改密码时调用确认密码的验证）
const validatePassword = async(_rule, value) => {
  if (FormState.password.trim() === '') {
    return Promise.reject('密码不能为空！');
  }
  const pattern = /^(?![0-9]+$)(?![a-zA-Z]+$)(?!([^(0-9a-zA-Z)])+$)\S{8,20}$/;
  if (!(pattern.test(value))) {
    return Promise.reject('密码必须包含数字、字母、字符其中任意两种及以上，且长度在8-20之间');
  }
  if (FormState.checkPassword !== '') {
    formRef.value.validateFields('checkPassword')
    .then(() => {})
    .catch(() => {});
    return Promise.resolve();
  }
  return Promise.resolve();
}
// 自定义确认密码验证
const checkPassword = async(_rule, value) => {
  if (value.trim() === '') {
    return Promise.reject('确认密码不能为空！');
  }
  if (value !== FormState.password) {
    return Promise.reject('两次输入密码不一致！');
  }
  return Promise.resolve();
}
// 自定义电话号码验证（用于更改电话号时触发验证码的verify）
const verifyTelephone = async(_rule, value) => {
  if (value.trim() === '') {
    return Promise.reject('电话号码不能为空！');
  }
  const pattern = /^1((34[0-8])|(8\d{2})|(([35][0-35-9]|4[579]|66|7[35678]|9[1389])\d))\d{7}$/;
  if (!(pattern.test(value))) {
    return Promise.reject('电话号码格式不正确！');
  }
  if (FormState.verifyCode) {
    formRef.value.validateFields('verifyCode')
    .then(() => {})
    .catch(() => {});
    return Promise.resolve();
  }
  return Promise.resolve();
}
// 自定义验证码验证
const checkVerifyCode = async(_rule, value) => {
  if (value.trim() === '') {
    return Promise.reject('验证码不能为空！');
  }
  if (value !== lastCodeVerifyCode.value) {
    return Promise.reject('验证码输入不正确！');
  }
  return Promise.resolve();
}


// 生成验证码,digits为位数
const generateVerifyCode = (digits) => {
  let verifyCode = "";
  for (let i = 0;i < digits;i++) {
    verifyCode += Math.floor(Math.random() * 10);
  }
  return verifyCode;
}
// 发送验证码
const sendVerifyCode = () => {
  // 重置验证码字段
  formRef.value.resetFields('verifyCode');
  // 检查电话号码是否正确
  formRef.value.validateFields('telephone')
  .then(() => {
    const TIME_COUNT = 60;
    if (!verifyCodeTimer.timer) {
      // 获取当前时间戳，和上次发送时间比较，抛出等待警告
      const time = Math.floor(new Date().getTime() / 1000);
      const lastVerifiedCodeTime = lastCodeVerifyTime.value;
      if (lastVerifiedCodeTime && time - lastVerifiedCodeTime <= 60) {
        const duration = 60 - (time - lastVerifiedCodeTime);
        message.warning(`请等待${duration}秒后重新发送！`);
        return;
      }
      const params = {
        verifyCode: generateVerifyCode(6).toString(),
        telephone: FormState.telephone.toString()
      }
      apiSendCode(params)
        .then(response => {
          ResponseToMessage(response);
          if (response.data.status === 200) {
            // 提交到vuex，以避免频繁发送验证码，以及判断验证码是否过期
            const phone = FormState.telephone;
            const code = params.verifyCode;
            Bus.$emit('updateLastCodeVerify', {phone, code, time});
            // 设置验证码发送计时器以及按钮
            verifyCodeTimer.disabled = true;
            verifyCodeTimer.count = TIME_COUNT;
            verifyCodeTimer.timer = setInterval(() => {
              if (verifyCodeTimer.count > 0 && verifyCodeTimer.count <= TIME_COUNT) {
                verifyCodeTimer.count -= 1;
              } else {
                verifyCodeTimer.disabled = false;
                clearInterval(verifyCodeTimer.timer);
                verifyCodeTimer.timer = null;
              }
            }, 1000);
          }
        })
        .catch((error) => {
          ReportErrorMessage(error);
        })
    }
  })
  .catch(() => {
    message.warning('请输入正确的手机号码！');
  })
}
// 提交成功，注册
const SignUp = (value) => {
  const time = Math.floor(new Date().getTime() / 1000);
  // 如果验证码超过15分钟，就删除原来的记录
  if (lastCodeVerifyTime.value && time - lastCodeVerifyTime.value > 900) {
    message.error('验证码过期，请重新发送！');
    Bus.$emit('clearLastCodeVerify', FormState.telephone);
  } else {
    const params = {
      username: FormState.username,
      password: md5(FormState.password).toUpperCase(),
      email: FormState.email,
      telephone: FormState.telephone
    }
    apiSignUp(params)
      .then(response => {
        ResponseToMessage(response);
        if (response.data.status === 200) {
          const params = {
            email: FormState.email,
            telephone: FormState.telephone
          }
          apiSendEmail(params)
            .then(response => {
              ResponseToMessage(response, false);
              if (response.data.status === 200) {
                store.commit('entrance/clearLastCodeVerify', FormState.telephone);
                router.push('/sign-in');
              }
            })
            .catch(error => {
              ReportErrorMessage(error);
            })
        }
      })
      .catch(error => {
        ReportErrorMessage(error);
      })
  }
}
// 提交失败，报错
const validFailed = ({values, errorFields, outOfDate}) => {
  message.error('请检查输入！');
}


// 验证规则
const rules = {
  // 用户名验证规则，只能包含汉字、数字、字母及下划线，且长度在2-15之间
  username: [{required: true, whitespace: true, message: '用户名不能为空！'},
    {pattern: /^[\p{Unified_Ideograph}0-9a-zA-Z_]{2,15}$/u, message: '用户名只能包含汉字、数字、字母及下划线，且长度在2-15之间'}],
  // 密码验证规则，必须包含数字、字母、字符两种及以上，且在8-20位之间
  password: [{required:true, whitespace:true, validator:validatePassword, trigger:'change'}],
  // 确认密码验证规则，必须和输入密码一致
  checkPassword: [{required:true, whitespace:true, validator: checkPassword, trigger: 'change'}],
  // 验证邮箱规则
  email: [{required: true, whitespace: true, message: '邮箱不能为空！'},
    {pattern: /^[a-zA-Z0-9]+([-_.][A-Za-z\d]+)*@([a-zA-Z0-9]+[-.])+[A-Za-zd]{2,5}$/, message: '邮箱格式不正确！'}],
  // 手机号验证规则
  telephone: [{required:true, whitespace:true, validator:verifyTelephone, trigger:'change'}],
  // 验证码验证
  verifyCode: [{required:true, whitespace:true, validator:checkVerifyCode, trigger:'change'}]
}

</script>


<style scoped>

</style>
