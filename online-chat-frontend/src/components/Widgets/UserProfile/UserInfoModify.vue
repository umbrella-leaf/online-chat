<template>
  <a-card class="user-info">
    <template #title>
      <span>个人信息</span>
    </template>
    <a-form>
      <a-form-item class="avatar-item">
        <a-upload :file-list="fileList"
                  style="display: flex;justify-content: center;align-items: center;"
                  name="avatar"
                  list-type="picture-card"
                  accept=".jpg,.png,.jpeg"
                  :show-upload-list="false"
                  :before-upload="beforeUpload"
                  :custom-request="customUpload">
          <a-avatar shape="circle" :src="FormState.avatar_url"></a-avatar>
        </a-upload>
      </a-form-item>
      <a-form-item label="用户ID" :label-col="{span: 6}" :wrapper-col="{span: 8}">
        <a-input disabled v-model:value="UserInfo.id"></a-input>
      </a-form-item>
      <a-form-item label="用户名" :label-col="{span: 6}" :wrapper-col="{span: 12}">
        <a-input disabled v-model:value="UserInfo.username"></a-input>
      </a-form-item>
      <a-form-item label="昵称" :label-col="{span: 6}" :wrapper-col="{span: 14}">
        <a-input-search readOnly v-model:value="FormState.nickname" v-show="!NickNameEditing"
                        @search="changeEditStatus('nickname', true)">
          <template #enterButton>
            <a-button type="primary" title="编辑昵称"><template #icon><EditFilled /></template></a-button>
          </template>
        </a-input-search>
        <a-input-search v-model:value="FormState.nickname" v-show="NickNameEditing" ref="nickname"
                        @search="changeEditStatus('nickname', false)">
          <template #enterButton>
            <a-button type="primary" danger title="取消编辑"><template #icon><EditFilled /></template></a-button>
          </template>
        </a-input-search>
      </a-form-item>
      <a-form-item label="联系方式" :label-col="{span: 6}" :wrapper-col="{span: 12}">
        <a-input disabled v-model:value="UserInfo.telephone"></a-input>
      </a-form-item>
      <a-form-item label="签名" :label-col="{span: 6}" :wrapper-col="{span: 18}">
        <a-input-search readOnly v-model:value="FormState.signature" v-show="!SignatureEditing"
                        @search="changeEditStatus('sign', true)">
          <template #enterButton>
            <a-button type="primary" title="编辑签名"><template #icon><EditFilled /></template></a-button>
          </template>
        </a-input-search>
        <a-input-search v-model:value="FormState.signature" v-show="SignatureEditing" ref="signature"
                        @search="changeEditStatus('sign', false)">
          <template #enterButton>
            <a-button type="primary" danger title="取消编辑"><template #icon><EditOutlined /></template></a-button>
          </template>
        </a-input-search>
      </a-form-item>
      <a-form-item :wrapper-col="{offset:3, span: 18}" class="submit-item">
        <a-button type="primary" @click="ChangeInfo" :disabled="!InfoChanged" title="保存修改">
          <template #icon>
            <FormOutlined />
          </template>
          保存
        </a-button>
        <a-button type="danger" @click="ResetInfo" title="重置修改">
          <template #icon><DeleteOutlined /></template>
          重置
        </a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup>
import {computed, nextTick, ref, watch} from "vue";
import { FormOutlined, DeleteOutlined, EditOutlined, EditFilled } from "@ant-design/icons-vue";
import {message} from "ant-design-vue";
import {apiChangeInfo} from "@/apis/user/change-info";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";
import Bus from "@/utils/EventBus";
import {chat_socket} from "@/utils/WebSocket";
import {useStore} from "vuex";


const store = useStore();
const props = defineProps({
  UserInfo: {
    type: Object,
    default: {}
  }
})
// 获取传入的UserInfo
const UserInfo = computed(() => {
  return props.UserInfo;
})
// 当前用户ID
const cur_id = computed(() => store.state.user.info.id);
// 提交表单设置，同时设置监听
const FormState = ref({
  nickname: UserInfo.value.nickname,
  signature: UserInfo.value.signature,
  avatar_url: UserInfo.value.avatar_url
});
watch(() => UserInfo.value, (newVal, oldVal) => {
  FormState.value.nickname = UserInfo.value.nickname;
  FormState.value.signature = UserInfo.value.signature;
  FormState.value.avatar_url = UserInfo.value.avatar_url;
})


