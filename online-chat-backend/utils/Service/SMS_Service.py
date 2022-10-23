from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tencentcloud.sms.v20210111 import sms_client, models

from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from utils.Response import *
import json


# 用于发送短信验证码的SMS类
class SMS:
    # 初始化
    def __init__(self):
        SecretId = "AKIDFMFrDI6dutb2C6j5AzYqrb4GAn9E2bvy"
        SecretKey = "nJZYGhsmQntiFVUCdngIirjKehTyC8oD"
        cred = credential.Credential(SecretId, SecretKey)

        self.httpProfile = HttpProfile()
        self.httpProfile.reqMethod = "POST"
        self.httpProfile.reqTimeout = 30
        self.httpProfile.endpoint = "sms.tencentcloudapi.com"

        self.clientProfile = ClientProfile()
        self.clientProfile.signMethod = "TC3-HMAC-SHA256"
        self.clientProfile.language = "en-US"
        self.clientProfile.httpProfile = self.httpProfile

        self.client = sms_client.SmsClient(cred, "ap-nanjing")

    # 发送验证码
    def SendVerifyCode(self, code, telephone) -> Response:
        try:
            req = models.SendSmsRequest()
            req.SmsSdkAppId = "1400663163"
            req.SignName = "水泥LCA信息库"
            req.TemplateId = "1366720"
            req.TemplateParamSet = [code]
            req.PhoneNumberSet = ["+86" + str(telephone)]
            req.SessionContext = ""
            req.ExtendCode = ""
            req.SenderId = ""

            resp = self.client.SendSms(req)
            resp_dict = json.loads(resp.to_json_string())
            if resp_dict['SendStatusSet'][0]['Code'] == "Ok":
                return Success(data=True)
            return Success(data=False)
        except TencentCloudSDKException as err:
            print(err)
            return Error()


if __name__ == '__main__':
    sms = SMS()
    sms.SendVerifyCode('1234', '13632825509').to_dict()

