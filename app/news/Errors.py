# -*- coding: utf-8 -*-

from flask import render_template
from . import news


@news.app_errorhandler(404)
def pageNoteFound(error):
    return render_template("404.html"), 404