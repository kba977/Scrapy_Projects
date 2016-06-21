# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class UserItem(Item):
    url = Field()
    name = Field()
    bio = Field()
    location = Field()
    business = Field()
    gender = Field()
    avatar = Field()
    education = Field()
    major = Field()
    employment = Field()
    position = Field()
    content = Field()
    ask = Field()
    answer = Field()
    agree = Field()
    thanks = Field()
    followee_count = Field()
    follower_count = Field()