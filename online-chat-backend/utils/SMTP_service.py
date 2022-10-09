import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from utils.Response import *


# 发送验证邮箱的工具类（使用SMTP）
class SMTP:
    # 初始化连接设置
    def __init__(self):
        self.mail_host = "smtp.qq.com"
        self.mail_post = 465
        self.mail_user = "online_chat_site@qq.com"
        self.mail_pass = 'pdvksywrqwjmecfd'

    #
    def SendVerifyEmail(self, email, telephone) -> Response:
        try:
            mail_msg = f"""
            <p>尊敬的Online-chat新用户：</p>
            <p>您好！</p>
            <p>感谢您注册Online-chat在线聊天室服务，请
            <a href='http://127.0.0.1:5000/user/change-status?telephone={telephone}'>点击</a>
            该链接进行账户激活！</p>
            <p>感谢您的配合！</p>
            """
            msg = MIMEText(mail_msg, 'html', 'utf-8')
            msg['From'] = formataddr(("Online-chat在线聊天室", self.mail_user))
            msg['To'] = formataddr(("您", email))
            msg['Subject'] = "Online-chat在线聊天室用户激活邮件"

            server = smtplib.SMTP_SSL(self.mail_host, self.mail_post)
            server.login(self.mail_user, self.mail_pass)
            res = server.sendmail(self.mail_user, email, msg.as_string())
            server.quit()
            if res == {}:
                return Success(data=True)
            return Success(data=False)
        except smtplib.SMTPException as e:
            print(e)
            return Error()


if __name__ == '__main__':
    smtp = SMTP()
    smtp.SendVerifyEmail('2313678365@qq.com', '13632825509')