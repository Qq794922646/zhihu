# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.loader import ItemLoader
from zhihu.items import ZhihuAnswerItem,ZhihuQuestionItem
import pickle
import time
from urllib import parse
from mouse import move,click
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    # headers='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    def parse(self, response):
        # 提取出HTML页面中的所有url，并跟踪这些url
        all_urls=response.css("a::attr(href)").extract()
        all_urls=[parse.urljoin(response.url,url)for url in all_urls]
        # all_urls=filter(lambda x:True if x.startwith("https") else False,all_urls)
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj=re.match('(.*zhihu.com/question/(\d+))(/|$).*',url)
            if match_obj:
                request_url=match_obj.group(1)
                quetion_id=match_obj.group(2)
                yield scrapy.Request(request_url,callback=self.parse_question)
    # 从页面提取question item
    def parse_question(self, response):
        match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*', response.url)
        if match_obj:
            quetion_id = int(match_obj.group(2))
        item_loader=ItemLoader(item=ZhihuQuestionItem(),response=response)
        item_loader.add_css('title','.QuestionHeader-title::text')
        item_loader.add_css('content', '.QuestionHeader-detail')
        item_loader.add_value('url', response.url)
        item_loader.add_value('ID',quetion_id)
        item_loader.add_css('answer_num','.List-headerText span::text')
        item_loader.add_css('comments_num','.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num','.NumberBoard-itemValue::text')
        item_loader.add_css('topics','.QuestionHeader-topics .Popover div::text')
        quetion_item=item_loader.load_item()
        pass

    # def start_requests(self):
    #
    #     # cookies=pickle.load(open('D:/python/project/zhihu/cookies/zhihui.cookie',"rb"))
    #     # cookie_dict = {}
    #     # for cookie in cookies:
    #     #     cookie_dict[cookie["name"]] = cookie["value"]
    #     # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
    #
    #     from selenium.webdriver.chrome.options import Options
    #     chrome_option=Options()
    #     chrome_option.add_argument('--disable-extensions')
    #     chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:9222')
    #     brower=webdriver.Chrome(executable_path='D:/python/chromedriver/chromedriver.exe',chrome_options=chrome_option)
    #     brower.get('https://www.zhihu.com/signin')   #请求URL
    #     # 选中输入框的内容
    #     brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL+'a')
    #     # 在输入用户名
    #     brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("18622106094")
    #     # 选中输入框的内容
    #     brower.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
    #     # 在输入密码
    #     brower.find_element_by_css_selector(".SignFlow-password input").send_keys("q143256987")
    #     time.sleep(3)
    #     # 点击登录按钮
    #     move(898,617)
    #     click()
    #     # brower.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
    #     time.sleep(60)
    #     brower.get('https://www.zhihu.com/')
    #     cookies=brower.get_cookies()
    #     pickle.dump(cookies,open('D:/python/project/zhihu/cookies/zhihui.cookie',"wb"))
    #     cookie_dict={}
    #     for cookie in cookies:
    #         cookie_dict[cookie["name"]]=cookie["value"]
    #     return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict)]
    #
    #     pass
    def start_requests(self):

        cookies=pickle.load(open('D:/python/project/zhihu/cookies/zhihui.cookie',"rb"))
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.keys import Keys
        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:9222')
        brower=webdriver.Chrome(executable_path='D:/python/chromedriver/chromedriver.exe',chrome_options=chrome_option)
        try:
            brower.maximize_window()
        except:
            pass
        brower.get('https://www.zhihu.com/signin')
        # 选中输入框的内容
        brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL+'a')
        # 在输入用户名
        brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("18622106094")
        # 选中输入框的内容
        brower.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
        # 在输入密码
        brower.find_element_by_css_selector(".SignFlow-password input").send_keys("q143256987")
        brower.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(10)
        login_success=False
        while not login_success:
            try:
                notify_ele=brower.find_element_by_class_name('GlobalWrite-nav')
                login_success=True
            except:
                pass
            try:
                english_captcha_element=brower.find_element_by_class_name('Captcha-englishImg')
            except:
                english_captcha_element=None
            try:
                chinese_captcha_element = brower.find_element_by_class_name('Captcha-chineseImg')
            except:
                chinese_captcha_element=None
            if chinese_captcha_element:
                # 获取验证码坐标
                ele_postion=chinese_captcha_element.location
                x_relative=ele_postion['x']
                y_relative=ele_postion['y']
                # 获取地址栏高度
                browser_navigation_panel_height=brower.execute_script('return window.outerHeight - window.innerHeight;')

                # base图片解码
                base_text=chinese_captcha_element.get_attribute("src")
                import base64
                code = base_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
                fh=open('yzm_cn.jpeg','wb')
                fh.write(base64.b64decode(code))
                fh.close()

                from zheye import zheye
                z = zheye()
                positions = z.Recognize('yzm_cn.jpeg')
                # 倒立文字处理  变换x轴Y轴的位置
                last_positions = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        last_positions.append([positions[1][1], positions[1][0]])
                        last_positions.append([positions[0][1], positions[0][0]])
                    else:
                        last_positions.append([positions[0][1], positions[0][0]])
                        last_positions.append([positions[1][1], positions[1][0]])
                    first_position=[int(last_positions[0][0]/2),int(last_positions[0][1]/2)]
                    second_position = [int(last_positions[1][0]/2), int(last_positions[1][1]/2)]
                    first_position_0=first_position[0]
                    first_position_1=first_position[1]
                    move(x_relative+first_position_0,y_relative+browser_navigation_panel_height+first_position_1)


                    click()

                    second_positions_0=second_position[0]
                    second_position_1=second_position[1]

                    move(x_relative + second_positions_0,y_relative + browser_navigation_panel_height + second_position_1)
                    click()
                    time.sleep(3)

                else:
                    last_positions.append([positions[0][1], positions[0][0]])
                    first_position = [int(last_positions[0][0] / 2), int(last_positions[0][1] / 2)]
                    # last_positions_00=last_positions[0]
                    first_position_11=first_position[1]
                    first_position_00 = first_position[0]
                    move(x_relative + first_position_00,y_relative + browser_navigation_panel_height + first_position_11)
                    click()
                brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + 'a')
                # 在输入用户名
                brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "18622106094")
                # 选中输入框的内容
                brower.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
                # 在输入密码
                brower.find_element_by_css_selector(".SignFlow-password input").send_keys("q143256987")
                move(917, 657)
                click()
            if english_captcha_element:
                base_text = english_captcha_element.get_attribute('src')
                import base64
                code = base_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
                fh = open('yzm_en.jpeg', 'wb')
                fh.write(base64.b64decode(code))
                fh.close()
                from tools.yundama_requests import YDMHttp
                yundama=YDMHttp('q794922646','q143256987',7367,'6472fbbafe3976a3767863d38bb52d25')
                code=yundama.decode('yzm_en.jpeg',5000,60)
                while True:
                    if code=='':
                        code=yundama.decode('yzm_en.jpeg',5000,60)
                    else:
                        break
                brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(Keys.CONTROL + 'a')
                brower.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(code)
                brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    Keys.CONTROL + 'a')
                # 在输入用户名

                brower.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                    "18622106094")
                # 选中输入框的内容
                brower.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + 'a')
                # 在输入密码
                brower.find_element_by_css_selector(".SignFlow-password input").send_keys("q143256987")
                move(933, 641)
                click()
        time.sleep(10)
        if brower.find_element_by_css_selector(".Tabs-link is-active"):
            print('进入首页')
            click()
        else:
            print('进入首页失败')


        brower.get('https://www.zhihu.com/')
        cookies = brower.get_cookies()
        pickle.dump(cookies,open('D:/python/project/zhihu/cookies/zhihui.cookie',"wb"))
        cookie_dict={}
        for cookie in cookies:
            cookie_dict[cookie["name"]]=cookie["value"]
        return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict)]
