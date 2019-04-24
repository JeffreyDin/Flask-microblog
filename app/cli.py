#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 16:09
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : cli.py
# @Software: PyCharm
#
# import os
# import click
# from app import jeff
#
#
# # flask translate init LANG用于添加新语言
# # flask translate update用于更新所有语言存储库
# # flask translate compile用于编译所有语言存储库
# @jeff.cli.group()
# def translate():
#     """Translation and localization commands."""
#     pass
#
#
# @translate.command()
# @click.argument('lang')
# def init(lang):
#     """Initialize a new language."""
#     if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
#         raise RuntimeError('extract command failed')
#     if os.system(
#             'pybabel init -i messages.pot -d app/translations -l ' + lang):
#         raise RuntimeError('init command failed')
#     os.remove('messages.pot')
#
#
# @translate.command()
# def update():
#     """Update all languages."""
#     if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
#         raise RuntimeError('extract command failed')
#     if os.system('pybabel update -i messages.pot -d app/translations'):
#         raise RuntimeError('update command failed')
#     os.remove('messages.pot')
#
#
# @translate.command()
# def compile():
#     """Compile all languages."""
#     if os.system('pybabel compile -d app/translations'):
#         raise RuntimeError('compile command failed')
import os
import click


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')