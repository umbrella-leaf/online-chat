import httpRequest from '@/apis/index'

interface ChangeStatusParam {
    telephone: string
}

export function apiChangeStatus(param: ChangeStatusParam) {
    return httpRequest({
        url: '/user/change-status',
        method: 'get',
        params: param
    })
}
