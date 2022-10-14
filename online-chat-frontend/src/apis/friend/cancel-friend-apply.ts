import httpRequest from '@/apis/index'

interface CancelFriendApplyParam {
    friendship_id: number
}

export function apiCancelFriendApply(param: CancelFriendApplyParam) {
    return httpRequest({
        url: '/friend/cancel-friend-apply',
        method: 'post',
        data: param
    })
}
