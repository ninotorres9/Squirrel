# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from Config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
loginMananger = LoginManager()

loginMananger.session_protection = "strong"
loginMananger.login_view = "auth.login"


def createApp(configName="default"):
    app = Flask(__name__)
    app.config.from_object(config[configName])
    config[configName].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    loginMananger.init_app(app)

    from .news import news
    from .auth import auth
    app.register_blueprint(news, url_prefix="/news")
    app.register_blueprint(auth, url_prefix="/auth")

    return app
