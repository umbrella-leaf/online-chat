from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from utils.SMS_Service import SMS
from utils.SMTP_service import SMTP

db = SQLAlchemy()

# Flask应用验证
auth_user = HTTPBasicAuth()  # 用户验证
auth_token = HTTPTokenAuth()  # token验证

# 初始化SMS对象
sms = SMS()

# 初始化SMTP对象
smtp = SMTP()

