# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings

class DateFormatPipeline(object):
    def process_item(self, item, spider):
        item['title'] = re.split('[丨|]', item['title'])[-1].strip()
        item['date'] = item['date'].split('：')[-1]
        item['image_url'] = item['image_url'].split('@')[0]
        
        description = item['description']
        if '内容简介' in description:
            description = re.findall(r'内容简介：(.*)', description, re.S)[0]
            if '更多' in description:
                description = re.findall(r'(.*)更多.*', description, re.S)[0]
            item['description'] = description.replace('\n', '')
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
            self.collection = self.db[settings['MONGODB_TABLE']]
            self.collection.insert(dict(item))
        return item
