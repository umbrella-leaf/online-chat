import httpRequest from '@/apis/index'

export function apiGetInfo() {
    return httpRequest({
        url: '/user/get-info',
        method: 'get'
    })
}
