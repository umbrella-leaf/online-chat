from exts import db
from utils.Enums import FriendState
from sqlalchemy.sql import func
from sqlalchemy import text


class FriendShip(db.Model):
    __tablename__ = 'friendship'
    __table_args__ = (db.UniqueConstraint("user_id", "friend_id", name="relation_unique"), )
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                          nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=func.now())
    message_cnt = db.Column(db.Integer, nullable=False, server_default=text('0'))
    status = db.Column(db.Integer, nullable=False, server_default=text(str(FriendState.unaccepted.value)))
    user = db.relationship("User", backref="friendships", foreign_keys=[user_id])
    friend = db.relationship("User", backref="userships", foreign_keys=[friend_id])

    def __repr__(self):
        return f"<Friend(user_id={self.user_id}, friend_id={self.friend_id})>"

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
