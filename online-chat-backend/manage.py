from flask import Flask, jsonify, g, request, make_response
from flask_socketio import SocketIO
from flask_cors import CORS
from utils.Response import Success, Warn, Error
from utils.Token import Token
from utils.dbOperation import MySQL
from exts import *
from entrance.view import entrance_route
from user.view import user_route
from friend.view import friend_route
import config
import re


app = Flask(__name__)
app.config.from_object(config)
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
db.init_app(app)
db.create_all(app=app)
# 注册蓝图
app.register_blueprint(entrance_route, url_prefix='/')
app.register_blueprint(friend_route, url_prefix='/friend')
app.register_blueprint(user_route, url_prefix='/user')
# 初始化CORS跨域模块
CORS(app, supports_credentials=True)
# 为app绑定webSocket
socketio = SocketIO()
socketio.init_app(app)


# 用户名和密码验证
@auth_user.verify_password
def verify_password(username, password):
    telephone = username
    res = MySQL.checkUser(telephone, password)
    g.res = res
    if res.status == 200 and res.data:
        g.telephone = telephone
        return True
    return False


# 用户验证错误
@auth_user.error_handler
def signin_error():
    if g.res.status == 200:
        return jsonify(Error(message='用户名和密码不正确！').to_dict())
    else:
        return jsonify(Error.error.to_dict())


# token验证
@auth_token.verify_token
def verify_token(token):
    token = re.sub(r'^"|"$', '', token)
    res = Token.resolve_auth_token(token)
    g.res = res
    if res.status == 200:
        g.telephone = res.data['telephone']
        g.user_id = res.data['user_id']
        return True
    return False


# token验证错误
@auth_token.error_handler
def token_error():
    if g.res.message == 'token过期':
        return jsonify(Warn(message='token expired').to_dict())
    else:
        return jsonify(Error(message='token error').to_dict())


if __name__ == '__main__':
    # app.run()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
