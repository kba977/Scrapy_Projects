# -*- coding: utf-8 -*-

import os
import sys

from scrapy.spiders import Spider
from scrapy.selector import Selector
from dbMeiNv.items import DbmeinvItem

imageType = {u"大胸": 2, u"美腿": 3, u"颜值": 4, u"杂烩": 5, u"翘臀": 6, u"黑丝": 7}
imageTypeStr = ",".join(imageType.keys())

reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(Spider):
    name = "meinv"
    allowed_domains = ["http://www.dbmeinv.com"]
    imgType = (raw_input(u"请输入你想爬取的图片类型(默认所有): " + imageTypeStr + "\n")).decode('utf-8')
    try:
        if imgType == u'':
            url = "http://www.dbmeinv.com/dbgroup/show.htm?"
        else:
            url = "http://www.dbmeinv.com/dbgroup/show.htm?cid=%d" % imageType[imgType]
    except KeyError, e:
        raise u"输入有误, 请重新输入"

    pageNum = raw_input(u"请问您想抓取多少页(默认十页): ")
    try:
        if pageNum == "":
            pageNum = 10
        else:
            pageNum = int(pageNum)
    except ValueError, e:
        raise u"输入有误, 请重新输入"

    start_urls = [
        url + "&pager_offset=%d" % i for i in xrange(1,pageNum+1)
    ]

    def parse(self, response):
        imgs = Selector(response).xpath("//div[@class='thumbnail']/div[@class='img_single']/a[@class='link']/img[@class='height_min']")

        for img in imgs:
            item = DbmeinvItem()
            item['img_type'] = self.imgType
            item['title'] = img.xpath('@title').extract()[0]
            item['image_urls'] = img.xpath('@src').extract()
            yield item


