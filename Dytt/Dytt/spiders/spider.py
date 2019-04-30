# -*- coding: utf-8 -*-
import scrapy
from Dytt.items import DyttItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://dytt8.net/']

    def parse(self, response):
        dyttItem = DyttItem()
        item = response.xpath("//div[@class='co_area2']/div[@class='co_content8']/ul/table/tr")[1]
        title = item.xpath('td/a[2]/text()').extract()[0]
        href = item.xpath('td/a[2]/@href').extract()[0]
        date = item.xpath('td[2]/font/text()').extract()[0]
        # print(title)
        # print(date)
        dyttItem['title'] = title
        dyttItem['date'] = date

        yield scrapy.Request(
            url = 'http://dytt8.net' + href,
            callback = self.parse_item,
            meta = {
                'item': dyttItem,
            }
        )

    def parse_item(self, response):
        dyttItem = response.meta['item']
        image = response.xpath("//div[@id='Zoom']//img[1]/@src").extract()[0]
        content = [i for i in response.xpath("//div[@id='Zoom']//text()[preceding-sibling::br]").extract() if i.strip() != ""]
        download_url = response.xpath("//div[@id='Zoom']//a/@href").extract()
        # print (image)
        # print ("\n".join(content))
        # print ("\n".join(download_url))
        dyttItem['image'] = image
        dyttItem['content'] = "\n".join(content)
        dyttItem['download_url'] = "\n".join(download_url)

        return dyttItem
