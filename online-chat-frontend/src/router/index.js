import { createRouter, createWebHashHistory } from 'vue-router'
import {ConstantRoutes} from "@/router/ConstantRoutes";

const routes = [
  // {
  //   path: '/sign-in',
  //   name: '登录',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/SignIn')
  // },
  ...ConstantRoutes
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
