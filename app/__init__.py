#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 18:12
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Flask, current_app
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
# 在客户端中使用JavaScript来对UTC和本地时区之间进行转换.
from flask_moment import Moment
# 国际化和本地化，通常缩写为I18n和L10n.翻译.
from flask_babel import Babel, lazy_gettext as _l
# Babel实例提供了一个localeselector装饰器.为每个请求调用装饰器函数以选择用于该请求的语言：
from flask import request
# 全文搜索
from elasticsearch import Elasticsearch

import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os


# jeff = Flask(__name__)
# # 数据库在应用的表现形式是一个数据库实例，数据库迁移引擎同样如此。
# # 它们将会在应用实例化之后进行实例化和注册操作.
# # 这里在初始化db之前需要先加载配置文件.
# jeff.config.from_object(Config)
# db = SQLAlchemy(jeff)
# # 数据库迁移引擎migrate初始化
# migrate = Migrate(jeff, db)
#
# # Flask-Login被创建和初始化
# login = LoginManager(jeff)
# # 强制用户在查看应用的特定页面之前登录。 如果未登录的用户尝试查看受保护的页面
# login.login_view = 'login'
# login.login_message = _l('Please log in to access this page.')
# # mail是类Mail的一个实例
# mail = Mail(jeff)
# # 初始化, Flask-Bootstrap实例,美化
# bootstrap = Bootstrap(jeff)
# # Flask-Moment实例
# moment = Moment(jeff)
# # Flask-Babel实例
# babel = Babel(jeff)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

# ...
# if not jeff.debug:
#     if jeff.config['MAIL_SERVER']:
#         auth = None
#         if jeff.config['MAIL_USERNAME'] or jeff.config['MAIL_PASSWORD']:
#             auth = (jeff.config['MAIL_USERNAME'], jeff.config['MAIL_PASSWORD'])
#         secure = None
#         if jeff.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(jeff.config['MAIL_SERVER'], jeff.config['MAIL_PORT']),
#             fromaddr='no-reply@' + jeff.config['MAIL_SERVER'],
#             toaddrs=jeff.config['ADMINS'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         jeff.logger.addHandler(mail_handler)
#     # 错误提示记录日志到文件中
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
#                                        backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     jeff.logger.addHandler(file_handler)
#
#     jeff.logger.setLevel(logging.INFO)
#     jeff.logger.info('Microblog startup')


# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(app.config['LANGUAGES'])

# @babel.localeselector
# def get_locale():
#     # return request.accept_languages.best_match(app.config['LANGUAGES'])
#     return 'es'

# @babel.localeselector
# def get_locale():
#     # return request.accept_languages.best_match(app.config['LANGUAGES'])
#     return 'zh-Hans-CN'


# @babel.localeselector
# def get_locale():
#     # return request.accept_languages.best_match(app.config['LANGUAGES'])
#     return 'zh'

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

# from app.main import routes, models, errors, cli


from app import models