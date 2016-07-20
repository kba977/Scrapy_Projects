# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from QiuShiBaiKe.items import QiushibaikeItem

class MySpider(Spider):
    name = "xiaohua"
    allowed_domains = ["qiushibaike.com"]
    start_urls = [
        "http://www.qiushibaike.com/8hr/page/%s" % i for i in range(1, 3)
    ]

    def parse(self, response):
        xhs = Selector(response).xpath('//div[@class="article block untagged mb15"]')
        print xhs

        for xh in xhs:
            item = QiushibaikeItem()
            item['author'] = xh.xpath('div/a[2]/h2/text()').extract_first()
            item['content'] = xh.xpath('div[@class="content"]').xpath("string(.)").extract_first().strip()
            yield item
