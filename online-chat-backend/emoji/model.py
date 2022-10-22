from exts import db


class Emoji(db.Model):
    __tablename__ = "emoji"
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref="emojis", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Emoji(id={self.id})>"

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

