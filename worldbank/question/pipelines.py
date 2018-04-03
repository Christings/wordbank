# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import codecs
import json
from saas.items import WorldBankItem
from saas.mysql import MySql


# class JsonWithEncodingWorldBankPipeline(object):
#     '''保存到文件中对应的class
#            1、在settings.py文件中配置
#            2、在自己实现的爬虫类中yield item,会自动执行'''
#
#     def __init__(self):
#         self.file = codecs.open('info.json', 'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"  # 转换为json的
#         self.file.write(line)  # 写入文件
#         return item
#
#     def spider_closed(self, spider):  # 爬虫结束时关闭文件
#         self.file.close()


class WorldBankPipeline(object):
    # """"保存到数据库中对应的class
    #     1、在setting.py文件中配置
    #     2、在自己实现的爬虫类中yield item,会自动执行"""
    #
    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #     ''' 这里注释中采用写死在代码中的方式连接线程池，可以从settings配置文件中读取，更加灵活
    #     self.dbpool=adbapi.ConnectionPool('MySQLdb',
    #                                   host='127.0.0.1',
    #                                   db='crawlpicturesdb',
    #                                   user='root',
    #                                   passwd='123456',
    #                                   cursorclass=MySQLdb.cursors.DictCursor,
    #                                   charset='utf8',
    #                                   use_unicode=False)'''
    #
    # @classmethod
    # def from_setting(cls, settings):
    #     '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
    #                2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
    #                3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
    #     dbparams = dict(
    #         # 读取settings中的配置
    #         host=settings['MYSQL_HOST'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         db=settings['MYSQL_DBNAME'],
    #         charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
    #         cursorclass=pymysql.cursors.DictCursor,
    #         use_unicode=False,
    #     )
    #     dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
    #     return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到
    #
    # # pipeline默认调用
    # def process_item(self, item, spider):
    #     query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
    #     query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
    #
    # # 写入数据库中
    # def _conditional_insert(self, tx, item):
    #     # print(item['indi_name_en'])
    #     sql = "insert into worldbank_indicators(indi_name_en,indi_name_cn)values(%s,%s)"
    #     params = (item["indi_name_en"], "indi_name_cn")
    #     tx.execute(sql, params)
    #
    # # 错误处理方法
    # def _handle_error(self, failure, item, spider):
    #     print('--------------database operation exception!!-----------------')
    #     print('-------------------------------------------------------------')
    #     print(failure)
    # pipeline默认调用

    def process_item(self, item, spider):
        if isinstance(item, WorldBankItem):
            ms = MySql(host="localhost", user="root", pwd="421498", db="saas")
            if len(item['indi_name_cn']) == 0:
                pass
            else:
                newsql = "insert into worldbank_indicators(indi_name_en,indi_name_cn)values('%s','%s')" % (
                    item['indi_name_en'], item['indi_name_cn'])
                print(newsql)
                ms.ExecNoQuery(newsql.encode('utf-8'))
        else:
            pass
        return item

# class SaasPipeline(object):
#     def process_item(self, item, spider):
#         return item
