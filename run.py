#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 18:18
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : microblog.py
# @Software: PyCharm


# from app import jeff
# # from app.main import cli
#
# jeff.run(debug=True)
# # jeff.run()
# # jeff.cli

from app import create_app, db, cli
from app.models import User, Post

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}