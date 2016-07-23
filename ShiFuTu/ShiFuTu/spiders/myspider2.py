import scrapy
from ShiFuTu.items import ShifutuItem 
from scrapy.selector import Selector

class ShiFuTuSpider2(scrapy.spiders.Spider):
    name = "ShiFuTu2"
    allowed_domains = ["www.10futu.com"]
    start_urls = [
        "http://www.10futu.com/ten_info.php?id=%d" % i for i in xrange(1, 2)
    ]

    def parse(self, response):
        item = ShifutuItem()
        sel = Selector(response)
        item['id'] = response.url[38:]
        item['title'] = sel.xpath("//h1[@class='info2_h1']/text()").extract()[0]
        item['imgurl'] = sel.xpath("//div[@class='news_info']/img/@src").extract()[0]
        return item