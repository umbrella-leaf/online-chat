from flask import g, request, jsonify, Blueprint
from utils.Response import Success, Error, Warn
from utils.dbOperation import MySQL
from exts import auth_token
from emoji.model import Emoji


emoji_route = Blueprint('emoji', __name__)


@emoji_route.route('/get-emoji-list', methods=['GET'])
@auth_token.login_required
def GetEmojiList():
    user_id = g.user_id
    res = MySQL.getEmojiList(user_id)
    if res.status != 200:
        return jsonify(Error.error.to_dict())
    return jsonify(Success(data=res.data, message="获取表情列表成功！").to_dict())


@emoji_route.route('/add-user-emoji', methods=['POST'])
@auth_token.login_required
def AddUserEmoji():
    user_id = g.user_id
    emoji_list = request.json.get('emoji_list')
    if emoji_list is None:
        return jsonify(Error(message="表情列表不能为空！").to_dict())
    for emoji in emoji_list:
        emoji_base64 = emoji.get('emoji_url')
        if emoji_base64 is None:
            return jsonify(Error(message="表情base64数据不能为空！").to_dict())
        res = MySQL.addUserEmoji(user_id, emoji_base64)
        if res.status != 200:
            return jsonify(Error.error.to_dict())
    return jsonify(Success(message="添加表情成功！").to_dict())