# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

import logging

from meizitu_crawler.items import ImagesItem, ImagesItemLoader


class BeautySpider(CrawlSpider):
    name = "beauty_spider"
    allowed_domains = ['www.mmjpg.com']
    start_urls = ["http://www.mmjpg.com"]

    rules = (
        # Rule(LinkExtractor(allow=(r'/tag/[\w]*'))),
        Rule(LinkExtractor(allow=(r'/mm/[\d/]*')), callback='parse_item'),
    )

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

        # 提取下一页
        next_page = response.xpath(
            u"//*[@id='page']/a[@class='ch next']/@href").extract()
        for url in next_page:
            yield Request("http://www.mmjpg.com" + url, callback=self.parse_item)
