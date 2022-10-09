import httpRequest from '@/apis/index'

interface SignUpParam {
    username: string,
    password: string,
    email: string,
    telephone: string
}

export function apiSignUp(param: SignUpParam) {
    return httpRequest({
        url: '/sign-up',
        method: 'post',
        data: param
    })
}
