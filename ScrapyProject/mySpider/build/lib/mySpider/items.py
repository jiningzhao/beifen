# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class StockstarItemLoader(ItemLoader):  # 自定义itemloader，用于存储爬虫所抓取的字段内容
    default_output_processor = TakeFirst()


class StockstarItem(scrapy.Item):  # 建立相应的字段
    code = scrapy.Field()  # 股票代码
    abbr = scrapy.Field()  # 股票简称
    traded_market_value = scrapy.Field()  # 流通市值
    total_value = scrapy.Field()  # 总市值
    Flow_of_equity = scrapy.Field()  # 流通股本
    general_capital = scrapy.Field()  # 总股本

