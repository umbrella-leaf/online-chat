# 腾讯云对象储存COS服务
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import re
import sys
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class COS:
    def __init__(self):
        self.secret_id = 'AKIDFMFrDI6dutb2C6j5AzYqrb4GAn9E2bvy'
        self.secret_key = 'nJZYGhsmQntiFVUCdngIirjKehTyC8oD'
        self.region = 'ap-guangzhou'
        self.token = None
        self.schema = 'https'
        self.bucket = 'image-1301913122'
        config = CosConfig(Region=self.region, SecretId=self.secret_id,
                           SecretKey=self.secret_key, Token=self.token,
                           Scheme=self.schema)
        self.client = CosS3Client(config)
        self.cdn_base_url = "http://image.umbrella-leaf.com"

    def upload_object(self, data, key):
        # 上传二进制流文件
        self.client.put_object(
            Bucket=self.bucket,
            Body=data,
            Key=key,
            StorageClass='STANDARD',
            EnableMD5=False
        )

    def get_object_url(self, key):
        # 获取上传文件Url
        url = self.client.get_object_url(
            Bucket=self.bucket,
            Key=key
        )
        url = re.sub(r"^https.*com", self.cdn_base_url, url)
        return url

    def object_exist(self, key):
        # 判断文件是否存在
        response = self.client.object_exists(
            Bucket=self.bucket,
            Key=key
        )
        return response


if __name__ == '__main__':
    myCos = COS()
    with open('.\\face-1.jpg', 'rb') as fp:
        myCos.upload_object(fp, '/a/face.png')
        print(myCos.get_object_url('/a/face.png'))