import httpRequest from '@/apis/index'

interface GetMessageListParam {
    chat_id: number
}

export function apiGetMessageList(param: GetMessageListParam) {
    return httpRequest({
        url: `/chat/get-message-list/${param.chat_id}`,
        method: 'get'
    })
}
