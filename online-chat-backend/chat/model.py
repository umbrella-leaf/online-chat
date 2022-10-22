from exts import db
from sqlalchemy import func, text
from utils.Enums import MessageState, MessageType


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    friendship_id = db.Column(db.Integer, db.ForeignKey('friendship.id', ondelete='CASCADE'), nullable=False)
    latest_msg_id = db.Column(db.Integer, db.ForeignKey('message.id', ondelete='CASCADE'), nullable=True)
    online = db.Column(db.Integer, nullable=False, server_default=text('0'))
    latest_msg = db.relationship('Message', uselist=False, backref='chatroom', foreign_keys=[latest_msg_id])

    def __repr__(self):
        return f"<Chat(id={self.id})>"

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    send_time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    content = db.Column(db.Text, nullable=False)
    html = db.Column(db.Text(100000), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=text(str(MessageState.unread.value)))
    type = db.Column(db.Integer, nullable=False, server_default=text(str(MessageType.text.value)))
    sender = db.relationship('User', backref="sends", foreign_keys=[sender_id])
    chat = db.relationship('Chat', backref="messages", foreign_keys=[chat_id])

    def __repr__(self):
        return f"<Message(id={self.id})>"

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
