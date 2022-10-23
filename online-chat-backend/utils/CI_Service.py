# 腾讯云数据万象（Cloud Infinity）服务，建立在对象存储COS服务之上
from utils.COS_Service import COS
# from exts import cos


class CI:
    def __init__(self, cos: COS):
        self.client = cos.client
        self.bucket = 'text-audit-1301913122'
        # 审核共六个部分，分别为谩骂、广告、非法内容、涉政、色情、暴恐
        self.sections = ["AbuseInfo", "AdsInfo", "IllegalInfo", "PoliticsInfo", "PornInfo", "TerrorismInfo"]

    # 调用数据万象服务对消息文本进行审核
    def text_audit(self, message: str):
        res = self.client.ci_auditing_text_submit(
            Bucket=self.bucket,
            Key=None,
            Content=message.encode("UTF-8")
        )
        return res

    # 根据审核结果对消息进行过滤
    def filter_text(self, message: str, html: str):
        res = self.text_audit(message)
        res = res["JobsDetail"]["Section"][0]
        # 对六个部分审核结果进行处理
        for section in self.sections:
            audit_res = res[section]
            if audit_res["Keywords"] is not None:
                audit_keywords = audit_res["Keywords"].split(",")
                for audit_keyword in audit_keywords:
                    message = message.replace(audit_keyword, "*" * len(audit_keyword))
                    html = html.replace(audit_keyword, "*" * len(audit_keyword))
        return message, html


# if __name__ == '__main__':
#     ci = CI(cos)
#     print(ci.filter_text('我日你妈的大爷，你[打脸]这是什么垃圾玩意，你这个狗娘养的！nmsl！今晚去不去夜总会嫖娼',
#                          '<p>我日你妈的大爷，你[打脸]这是什么垃圾玩意，你这个狗娘养的！nmsl！今晚去不去夜总会嫖娼</p>'))
