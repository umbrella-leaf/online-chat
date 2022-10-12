import httpRequest from '@/apis/index'

export function apiGetFriendList() {
    return httpRequest({
        url: '/friend/get-friend-list',
        method: 'get'
    })
}
