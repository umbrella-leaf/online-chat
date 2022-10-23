import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
from utils.Response import Response, Success, Error
from utils.Enums import MessageEmotion


class NLP:
    def __init__(self):
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        SecretId = "AKIDFMFrDI6dutb2C6j5AzYqrb4GAn9E2bvy"
        SecretKey = "nJZYGhsmQntiFVUCdngIirjKehTyC8oD"
        cred = credential.Credential(SecretId, SecretKey)

        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "nlp.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile

        # 实例化要请求产品的client对象,clientProfile是可选的
        self.client = nlp_client.NlpClient(cred, "ap-guangzhou", self.clientProfile)

    def GetEmotionAnalyzeRes(self, message) -> Response:
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.SentimentAnalysisRequest()
            params = {
                "Text": message,
                "Mode": "3class"
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个SentimentAnalysisResponse的实例，与请求对象对应
            resp = self.client.SentimentAnalysis(req)
            # 输出json格式的字符串回包
            Positive, Neutral, Negative = resp.Positive, resp.Neutral, resp.Negative
            degree = 0
            sentiment = 0
            if resp.Sentiment == "positive":
                sentiment = MessageEmotion.positive.value
                degree = Positive
            if resp.Sentiment == "neutral":
                sentiment = MessageEmotion.neutral.value
                degree = Neutral
            if resp.Sentiment == "negative":
                sentiment = MessageEmotion.negative.value
                degree = Negative
            return Success(data={"sentiment": sentiment, "degree": degree})
        except TencentCloudSDKException as err:
            print(err)
            return Error()


if __name__ == "__main__":
    nlp = NLP()
    print(nlp.GetEmotionAnalyzeRes("[捂脸]").to_dict())
