# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_login import current_user
from app.auth.Form import LoginForm, PasswordResetForm
from app.auth.Form import RegistrationForm, PasswordResetRequestForm
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
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash("邮箱已注册")
        else:
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data)

            db.session.add(user)
            db.session.commit()

            # 发送确认邮件
            token = user.generateConfirmationToken()
            sendMail(
                user.email,
                "确认您的账号",
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


@auth.route("/reset", methods=["GET", "POST"])
def passwordResetRequest():
    if not current_user.is_anonymous:
        return redirect(url_for("news.index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generateResetToken()
            sendMail(
                user.email,
                "重置密码",
                "auth/email/resetPassword",
                user=user,
                token=token)
            flash("重置电子邮件已发送至您的邮箱")
        else:
            flash("该邮箱不存在")
        return redirect(url_for("auth.login"))
    return render_template("auth/resetPassword.html", form=form)


@auth.route("/reset/<token>", methods=["GET", "POST"])
def passwordReset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("news.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.resetPassword(token, form.password.data):
            db.session.commit()
            flash("修改成功")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("news.index"))
    return render_template("auth/resetPassword.html", form=form)