// 编辑状态设置
const NickNameEditing = ref(false);
const SignatureEditing = ref(false);
const nickname = ref();
const signature = ref();
const changeEditStatus = (input, status) => {
  if (input === 'nickname') {
    NickNameEditing.value = status;
    if (status) {
      nextTick(() => {nickname.value.focus();})
    } else {
      nextTick(() => {nickname.value.blur();})
    }
  }
  if (input === 'sign') {
    SignatureEditing.value = status;
    if (status) {
      nextTick(() => {signature.value.focus();})
    } else {
      nextTick(() => {signature.value.blur();})
    }
  }
}


// 头像上传设置
const fileList = ref([]);
// img转化为Base64格式
const fileToBase64 = (file) => {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  return new Promise((resolve, reject) => {
    reader.onload = function (event) {
      if (this.result) {
        resolve(this.result)
      } else {
        console.log(event);
        reject("图片转换错误，请稍后重试");
      }
    }
  })
}
// 改写上传动作
const customUpload = async(fileInfo) => {
  const {file} = fileInfo;
  try {
    FormState.value.avatar_url = await fileToBase64(file);
    message.success('头像上传成功！');
  } catch(err) {
    message.error(err);
  }
}
// 在上传前对文件格式进行检查
const beforeUpload  = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('请上传jpeg/png格式图片！');
  }
  const isLessThan2M = file.size / 1024 / 1024 < 2;

  if (!isLessThan2M) {
    message.error('图像大小不能超过2MB！');
  }
  return isJpgOrPng && isLessThan2M;
}



// 信息发生改变时才允许提交
const NickNameChanged = computed(() => {
  return FormState.value.nickname?.toString().trim() !== UserInfo.value.nickname;
})
const SignatureChanged = computed(() => {
  return FormState.value.signature?.toString().trim() !== UserInfo.value.signature;
})
const AvatarUrlChanged = computed(() => {
  return FormState.value.avatar_url !== UserInfo.value.avatar_url;
})
const InfoChanged = computed(() => {
  return NickNameChanged.value || SignatureChanged.value || AvatarUrlChanged.value;
})
// 获取变动字段
const getChangedFormFields = () => {
  const params = {};
  if (NickNameChanged.value) {
    params.nickname = FormState.value.nickname?.toString().trim();
  }
  if (SignatureChanged.value) {
    params.signature = FormState.value.signature?.toString().trim();
  }
  if (AvatarUrlChanged.value) {
    params.avatar_url = FormState.value?.avatar_url;
  }
  return params;
}
// 提交事件
const ChangeInfo = () => {
  const params = getChangedFormFields();
  if (FormState.value.nickname.length > 15) {
    message.warning("昵称不得超过15字！");
    nextTick(() => {nickname.value.focus();})
    return;
  }
  if (FormState.value.signature.length === 0) {
    message.warning("签名不得为空！");
    nextTick(() => {signature.value.focus();})
    return;
  }
  if (FormState.value.nickname.length > 30) {
    message.warning("签名不得超过30字！");
    nextTick(() => {signature.value.focus();})
    return;
  }
  apiChangeInfo(params)
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        Bus.$emit('updateUserInfo');
        chat_socket.emit("modifyInfo", {cur_id: cur_id.value});
        changeEditStatus("nickname", false);
        changeEditStatus("sign", false);
      }
    })
    .catch(error => {
      // console.log(error);
      ReportErrorMessage(error);
    })
}
// 重置事件
const ResetInfo = () => {
  FormState.value = {
    nickname: UserInfo.value.nickname,
    signature: UserInfo.value.signature,
    avatar_url: UserInfo.value.avatar_url
  };
}

</script>

<style scoped>

</style>
