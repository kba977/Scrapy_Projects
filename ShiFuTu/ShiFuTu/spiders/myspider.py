import scrapy
from ShiFuTu.items import ShifutuItem 
from scrapy.selector import Selector

class ShiFuTuSpider(scrapy.spiders.Spider):
    name = "ShiFuTu"
    allowed_domains = ["www.10futu.com"]
    start_urls = [
        "http://www.10futu.com/",
    ]

    def parse(self, response):
        for sel in Selector(response).xpath("//div[@id>1]"):
            item = ShifutuItem()
            item['id'] = sel.xpath('./@id').extract()[0]
            item['title'] = sel.xpath('div[2]/a/img/@alt').extract()[0]
            item['imgurl'] = sel.xpath('div[2]/a/img/@src').extract()[0]
            yield item