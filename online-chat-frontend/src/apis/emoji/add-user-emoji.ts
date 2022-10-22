import httpRequest from '@/apis/index'

interface AddUserEmojiParam {
    emoji_list: Array<any>
}

export function apiAddUserEmoji(param: AddUserEmojiParam) {
    return httpRequest({
        url: '/emoji/add-user-emoji',
        method: 'post',
        data: param
    })
}
