from exts import db, cos, wcloud, ci, nlp
from user.model import User
from friend.model import FriendShip
from chat.model import Chat, Message
from emoji.model import Emoji
from utils.Response import Response, Success, Error
from utils.Enums import UserState, FriendState, MessageState, MessageType, MessageEmotion
from sqlalchemy import or_, and_, not_, func
from time import time
from datetime import datetime
import base64
import traceback
import re
import pymysql


class MySQL:
    # 封装的报错函数
    @staticmethod
    def errOut(err):
        print(f"发生错误：{str(err)}")
        print(traceback.format_exc())
        # logger.error(err, exc_info=True, stack_info=True)

    # 通过手机号+密码验证用户是否在数据库中
    @staticmethod
    def checkUser(telephone, password) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone, password=password).first()
            return Success(data=user is not None)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 查询手机号是否重复，返回data=True代表手机号存在，否则不存在
    @staticmethod
    def isPhoneExist(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user is not None)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 添加用户到数据库
    @staticmethod
    def addUser(username, email, password, telephone) -> Response:
        try:
            user = User(user_name=username, email=email,
                        password=password, telephone=telephone)
            db.session.add(user)
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 从数据库删除用户
    @staticmethod
    def deleteUser(telephone) -> Response:
        try:
            User.query.filter_by(telephone=telephone).delete()
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 改变用户验证（邮件）状态
    @staticmethod
    def ChangeStatus(telephone) -> Response:
        try:
            User.query.filter_by(telephone=telephone).update({'status': UserState.authorized.value})
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 获取用户ID
    @staticmethod
    def getUserID(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user.user_id)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 查询该ID用户是否存在
    @staticmethod
    def checkUserByID(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            return Success(data=user is not None)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 查询用户状态（是否已经验证）
    @staticmethod
    def getStatus(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user.status)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 过滤得到所需用户信息
    @staticmethod
    def filterUserInfo(user: User):
        return {
            'id': user.user_id,
            'username': user.user_name,
            'nickname': user.nickname,
            'signature': user.signature,
            'telephone': user.telephone,
            'avatar_url': user.avatar_url,
            'email': user.email
        }

    # 获取当前用户信息
    @staticmethod
    def getUserInfo(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=MySQL.filterUserInfo(user))
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 查询用户名字
    @staticmethod
    def getUserNameByID(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            return Success(data=user.nickname if user.nickname is not None else user.user_name)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 处理并上传用户头像
    @staticmethod
    def ProcessUserAvatar(telephone, avatar_base64: str):
        # 如果图像地址是base64格式，获取其有效数据
        ext_begin = avatar_base64.find('/')
        ext_end = avatar_base64.find(";", ext_begin)
        ext = avatar_base64[ext_begin + 1:ext_end]
        # 是base64则转换并上传
        if avatar_base64.find('base64') != -1:
            # 拼接文件路径
            avatar_name = f"/online-chat/avatar/{telephone}/{telephone}.{ext}"
            b = base64.b64decode(avatar_base64[ext_end + 8:])
            # 上传到cos
            cos.upload_object(b, avatar_name)
            # 返回url
            avatar_url = f"{cos.get_object_url(avatar_name)}?timestamp={int(time())}"
        # 否则按当前时间拼接url
        else:
            if avatar_base64.find('?') != -1:
                avatar_url = f"{avatar_base64.split('?')[0]}?timestamp={int(time())}"
            else:
                avatar_url = f"{avatar_base64}?timestamp={int(time())}"
        return avatar_url

    # 修改用户信息
    @staticmethod
    def changeUserInfo(telephone, info_dict) -> Response:
        try:
            if "avatar_url" in info_dict:
                avatar_base64 = info_dict["avatar_url"]
                avatar_url = MySQL.ProcessUserAvatar(telephone, avatar_base64)
                info_dict["avatar_url"] = avatar_url
            User.query.filter_by(telephone=telephone).update(info_dict)
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 获取好友列表
    @staticmethod
    def getFriendList(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            friendships = user.friendships
            userships = user.userships
            friend_list = []
            # 用户是主动加好友一方
            for friendship in friendships:
                friend_list.append({"user": {**MySQL.filterUserInfo(friendship.friend)},
                                    'id': friendship.id,
                                    'start': friendship.start_time,
                                    'status': friendship.status,
                                    'pos_id': friendship.user_id,
                                    'neg_id': friendship.friend_id})
            # 用户是被动加好友一方
            for usership in userships:
                friend_list.append({"user": {**MySQL.filterUserInfo(usership.user)},
                                    'id': usership.id,
                                    'start': usership.start_time,
                                    'status': usership.status,
                                    'pos_id': usership.user_id,
                                    'neg_id': usership.friend_id})
            # 按id排序
            friend_list = sorted(friend_list, key=lambda x: x['start'], reverse=True)
            # 合起来得到完整的好友列表
            return Success(data=friend_list)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 获取全部好友的ID（包括四个状态的好友关系，只要有好友关系就获取）
    @staticmethod
    def getAllFriendID(user_id, normal=False, active=False) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            # 获取主动添加好友列表
            friendships = user.friendships
            # 获取被动接受好友列表
            userships = user.userships
            friend_id_list = []
            for friendship in friendships:
                if normal and friendship.status != FriendState.normal.value:
                    continue
                if active and friendship.chat.online < 1:
                    continue
                friend_id_list.append(friendship.friend.user_id)
            for usership in userships:
                if normal and usership.status != FriendState.normal.value:
                    continue
                if active and usership.chat.online < 1:
                    continue
                friend_id_list.append(usership.user.user_id)
            return Success(data=friend_id_list)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 查询好友关系是否存在
    @staticmethod
    def checkFriendShip(friendship_id) -> Response:
        try:
            friendship = FriendShip.query.filter_by(id=friendship_id).first()
            return Success(data=friendship is not None)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 获取好友关系中主动方用户ID
    @staticmethod
    def getFriendShipPosID(friendship_id) -> Response:
        try:
            friendship = FriendShip.query.filter_by(id=friendship_id).first()
            return Success(data=friendship.user_id)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 修改好友关系状态
    @staticmethod
    def changeFriendStatus(friendship_id, status, accept_time=None) -> Response:
        try:
            update_dict = {"status": status.value}
            # 接收申请的同时，更新好友关系的开始时间
            if accept_time is not None:
                update_dict.setdefault("start_time", accept_time)
            FriendShip.query.filter_by(id=friendship_id).update(update_dict)
            db.session.commit()
            # 如果是接收申请，就新建一个聊天chat，然后发送一条问候消息
            if accept_time is not None:
                friendship = FriendShip.query.filter_by(id=friendship_id).first()
                chat = Chat(friendship_id=friendship_id)
                db.session.add(chat)
                db.session.commit()
                res = MySQL.sendNewMessage(chat_id=chat.id, content="我们已经是好友了，快来一起聊天吧！",
                                           html="<p>我们已经是好友了，快来一起聊天吧！</p>", sender_id=friendship.user_id)
                if res.status != 200:
                    return Error()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 删除好友关系
    @staticmethod
    def deleteFriendShip(friendship_id) -> Response:
        try:
            chat = Chat.query.filter_by(friendship_id=friendship_id).first()
            chat_id = None
            # 如果是删除好友（聊天室存在），额外返回删除的聊天ID
            if chat is not None:
                chat_id = chat.id
            FriendShip.query.filter_by(id=friendship_id).delete()
            db.session.commit()
            return Success(data=chat_id)
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 添加好友关系
    @staticmethod
    def addFriendShip(pos_id, neg_id) -> Response:
        try:
            friendship = FriendShip(user_id=pos_id, friend_id=neg_id)
            db.session.add(friendship)
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 根据用户ID user_id搜索全体用户，user_id为当前用户ID（此参数是为了过滤当前用户好友）
    @staticmethod
    def searchAllUsersByID(user_id, target_id) -> Response:
        try:
            res = MySQL.getAllFriendID(user_id)
            if res.status != 200:
                return Error()
            # 好友ID列表中包括自己，把自己也过滤
            friend_id_list = [*res.data, user_id]
            if target_id in friend_id_list:
                return Success(data={'user_list': [], 'total': 0})
            # 因为一个user_id只对应一个用户，故此处用first()
            target_user = User.query.filter_by(user_id=target_id, status=UserState.authorized.value).first()
            # 找不到该用户，返回空列表
            if target_user is None:
                return Success(data={'user_list': [], 'total': 0})
            return Success(data={'user_list': [MySQL.filterUserInfo(target_user)], 'total': 1})
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 根据关键字name搜索全体用户（用户名或昵称匹配），同样需要获取当前用户ID来过滤，此处根据前端传来的分页情况进行分页
    @staticmethod
    def searchAllUsersByName(user_id, name, curPage, pageSize) -> Response:
        try:
            res = MySQL.getAllFriendID(user_id)
            if res.status != 200:
                return Error()
            # 好友ID列表中包括自己，把自己也过滤
            friend_id_list = [*res.data, user_id]
            # 搜索用户名或昵称匹配关键字的用户
            UserNameMatch = User.user_name.ilike('%{keyword}%'.format(keyword=name))
            NickNameNone = or_(User.nickname.is_(None), User.nickname == '')
            NickNameMatch = User.nickname.ilike('%{keyword}%'.format(keyword=name))
            # 搜索非用户好友且已验证的好友
            NotUserFriend = not_(User.user_id.in_(friend_id_list))
            IsAuthorized = User.status == UserState.authorized.value
            # 目标用户昵称空则匹配用户名，否则匹配昵称，并且不是当前用户并已通过验证，根据页码curPage与页大小pageSize分页查询
            users_query = User.query.filter(
                and_(or_(and_(NickNameNone, UserNameMatch), NickNameMatch), NotUserFriend, IsAuthorized))
            # 获取总数
            total = users_query.count()
            # 分页查询
            target_users = users_query.limit(pageSize).offset((curPage - 1) * pageSize)
            target_users = [MySQL.filterUserInfo(target_user) for target_user in target_users]
            return Success(data={'user_list': target_users, 'total': total})
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 判断用户ID关键字是否是正整数（工具函数）
    @staticmethod
    def userIDKeywordIsInteger(keyword):
        try:
            n = float(keyword)
            return n.is_integer() and str(keyword).count('.') == 0 and int(n) > 0
        except Exception as e:
            return False

    # 通过friendship_id找chat_id
    @staticmethod
    def getChatIDByFriendShipID(friendship_id) -> Response:
        try:
            friendship = FriendShip.query.filter_by(id=friendship_id).first()
            return Success(data=friendship.chat.id)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 获取聊天列表
    @staticmethod
    def getChatList(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            friendships = user.friendships
            userships = user.userships
            chat_list = []
            for friendship in friendships:
                if friendship.status == FriendState.normal.value:
                    friend = friendship.friend
                    res_dict = {'friend': {**MySQL.filterUserInfo(friend)}}
                    chat = friendship.chat
                    # 查找我的未读消息数
                    unread = db.session.query(func.count(Message.id)).filter(Message.chat_id == chat.id,
                                                                             Message.sender_id != user_id,
                                                                             Message.status == MessageState.unread.value).scalar()
                    chat_dict = chat.to_dict()
                    chat_dict.update({"unread": unread})
                    res_dict.setdefault('chat', chat_dict)
                    res_dict.setdefault('latest_msg', {**chat.latest_msg.to_dict()})
                    chat_list.append(res_dict)
            for usership in userships:
                if usership.status == FriendState.normal.value:
                    friend = usership.user
                    res_dict = {'friend': {**MySQL.filterUserInfo(friend)}}
                    chat = usership.chat
                    # 查找我的未读消息数
                    unread = db.session.query(func.count(Message.id)).filter(Message.chat_id == chat.id,
                                                                             Message.sender_id != user_id,
                                                                             Message.status == MessageState.unread.value).scalar()
                    chat_dict = chat.to_dict()
                    chat_dict.update({"unread": unread})
                    res_dict.setdefault('chat', chat_dict)
                    res_dict.setdefault('latest_msg', {**chat.latest_msg.to_dict()})
                    chat_list.append(res_dict)
            chat_list = sorted(chat_list, key=lambda x: x['latest_msg']['send_time'], reverse=True)
            return Success(data=chat_list)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 过滤消息字段
    @staticmethod
    def filterMessageInfo(message: Message):
        return {
            'id': message.id,
            'time': message.send_time,
            'content': message.content,
            'html': message.html,
            'status': message.status,
            'type': message.type,
            'sentiment': message.sentiment,
            'degree': message.degree,
            'sender_id': message.sender_id,
            'sender_avatar': message.sender.avatar_url
        }

    # 获取聊天消息
    @staticmethod
    def getChatMessageList(chat_id) -> Response:
        try:
            chat = Chat.query.filter_by(id=chat_id).first()
            messages = chat.messages
            message_list = [MySQL.filterMessageInfo(message) for message in messages]
            return Success(data=message_list)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 检查当前聊天是否还存在（是否已被删除或屏蔽）
    @staticmethod
    def checkChatExist(chat_id, cur_id) -> Response:
        try:
            chat = Chat.query.filter_by(id=chat_id).first()
            # 聊天不存在，被删除
            if chat is None:
                return Success(data="delete")
            friendship = chat.friendship
            # 聊天被另一方屏蔽：我是被动方且被主动方屏蔽或我是主动方且被被动方屏蔽
            if (cur_id == friendship.friend_id and friendship.status == FriendState.pos_black.value) \
                    or (cur_id == friendship.user_id and friendship.status == FriendState.neg_black.value):
                return Success(data="black")
            return Success(data="normal")
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 发送聊天消息
    @staticmethod
    def sendNewMessage(chat_id, content, html, sender_id, msg_type=MessageType.text.value) -> Response:
        try:
            chat = Chat.query.filter_by(id=chat_id).first()
            online = chat.online
            # 聊天室只有发信者在线，那么发的消息设为（对方）未读状态，否则设为已读
            if online <= 1:
                status = MessageState.unread.value
            else:
                status = MessageState.read.value
            # 默认消息为中性，且程度为1
            sentiment = MessageEmotion.neutral.value
            degree = 1
            # 消息如果是纯图就不进行情感分析和文本过滤
            if content != "[图片表情]":
                # 消息情感分析
                res = nlp.GetEmotionAnalyzeRes(message=content)
                if res.status != 200:
                    return Error()
                sentiment = res.data["sentiment"]
                degree = res.data["degree"]
                # 过滤消息内容
                content, html = ci.filter_text(message=content, html=html)
            message = Message(chat_id=chat_id, content=content, html=html,
                              sender_id=sender_id, status=status, type=msg_type,
                              sentiment=sentiment, degree=degree)
            # 插入消息到Message表
            db.session.add(message)
            db.session.commit()
            # 更新聊天的latest_msg_id
            chat.latest_msg_id = message.id
            db.session.commit()
            # 好友关系message_cnt + 1
            friendship = chat.friendship
            friendship.message_cnt += 1
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 进入聊天室
    @staticmethod
    def enterChatRoom(chat_id, cur_id) -> Response:
        try:
            # 聊天室在线人数+1
            chat = Chat.query.filter_by(id=chat_id).first()
            chat.online += 1
            db.session.commit()
            # 所有我收到的消息(不是我发送的）设为已读
            messages = chat.messages
            for message in messages:
                if message.sender_id != cur_id:
                    message.status = MessageState.read.value
                    db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 离开聊天室
    @staticmethod
    def leaveChatRoom(chat_id) -> Response:
        try:
            # 聊天室在线人数-1
            chat = Chat.query.filter_by(id=chat_id).first()
            if chat is not None:
                # 防止部分浏览器问题导致多次执行-1
                if chat.online > 0:
                    chat.online -= 1
                    db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 亲密度计算，格式化好友关系数据
    @staticmethod
    def formatFriendship(friendship: FriendShip):
        message_cnt = friendship.message_cnt
        start_time = friendship.start_time
        # 亲密度 = 消息数 + 认识天数
        start_from_now_day = (datetime.now() - start_time).days
        return {
            **friendship.to_dict(),
            "intimacy": message_cnt + start_from_now_day
        }

    # 获取亲密度排行列表
    @staticmethod
    def getIntimacyRankList(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            intimacy_rank_list = []
            for friendship in user.friendships:
                if friendship.status == FriendState.normal.value:
                    intimacy_rank_list.append({**MySQL.formatFriendship(friendship),
                                               "friend": MySQL.filterUserInfo(friendship.friend)})
            for usership in user.userships:
                if usership.status == FriendState.normal.value:
                    intimacy_rank_list.append({**MySQL.formatFriendship(usership),
                                               "friend": MySQL.filterUserInfo(usership.user)})
            intimacy_rank_list.sort(key=lambda x: x["intimacy"], reverse=True)
            return Success(data=intimacy_rank_list)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 获取表情包
    @staticmethod
    def getEmojiList(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            emojis = [emoji.to_dict() for emoji in user.emojis]
            emojis.sort(key=lambda x: x["id"], reverse=True)
            return Success(data=emojis)
        except Exception as e:
            MySQL.errOut(e)
            return Error()

    # 处理用户表情包图片base64地址
    @staticmethod
    def processEmojiUrl(user_id, emoji_base64, emoji_id):
        # 处理base64地址得到后缀名
        ext_begin = emoji_base64.find('/')
        ext_end = emoji_base64.find(";", ext_begin)
        ext = emoji_base64[ext_begin + 1:ext_end]
        # 拼接获得表情包路径
        emoji_name = f"/online-chat/emojis/user_{user_id}/emoji_{emoji_id}.{ext}"
        b = base64.b64decode(emoji_base64[ext_end + 8:])
        # 上传表情包
        cos.upload_object(b, emoji_name)
        # 获得返回url
        emoji_url = f"{cos.get_object_url(emoji_name)}"
        return emoji_url

    # 添加用户表情包
    @staticmethod
    def addUserEmoji(user_id, emoji_base64) -> Response:
        try:
            emoji_cnt = db.session.query(func.count(Emoji.id)).scalar()
            emoji_url = MySQL.processEmojiUrl(user_id, emoji_base64, emoji_cnt + 1)
            # 插入表情地址到数据库
            emoji = Emoji(user_id=user_id, url=emoji_url)
            db.session.add(emoji)
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 生成词云
    @staticmethod
    def generateWordCloud(chat_id) -> Response:
        try:
            chat = Chat.query.filter_by(id=chat_id).first()
            messages = [message.to_dict() for message in chat.messages]
            return Success(data=wcloud.get_word_cloud(messages))
        except Exception as e:
            MySQL.errOut(e)
            return Error()


