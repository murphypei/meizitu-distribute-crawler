# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import threading
import re
import logging

from meizitu_crawler.settings import IMAGES_STORE_PATH


class BeautySpiderPipeline(object):
    def __init__(self):
        self.pics = 0

    # item从spider中传递过来
    def process_item(self, item, spider):

        # 如果item有内容
        if item is not None:
            # 设置图片存储目录，去掉末尾的序号，将其进行简单的合并
            images_name = item['name']
            m = re.match(r'([\u4e00-\u9fa5]*)(\(\d*\))?', images_name)
            dir_name = m.group(1)
            storage_path = os.path.join(IMAGES_STORE_PATH, spider.name,
                                        dir_name)

            # 递归创建存储文件夹
            if not os.path.exists(storage_path):
                os.makedirs(storage_path)
                # 保存page_url和tags文件
                # with open(os.path.join(storage_path, 'info.txt'), 'w') as f:
                #     f.write(item['page_url'] + '\n')
                #     f.write("tags: " + " ".join(item['tags']))

            image_url = item['image_urls']
            img_name = image_url.split('/')[-1]
            file_path = os.path.join(storage_path, img_name)

            # 防止重复爬取
            if not os.path.exists(file_path):
                # 多线程是为了多张图片的保存，此处虽然只有一张图片，但还是使用多线程
                t = threading.Thread(
                    target=self._write_image, args=(file_path, image_url))
                t.start()
                t.join()

        return item

    def _write_image(self, file_path, image_url):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",
            "Referer": "http://www.mmjpg.com/mm",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        with open(file_path, 'wb') as handle:
            response = requests.get(image_url, headers=headers, stream=True)
            logging.info("Start downloading image: {}".format(image_url))
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            handle.close()
            logging.info("Save image {} successfully".format(image_url))
