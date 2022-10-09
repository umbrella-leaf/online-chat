import httpRequest from '@/apis/index'

interface SendEmailParam {
    email: string,
    telephone: string
}

export function apiSendEmail(param: SendEmailParam) {
    return httpRequest({
        url: '/send-email',
        method: 'post',
        data: param
    })
}
