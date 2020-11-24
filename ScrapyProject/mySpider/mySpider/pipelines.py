# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import Stockstar


class MyspiderPipeline:

    def process_item(self, item, spider):
        if Stockstar.table_exists() == False:
            Stockstar.create_table()
        try:
            Stockstar.create(
                code=item['code'],
                abbr=item['abbr'],
                traded_market_value=item['traded_market_value'],
                total_value=item['total_value'],
                Flow_of_equity=item['Flow_of_equity'],
                general_capital=item['general_capital']
            )
        except Exception as e:
            if str(e.args[0]) == '1062':
                print("重复数据，跳过。")
            else:
                print(e.args[0], e.args[1])
        return item
