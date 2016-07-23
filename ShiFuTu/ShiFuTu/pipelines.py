# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class ShifutuPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = u'{0}.jpg'.format(item['title'])
        return filename
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['imgurl'], meta={'item': item})
    def item_completed(self, results, item, info):
        return item