# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, redirect
from app.Hamster import Hamster
from . import news


@news.route("/")
def index():
    hamster = Hamster()
    news = list(hamster.getPsnineNews())
    return render_template("news.html", news=news)


@news.route("/update")
def update():
    hamster = Hamster()
    hamster.savePsnineNews()
    return redirect(url_for("news.index"))


@news.route("/<key>")
def filter(key):
    hamster = Hamster()
    news = hamster.getPsnineNewsByKey(key)
    return render_template("news.html", news=news)