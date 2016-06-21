# coding: utf-8
import re
from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from JiKeXueYuan.items import JiKeXueYuanItem

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CourseSpider(Spider):
    name = "course"
    baseurl = "http://www.jikexueyuan.com/course/"
    allowed_domains = ["http://www.jikexueyuan.com/", "search.jikexueyuan.com", "jikexueyuan.com"]
    start_urls = [
        # 修改这里以完成整站的爬取
        # 'http://www.jikexueyuan.com/course/?pageNum=%d' % i for i in xrange(1, 86)
        'http://www.jikexueyuan.com/course/?pageNum=1'
    ]

    def __init__(self):
        self.cookies = {your-cookie}
        
    def parse(self, response):   
        s_total = Selector(text=response.body).xpath("//ul[@class='cf']/li/div[@class='lessonimg-box']/a/@href").extract()
        
        if len(s_total) > 0:
            for page in s_total:
                yield Request(page, callback=self.get_course_page, cookies=self.cookies)
        else:
            pass

    def get_course_page(self, response):
        x_course = Selector(text=response.body).xpath("//ul/li/div[@class='text-box']/h2/a")
        for x in x_course:
            try:
                href = x.xpath('@href').extract()[0]
                title = x.xpath('text()').extract()[0]

                meta = {}
                meta['href'] = href
                meta['title'] = title
                yield Request(href, callback=self.get_down_urls, meta={'meta': meta},  cookies=self.cookies)
            except:
                pass

    def get_down_urls(self, response):
        meta = response.meta['meta']
        path = Selector(text=response.body).xpath("//div[@class='crumbs']/div[@class='w-1000']/a/text()").extract()
        course_down = re.findall(r'source src="(.*?)"', response.body, re.S)
        item = JiKeXueYuanItem()
        if course_down:
            item['course_id'] = meta['href']
            item['course_name'] = meta['title']
            item['course_url'] = course_down[0]
            item['course_path'] = path
            yield item