#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 19:34
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : models.py
# @Software: PyCharm


from app import db
from datetime import datetime
# # from config import Config
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# # 头像与用户相关联，所以将生成头像URL的逻辑添加到用户模型
from hashlib import md5
# # 密码重置，令牌生成和验证
from time import time
import jwt
# from app import jeff
from flask import current_app
# 搜索
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        # print(cls.__tablename__)
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


# 粉丝followers关联表
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('Jeff_users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('Jeff_users.id'))
                     )


# 用户
class User(UserMixin, db.Model):
    __tablename__ = 'Jeff_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        # return '<User %r>' % self.name
        return '<User {}>'.format(self.username)

    # 通过generate_password_hash将明文转换为长编码字符串，哈希加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码哈希值匹配，相同返回True
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # get_reset_password_token()函数以字符串形式生成一个JWT令牌,decode('utf-8')是必须的
    # jwt.encode()函数将令牌作为字节序列返回
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # verify_reset_password_token()是一个静态方法，这意味着它可以直接从类中调用。
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # User类新增的avatar()方法需要传入需求头像的像素大小，并返回用户头像图片的URL。
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # 粉丝关注和取消关注，follow()和unfollow()方法使用关系对象的append()和remove()方法。
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 用户动态
class Post(SearchableMixin, db.Model):
    __tablename__ = 'Jeff_posts'
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Jeff_users.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        # return '<Post %r>' % (self.body)
        return '<Post {}>'.format(self.body)





