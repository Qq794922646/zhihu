# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import pickle
import time
from selenium.webdriver.common.keys import Keys
from mouse import move,click
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        pass
    def start_requests(self):

        # cookies=pickle.load(open('D:/python/project/zhihu/cookies/zhihui.cookie',"rb"))
        # cookie_dict = {}
        # for cookie in cookies:
        #     cookie_dict[cookie["name"]] = cookie["value"]
        # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

        from selenium.webdriver.chrome.options import Options
        chrome_option=Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:9222')
        brower=webdriver.Chrome(executable_path='D:/python/chromedriver/chromedriver.exe',chrome_options=chrome_option)
        brower.get('https://www.zhihu.com/signin')   #请求URL
        # 选中输入框的内容
        brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL+'a')
        # 在输入用户名
        brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("18622106094")
        # 选中输入框的内容
        brower.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
        # 在输入密码
        brower.find_element_by_css_selector(".SignFlow-password input").send_keys("q143256987")
        time.sleep(3)
        # 点击登录按钮
        move(898,617)
        click()
        brower.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(60)
        brower.get('https://www.zhihu.com/')
        cookies=brower.get_cookies()
        pickle.dump(cookies,open('D:/python/project/zhihu/cookies/zhihui.cookie',"wb"))
        cookie_dict={}
        for cookie in cookies:
            cookie_dict[cookie["name"]]=cookie["value"]
        return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict)]

        pass
