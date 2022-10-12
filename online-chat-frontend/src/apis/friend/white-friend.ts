import httpRequest from '@/apis/index'

interface WhiteFriendParam {
    friendship_id: number
}

export function apiWhiteFriend(param: WhiteFriendParam) {
    return httpRequest({
        url: '/friend/white-friend',
        method: 'post',
        data: param
    })
}
