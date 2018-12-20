# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 引入keys类操作
import time
import requests
import threading


class MyThread(threading.Thread):
    def __init__(self,data,cookies):
        super(MyThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.data = data
        self.cookies = cookies
    def run(self):#定义每个线程要运行的函数
        try:
            url = "http://gxk.szjxjy.com.cn/student/video/json/ajaxPlay.do"
            urls = url+"?status="+self.data['status']
            urls += "&location="+self.data['location']
            urls += "&sessionTime=" + self.data['sessionTime']
            urls += "&courseStudentId=" + self.data['courseStudentId']
            urls += "&watchId=" + self.data['watchId']
            urls += "&farthestPosition=" + self.data['farthestPosition']
            urls += "&lastVideoPosition=" + self.data['lastVideoPosition']
            urls += "&canJump=" + self.data['canJump']
            urls += "&courseNo=" + self.data['courseNo']
            urls += "&courseId=" + self.data['courseId']
            urls += "&studentId=" + self.data['studentId']
            urls += "&currentWatchVersion=" + self.data['currentWatchVersion']
            urls += "&userId=" + self.data['userId']
            urls += "&validPlaySeconds=" + self.data['validPlaySeconds']


            res = requests.get(urls, cookies = self.cookies)
            print(res)
        except:
            pass

browser = webdriver.Chrome()
print('登录')
browser.get('https://gxk.szjxjy.com.cn/index.do')
time.sleep(1)
browser.find_element_by_name('j_username').clear()  # 这个是以name选择元素
browser.find_element_by_name('j_username').send_keys('***')
time.sleep(1)
browser.find_element_by_name('j_password').clear()  # 这个是以name选择元素
browser.find_element_by_name('j_password').send_keys('***')
time.sleep(1)
browser.find_element_by_xpath(".//*[@class='denglu']").send_keys(Keys.ENTER)  # 这里通过点击Enter键来登录
time.sleep(2)
try:
    radios = browser.find_elements_by_css_selector('input[type=checkbox]')
    for radio in radios:
        radio.click()
        time.sleep(2)
    browser.find_element_by_xpath(".//*[@id='begin']").click()
except:
    browser.find_element_by_class_name("xuexizhongxin").click()


time.sleep(5)
URL = []


flag = True
try:
    while flag:
        for link in browser.find_elements_by_xpath("//*[@href]"):
            if link.get_attribute('href')[0] == '/':
                if "https://gxk.szjxjy.com.cn/"+link.get_attribute('href') in URL:
                    flag = False
                else:
                    URL.append("https://gxk.szjxjy.com.cn/" + link.get_attribute('href'))
                    print("https://gxk.szjxjy.com.cn/" + link.get_attribute('href'))

        browser.find_element_by_id("queryForm").find_element_by_class_name("end").click()
        time.sleep(5)
except Exception as e:
    print(e)



for i in range(0,len(URL)):
    try:
        browser.get(URL[i])
        data ={
            "status" : "not+attempted",
            "location" : "5000",
            "farthestPosition" : "5000",
            "lastVideoPosition" :"5000",
            "sessionTime" : "30%3A51",
            "courseStudentId" : browser.find_element_by_name("courseStudentId").get_attribute('value'),
            "watchId" : browser.find_element_by_name("watchId").get_attribute('value'),
            "canJump" : browser.find_element_by_name("canJump").get_attribute('value'),
            "courseNo" : browser.find_element_by_name("courseNo").get_attribute('value'),
            "courseId" :browser.find_element_by_name("courseId").get_attribute('value'),
            "studentId" :browser.find_element_by_name("studentId").get_attribute('value'),
            "currentWatchVersion" :browser.find_element_by_name("currentWatchVersion").get_attribute('value'),
            "userId" : browser.find_element_by_name("userId").get_attribute('value'),
            "validPlaySeconds" : browser.find_element_by_name("validPlaySeconds").get_attribute('value')
        }
        print(data)

        cookie = {}
        for i in browser.get_cookies():
            cookie[i["name"]] = i["value"]

        thread = MyThread(data=data,cookies=cookie)
        thread.start()


    except Exception as e:
        print(e)

