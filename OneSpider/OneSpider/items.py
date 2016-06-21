# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PhotoItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    date = scrapy.Field()
    motto = scrapy.Field()

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()

class AskItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
