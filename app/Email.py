# -*- coding: utf-8 -*

from flask import render_template
from flask_mail import Mail, Message
from . import mail
from Launcher import app


def sendMail(target, subject, template, **kwargs):

    message = Message(
        app.config["HAMSTER_MAIL_SUBJECT_PREFIX"] + subject,
        sender=app.config["HAMSTER_MAIL_SENDER"],
        recipients=[target])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    mail.send(message)