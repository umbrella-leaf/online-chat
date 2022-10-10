export const SidebarRoutes = [
  {
    path: '/chatroom',
    name: '聊天室',
    component: () => import("../views/ChatRoom")
  },
  {
    path: '/profile',
    name: '用户',
    component: () => import("../views/UserProfile")
  }
]
