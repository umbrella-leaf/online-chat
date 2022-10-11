import base64

from exts import db, cos
from user.model import User
from utils.Response import Response, Success, Error
from datetime import datetime
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
            register_time = datetime.now().strftime("%Y-%m-%d %X")
            user = User(user_name=username, email=email, password=password,
                        telephone=telephone, register_time=register_time)
            db.session.add(user)
            db.session.commit()
            return Success()
        except pymysql.err as e:
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
            MySQL.errOut(e)
            return Error()

    # 改变用户验证（邮件）状态
    @staticmethod
    def ChangeStatus(telephone):
        try:
            User.query.filter_by(telephone=telephone).update({'status': 1})
            db.session.commit()
            return Success()
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

    # 获取用户信息
    @staticmethod
    def getUserInfo(telephone) -> Response:
        try:
            user = User.query.filter_by(telephone=telephone).first()
            return Success(data={'id': user.user_id,
                                 'username': user.user_name,
                                 'nickname': user.nickname,
                                 'signature': user.signature,
                                 'telephone': user.telephone,
                                 'avatar_url': user.avatar_url})
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
            MySQL.errOut(e)
            return Error()




