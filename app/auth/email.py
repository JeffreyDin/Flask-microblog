#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 14:09
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : email.py
# @Software: PyCharm


# 简单的电子邮件框架
# from flask_mail import Message
# from app import mail
# 发送密码重置电子邮件
from flask import render_template
from flask import current_app
from app.email import send_email
# from app import jeff
# 异步电子邮件
# Python多种方式支持运行异步任务，threading和multiprocessing模块都可以做到这一点。
# from threading import Thread
from flask_babel import _


# send_password_reset_email()函数依赖于上面写的send_email()函数
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print(1)
    send_email(_('[GXS] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
               # text_body= 'test2.body',
               # html_body= '<h1>ttt<h1>')



