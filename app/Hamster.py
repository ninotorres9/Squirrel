# -*- coding: utf-8 -*-

import pymysql
from app.Spider import Spider
from app.Models import Psnine
# from app.Config import db
from . import db


class Hamster:
    def __init__(self):
        pass

    def createAll(self):
        """
        创建所有table
        """
        db.create_all()

    def savePsnineNews(self):
        """
            将psnine新闻存入database
        """
        url = "http://psnine.com/news"
        spider = Spider()

        for new in spider.getPsnineNews(url):
            id = new[0]
            title = new[1].replace("\'", "\\'")  # 添加转义符
            link = new[2]
            db.session.merge(Psnine(id, title, link))

        db.session.commit()

    def getPsnineNews(self):
        """
            取出psnine新闻
        """
        # psnine new页面有两个奇怪的网页id，以34开头，直接排除
        return Psnine.query.filter(~Psnine.id.like("34%")).order_by(
            Psnine.id.desc())

    def getPsnineNewsByKey(self, key):
        """
            根据key搜索新闻
        """
        return Psnine.query.filter(
            Psnine.title.like("%{key}%".format(key=key))).all()


def main():
    hamster = Hamster()
    # hamster.createAll()
    # hamster.savePsnineNews()
    for new in hamster.getPsnineNews():
        print("id: {id}, title: {title}, link:{link}".format(
            id=new.id, title=new.title, link=new.link))


if __name__ == '__main__':
    main()