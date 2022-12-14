import httpRequest from '@/apis/index'

interface SendCodeParam {
    verifyCode: string,
    telephone: string
}

export function apiSendCode(param: SendCodeParam) {
    return httpRequest({
        url: '/send-code',
        method: 'post',
        data: param
    })
}
