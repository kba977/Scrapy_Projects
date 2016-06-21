# -*- coding: utf-8 -*-

import os
import time
from logging import log
import json
from urllib import urlencode

import scrapy
from scrapy import Spider
from ZhiHuUser.items import UserItem
from scrapy.selector import Selector
from scrapy.shell import inspect_response

class UserSpider(Spider):
    name = 'users'
    domain = 'https://www.zhihu.com'
    login_url = 'https://www.zhihu.com/login/email'
    _xsrf = ''

    def __init__(self, url = None):
        self.user_url = url

    def start_requests(self):
        yield scrapy.Request(
            url = self.domain,
            callback = self.request_captcha
        )

    def request_captcha(self, response):
        # 获取_xsrf值
        self._xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
        # 获取验证码地址
        t = str(int(time.time()*1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'

        # 准备下载验证码
        yield scrapy.Request(
            url = captcha_url,
            meta = {
                '_xsrf': self._xsrf
            },
            callback = self.download_captcha
        )

    def download_captcha(self, response):
        # 下载验证码
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        # 用软件打开验证码图片
        os.system('open captcha.gif')
        # 输入验证码
        captcha = raw_input('Please enter captcha: ')

        yield scrapy.FormRequest(
            url = self.login_url,
            formdata = {
                'email': '***********',
                'password': '***********',
                '_xsrf': self._xsrf,
                'remember_me': 'true',
                'captcha': captcha
            },
            callback = self.after_login
        )


    def after_login(self, response):
        yield scrapy.Request(
            url = self.user_url,
            callback = self.parse_people,
        )


    def parse_people(self, response):
        '''
        function:
        1. 抓取个人资料
        2. 提取该人的 followees 和 followers 链接并发送请求
        '''

        sel = response.xpath('//div[@class="zm-profile-header ProfileCard"]')

        item = UserItem()
        item['url'] = response.url[:-6]
        item['name'] = sel.xpath('//div[@class="title-section ellipsis"]/span[@class="name"]/text()').extract_first()
        item['bio'] = sel.xpath('//div[@class="title-section ellipsis"]/span[@class="bio"]/@title').extract_first()
        item['location'] = sel.xpath('//span[@class="location item"]/@title').extract_first()
        item['business'] = sel.xpath('//span[@class="business item"]/@title').extract_first()
        item['gender'] = 0 if sel.xpath('//i[contains(@class, "icon-profile-female")]') else 1
        item['avatar'] = sel.xpath('//img[@class="Avatar Avatar--l"]/@src').extract_first()
        item['education'] = sel.xpath('//span[@class="education item"]/@title').extract_first()
        item['major'] = sel.xpath('//span[contains(@class, "education-extra")]/@title').extract_first()
        item['employment'] = sel.xpath('//span[contains(@class, "employment")]/@title').extract_first()
        item['position'] = sel.xpath('//span[contains(@class, "position")]/@title').extract_first()
        item['content'] = "".join(sel.xpath('//span[@class="fold-item"]/span[@class="content"]/text()').extract()).strip()
        item['ask'] = int(sel.xpath('//div[contains(@class, "profile-navbar")]/a[2]/span[@class="num"]/text()').extract_first())
        item['answer'] = int(sel.xpath('//div[contains(@class, "profile-navbar")]/a[3]/span[@class="num"]/text()').extract_first())
        item['agree'] = int(sel.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract_first())
        item['thanks'] = int(sel.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract_first())
        item['followee_count'] = int(sel.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@class="item"]/strong/text()').extract()[0])
        item['follower_count'] = int(sel.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[@class="item"]/strong/text()').extract()[1])


        ## 抓取 followees列表 (即该用户关注了谁)
        if item['followee_count'] != 0:
            yield scrapy.Request(
                url = self.user_url + '/followees',
                meta = {
                    'people_count': item['followee_count'],
                    'type': 'followee'
                },
                callback = self.parse_follow,
            )

        ## 抓取 followers列表 (即谁关注了该用户)
        if item['follower_count'] != 0:
            yield scrapy.Request(
                url = response.url + '/followers',
                meta = {
                    'people_count': item['follower_count'],
                    'type': 'follower'
                },
                callback = self.parse_follow
            )

        yield item

    def parse_follow(self, response):

        """
        1. 处理follow数据 (followee and follower), 即获取每一个用户信息
        2. 向获取更多列表数据发送请求
        """

        sel = Selector(response)
        people_links = sel.xpath('//a[@class="zg-link"]/@href').extract()
        people_count = response.meta['people_count']
        people_param = json.loads(sel.xpath('//div[@class="zh-general-list clearfix"]/@data-init').extract_first())
        

        # 请求所有的人
        zhihu_ids = []
        for people_url in people_links:
            zhihu_ids.append(os.path.split(people_url)[-1])
            yield scrapy.Request(
                url = people_url,
                callback = self.parse_people
            )

        ## 处理动态加载的用户(发送Ajax请求)

        if response.meta['type'] == 'followee':
            url = 'https://www.zhihu.com/node/ProfileFolloweesListV2'
        else:
            url = 'https://www.zhihu.com/node/ProfileFollowersListV2'


        # 请求所有的用户数据(更多列表 动态加载)
        start = 20
        while start < people_count:
            payload = {
                'method': 'next',
                '_xsrf': self._xsrf,
                'params': people_param['params']
            }
            payload['params']['offset'] = start
            payload['params'] = json.dumps(payload['params'])
            start += 20

            yield scrapy.Request(
                url = url,
                method='POST',
                body=urlencode(payload),
                callback=self.parse_post_follow
            )

        
    def parse_post_follow(self, response):
        """
        1. 获取动态请求拿到的人员
        """
        body = json.loads(response.body)
        people_divs = body.get('msg', [])

        # 请求所有的人
        zhihu_ids = []
        for div in people_divs:
            selector = Selector(text=div)
            link = selector.xpath('//a[@class="zg-link"]/@href').extract_first()
            print link
            if not link:
                continue

            zhihu_ids.append(os.path.split(link)[-1])
            yield scrapy.Request(
                url=link,
                callback=self.parse_people,
            )

    def parse_err(self, response):
        print 'crawl {} failed'.format(response.url)
