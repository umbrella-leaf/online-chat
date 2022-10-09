import httpRequest from '@/apis/index'

interface SignInParam {
    username: string,
    password: string
}

export function apiSignIn(param: SignInParam) {
    return httpRequest({
        url: '/sign-in',
        method: 'post',
        auth: param
    })
}
