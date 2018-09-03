# -*- coding: utf-8 -*-

from flask import Blueprint

news = Blueprint("news", __name__)

from . import Views, Errors