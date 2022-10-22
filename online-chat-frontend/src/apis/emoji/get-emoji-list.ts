import httpRequest from '@/apis/index'

export function apiGetEmojiList() {
    return httpRequest({
        url: '/emoji/get-emoji-list',
        method: 'get'
    })
}
