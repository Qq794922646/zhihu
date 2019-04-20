# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from zhihu.utils.commos import extract_num,question_content
from zhihu.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT

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
    def get_insert_sql(self):
#         插入知乎question表的SQL
        insert_sql='''
          insert into zhihu_question(ID,topics,url,title,content,answer_num,conmments_num,watch_user_num,click_num,crawl_time)
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)   
          
          ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), conmments_num=VALUES(conmments_num),
          watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        '''
        ID=self['ID'][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        conmments_num = extract_num("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = extract_num(self["watch_user_num"][0])
            click_num = extract_num(self["watch_user_num"][1])
        else:
            watch_user_num = extract_num(self["watch_user_num"][0])
            click_num = 0

        crawl_time=datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)


        params=(ID,topics,url,title,content,answer_num,conmments_num,watch_user_num,click_num,crawl_time)
        return insert_sql,params
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

    def get_insert_sql(self):
        #         插入知乎answer表的SQL
        insert_sql = '''
              insert into zhihu_answer(ID,url,question_id,author_id,content,parise_num,comments_num,create_time,update_time,crawl_time)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)   

              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), parise_num=VALUES(parise_num),
              update_time=VALUES(update_time)
            '''

        create_time=datetime.datetime.fromtimestamp(self['create_time']).strftime(SQL_DATETIME_FORMAT)
        update_time= datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)
        params=(self['ID'],self['url'],self['quertion_id'],self['author_id'],self['content'],self['parise_num'],self['comments_num'],create_time,update_time,self['crawl_time'].strftime(SQL_DATETIME_FORMAT))
        return insert_sql,params