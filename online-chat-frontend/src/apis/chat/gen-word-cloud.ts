import httpRequest from '@/apis/index'

interface GenWordCloudParam {
  chat_id: number
}

export function apiGenWordCloud(param: GenWordCloudParam) {
  return httpRequest({
    url: `/chat/gen-word-cloud/${param.chat_id}`,
    method: 'get'
  })
}
