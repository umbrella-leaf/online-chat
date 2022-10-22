import httpRequest from '@/apis/index'

interface SendNewMessageParam {
    chat_id: number,
    content: string,
    sender_id: number,
    type: number
}

export function apiSendNewMessage(param: SendNewMessageParam) {
    return httpRequest({
        url: `/chat/send-new-message/${param.chat_id}`,
        method: 'post',
        data: param
    })
}
