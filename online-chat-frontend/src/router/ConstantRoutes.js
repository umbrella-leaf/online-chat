import {SidebarRoutes} from "@/router/SidebarRoutes";
import {EntranceRoutes} from "@/router/EntranceRoutes";

export const ConstantRoutes = [
  {
    path: '/layout',
    name: 'Layout',
    redirect: '/chatroom',
    component: () => import('../layouts/DefaultLayout'),
    children: [...SidebarRoutes]
  },
  {
    path: '/',
    name: 'Entrance',
    redirect: '/sign-in',
    component: () => import('../layouts/EntranceLayout'),
    children: [...EntranceRoutes]
  },
  {
    path:'/404NotFound',
    name:'NotFound',
    meta: {title: '404'},
    component:()=>import('@/views/404NotFound.vue')
  },
  { path: '/:pathMatch(.*)*', redirect: '/404NotFound' },
]
