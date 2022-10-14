import httpRequest from '@/apis/index'

interface RefuseFriendApplyParam {
    friendship_id: number
}

export function apiRefuseFriendApply(param: RefuseFriendApplyParam) {
    return httpRequest({
        url: '/friend/refuse-friend-apply',
        method: 'post',
        data: param
    })
}
