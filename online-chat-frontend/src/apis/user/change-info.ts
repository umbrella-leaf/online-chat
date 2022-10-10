import httpRequest from '@/apis/index'

interface ChangeInfoParam {
    nickname: string,
    signature: string,
    avatar_url: string
}

export function apiChangeInfo(param: ChangeInfoParam) {
    return httpRequest({
        url: '/user/change-info',
        method: 'post',
        data: param
    })
}
