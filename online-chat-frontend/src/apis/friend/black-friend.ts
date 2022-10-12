import httpRequest from '@/apis/index'

interface BlackFriendParam {
    friendship_id: number
}

export function apiBlackFriend(param: BlackFriendParam) {
    return httpRequest({
        url: '/friend/black-friend',
        method: 'post',
        data: param
    })
}
