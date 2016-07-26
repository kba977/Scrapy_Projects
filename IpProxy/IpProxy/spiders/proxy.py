# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from IpProxy.items import IpproxyItem
import time
class MyspiderSpider(scrapy.Spider):
    name = "kuaidaili"
    allowed_domains = ["http://www.kuaidaili.com/"]
    start_urls = (
        'http://www.kuaidaili.com/proxylist/%d/' % i for i in xrange(1,21)
    )

    def parse(self, response):
        item = IpproxyItem()
        IP = Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[1]/text()').extract()
        port = Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[2]/text()').extract()
        #status = Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[3]/text()').extract()
        #types = Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[4]/text()').extract()
        #support = Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[5]/text()').extract()
        #address = Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[6]/text()').extract()
        #speed= Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[7]/text()').extract()
        #testtime= Selector(response).xpath('//*[@id="index_free_list"]/table/tbody/tr/td[8]/text()').extract()

        for i in range(len(IP)):
            item['IP'] = IP[i]
            item['port'] = port[i]
            #item['status'] = status[i]
            #item['types'] = types[i]
            #item['support'] = support[i]
            #item['address'] = address[i]
            #item['speed'] = speed[i]
            #item['testtime'] = testtime[i]
            #item['grab_time'] = time.strftime('%Y-%m-%d')
            yield item









