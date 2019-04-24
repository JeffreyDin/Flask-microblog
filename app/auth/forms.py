#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 14:16
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

# 用户登录/注册表单
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
# from app.main.models import User
from app.models import User
# 用户个人资料表单
# from wtforms import StringField, TextAreaField, SubmitField
# from wtforms.validators import DataRequired, Length
# 翻译
from flask_babel import _, lazy_gettext as _l


# 用户登陆表单
class LoginForm(FlaskForm):
    # validators用于验证输入字段是否符合预期。
    # DataRequired验证器仅验证字段输入是否为空。更多的验证器将会在未来的表单中接触到。
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    # remember_me = BooleanField('remember_me', default=False)
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class OpenIDForm(FlaskForm):
    # openid = StringField('openid', validators=[DataRequired()])
    openid = StringField(_l('OpenId'), validators=[DataRequired()])
    # remember_me = BooleanField('remember_me', default=False)
    remember_me = BooleanField(_l('Remember Me'), default=False)
    submit = SubmitField(_l('Sign In'))


# 用户注册表单
class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


# 请求密码重置表单，输入注册的电子邮件地址，以启动密码重置过程
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


# 令牌是有效的，那么向用户呈现第二个表单，需要用户其中输入新密码.密码重置表单.
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
