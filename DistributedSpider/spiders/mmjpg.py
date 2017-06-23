# -*- coding: utf-8 -*-

__author__ = 'peic'

from scrapy_redis.spiders import RedisSpider
from scrapy.selector import Selector
from scrapy.http import Request

from DistributedSpider.items import DistributedSpiderItem
from DistributedSpider.items import DistributedSpiderItemLoader
from DistributedSpider.logger import logger

from DistributedSpider.settings import *

from redis import Redis

class Spider(RedisSpider):
    name = "mmjpg"
    redis_key = 'spider:start_urls'

    def __init__(self, category=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        # 限定域名表
        self.allowed_domains = ['www.mmjpg.com']
        self.url = "http://www.mmjpg.com"
    
    def parse(self, response):

        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWD)
        item = DistributedSpiderItem()
        loader = DistributedSpiderItemLoader(item, response)
        loader.add_xpath('category', u"/html/body/div[2]/div[1]/h2/text()")
        loader.add_value('page_url', response.url)
        loader.add_xpath('image_urls', u"//*[@id='content']//img/@src")
       
        nextUrl = response.xpath(u"//*[@id='page']/a[@class='ch next']/@href").extract()
        logger.debug(nextUrl)
        
        # 将获取到的url存放在redis中
        if nextUrl is not None:
            for u in nextUrl:
                redis.lpush('spider:start_urls', self.url + u)
        item = loader.load_item()    
        logger.debug(item)
        return loader.load_item()
