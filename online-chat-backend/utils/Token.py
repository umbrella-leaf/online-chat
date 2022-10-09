from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.Response import Response, Success, Error
import time

# 采用JWT技术，产生token并返回给前端
SECRET_KEY = 'Backend for online chat web system'


class Token:
    # 生成token，有效期60min
    @staticmethod
    def generate_auth_token(telephone, expiration=3600) -> Response:
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return Success(data=s.dumps({'telephone': telephone, 'time': int(time.time())}).decode())

    # 解析token
    @staticmethod
    def resolve_auth_token(token) -> Response:
        s = Serializer(SECRET_KEY)
        try:
            # token正确
            info = s.loads(token)
            return Success(data=info)
        except SignatureExpired:
            # token过期
            print("token已经过期")
            return Error(message='token过期')
        except BadSignature:
            # token错误
            print("token错误")
            return Error(message='token错误')
