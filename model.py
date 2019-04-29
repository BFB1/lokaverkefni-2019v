from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'Account'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String(254), unique=True, nullable=False)

    password = db.Column(db.String, nullable=False)

    timeCreated = db.Column(db.DateTime, server_default=func.now())
    timeModified = db.Column(db.DateTime, server_default=func.now(), server_onupdate=func.now())
    timeLastLogin = db.Column(db.DateTime, server_default=func.now())

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")

    def __repr__(self):
        return 'Account with name {}'.format(self.username)


class Thread(db.Model):
    __tablename__ = 'Thread'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    timeCreated = db.Column(db.DateTime, server_default=func.now())
    timeModified = db.Column(db.DateTime, server_default=func.now(), server_onupdate=func.now())
    modified = db.Column(db.Boolean, server_default='false', server_onupdate='true')
    locked = db.Column(db.Boolean, server_default='false')

    accountId = db.Column(db.Integer, db.ForeignKey('Account.id'), nullable=False)

    comments = db.relationship('Comment', backref='Thread', lazy=True)


class Comment(db.Model):
    __tablename__ = 'Comment'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=False)

    threadId = db.Column(db.Integer, db.ForeignKey('Thread.id'), nullable=True)

    parent = db.relationship('Comment', remote_side=id, backref='children')
    parentCommentId = db.Column(db.Integer, db.ForeignKey('Comment.id'), nullable=False)
