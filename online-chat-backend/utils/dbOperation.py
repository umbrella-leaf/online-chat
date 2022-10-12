import base64

from exts import db, cos
from user.model import User
from friend.model import FriendShip
from utils.Response import Response, Success, Error
from utils.Enums import UserState, FriendState
from time import time
import pymysql


class MySQL:
    # 封装的报错函数
    @staticmethod
    def errOut(err):
        print(f"数据库发生错误：{str(err)}")

    # 通过手机号+密码验证用户是否在数据库中
    @staticmethod
    def checkUser(telephone, password) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone, password=password).first()
            return Success(data=user is not None)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 查询手机号是否重复，返回data=True代表手机号存在，否则不存在
    @staticmethod
    def checkTel(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user is not None)
        except pymysql.err as e:
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
        except pymysql.err as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 从数据库删除用户
    @staticmethod
    def delUser(telephone) -> Response:
        try:
            User.query.filter_by(telephone=telephone).delete()
            db.session.commit()
            return Success()
        except pymysql.err as e:
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
        except pymysql.err as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 获取用户ID
    @staticmethod
    def getUserID(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user.user_id)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 查询用户状态（是否已经验证）
    @staticmethod
    def getStatus(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user.status)
        except pymysql.err as e:
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
            'avatar_url': user.avatar_url
        }

    # 获取用户信息
    @staticmethod
    def getUserInfo(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=MySQL.filterUserInfo(user))
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 查询用户头像地址
    @staticmethod
    def getAvatarUrl(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data=user.avatar_url)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 处理并上传用户头像
    @staticmethod
    def ProcessUserAvatar(telephone, avatar_base64: str):
        # 如果图像地址是base64格式，获取其有效数据
        ext_begin = avatar_base64.find('/')
        ext_end = avatar_base64.find(";", ext_begin)
        ext = avatar_base64[ext_begin + 1:ext_end]
        if avatar_base64.find('base64') != -1:
            avatar_name = f"/avatar/{telephone}/{telephone}.{ext}"
            b = base64.b64decode(avatar_base64[ext_end + 8:])
            cos.upload_object(b, avatar_name)
            avatar_url = f"{cos.get_object_url(avatar_name)}?timestamp={int(time())}"
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
        except pymysql.err as e:
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
                friend_list.append({**MySQL.filterUserInfo(friendship.friend),
                                    'id': friendship.id,
                                    'start': friendship.start_time,
                                    'status': friendship.status,
                                    'pos_id': friendship.user_id,
                                    'neg_id': friendship.friend_id})
            # 用户是被动加好友一方
            for usership in userships:
                friend_list.append({**MySQL.filterUserInfo(usership.user),
                                    'id': usership.id,
                                    'start': usership.start_time,
                                    'status': usership.status,
                                    'pos_id': usership.user_id,
                                    'neg_id': usership.friend_id})
            # 按id排序
            friend_list = sorted(friend_list, key=lambda x: x['id'])
            # 合起来得到完整的好友列表
            return Success(data=friend_list)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 查询好友关系是否存在
    @staticmethod
    def checkFriendShip(friendship_id) -> Response:
        try:
            friendship = FriendShip.query.filter_by(id=friendship_id).first()
            return Success(data=friendship is not None)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 获取好友关系中主动方用户ID
    @staticmethod
    def getFriendShipPosID(friendship_id) -> Response:
        try:
            friendship = FriendShip.query.filter_by(id=friendship_id).first()
            return Success(data=friendship.user_id)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 修改好友关系状态
    @staticmethod
    def changeFriendStatus(friendship_id, status) -> Response:
        try:
            FriendShip.query.filter_by(id=friendship_id).update({"status": status.value})
            db.session.commit()
            return Success()
        except pymysql.err as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()

    # 删除好友关系
    @staticmethod
    def deleteFriendShip(friendship_id) -> Response:
        try:
            FriendShip.query.filter_by(id=friendship_id).delete()
            db.session.commit()
            return Success()
        except pymysql.err as e:
            db.session.rollback()
            MySQL.errOut(e)
            return Error()







