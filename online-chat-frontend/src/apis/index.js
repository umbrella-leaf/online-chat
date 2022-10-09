import axios from "axios";
import store from "@/store";
import router from "@/router";
import {message} from "ant-design-vue";


// 创建一个axios实例
const service = axios.create({
  baseURL: store.state.urls.backend_url, // 请求前缀地址
  timeout: 6000, // 请求超时毫秒数
  withCredentials: true, // 异步请求携带cookie
  headers: {
    // 设置后端需要的传参类型
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  }
})

// 添加请求拦截器
service.interceptors.request.use(
  function (config) {
    const token = store.state.user.token;
    // 如果有token则添加token
    if (token) {
      config.headers.Authorization = 'Bearer ' + token;
    }
    return config;
  },
  function (error) {
    console.log(error);
    return Promise.reject(error);
  }
)

service.interceptors.response.use(
  function (response) {
    const {status, message: msg} = response.data;
    if (status === 300 && msg === 'token expired') {
      message.warning('登录过期，请重新登录！');
      store.commit('user/deleteToken');
      router.push('/sign-in');
      return Promise.reject('token expired');
    } else if (status === 400 && msg === 'token error') {
      message.error('token错误，无访问权限！');
      store.commit('user/deleteToken');
      router.push('/sign-in');
      return Promise.reject('token error');
    }
    return response;
  },
  function (error) {
    console.log(error);
    return Promise.reject(error);
  }
)

export default service
