#! -*- coding: utf-8 -*-

"""获取cookie用于登录，根据实际需求进行相应修改"""

import requests
import json
from scrapy_redis.connection import get_redis
import random
import logging
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware


def get_cookie(username, password):
    """利用request.Sesssion直接获取登录保存的cookie"""

    login_url = "http://www.xxx.com/login"
    sess = requests.Session()
    payload = {
        'username': username,
        'password': password,
        'rememberme': 'forever',
        'wp-submit': "登录",
        'redirect_to': "http://www.xxx.com/index",
        'testcookie': 1
    }
    response = sess.post(login_url, data=payload)
    cookies = response.cookies.get_dict()
    logging.warning("Get cookie successfully! username: {}".format(username))
    return json.dumps(cookies)


def init_cookie(user_reds, cookie_reds, spidername):
    """利用Redis数据库中保存的用户名和密码，生成cookie并保存在数据库中"""
    keys = user_reds.keys()
    for user in keys:
        password = user_reds.get(user)
        if cookie_reds.get("%s:cookies:%s-%s" %
                           (spidername, user, password)) is None:
            cookie = get_cookie(user, password)
            cookie_reds.set("%s:cookies:%s-%s" % (spidername, user, password),
                            cookie)


class CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        self.user_reds = get_redis(url=settings['REDIS_URL'], db=settings['USER_DB'], decode_responses=True)
        self.cookie_reds = get_redis(url=settings['REDIS_URL'], db=settings['COOKIE_DB'], decode_responses=True)
        init_cookie(self.user_reds, self.cookie_reds, crawler.spider.name)

    # 获取爬虫配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)
    
    def process_request(self, request, spider):
        """从cookie数据库中随机获取对应的cookie"""

        redis_keys = self.cookie_reds.keys()
        while(len(redis_keys) > 0):
            elem = random.choice(redis_keys)
            if spider.name + ':cookies' in elem:
                cookie = json.load(self.cookie_reds.get(elem))
                request.cookies = cookie
                request.meta['accoutText'] = elem.split("cookies:"[-1])
                break
