import requests
from bs4 import BeautifulSoup
import re
import json


class InterfaceSpider:
    """
    爬虫模块
    爬取对应接口文档中的接口name和接口入参规范
    """

    def __init__(self, path):
        self.path = path
        self.list = []

    def spider(self):
        url = f'https://service-wbs321.newtamp.cn/{self.path}/api/doc'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.select('#readme > article >div[class="api-item"]')
        for item in data:

            detail = item.select('h2')[0].text
            name = \
            re.findall(r"\w*\.\w*\.\w*|\w*\.\w*", item.select('div.doc-name-version > div:nth-child(1)')[0].text)[0]
            data = {}
            for i in item.select('div.api-block > form > table > tr > td:nth-child(1)'):
                data[i.get_text()] = ""
            self.list.append({
                "detail": detail,
                "name": name,
                "data": data
            })
        return self.list

# InterfaceSpider('pdc').spider()
