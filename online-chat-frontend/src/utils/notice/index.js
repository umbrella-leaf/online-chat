import {message} from "ant-design-vue";

export function ResponseToMessage(response, need_suc=true) {
  if (response.data.status === 200) {
    if (need_suc) {
      message.success(response.data.message);
    }
  } else if (response.data.status === 300) {
    message.warning(response.data.message);
  } else {
    message.error(response.data.message);
  }
}

export function ReportErrorMessage(error) {
  if (error === 'token expired' || error === 'token error') {
    return;
  }
  message.error('请求发送出错！');
}
