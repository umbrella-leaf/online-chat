from flask import Blueprint, request, g, jsonify
from utils.dbOperation import MySQL
from utils.Response import Error, Success, Warn
from utils.Enums import UserState
from exts import auth_token

user_route = Blueprint('user', __name__)


# 获取用户信息
@user_route.route('/get-info', methods=['GET'])
@auth_token.login_required
def getUserInfo():
    telephone = g.telephone
    res = MySQL.getUserInfo(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(data=res.data, message="获取用户信息成功！").to_dict())


# 修改用户验证状态路由
@user_route.route('/change-status', methods=['GET'])
def changeStatus():
    telephone = request.args.get('telephone')
    # 手机号参数不存在
    if telephone is None:
        return jsonify(Error(message="未指定手机号，无权限！").to_dict())
    res = MySQL.isPhoneExist(telephone)
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
    if res.data == UserState.authorized.value:
        return jsonify(Warn(message="该用户已经验证过！").to_dict())
    # 未验证则提交验证状态改变
    res = MySQL.ChangeStatus(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="验证成功，用户现已可正常登录！").to_dict())


# 修改用户信息
@user_route.route('/change-info', methods=['POST'])
@auth_token.login_required
def ChangeUserInfo():
    telephone = g.telephone
    info_dict = request.json
    expect_keys = ['nickname', 'signature', 'avatar_url']
    if not (set(info_dict.keys()) <= set(expect_keys)):
        return jsonify(Error(message="参数格式错误！").to_dict())
    res = MySQL.changeUserInfo(telephone, info_dict)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="信息修改成功！").to_dict())


# 获取全部用户信息
@user_route.route('/search-user', methods=['POST'])
@auth_token.login_required
def SearchUser():
    user_id = g.user_id
    search_by = request.json.get("search_by")
    search_methods = ['id', 'name']
    if search_by not in search_methods:
        return jsonify(Error(message="搜索方式不正确！").to_dict())
    keyword = request.json.get('keyword')
    if keyword is None:
        return jsonify(Error(message="关键字不能为空！").to_dict())
    # 根据用户ID搜索
    if search_by == 'id':
        # 确保ID关键字是正整数
        if not MySQL.userIDKeywordIsInteger(keyword):
            return jsonify(Warn(message="ID关键字必须为正整数！").to_dict())
        res = MySQL.searchAllUsersByID(user_id, int(keyword))
    # 根据用户名称搜索
    else:
        curPage = request.json.get('currentPage')
        if curPage is None:
            return jsonify(Error(message="页码不能为空！"))
        pageSize = request.json.get('pageSize')
        if pageSize is None:
            return jsonify(Error(message="页大小不能为空！"))
        res = MySQL.searchAllUsersByName(user_id, keyword, curPage, pageSize)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    user_list = res.data
    return jsonify(Success(data=user_list, message="搜索用户成功！").to_dict())




