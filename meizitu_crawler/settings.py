# -*- coding: utf-8 -*-

# Scrapy settings for meizitu_crawler project
#


import os
import time

# 获取当前目录
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'meizitu_crawler'

SPIDER_MODULES = ['meizitu_crawler.spiders']
NEWSPIDER_MODULE = 'meizitu_crawler.spiders'

# 使用scrapy-redis调度请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Redis保存队列，不清除记录，能够回复和暂停爬虫
# SCHEDULER_PERSIST = True

# 确保所有的URL经过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'meizitu_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# 设置默认的Item
DEFAULT_ITEM_CLASS = 'meizitu_crawler.items.ImagesItem'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 设置cookie登录
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'image/webp,*/*;q=0.8',
    'Accept-language': 'zh-CN,zh;q=0.8',
    'Referer': 'https://www.mmjpg.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'meizitu_crawler.middlewares.meizitu_crawlerSpiderMiddleware': 543,
#}



# 默认开启站点隔离（也就是只爬取allow_domains的站点）
# SPIDER_MIDDLEWARES = {
#         'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': 500
# }

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    # 'meizitu_crawler.middlewares.cookie.CookieMiddleware': 500,
    # 'meizitu_crawler.middlewares.proxy.ProxyMiddleware': 543,
    'meizitu_crawler.middlewares.useragents.RotateUserAgentMiddleware': 400
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 设置item的pipelines
ITEM_PIPELINES = {
    'meizitu_crawler.pipelines.BeautySpiderPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400
}

# 设置item在redis中的默认存储键
REDIS_ITEMS_KEY = "meizitu:item"

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 图片保存路径
IMAGES_STORE_PATH = os.path.join(PROJECT_DIR, 'images_storage')

# 设置终止条件
# CLOSESPIDER_ITEMCOUNT = 2000

# Redis数据库设置
REDIS_URL = "redis://username:password@ip:port"
URL_DB = 0
USER_DB = 1
COOKIE_DB = 2

# 日志设置
# current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
# LOG_FILE = os.path.join(PROJECT_DIR, 'crawler_{}.log'.format(current_time))
LOG_FILE = os.path.join(PROJECT_DIR, 'crawler.log')