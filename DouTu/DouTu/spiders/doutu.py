# -*- coding: utf-8 -*-
import os
import requests
import scrapy
from DouTu.items import DoutuItem


class DoutuSpider(scrapy.Spider):
    name = "doutu"
    allowed_domains = ["doutula.com", "sinaimg.cn"]
    start_urls = ['https://www.doutula.com/photo/list/?page={}'.format(i) for i in range(1, 40)]

    def parse(self, response):
        i = 0
        for content in response.xpath('//li[@class="list-group-item"]/div/div/a'):
            i += 1
            item = DoutuItem()
            item['img_url'] = content.xpath('//img/@data-original').extract()[i]
            item['name'] = content.xpath('//p/text()').extract()[i]

            try:
                if not os.path.exists('doutu'):
                    os.makedirs('doutu')
                r = requests.get(item['img_url'])
                filename = 'doutu/{}'.format(item['name']) + item['img_url'][-4:]
                with open(filename, 'wb') as fo:
                    fo.write(r.content)
            except Exception as e:
                raise e

            yield item
