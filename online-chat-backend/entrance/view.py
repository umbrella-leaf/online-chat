from flask import Blueprint, request, g, jsonify
from utils.dbOperation import MySQL
from utils.Response import Warn, Error, Success
from utils.Enums import UserState
from utils.Token import Token
from exts import auth_user, sms, smtp


entrance_route = Blueprint('entrance', __name__)


@entrance_route.route('/sign-in', methods=['POST'])
@auth_user.login_required
def signIn():
    telephone = g.telephone
    # 检查用户状态
    res = MySQL.getStatus(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    status = res.data
    if status == UserState.unauthorized.value:
        return jsonify(Warn(message='登录失败，用户未进行邮箱验证！').to_dict())
    # 获取用户ID
    res = MySQL.getUserID(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    user_id = res.data
    # 结合手机号和用户ID生成token
    res = Token.generate_auth_token(telephone, user_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    token = res.data

    res_data = {'token': token, 'user_id': user_id}
    return jsonify(Success(data=res_data, message='登录成功！').to_dict())


@entrance_route.route('/sign-up', methods=['POST'])
def signUp():
    # 获取数据
    username = request.json.get("username")
    if username is None:
        return jsonify(Error(message="用户名不能为空！").to_dict())
    password = request.json.get("password")
    if password is None:
        return jsonify(Error(message="密码不能为空！").to_dict())
    email = request.json.get("email")
    if email is None:
        return jsonify(Error(message="邮箱不能为空！").to_dict())
    telephone = request.json.get("telephone")
    if telephone is None:
        return jsonify(Error(message="手机号不能为空！").to_dict())

    # 检查手机号是否已被注册
    res = MySQL.isPhoneExist(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if res.data:
        # 用户状态
        res = MySQL.getStatus(telephone)
        if res.status != 200:
            return jsonify(Error.error.to_dict())
        status = res.data
        # 已注册且已验证，直接报错
        if status == UserState.authorized.value:
            return jsonify(Warn(message='该手机号已被注册！').to_dict())
        # 已注册未验证，删除原有用户记录
        else:
            res = MySQL.deleteUser(telephone)
            if res.status != 200:
                return jsonify(Error.error.to_dict())
    res = MySQL.addUser(username, email, password, telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message='注册成功，请尽快前往邮箱验证！').to_dict())


@entrance_route.route('/send-code', methods=['POST'])
def sendVerifyCode():
    verifyCode = request.json.get("verifyCode")
    if verifyCode is None:
        return jsonify(Error(message="验证码不能为空！").to_dict())
    telephone = request.json.get("telephone")
    if telephone is None:
        return jsonify(Error(message="手机号不能为空！").to_dict())
    # 发送验证码
    res = sms.SendVerifyCode(verifyCode, telephone)
    if res.status != 200:
        return jsonify(Error(message="验证码发送失败！").to_dict())
    else:
        if res.data:
            return jsonify(Success(message="验证码发送成功！").to_dict())
        else:
            return jsonify(Warn(message="该号码1h内发送次数太多！").to_dict())


@entrance_route.route('/send-email', methods=['POST'])
def sendVerifyEmail():
    email = request.json.get("email")
    if email is None:
        return jsonify(Error(message="邮箱不能为空！").to_dict())
    telephone = request.json.get("telephone")
    if telephone is None:
        return jsonify(Error(message="手机号不能为空！").to_dict())
    # 发送验证邮件
    res = smtp.SendVerifyEmail(email, telephone)
    if res.status != 200:
        return jsonify(Error(message="邮件发送出错！").to_dict())
    else:
        if res.data:
            return jsonify(Success(message="邮件发送成功！").to_dict())
        else:
            return jsonify(Error(message="邮件发送失败！").to_dict())