import httpRequest from '@/apis/index'

interface DeleteFriendParam {
    friendship_id: number
}

export function apiDeleteFriend(param: DeleteFriendParam) {
    return httpRequest({
        url: '/friend/delete-friend',
        method: 'post',
        data: param
    })
}
