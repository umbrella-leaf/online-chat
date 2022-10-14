import httpRequest from '@/apis/index'

interface SearchUserParam {
    search_by: string,
    keyword: string
}

export function apiSearchUser(param: SearchUserParam) {
    return httpRequest({
        url: '/user/search-user',
        method: 'post',
        data: param
    })
}
