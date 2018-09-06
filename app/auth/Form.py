# -*- coding: utf-8 -*-

# from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Required, Length, Email, Regexp, EqualTo
from ..Models import User


class LoginForm(FlaskForm):
    email = StringField("账号", validators=[Required(), Length(1, 64), Email()])
    password = PasswordField("密码", validators=[Required()])
    remeberMe = BooleanField("记住我")
    submit = SubmitField("登陆")


class RegistrationForm(FlaskForm):
    email = StringField("账号", validators=[Required(), Length(1, 64), Email()])
    username = StringField(
        "昵称",
        validators=[
            Required(),
            Length(1, 64),
            Regexp("^[A-Za-z][A-Za-z0-9_]*$", 0, "昵称只能包含字母，数字和下划线")
        ])
    password = PasswordField(
        "密码", validators=[Required(),
                          EqualTo("password2", "两次密码输入必须一致")])
    password2 = PasswordField(
        "确认密码", validators=[Required(), Length(8, 16, "密码需要8-16位")])
    submit = SubmitField("注册")

    def validateEmail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已注册")

    def validateUsername(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("该昵称已注册")


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        "邮箱", validators=[DataRequired(),
                          Length(1, 64),
                          Email()])
    submit = SubmitField("密码重置")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "新密码", validators=[DataRequired(),
                           EqualTo("password2", "两次密码输入必须一致")])
    password2 = PasswordField("确认密码", validators=[Required()])
    submit = SubmitField("密码重置")
