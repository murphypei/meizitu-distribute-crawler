### 基于scrapy和redis的简单爬虫

* 目标网站

    http://www.mmjpg.com/

* 分布式和非分布式

    在`spiders`中包含两个爬虫程序，`beauty_spider`是普通单机爬虫，`beauty_distribute_spider`是分布式爬虫。
    可以修改run.py文件选择需要运行的爬虫程序

* 运行

    `python run.py`

    