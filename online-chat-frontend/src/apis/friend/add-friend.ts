import httpRequest from '@/apis/index'

interface AddFriendParam {
    pos_id: number,
    neg_id: number
}

export function apiAddFriend(param: AddFriendParam) {
    return httpRequest({
        url: '/friend/add-friend',
        method: 'post',
        data: param
    })
}
