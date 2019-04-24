#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 14:22
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : routes.py
# @Software: PyCharm


# 表单视图
# 注册表单视图(用户注册的视图函数,RegistrationForm),
# 邮件支持，请求密码重置(邮件视图函数,ResetPasswordRequestForm)
# 密码重置视图函数ResetPasswordForm
from app.auth.forms import LoginForm, OpenIDForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.auth.email import send_password_reset_email
# 用户注册表单视图(用户注册的视图函数),装饰器将重定向到登录页面.
from flask import render_template, redirect, flash, url_for, request, current_app
from werkzeug.urls import url_parse
# 登入，登出表单视图,登入，登出视图函数2
from flask_login import current_user, login_user, logout_user
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.models import User


# 登入表单视图1-1
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if user is None or not (user.password_hash == form.password.data):
        if user is None or not user.verify_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


# 登入表单视图1
@bp.route('/openid', methods=['GET', 'POST'])
def openid():
    form = OpenIDForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me='
              + str(form.remember_me.data))
        return redirect(url_for('main.index'))
    return render_template('auth/openid.html', title='Sign In', form=form, providers=current_app.config['OPENID_PROVIDERS'])


# 登出表单视图1-1
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# 用户注册表单视图1-1
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


# 请求重置密码视图
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


# 重置密码视图
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)







