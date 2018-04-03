# -*- coding:utf-8 -*-
import scrapy
import requests
import re
from worldbank.items import WorldBankItem


class WorldBankSpider(scrapy.Spider):
    name = "worldbank"
    filenames = []

    # excel_url = "http://api.worldbank.org/v2/zh/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel" #世界银行——中文——下载excel地址样式
    # excel_url = "http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel" #世界银行——英文——下载excel地址样式

    # excel_url = "http://api.worldbank.org/v2/zh"
    excel_url = "http://api.worldbank.org/v2/en"

    # output_path = './test.xls'

    # start_url = 'http://data.worldbank.org.cn/indicator?tab=all' #世界银行——中文——获取指标
    start_url = 'http://data.worldbank.org/indicator?tab=all'  # 世界银行——英文——获取指标

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_urls)

    def parse_urls(self, response):
        item = WorldBankItem()
        selector = scrapy.Selector(response)

        indicators = selector.xpath('//*[@id="main"]/div[2]')
        indi_url = indicators.xpath('section[@class="nav-item"]/ul/li/a/@href').extract()
        # indi = re.findall(r'/indicator/.*/?view=chart', indicators, re.S)
        indi_name = indicators.xpath('section[@class="nav-item"]/ul/li/a/text()').extract()





        for each in indi_url:
            each = each[:-10] + "downloadformat=excel"
            # i.replace("view=chart", "downloadformat=excel") #使用replace进行替换时总是不成功，有待探索！
            item['indi_url'] = each
            print("indi_url", item['indi_url'])
            yield item
            yield scrapy.Request(url="http://api.worldbank.org/v2/en" + each,
                                 callback=self.download_excel)

        for each in indi_name:
            print("indi_name:", each)
            item['indi_name'] = each
            # self.filenames = indi_name
            yield item


    def download_excel(self, response):
        # item=response.meta['item']
        name_temp = response.url.split("/")[-1]
        name = name_temp.split("?")[-2]
        print("storename:", name, '-', response.url)
        filename = r"D:\workspace\scrapy\saas\worldbankexcelfiles\%s.xls" % name
        resp = requests.get(response.url)
        output = open(filename, 'wb')
        output.write(resp.content)
        output.close()
        yield None
