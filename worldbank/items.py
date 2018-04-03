# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WorldBankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    indi_url = scrapy.Field()  # 指标(indicator)的url
    indi_name = scrapy.Field()  # 指标(indicator)的名字


class WorldBankNameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # indi_url = scrapy.Field()  # 指标(indicator)的url
    indi_name = scrapy.Field()  # 指标(indicator)的名字
