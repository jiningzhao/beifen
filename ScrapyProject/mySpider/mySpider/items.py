# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from peewee import *

db = MySQLDatabase("jining_test", host="127.0.0.1", port=3306, user="root", passwd="zmgui024624", charset="utf8")


# 自定义itemloader，用于存储爬虫所抓取的字段内容
class StockstarItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class StockstarItem(scrapy.Item):  # 建立相应的字段
    code = scrapy.Field()  # 股票代码
    abbr = scrapy.Field()  # 股票简称
    traded_market_value = scrapy.Field()  # 流通市值
    total_value = scrapy.Field()  # 总市值
    Flow_of_equity = scrapy.Field()  # 流通股本
    general_capital = scrapy.Field()  # 总股本


class Stockstar(Model):
    code = CharField(verbose_name="股票代码", max_length=100, primary_key=True, null=False)
    abbr = CharField(verbose_name="股票简称", max_length=100, null=False)
    traded_market_value = CharField(verbose_name="流通市值", max_length=100, null=False)
    total_value = CharField(verbose_name="总市值", max_length=100, null=False)
    Flow_of_equity = CharField(verbose_name="流通股本", max_length=100, null=False)
    general_capital = CharField(verbose_name="总股本", max_length=100, null=False)

    class Meta:
        database = db
