# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

import logging

from meizitu_crawler.items import ImagesItem, ImagesItemLoader


class BeautyDistributeSpider(RedisCrawlSpider):
    name = "beauty_distribute_spider"
    redis_key = "crawler:start_urls"
    allowed_domains = ['www.mmjpg.com']

    # 设置提取的url格式
    rules = (
        Rule(LinkExtractor(allow=(r'/tag/[\w]*'))),
        Rule(LinkExtractor(allow=(r'/mm/[\d/]*')), callback='parse_item'),
    )

    def __init__(self, category=None, *args, **kwargs):
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))

        super(BeautyCrawlerSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        """处理图片页面，提取图片Item
        """

        logging.info("Parsing item page: {}".format(response.url))

        item = ImagesItem()
        loader = ImagesItemLoader(item, response)
        loader.add_xpath('name', u"/html/body/div[2]/div[1]/h2/text()")
        loader.add_value('page_url', response.url)
        loader.add_xpath('image_urls', u"//*[@id='content']//img/@src")
        loader.add_xpath('tags', u"//*[@class='tags']//a/text()")
        yield loader.load_item()

        # 爬取下一页
        next_page = response.xpath(
            u"//*[@id='page']/a[@class='ch next']/@href").extract()
        for url in next_page:
            yield Request("http://www.mmjpg.com" + url, callback=self.parse_item)
