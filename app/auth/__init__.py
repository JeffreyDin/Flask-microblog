#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 13:53
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes