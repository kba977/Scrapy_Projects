# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Dbmoviestop250Item(scrapy.Item):
    name = scrapy.Field()  # 电影名字
    year = scrapy.Field()  # 上映年份
    score = scrapy.Field()  # 豆瓣分数
    director = scrapy.Field() # 导演
    classification = scrapy.Field() # 分类
    actor = scrapy.Field() # 演员
    image_urls = scrapy.Field() # 封面图片