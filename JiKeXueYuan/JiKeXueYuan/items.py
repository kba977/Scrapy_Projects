# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class JiKeXueYuanItem(Item):
    course_id = Field()
    course_name = Field()
    course_url = Field()
    course_path = Field()
    pass

