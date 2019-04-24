#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 21:38
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

bp = Blueprint('main', __name__)


from app.main import routes