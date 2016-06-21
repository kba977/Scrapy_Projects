# coding: utf-8

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from OneSpider.items import PhotoItem, ArticleItem, AskItem

class MySpider(Spider):
    name = "ones"
    allowed_domains = ["caodan.org"]
    start_urls = [
        # "http://caodan.org/page/%d" % i for i in xrange(1, 1340)
        "http://caodan.org/page/%d" % i for i in xrange(1, 3)

    ]

    def parse(self, response):
        html = Selector(response).xpath("//div[@class='content']/h1[@class='entry-title']/a/@href").extract()
        # html 为列表, 其中有3个元素, 分别是 photo, article, ask 页面的链接

        ## 请求图片详情页
        yield scrapy.Request(
            url = html[0],
            callback = self.parse_photo
        )

        ## 请求文章详情页
        yield scrapy.Request(
            url = html[1],
            callback = self.parse_article
        )

        ## 请求问题详情页
        yield scrapy.Request(
            url = html[2],
            callback = self.parse_ask
        )


    def parse_photo(self, response):
        sel = Selector(response)

        item = PhotoItem()
        item['title'] = sel.xpath('//h1/text()').extract()[0]
        item['date'] = sel.xpath('//div[@class="date"]//p').xpath("string(.)").extract()[0]
        item['image_urls'] = sel.xpath('//div[@class="entry-content"]//img/@src').extract()
        item['motto'] = sel.xpath('//blockquote/p/text()').extract()[0]
        yield item

    def parse_article(self, response):
        sel = Selector(response)

        item = ArticleItem()
        item['title'] = sel.xpath('//h1/text()').extract()[0]
        item['date'] = sel.xpath('//div[@class="date"]//p').xpath("string(.)").extract()[0]
        item['content'] = sel.xpath('//div[@class="entry-content"]').xpath("string(.)").extract()[0]
        yield item
        

    def parse_ask(self, response):
        sel = Selector(response)

        item = AskItem()
        item['title'] = sel.xpath('//h1/text()').extract()[0]
        item['date'] = sel.xpath('//div[@class="date"]//p').xpath("string(.)").extract()[0]
        item['question'] = sel.xpath('//div[@class="cuestion-contenido"]/text()').extract()[0]
        item['answer'] = sel.xpath('//div[@class="cuestion-contenido"]')[1].xpath("string(.)").extract()[0]
        yield item