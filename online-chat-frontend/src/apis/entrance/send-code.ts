import httpRequest from '@/apis/index'

interface SendCodeParam {
    username: string,
    password: string
}

export function apiSendCode(param: SendCodeParam) {
    return httpRequest({
        url: '/send-code',
        method: 'post',
        data: param
    })
}
