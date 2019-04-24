#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 12:04
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : db_upgrade.py
# @Software: PyCharm


# from migrate.versioning import api
# from config import MigrateConfig
# from config import UserConfig
# api.upgrade(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# v = api.db_version(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# print('Current database version: ' + str(v))


from migrate.versioning import api
from config import Config
# from config import MigrateConfig
# from config import UserConfig
api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
print('Current database version: ' + str(v))
