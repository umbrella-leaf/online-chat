from flask import Blueprint, request, g, jsonify
from utils.dbOperation import MySQL
from utils.Response import Error, Success, Warn
from utils.Token import Token
from exts import auth_user, sms

user_route = Blueprint('user', __name__)


@user_route.route('/change-status', methods=['GET'])
def changeStatus():
    telephone = request.args.get('telephone')
    # 手机号参数不存在
    if telephone is None:
        return jsonify(Error(message="未指定手机号，无权限！").to_dict())
    res = MySQL.checkTel(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    # 手机号未注册
    if not res.data:
        return jsonify(Error(message="用户未注册，验证失败！").to_dict())
    # 手机号已注册，则检查是否已验证过
    res = MySQL.getStatus(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    # 已验证
    if res.data == 1:
        return jsonify(Warn(message="该用户已经验证过！").to_dict())
    # 未验证则提交验证状态改变
    res = MySQL.ChangeStatus(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="验证成功，用户现已可正常登录！").to_dict())

