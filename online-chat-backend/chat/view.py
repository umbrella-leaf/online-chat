from flask import Blueprint, request, g, jsonify
from utils.dbOperation import MySQL
from utils.Response import Response, Error, Success
from exts import auth_token, db
from chat.model import Chat, Message


chat_route = Blueprint('chat', __name__)


@chat_route.route('/get-chat-list', methods=['GET'])
@auth_token.login_required
def GetChatList():
    user_id = g.user_id
    res = MySQL.checkUserByID(user_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="用户不存在！").to_dict())
    res = MySQL.getChatList(user_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    chat_list = res.data
    return jsonify(Success(data=chat_list, message="获取聊天列表成功！").to_dict())


@chat_route.route('/get-message-list/<chat_id>', methods=['GET'])
@auth_token.login_required
def GetMessageList(chat_id):
    if chat_id is None:
        return jsonify(Error(message="聊天ID不能为空!").to_dict())
    res = MySQL.checkChatByID(chat_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    if not res.data:
        return jsonify(Error(message="聊天室不存在！").to_dict())
    res = MySQL.getChatMessageList(chat_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    message_list = res.data
    return jsonify(Success(data=message_list, message="聊天消息获取成功！").to_dict())


@chat_route.route('/send-new-message/<chat_id>', methods=['POST'])
@auth_token.login_required
def SendNewMessage(chat_id):
    if chat_id is None:
        return jsonify(Error(message="聊天ID不能为空!").to_dict())
    content = request.json.get('content')
    if content is None:
        return jsonify(Error(message="消息内容不能为空!").to_dict())
    sender_id = request.json.get('sender_id')
    if sender_id is None:
        return jsonify(Error(message="发送者ID不能为空!").to_dict())
    res = MySQL.sendNewMessage(chat_id, content, sender_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(message="消息发送成功！").to_dict())