# -*- coding: utf-8 -*-

import os
from flask_mail import Message
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("WEB_EMAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("WEB_EMAIL_PASSWORD")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HAMSTER_MAIL_SUBJECT_PREFIX = "[Hamster]"
    HAMSTER_MAIL_SENDER = "Hamster Admin <superhamster@163.com>"
    HAMSTER_ADMIN = os.environ.get("WEB_EMAIL_USERNAME")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") + "hamster"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") + "testing"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
