from flask import Blueprint, request, g, jsonify
from utils.dbOperation import MySQL
from utils.Response import Error, Success, Warn
from exts import auth_token
from friend.model import FriendShip
from utils.Enums import FriendState

friend_route = Blueprint('friend', __name__)


# 获取好友列表
@friend_route.route('/get-friend-list', methods=['GET'])
@auth_token.login_required
def GetFriendList():
    telephone = g.telephone
    res = MySQL.getFriendList(telephone)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    friend_list = res.data
    return Success(data=friend_list, message="获取好友列表成功！").to_dict()


# 屏蔽好友
@friend_route.route('/black-friend', methods=['POST'])
@auth_token.login_required
def BlackFriend():
    user_id = g.user_id
    friendship_id = request.json.get("friendship_id")
    if friendship_id is None:
        return jsonify(Error(message="好友关系ID不能为空！").to_dict())
    # 查找好友关系是否存在
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    # 获取好友关系主动方ID
    res = MySQL.getFriendShipPosID(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    pos_id = res.data
    # 当前用户是主动方，状态设-1（主动方拉黑），否则设-2（被动方拉黑）
    target_status = FriendState.pos_black if user_id == pos_id else FriendState.neg_black
    res = MySQL.changeFriendStatus(friendship_id, target_status)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="屏蔽成功！").to_dict())


# 解除好友屏蔽
@friend_route.route('/white-friend', methods=['POST'])
@auth_token.login_required
def WhiteFriend():
    friendship_id = request.json.get("friendship_id")
    if friendship_id is None:
        return jsonify(Error(message="好友关系ID不能为空！").to_dict())
    # 检查好友关系是否存在
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    target_status = FriendState.normal
    # 解除屏蔽
    res = MySQL.changeFriendStatus(friendship_id, target_status)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="解除屏蔽成功！").to_dict())


# 删除好友
@friend_route.route('/delete-friend', methods=['POST'])
@auth_token.login_required
def DeleteFriend():
    friendship_id = request.json.get("friendship_id")
    if friendship_id is None:
        return jsonify(Error(message="好友关系ID不能为空！").to_dict())
    # 检查好友关系是否存在
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    # 删除好友关系
    res = MySQL.deleteFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="删除好友成功！").to_dict())


# 添加好友
@friend_route.route('/add-friend', methods=['POST'])
@auth_token.login_required
def AddFriend():
    pos_id = request.json.get("pos_id")
    if pos_id is None:
        return jsonify(Error(message="主动方ID不能为空！").to_dict())
    neg_id = request.json.get("neg_id")
    if neg_id is None:
        return jsonify(Error(message="被动方ID不能为空！").to_dict())
    # 检查主动方用户是否存在
    res = MySQL.checkUserByID(pos_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="主动方用户不存在！").to_dict())
    # 检查被动方用户是否存在
    res = MySQL.checkUserByID(neg_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="被动方用户不存在！").to_dict())
    # 添加好友关系（主动方，被动方）
    res = MySQL.addFriendShip(pos_id, neg_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message='申请成功，请到"个人中心"-"好友管理"-"申请管理"中查看！').to_dict())


# 同意好友申请
@friend_route.route('accept-friend-apply', methods=['POST'])
@auth_token.login_required
def AcceptFriendApply():
    friendship_id = request.json.get("friendship_id")
    if friendship_id is None:
        return jsonify(Error(message="好友关系ID不能为空！").to_dict())
    # 检查好友关系是否存在
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    # 同意好友申请（状态置1）
    target_status = FriendState.normal
    res = MySQL.changeFriendStatus(friendship_id, target_status)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="已同意好友申请！").to_dict())


# 拒绝好友申请（除了返回成功信息外与删除好友无区别）
@friend_route.route('/refuse-friend-apply', methods=['POST'])
@auth_token.login_required
def RefuseFriendApply():
    friendship_id = request.json.get("friendship_id")
    if friendship_id is None:
        return jsonify(Error(message="好友关系ID不能为空！").to_dict())
    # 检查好友关系是否存在
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    # 拒绝好友申请（删除）
    res = MySQL.deleteFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="已拒绝好友申请！").to_dict())


# 撤销好友申请（除了返回成功信息外与删除好友无区别）
@friend_route.route('/cancel-friend-apply', methods=['POST'])
@auth_token.login_required
def CancelFriendApply():
    friendship_id = request.json.get("friendship_id")
    if friendship_id is None:
        return jsonify(Error(message="好友关系ID不能为空！").to_dict())
    # 检查好友关系是否存在
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    # 撤销好友申请（删除）
    res = MySQL.deleteFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="已撤销好友申请！").to_dict())

