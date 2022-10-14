import httpRequest from '@/apis/index'

interface AcceptFriendApplyParam {
    friendship_id: number
}

export function apiAcceptFriendApply(param: AcceptFriendApplyParam) {
    return httpRequest({
        url: '/friend/accept-friend-apply',
        method: 'post',
        data: param
    })
}
