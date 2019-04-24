#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 11:47
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : db_migrate.py.py
# @Software: PyCharm


# import imp
# from migrate.versioning import api
# from app import db
# from config import MigrateConfig
# from config import UserConfig
# v = api.db_version(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# migration = MigrateConfig.SQLALCHEMY_MIGRATE_JEFF + ('/versions/%03d_migration.py' % (v+1))
# tmp_module = imp.new_module('old_model')
# old_model = api.create_model(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# exec(old_model, tmp_module.__dict__)
# script = api.make_update_script_for_model(UserConfig.SQLALCHEMY_DATABASE_URI,
#                                           MigrateConfig.SQLALCHEMY_MIGRATE_JEFF,
#                                           tmp_module.meta, db.metadata)
# open(migration, "wt").write(script)
# api.upgrade(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# v = api.db_version(UserConfig.SQLALCHEMY_DATABASE_URI, MigrateConfig.SQLALCHEMY_MIGRATE_JEFF)
# print('New migration saved as ' + migration)
# print('Current database version: ' + str(v))

import imp
from migrate.versioning import api
from app import db
from config import Config
# from config import MigrateConfig
# from config import UserConfig
v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
migration = Config.SQLALCHEMY_MIGRATE_JEFF + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(Config.SQLALCHEMY_DATABASE_URI,
                                          Config.SQLALCHEMY_MIGRATE_JEFF,
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_JEFF)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))

