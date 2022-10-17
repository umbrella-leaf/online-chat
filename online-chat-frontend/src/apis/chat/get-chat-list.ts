import httpRequest from '@/apis/index'

export function apiGetChatList() {
    return httpRequest({
        url: '/chat/get-chat-list',
        method: 'get'
    })
}
