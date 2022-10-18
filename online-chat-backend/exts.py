from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_socketio import SocketIO
from utils.SMS_Service import SMS
from utils.SMTP_service import SMTP
from utils.COS_service import COS

db = SQLAlchemy()

# Flask应用验证
auth_user = HTTPBasicAuth()  # 用户验证
auth_token = HTTPTokenAuth()  # token验证

# 初始化SMS对象
sms = SMS()

# 初始化SMTP对象
smtp = SMTP()

# 初始化COS对象
cos = COS()

# 初始化SocketIO对象
socketio = SocketIO()

