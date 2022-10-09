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
  }
]
