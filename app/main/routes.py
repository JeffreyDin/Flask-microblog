#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 18:14
# @Author  : Jianfeng Ding
# @Site    : 
# @File    : routes.py
# @Software: PyCharm


# from app import jeff
# # 表单视图
# from app.main.forms import LoginForm, OpenIDForm
# from flask import render_template, flash, redirect, url_for
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from datetime import datetime
from app import db
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
# from app.translate import translate
from app.main import bp
# 全文搜索
from flask import g
from app.main.forms import SearchForm
# # 登入，登出表单视图,登入，登出视图函数2
# from flask_login import current_user, login_user, logout_user
# from app.main.models import User
# # 登入视图函数2,拒绝匿名用户的访问以保护某个视图函数
# from flask_login import login_required
# # 登入成功之后自定重定向自定重定向回到用户之前想要访问的页面.
# # 当一个没有登录的用户访问被@login_required装饰器保护的视图函数时，
# # 装饰器将重定向到登录页面.
# from flask import request
# from werkzeug.urls import url_parse
# # 用户注册表单视图(用户注册的视图函数)
# from app import db
# from app.main.forms import RegistrationForm
# 用户最后登陆的视图函数，记录用户的最后访问时间
# from datetime import datetime
# # 用户个人资料编辑器视图函数
# from app.main.forms import EditProfileForm
# # 用户动态视图函数
# from app.main.forms import PostForm
# from app.main.models import Post
# # 邮件支持，请求密码重置。邮件视图函数。
# from app.main.forms import ResetPasswordRequestForm
# from app.main.email import send_password_reset_email
# # 密码重置视图函数
# from app.main.forms import ResetPasswordForm
# # 翻译
# from flask_babel import _, get_locale
# from flask import g
# # from flask_babel import get_locale
# # Ajax
# # from guess_language import guess_language


# Flask提供的g容器。这个g变量是应用可以存储需要在整个请求期间持续存在的数据的地方。在这里，我将表单存储在g.search_form中，
# 当请求前置处理程序结束并且Flask调用处理请求的URL的视图函数时，g对象将会是相同的，并且表单仍然存在。
# 请求处理前的处理器中初始化搜索表单
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    # posts = current_user.followed_posts().all()
    # user = {'username': 'Gunxiaoshi'}
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


# @jeff.route('/test')
# def test():
#     user = {'username': 'Gunxiaoshi'}
#     posts = [
#         {
#             'author': {'username': 'John'},
#             'body': 'Beautiful day in Portland!'
#         },
#         {
#             'author': {'username': 'Susan'},
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template("test.html", title='Test', user=user, post=posts)

# 表单视图1
# @jeff.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit(): user {}, remember_me={}'.format(
# #                   form.username.data, form.remember_me.data))
# #         return redirect(url_for('index'))
# #     return render_template('login.htm
#         flash('Login requested forl', title='Sign In', form=form)

# 动态发现，分页视图函数
@bp.route('/explore')
@login_required
def explore():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


# # 登入表单视图1-1
# @jeff.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         # if user is None or not (user.password_hash == form.password.data):
#         if user is None or not user.verify_password(form.password.data):
#             flash(_('Invalid username or password'))
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)
#
#
# # 登出表单视图1-1
# @jeff.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
#
#
# # 用户注册表单视图1-1
# @jeff.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash(_('Congratulations, you are now a registered user!'))
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# 登陆动态表单视图1-1，动态地生成每个用户的主页。
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    # return render_template('user.html', user=user, posts=posts)
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


# 用户登录时间视图1-1
# 一旦某个用户向服务器发送请求，就将当前时间写入到这个字段。
@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


# 用户个人资料编辑器视图1-1
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # form = EditProfileForm()
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# 粉丝机制, 提供了用户关注的URL和逻辑实现
@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # flash('User {} not found.'.format(username))
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    # flash('You are following {}!'.format(username))
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


# 粉丝机制, 提供了用户取消关注的URL和逻辑实现
@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # flash('User {} not found.'.format(username))
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.index', username=username))
    current_user.unfollow(user)
    db.session.commit()
    # flash('You are not following {}.'.format(username))
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.index', username=username))


# # 请求重置密码视图
# @jeff.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_password_reset_email(user)
#         flash(_('Check your email for the instructions to reset your password'))
#         return redirect(url_for('login'))
#     return render_template('reset_password_request.html',
#                            title='Reset Password', form=form)
#
#
# # 重置密码视图
# @jeff.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash(_('Your password has been reset.'))
#         return redirect(url_for('login'))
#     return render_template('reset_password.html', form=form)
#
#
# # 登入表单视图1
# @jeff.route('/openid', methods=['GET', 'POST'])
# def openid():
#     form = OpenIDForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="' + form.openid.data + '", remember_me='
#               + str(form.remember_me.data))
#         return redirect(url_for('index'))
#     return render_template('openid.html', title='Sign In', form=form, providers=jeff.config['OPENID_PROVIDERS'])
#


# 搜索视图函数
@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)
