#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 17:56
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : email.py
# @Software: PyCharm

# # 简单的电子邮件框架
# from flask_mail import Message
# from app import mail
# # 发送密码重置电子邮件
# from flask import render_template
# from app import jeff
# # 异步电子邮件
# # Python多种方式支持运行异步任务，threading和multiprocessing模块都可以做到这一点。
# from threading import Thread
# from flask_babel import _
#
#
# # 为发送电子邮件启动一个后台线程
# # send_async_email函数现在运行在后台线程中，
# # 它通过send_email()的最后一行中的Thread()类来调用
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
#
# # 发送电子邮件的帮助函数
# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     # mail.send(msg)
#     Thread(target=send_async_email, args=(jeff, msg)).start()
#
#
# # send_password_reset_email()函数依赖于上面写的send_email()函数
# def send_password_reset_email(user):
#     token = user.get_reset_password_token()
#     send_email(_('[GXS] Reset Your Password'),
#                sender=jeff.config['ADMINS'][0],
#                recipients=[user.email],
#                text_body=render_template('email/reset_password',
#                                          user=user, token=token),
#                html_body=render_template('email/reset_password.html',
#                                          user=user, token=token))
#                # text_body= 'test.body',
#                # html_body= '<h1>ttt<h1>')
#

from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
