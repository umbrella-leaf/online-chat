from exts import socketio
from flask_socketio import emit, send, join_room, leave_room
from utils.dbOperation import MySQL


@socketio.on("connect", namespace="/chat")
def handle_connect():
    send("连接成功！")


# 加入聊天房间
@socketio.on("join", namespace="/chat")
def handle_join(data):
    chat_id = data["chat_id"]
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    join_room(room=f'chat_{chat_id}')
    MySQL.enterChatRoom(chat_id, sender_id)
    emit("updateMessageList", {"chat_id": chat_id}, room=f'chat_{chat_id}')
    emit("updateChatList", {"sender_id": sender_id, "receiver_id": receiver_id}, broadcast=True)


# 加入个人房间
@socketio.on("join_self", namespace="/chat")
def handle_join_self(data):
    cur_id = data["cur_id"]
    join_room(cur_id)


# 离开聊天房间
@socketio.on("leave", namespace="/chat")
def handle_leave(data):
    chat_id = data["chat_id"]
    leave_room(room=f'chat_{chat_id}')


# 消息发送推送
@socketio.on("send", namespace="/chat")
def handle_send(data):
    chat_id = data["chat_id"]
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    emit("updateMessageList", {"chat_id": chat_id}, room=f'chat_{chat_id}')
    emit("updateChatList", {"sender_id": sender_id, "receiver_id": receiver_id}, broadcast=True)
    emit("updateIntimacyRank", room=receiver_id)


# 用户信息修改推送
@socketio.on("modifyInfo", namespace="/chat")
def handle_modifyInfo(data):
    cur_id = data["cur_id"]
    normal_friends = MySQL.getAllFriendID(cur_id, normal=True).data
    normal_active_friends = MySQL.getAllFriendID(cur_id, normal=True, active=True).data
    all_friends = MySQL.getAllFriendID(cur_id).data
    for normal_friend in normal_friends:
        emit("updateChatList", {"sender_id": cur_id, "receiver_id": normal_friend}, room=normal_friend)
        emit("updateIntimacyRank", room=normal_friend)
    for normal_active_friend in normal_active_friends:
        emit("updateMessageList", {"force": True}, room=normal_active_friend)
    for friend in all_friends:
        emit("updateFriendList", room=friend)


# 好友管理改动推送
@socketio.on("alterFriendship", namespace="/chat")
def handle_alterFriendship(data):
    cur_id = data["cur_id"]
    receiver_id = data["receiver_id"]
    cur_name = MySQL.getUserNameByID(cur_id).data
    # 推送好友列表更新
    emit("updateFriendList", room=receiver_id)
    # 推送亲密度列表更新
    emit("updateIntimacyRank", room=receiver_id)
    # 接受申请
    if data["type"] == "accept":
        emit("notice", {"notice": f'用户"{cur_name}"同意了您的好友申请！', "type": "success"}, room=receiver_id)
        emit("updateChatList", {"sender_id": cur_id, "receiver_id": receiver_id}, room=receiver_id)
    # 解除屏蔽
    if data["type"] == "white":
        emit("updateChatList", {"sender_id": cur_id, "receiver_id": receiver_id}, room=receiver_id)
    # 屏蔽
    if data["type"] == "black":
        friendship_id = data["friendship_id"]
        chat_id = MySQL.getChatIDByFriendShipID(friendship_id).data
        emit("out_of_chat", {"chat_id": chat_id}, room=receiver_id)
        emit("notice", {"notice": f'您被好友"{cur_name}"屏蔽！', "type": "warning"}, room=receiver_id)
        emit("updateChatList", {"sender_id": cur_id, "receiver_id": receiver_id}, room=receiver_id)
    # 删除
    if data["type"] == "delete":
        chat_id = data["chat_id"]
        emit("out_of_chat", {"chat_id": chat_id}, room=receiver_id)
        emit("notice", {"notice": f'您被好友"{cur_name}"删除！', "type": "error"}, room=receiver_id)
        emit("updateChatList", {"sender_id": cur_id, "receiver_id": receiver_id}, room=receiver_id)
    # 发出申请
    if data["type"] == "apply":
        emit("notice", {"notice": f'您收到用户"{cur_name}"的好友申请！', "type": "success"}, room=receiver_id)
    # 拒绝申请
    if data["type"] == "refuse":
        emit("notice", {"notice": f'用户"{cur_name}"拒绝了您的好友申请！', "type": "warning"}, room=receiver_id)


@socketio.on("leave_self", namespace="/chat")
def handle_leave_self(data):
    cur_id = data["cur_id"]
    leave_room(cur_id)


