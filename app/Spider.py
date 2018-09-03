# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import datetime


class Spider():
    def __init__(self):
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

    def getHtml(self, url):
        """
            获取url文本
        """
        page = request.Request(url, headers=self.headers)
        return request.urlopen(page).read().decode('utf-8')

    def getPsnineNews(self, url):
        """
            获取P9新闻页标题
        """
        html = self.getHtml(url)
        soup = BeautifulSoup(html, "lxml")

        # 获取新闻标题以及连接
        for new in soup.findAll("a", {"class": "touch"}):
            link = new["href"]
            title = new.find("div", {
                "class": "content pb10"
            }).getText().replace("\r\n", "")
            # 获取当前时间
            id = link.split("/")[-1]
            yield [id, title, link]


def main():
    spider = Spider()
    url = "http://psnine.com/news"
    for title in spider.getPsnineNews(url):
        print(title)


if __name__ == '__main__':
    main()