from exts import db
from utils.Enums import UserState
from sqlalchemy.sql import func
from sqlalchemy import text


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    telephone = db.Column(db.String(13), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255), nullable=False,
                           server_default="http://image.umbrella-leaf.com/online-chat/avatar/default.png")
    signature = db.Column(db.String(255), nullable=False, server_default="一段有个性的签名")
    status = db.Column(db.Integer, nullable=False, server_default=text(str(UserState.unauthorized.value)))
    register_time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.user_id})>"

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
