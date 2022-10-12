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
    friendship_id = request.json["friendship_id"]
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
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
    friendship_id = request.json["friendship_id"]
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    target_status = FriendState.normal
    res = MySQL.changeFriendStatus(friendship_id, target_status)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="解除屏蔽成功！").to_dict())


# 删除好友
@friend_route.route('/delete-friend', methods=['POST'])
@auth_token.login_required
def DeleteFriend():
    friendship_id = request.json["friendship_id"]
    res = MySQL.checkFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="找不到该好友关系！").to_dict())
    res = MySQL.deleteFriendShip(friendship_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="删除好友成功！").to_dict())