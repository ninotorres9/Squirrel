# -*- coding: utf-8 -*-

from flask import redirect, url_for, render_template
from flask_script import Manager, Shell
from app import createApp

app = createApp("default")
launcher = Manager(app)


@launcher.command
def test():
    """
        执行单元测试
    """
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.route("/")
def index():
    return redirect(url_for("news.index"))


def main():
    # pass
    launcher.run()
    # test()


if __name__ == '__main__':
    main()