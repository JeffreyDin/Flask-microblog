#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 16:05
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : db_downgrade.py
# @Software: PyCharm

from migrate.versioning import api
from config import Config
v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
api.downgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF, v - 1)
v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
print('Current database version: ' + str(v))
