# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import logging
from meizitu_crawler.settings import LOG_FILE

if __name__ == "__main__":

    formatter = logging.Formatter(
        '%(asctime)s [%(filename)s: %(lineno)d] %(levelname)s %(message)s')
    fh = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(fh)
    logger.addHandler(ch)

    # 执行爬虫命令
    # execute(['scrapy', 'crawl', 'beauty_spider'])
    execute(['scrapy', 'crawl', 'beauty_distribute_spider'])