# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LitterloveItem(scrapy.Item):
    title = scrapy.Field()
    length = scrapy.Field()
    date = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    video = scrapy.Field()

class VideoItem(scrapy.Item):
    resolution = scrapy.Field()
    video_url = scrapy.Field()