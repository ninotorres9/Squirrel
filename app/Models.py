# -*- coding: utf-8 -*-

from . import db
from . import loginMananger
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@loginMananger.user_loader
def loadUser(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'))
    passwordHash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config["HAMSTER_ADMIN"]:
            self.role = Role.query.filter_by(permissions=0xff).first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        """
            禁止读取password
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
            生成password hash
        """
        self.passwordHash = generate_password_hash(password)

    def generateResetToken(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"reset": self.id}).decode("utf-8")

    @staticmethod
    def resetPassword(token, newPassword):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        # 获取user id
        user = User.query.get(data.get("reset"))
        if user is None:
            return False
        user.password = newPassword
        db.session.add(user)
        return True

    def generateConfirmationToken(self, expiration=3600):
        """
            生成带有时限的JSON WEB签名(令牌)
        """
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id})

    def confirm(self, token):
        """
            验证令牌
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def verifyPassword(self, password):
        """
            验证密码
        """
        return check_password_hash(self.passwordHash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def isAdministrator(self):
        return self.can(Permission.ADMINISTER)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    @staticmethod
    def insertRoles():
        roles = {
            "User": (Permission.FOLLOW | Permission.COMMENT
                     | Permission.WRITE_ARTICLES, True),
            "Moderator":
            (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES
             | Permission.MODERATE_COMMENTS, False),
            "Administrator": (0xff, False)  # 11111111 = 开启所有权限
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    """
        权限设置
    """
    FOLLOW = 0x01  # 关注用户 0b00000001
    COMMENT = 0X02  # 发表评论 0b00000010
    WRITE_ARTICLES = 0x04  # 写文章 0b00000100
    MODERATE_COMMENTS = 0x08  # 管理他人发表的评论 0b00001000
    ADMINISTER = 0x80  # 管理员权限 0b10000000


class Psnine(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)

    def __init__(self, id, title, link):
        self.id = id
        self.title = title
        self.link = link
