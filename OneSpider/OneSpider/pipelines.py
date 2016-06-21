# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from OneSpider.items import PhotoItem, ArticleItem, AskItem
from scrapy.pipelines.images import ImagesPipeline

class DateFormatPipeline(object):
        
    def process_item(self, item, spider):
        a = item['date'].replace(u'月','')
        tmp = a[:2] + '/' + a[2:]
        day = tmp.split('/')[0].strip()
        month = tmp.split('/')[1].strip()
        year = tmp.split('/')[2].strip()
        item['date'] = year+'/'+month+'/'+day
        return item


class MongoDBPipeline(object):

    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        vaild = True

        for data in item:
            if not data:
                vaild = False
                raise DropItem("Missing {0}!".format(data))
        if vaild:

            if isinstance(item, PhotoItem):
                self.collection = self.db['photo']
                self.collection.insert(dict(item))
            elif isinstance(item, ArticleItem):
                self.collection = self.db['article']
                self.collection.insert(dict(item))
            elif isinstance(item, AskItem):
                self.collection = self.db['ask']
                self.collection.insert(dict(item))
            else:
                raise DropItem("Error")
        return item