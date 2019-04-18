# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ZhihuQuestionItem(scrapy.Item):
    ID=scrapy.Field()
    topics=scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    answer_num=scrapy.Field()
    comments_num=scrapy.Field()
    watch_user_num=scrapy.Field()
    click_num=scrapy.Field()
    crawl_time=scrapy.Field()
class ZhihuAnswerItem(scrapy.Item):
    ID = scrapy.Field()
    url = scrapy.Field()
    quertion_id= scrapy.Field()
    author_id= scrapy.Field()
    content= scrapy.Field()
    parise_num= scrapy.Field()
    comments_num= scrapy.Field()
    create_time= scrapy.Field()
    update_time= scrapy.Field()
    crawl_time= scrapy.Field()