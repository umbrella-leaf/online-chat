import httpRequest from '@/apis/index'

export function apiGetAvatar() {
    return httpRequest({
        url: '/user/get-avatar',
        method: 'get'
    })
}
