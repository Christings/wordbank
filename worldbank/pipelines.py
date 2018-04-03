# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from worldbank.db.mysql import Mysql
from worldbank.items import WorldBankItem


class WorldbankPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WorldBankItem):
            mysql = Mysql(host='localhost', user='root', pwd='421498', db='saas')
            if len(item['indi_name']) == 0:
                pass
            else:
                newsql = "insert into worldbank_indi(indi_url,indi_name)values('%s','%s')" % (
                    item['indi_url'], item['indi_name'])
                print(newsql)
                mysql.ExecNoQuery(newsql.encode('utf-8'))
        else:
            pass
        return item
