# -*- coding: utf-8 -*-
import scrapy
from litterlove.items import LitterloveItem, VideoItem
import json, re

class MyspiderSpider(scrapy.Spider):
    name = "love"
    allowed_domains = ["xinpianchang.com"]
    start_urls = ['http://www.xinpianchang.com/index.php?app=user&ac=space&ajax=1&id=837979&page=%s' % i for i in range(1,6) ]

    def parse(self, response):
        # self.logger.info(response.url)
        lists = response.xpath('//li')

        for lst in lists:
            item = LitterloveItem()
            item['title'] = lst.xpath('a/img/@title').extract_first() 
            item['length'] = lst.xpath('a/em/text()').extract_first()
            item['date'] = lst.xpath('//span[@class="master-type-date"]/text()').extract_first()
            item['image_url'] = lst.xpath('a/img/@src').extract_first()
            item['description'] = lst.xpath('div[@class="master-type-intro master-type-intro-space"]/div/p/text()').extract_first()
            item['video'] = []
            video_detail_url = lst.xpath('a/@href').extract_first()

            yield scrapy.Request(
                url = video_detail_url,
                meta = {
                    'item': item
                },
                callback = self.video_detail_parse
            )

    def video_detail_parse(self, response):
        item = response.meta.get('item')
        self.logger.info(response.url)
        videos = json.loads(response.xpath('//script').re_first('origins = (\[.*?\])'))
        for video in videos:
            video_item = VideoItem()
            video_item['video_url'] = video.get('qiniu_url', None)
            video_item['resolution'] = video.get('resolution', None)
            item['video'].append(video_item)
        yield item