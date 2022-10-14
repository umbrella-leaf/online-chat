export const SidebarRoutes = [
  {
    path: '/chat-room',
    name: '聊天室',
    component: () => import("../views/ChatRoom")
  },
  {
    path: '/user-profile',
    name: '个人中心',
    component: () => import("../views/UserProfile")
  },
  {
    path: '/user-add',
    name: '添加好友',
    component: () => import("../views/UserSearch")
  }
]
