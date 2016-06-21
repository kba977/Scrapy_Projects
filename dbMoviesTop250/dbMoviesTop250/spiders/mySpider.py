from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from dbMoviesTop250.items import Dbmoviestop250Item

class MovieSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    rules = [Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
            Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),
                callback='parse_item', follow=False)
    ]

    def parse_item(self, response):

        sel = Selector(response)

        item = Dbmoviestop250Item()
        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()[0]
        item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').extract()[0]
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()[0]
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()[0]
        item['classification'] = sel.xpath('//span[@property="v:genre"]/text()').extract()[0]
        item['actor'] = sel.xpath('//*[@id="info"]/span[3]//a/text()').extract()[0]
        item['image_urls'] = sel.xpath('//div[@id="mainpic"]/a[@class="nbgnbg"]/img/@src').extract()

        return item