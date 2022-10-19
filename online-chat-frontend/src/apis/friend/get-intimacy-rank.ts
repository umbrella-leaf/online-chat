import httpRequest from '@/apis/index'

export function apiGetIntimacyRank() {
    return httpRequest({
        url: '/friend/get-intimacy-rank',
        method: 'get'
    })
}
