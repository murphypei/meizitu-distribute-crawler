# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import requests
import threading
import urllib

from .logger import logger
from DistributedSpider import settings

class DistributedspiderPipeline(object):

    def __init__(self):
        self.pics = 0

    # item从spider中传递过来
    def process_item(self, item, spider):

        # 如果item有内容
        if item is not None:
            # 图片存储路径
            for i in item:
                logger.debug(type(i))
            dir_path = os.path.join(settings.IMAGES_STORE_PATH, spider.name, item['category'].split('(')[0])

            # 递归创建存储文件夹
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            
            image_url = item['image_urls']
            img_name = image_url.split('/')[-1]
            file_path = os.path.join(dir_path, img_name)
            
            # 防止重复爬取
            if not os.path.exists(file_path):
                # 多线程是为了多张图片的保存，此处虽然只有一张图片，但还是使用多线程
                t = threading.Thread(target=self._write_image, args=(file_path, image_url))
                t.start()
                t.join()

        return item

    def _write_image(self, file_path, image_url):

        with open(file_path, 'wb') as handle:
            response = requests.get(image_url, stream=True)
            logger.debug("Start save image: {}".format(image_url))
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            handle.close()
            logger.debug("Save image {} successfully".format(image_url))
