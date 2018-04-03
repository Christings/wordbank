# -*- coding:utf-8 -*-
import scrapy
import requests
from worldbank.items import WorldBankItem


class WorldBankSpider(scrapy.Spider):
    name = "worldbank"
    filenames = []

    # excel_url = "http://api.worldbank.org/v2/zh/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel" #世界银行——中文——下载excel地址样式
    # excel_url = "http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD.ZG?downloadformat=excel" #世界银行——英文——下载excel地址样式

    # excel_url = "http://api.worldbank.org/v2/zh"
    excel_url = "http://api.worldbank.org/v2/en"

    # start_url = 'http://data.worldbank.org.cn/indicator?tab=all' #世界银行——中文——获取指标
    start_url = 'http://data.worldbank.org/indicator?tab=all'  # 世界银行——英文——获取指标

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse_urls)

    # 获取世界银行所有指标，并且进行url拼凑，再对获得的url进行请求，从而下载excel文件
    def parse_urls(self, response):
        item = WorldBankItem()
        selector = scrapy.Selector(response)

        indicators = selector.xpath('//*[@id="main"]/div[2]/section[@class="nav-item"]/ul/li')

        for i in indicators:
            temp_url = i.xpath('a/@href').extract()  # 得到的结果为list
            # indi_url = str(temp_url)[:-12] + "downloadformat=excel"
            indi_url = str(temp_url).replace("view=chart", "downloadformat=excel")
            item["indi_url"] = indi_url.replace("'", "").replace("[", "").replace("]", '')
            # print('item["indi_url"]:', item["indi_url"])

            indi_name = i.xpath('a/text()').extract()
            item["indi_name"] = str(indi_name)
            # print('item["indi_name"]:', item["indi_name"])
            yield item

            url = indi_url.replace("'", "").replace("[", "").replace("]", '')
            yield scrapy.Request(url="http://api.worldbank.org/v2/en" + url, callback=self.download_excel)

    # 下载excel文件
    def download_excel(self, response):
        # print("url:", response.url)
        file_name_temp = response.url.split("/")[-1]
        file_name = file_name_temp.split("?")[-2]
        # print("file_name:", file_name)  # 存储的文件名称
        filename_location = r"D:\workspace\scrapy\caas\files\worldbankexcelfiles\%s.xls" % file_name

        resp = requests.get(response.url)
        output = open(filename_location, "wb")
        output.write(resp.content)
        output.close()
        return None
