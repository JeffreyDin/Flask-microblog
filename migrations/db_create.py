#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 21:36
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : db_create.py
# @Software: PyCharm


# from migrate.versioning import api
# from config import MigrateConfig
# from config import UserConfig
# from app import db
# import os.path
# db.create_all()
# if not os.path.exists(MigrateConfig.SQLALCHEMY_MIGRATE_JEFF):
#     api.create(MigrateConfig.SQLALCHEMY_MIGRATE_JEFF, 'database repository')
#     api.version_control(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# else:
#     api.version_control(UserConfig.SQLALCHEMY_DATABASE_URI,
#                         MigrateConfig.SQLALCHEMY_MIGRATE_JEFF,
#                         api.version(MigrateConfig.SQLALCHEMY_MIGRATE_JEFF))


from migrate.versioning import api
from config import Config
# from config import UserConfig
from app import db
import os.path
db.create_all()
if not os.path.exists(Config.SQLALCHEMY_MIGRATE_JEFF):
    api.create(Config.SQLALCHEMY_MIGRATE_JEFF, 'database repository')
    api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
else:
    api.version_control(Config.SQLALCHEMY_DATABASE_URI,
                        Config.SQLALCHEMY_MIGRATE_JEFF,
                        api.version(Config.SQLALCHEMY_MIGRATE_JEFF))