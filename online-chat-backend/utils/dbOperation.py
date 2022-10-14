import base64

from exts import db, cos
from user.model import User
from friend.model import FriendShip
from utils.Response import Response, Success, Error
from utils.Enums import UserState, FriendState
from sqlalchemy import or_, and_
from time import time
from datetime import datetime
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
    def deleteUser(telephone) -> Response:
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

    # 查询该ID用户是否存在
    @staticmethod
    def checkUserByID(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            return Success(data=user is not None)
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

    # 获取当前用户信息
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
            friend_list = sorted(friend_list, key=lambda x: x['start'], reverse=True)
            # 合起来得到完整的好友列表
            return Success(data=friend_list)
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 获取全部好友的ID（包括四个状态的好友关系，只要有好友关系就获取）
    @staticmethod
    def getAllFriendID(user_id) -> Response:
        try:
            user = User.query.filter_by(user_id=user_id).first()
            # 获取主动添加好友列表
            friendships = user.friendships
            # 获取被动接受好友列表
            userships = user.userships
            friend_id_list = []
            for friendship in friendships:
                friend_id_list.append(friendship.friend.user_id)
            for usership in userships:
                friend_id_list.append(usership.user.user_id)
            return Success(data=friend_id_list)
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
            update_dict = {"status": status.value}
            if status == FriendState.normal:
                update_dict.setdefault("start_time", datetime.now().strftime("%Y-%m-%d %X"))
            FriendShip.query.filter_by(id=friendship_id).update(update_dict)
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

    # 添加好友关系
    @staticmethod
    def addFriendShip(pos_id, neg_id) -> Response:
        try:
            friendship = FriendShip(user_id=pos_id, friend_id=neg_id)
            db.session.add(friendship)
            db.session.commit()
            return Success()
        except pymysql.err as e:
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
                return Success(data=[])
            # 因为一个user_id只对应一个用户，故此处用first()
            target_user = User.query.filter_by(user_id=target_id, status=UserState.authorized.value).first()
            # 找不到该用户，返回空列表
            if target_user is None:
                return Success(data=[])
            return Success(data=[MySQL.filterUserInfo(target_user)])
        except pymysql.err as e:
            MySQL.errOut(e)
            return Error()

    # 根据关键字name搜索全体用户（用户名或昵称匹配），同样需要获取当前用户ID来过滤
    @staticmethod
    def searchAllUsersByName(user_id, name) -> Response:
        try:
            res = MySQL.getAllFriendID(user_id)
            if res.status != 200:
                return Error()
            # 好友ID列表中包括自己，把自己也过滤
            friend_id_list = [*res.data, user_id]
            # 搜索用户名或昵称匹配关键字（且已验证）的用户
            UserNameMatch = User.user_name.ilike('%{keyword}%'.format(keyword=name))
            NickNameNone = or_(User.nickname.is_(None), User.nickname == '')
            NickNameMatch = User.nickname.ilike('%{keyword}%'.format(keyword=name))
            target_users = User.query.filter(and_(
                or_(and_(NickNameNone, UserNameMatch), NickNameMatch),
                User.status == UserState.authorized.value)).all()
            target_users = [MySQL.filterUserInfo(target_user) for target_user in target_users
                            if target_user.user_id not in friend_id_list]
            return Success(data=target_users)
        except pymysql.err as e:
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
