# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.item import Item, Field


class ImagesItem(Item):

    # 图片目录名称（一个页面一个目录）
    name = Field()
    # 所属页面地址
    page_url = Field()
    # 标签
    tags = Field()
    # 图片地址集合
    image_urls = Field()


class ImagesItemLoader(ItemLoader):
    default_item_class = ImagesItem()

    # MapCompose provides a convenient way to compose functions that only work with single values (instead of iterables).
    default_input_processor = MapCompose(lambda s: s.strip())

    # TakeFirst returns the first non-null/non-empty value from the values received
    default_output_processor = TakeFirst()

    # Join returns the values joined with the separator given in the constructor.
    description_out = Join()
