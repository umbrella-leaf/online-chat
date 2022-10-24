<template>
  <a-modal :visible="visible" title="表情包上传" ok-text="上传" @ok="uploadUserEmoji" @cancel="closeUploader">
    <div class="clearfix">
      <a-upload
        :file-list="fileList"
        list-type="picture-card"
        @preview="handlePreview"
        @remove="handleRemove"
        accept=".jpg,.png,.jpeg,.gif"
        :before-upload="beforeUpload"
        :custom-request="customUpload"
      >
        <div v-if="fileList.length < 8">
          <PlusOutlined />
          <div style="margin-top: 8px">Upload</div>
        </div>
      </a-upload>
      <a-modal :visible="previewVisible" :title="previewTitle" :footer="null" @cancel="handleCancel" >
        <img alt="example" style="width: 100%" :src="previewImage" />
      </a-modal>
    </div>
  </a-modal>
</template>

<script setup>
import {ref} from "vue";
import {message} from "ant-design-vue";
import {PlusOutlined} from "@ant-design/icons-vue"
import Bus from  "@/utils/EventBus";
import {apiAddUserEmoji} from "@/apis/emoji/add-user-emoji";
import {ReportErrorMessage, ResponseToMessage} from "@/utils/notice";

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

// 上传预览设置
const previewVisible = ref(false);
const previewImage = ref('');
const previewTitle = ref('');

// 上传列表
const emoji_list = ref([]);
// 文件回显列表
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
// 改写上传动作, 回显并
const customUpload = async(fileInfo) => {
  const { file } = fileInfo;
  const {uid, name, type} = file;

  try {
    const emoji_base64 = await fileToBase64(file)
    emoji_list.value.push({uid: uid, emoji_url: emoji_base64});
    const param = {
      name: name,
      type: type,
      url: emoji_base64,
      uid: uid,
      status: 'done',
    }
    fileList.value.push(param);
    message.success('头像上传成功！');
  } catch(err) {
    message.error(err);
  }
}
// 在上传前对文件格式进行检查
const beforeUpload  = (file) => {
  const isJpgOrPngOrGif = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif';
  if (!isJpgOrPngOrGif) {
    message.error('请上传jpeg/png格式图片！');
  }
  const isLessThan2M = file.size / 1024 / 1024 < 2;

  if (!isLessThan2M) {
    message.error('图像大小不能超过2MB！');
  }
  return isJpgOrPngOrGif && isLessThan2M;
}
// 关闭上传预览
const handleCancel = () => {
  previewVisible.value = false;
  previewTitle.value = '';
};
// 解析上传图片为base64格式
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}
// 打开上传预览
const handlePreview = async (file) => {
  if (!file.url && !file.preview) {
    file.preview = (await getBase64(file.originFileObj));
  }
  previewImage.value = file.url || file.preview;
  previewVisible.value = true;
  previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1);
};
// 移除上传的文件
const handleRemove = async (file) => {
  const { uid } = file;
  fileList.value.splice(fileList.value.findIndex(file => file["uid"] === uid), 1);
  emoji_list.value.splice(emoji_list.value.findIndex(emoji => emoji["uid"] === uid), 1);
}

// 表情文件上传
const uploadUserEmoji = () => {
  apiAddUserEmoji({emoji_list: emoji_list.value})
    .then(response => {
      ResponseToMessage(response);
      if (response.data.status === 200) {
        // 更新用户表情列表
        Bus.$emit("UpdateUserEmojis");
        closeUploader();
      }
    })
    .catch(error => {
      // console.log(error);
      ReportErrorMessage(error);
    })
}


// 关闭上传框
const closeUploader = () => {
  // 清空文件回显列表
  fileList.value.splice(0);
  // 清空上传列表
  emoji_list.value.splice(0);
  Bus.$emit("ChangeUploaderVisible", false);
  // 重新打开选择框
  Bus.$emit("ChangePickerVisible", true);
}



</script>

<style scoped lang="scss">

</style>
