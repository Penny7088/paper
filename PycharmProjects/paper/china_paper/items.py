# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class ChinaPaperItem(scrapy.Item):
    # define the fields for your item here like:
    # NAME
    name = scrapy.Field()

    # 地址
    address = scrapy.Field()

    # 联系电话
    phone = scrapy.Field()

    # 公司
    company = scrapy.Field()

    # 邮箱
    email = scrapy.Field()

    # 描述
    describe = scrapy.Field()

    # 产品名称
    product_name = scrapy.Field()

    # 产品型号
    product_size = scrapy.Field()

    # 价格
    price = scrapy.Field()
