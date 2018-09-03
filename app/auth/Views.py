# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_login import current_user
from .Form import LoginForm, RegistrationForm
from . import auth
from ..Models import User
from .. import db
from ..Email import sendMail


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # 登陆状态直接转到首页
        return redirect(url_for("news.index"))
    else:
        form = LoginForm()
        # 按下登陆键
        if form.validate_on_submit():
            # 验证账号密码
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verifyPassword(form.password.data):
                login_user(user, form.remeberMe.data)
                return redirect(url_for("news.index"))
            else:
                flash('用户名或密码错误')

        return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("注销成功")
    return redirect(url_for("news.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data)

        # 确认邮箱是否已注册
        if User.query.filter_by(email=user.email).first() is not None:
            flash("该邮箱已经注册")
        else:
            db.session.add(user)
            db.session.commit()

            # 发送确认邮件
            token = user.generateConfirmationToken()
            sendMail(
                user.email,
                "Confirm Your Account",
                "auth/email/confirm",
                user=user,
                token=token)

            flash("注册成功")
            return redirect(url_for("news.index"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.is_authenticated:
        # 登陆状态直接转到首页
        return redirect(url_for("news.index"))
    else:
        if current_user.confirmed:
            return redirect(url_for("news.index"))
        if current_user.confirm(token):
            flash('You have confirmed your account. Thanks!')
        else:
            flash('The confirmation link is invalid or has expired.')
        return redirect(url_for("news.index"))
