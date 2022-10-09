// 存放登录/注册/找回密码界面的路由
export const EntranceRoutes = [
  {
    path: '/sign-in',
    name: '登录',
    component: () => import(/* webpackChunkName: "about" */ '../views/SignIn')
  },
  {
    path: '/sign-up',
    name: '注册',
    component: () => import('../views/SignUp')
  }
]
