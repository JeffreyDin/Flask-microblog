#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 20:32
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : config.py
# @Software: PyCharm
#
#
# import os
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
#
# class Config(object):
#
#     CSRF_ENABLED = os.environ.get('CSRF_ENABLED') or True
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will#%*-never!$@-guess-GXS$%'
#     TRACK_MODIFICATIONS = True
#     # print(SECRET_KEY)
#     # print(DATABASE_URI)
#     # print(MIGRATE_JEFF)
#     # SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     OPENID_PROVIDERS = [
#         {'name': 'Google', 'url': 'https://developers.google.com/identity/protocols/OpenIDConnect'},
#         {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
#         {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
#         {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
#         {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
#     # FLASK_DEBUG = 1
#     # DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jeff_users.db')
#     # 创建数据库迁移存储库
#     SQLALCHEMY_MIGRATE_JEFF = os.path.join(basedir, 'db_migrations')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     # print(SQLALCHEMY_DATABASE_URI)
#     # print(SQLALCHEMY_MIGRATE_REPO)
#     # MAIL_SERVER = os.environ.get('MAIL_SERVER')
#     # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
#     # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
#     # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#     # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
#     # ADMINS = ['your-email@example.com']

#
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = int(587 or 25)
#     MAIL_USE_TLS = 1
#     MAIL_USERNAME = 'your-email@example.com'
#     MAIL_PASSWORD = 'mima'
#     ADMINS = ['your-email@example.com']
#
#     # LANGUAGES = ['en', 'es', 'zh-CN', 'zh-Hans-CN']
#     LANGUAGES = ['en', 'es', 'zh']
#
#     POSTS_PER_PAGE = 3

# class MigrateConfig(Config):
#     SQLALCHEMY_MIGRATE_JEFF = os.path.join(basedir, 'db_migrations')
#
#
# class UserConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jeff_users.db')


# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
#                               'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
#
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
#
#
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#                               'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# config = {
#     'user': UserConfig,
#     'migrate': MigrateConfig,
#     # 'development': DevelopmentConfig,
#     # 'testing': TestingConfig,
#     # 'production': ProductionConfig,
#     # 'default': DevelopmentConfig
# }


# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'jeff_users.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_migrations')
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    OPENID_PROVIDERS = [
        {'name': 'Google', 'url': 'https://developers.google.com/identity/protocols/OpenIDConnect'},
        {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
        {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
        {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
        {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

    CSRF_ENABLED = os.environ.get('CSRF_ENABLED') or True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will#%*-never!$@-guess-GXS$%'
    TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jeff_users.db')
    # 创建数据库迁移存储库
    SQLALCHEMY_MIGRATE_JEFF = os.path.join(basedir, 'db_migrations')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ADMINS']
    # print(MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, ADMINS)
    # LANGUAGES = ['en', 'es', 'zh-CN', 'zh-Hans-CN']
    LANGUAGES = ['en', 'es', 'zh']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    POSTS_PER_PAGE = 25