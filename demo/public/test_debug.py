# from selenium import webdriver

# options=webdriver.ChromeOptions()
# options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument('--incognito')
# options.add_argument('--start-maximized')

# driver=webdriver.Chrome(chrome_options=options)
# driver.get('https://www.baidu.com/')
# import logging
# def logout(name):
#     # 先创建一个logger
#     logger = logging.getLogger(name)  # 定义Logger的名字，之前直接用logging调用的名字是root，日志格式用%(name)s可以获得。这里的名字也可以自定义比如"TEST"
#     logger.setLevel(logging.DEBUG)  # 低于这个级别将被忽略，后面还可以设置输出级别
#     # 创建handler和输出级别
#     ch = logging.StreamHandler()  # 输出到屏幕的handler
#     ch.setLevel(logging.INFO)  # 输出级别和上面的忽略级别都不一样，可以看一下效果

#     # 创建日志格式，可以为每个handler创建不同的格式
#     ch_formatter = logging.Formatter('%(name)s %(asctime)s {%(levelname)s}:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')  # 关键参数datefmt自定义日期格式

#     # 把上面的日志格式和handler关联起来
#     ch.setFormatter(ch_formatter)

#     # 将handler加入logger
#     logger.addHandler(ch)

#     return logger

# logout('test').info('thuehhth')
# # # 以上就完成了，下面来看一下输出的日志
# # logger.debug('logger test debug')
# # logger.info('logger test info')
# # logger.warning('logger test warning')
# # logger.error('logger test error')
# # logger.critical('logger test critical')

# from browser_actions import Commonweb
# from selenium import webdriver
# from randomdata import Random_data
# import time

# c=Commonweb()
# p=Random_data()
# c.open_browser()
# c.open_web('https://www.baidu.com/')
# time.sleep(2)
# c.double_click('css,.hot-refresh-text')
# time.sleep(3)
# c.suspension('css,.s-top-right-text')
# time.sleep(1)
# c.web_click('css,.soutu-btn')
# time.sleep(2)
# c.is_element_isdisplayed('css,.upload-pic')
# c.web_click('css,.upload-pic')
# time.sleep(1)
# c.uploadimg()
# time.sleep(2)
# c.get_screenpict('baidu')
# c.web_click('css,.upload-pic')
# time.sleep(1)
# c.uploadimg()

# import os
# import time
# print(os.getcwd())
# pictour_dir=os.path.join(os.sys.path[0],'pictour')
# print(pictour_dir)
# # # pict_name=time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time()))
# # # print(pict_name)
# # # pri_path=os.path.join(os.path.join(os.getcwd(),'pictour'),time.strftime('%Y-%m-%d-%H.%M.%S',time.localtime(time.time())))
# # # print(pri_path)

# # print(os.sys.path[0]) #上级目录
# # print(os.__file__)
# # print(os.path.abspath(__file__))
# # os.mkdir('pictour')
# # pict_path=os.path.join(os.sys.path[0],'picture')
# # if not os.path.exists(pict_path):
# #     os.mkdir(pict_path)
# # pict_name=os.path.join(pict_path,'{}.png'.format(54564))
# # print(pict_name)
# # # print(pict_path)
# # # print(os.path.exists('D:\master\pictour'))

# # def c(a):
# #     return a+1
    
# # c=lambda a:a+1


# # def c(a):
# #     return c+2

# # d=lambda y:test(y)
# from browser_actions import Commonweb
# from randomdata import Random_data
# import time
# import datetime

# c=Commonweb()
# p=Random_data()
# c.open_browser()
# c.open_web('https://at-bos-frontend-uat.atfxdev.com/login')
# c.display_input('css,.ivu-input-default','tyler.tang')
# c.display_input('css,.ivu-input-default','Tl123456',1)
# c.display_click('css,.ivu-btn-large')
# c.display_click('css,.ivu-badge>span')
# c.display_click('css,[data-old-padding-top] > [href="/client/clientListNew/:type*"]')
# c.display_input('css,.ivu-input-group-with-append > [placeholder]','1200008354')
# time.sleep(1)
# c.display_click('css,.ivu-btn-icon-only > .ivu-icon')
# time.sleep(1)
# c.display_click('css,div.ivu-table-overflowX>table>tbody.ivu-table-tbody>tr>td',1)
# c.switch_windows(1)
# time.sleep(2)
# c.display_click('css,[href="#tdAccount"]')
# time.sleep(4)
# print(c.is_element_selected('css,.ivu-checkbox-input'))
# print(c.get_attributes('css,label.switch>span.ivu-switch>input','value',2))
# time.sleep(1)
# list_len=c.get_lenofelement('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span')
# print(list_len)
# for i in range(0,list_len):
#     if str(c.get_text('xpath,//*[@id="tdAccount"]/div[2]/div/div/div[3]/div[1]/div[2]/table/tbody/tr/td[1]/div/div/span',i))==str(693005664):
#         print(i+1)
#         break


# star=datetime.datetime.now()
# c.display_click('css,.s_btn')
# end=datetime.datetime.now()
# print(end-star)
# c.web_click('css,.blk-sure-btn')
# time.sleep(0.5)
# if c.is_displayed('css,.la-redo-alt',2):
#     print(1111)
# else:
#     print(2222)

# time.sleep(1)
# # c.display_input('css,.s_ipt','python')
# print(c.display_get_text('css,.title-content-title',1))
# c.display_click('css,.title-content-title')
# time.sleep(1)
# c.switch_windows(1)
# c.js_scroll('down')
# time.sleep(5)


# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import time
# dr=webdriver.Chrome()
# dr.maximize_window()
# dr.get('https:\\www.baidu.com')

# ele=WebDriverWait(dr,10,0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.title-content-title')),message='timeout')
# print(ele)


#ele.click()

# from browser_actions import Commonweb
# from common_method import Commonmethod
# import time
# import os

# common=Commonweb()
# dr=common.open_browser()
# commethed=Commonmethod(dr)

# common.open_web('https://at-client-portal-uat.atfxdev.com/login')
# commethed.remove_register_topup()
# time.sleep(1)
# commethed.choose_register_lang('CN')
# commethed.login_cp('lemon.lin@newtype.io', 'Tl123456')
# time.sleep(10)
# print(common.element_is_visible('xpath,//div[@class="el-loading-mask"]'))
# while True:
#     text=common.get_attributes('xpath,//div[@class="el-loading-mask"]', 'style')
#     if 'display' not in text:
#         print(text)
#         continue
#     else:
#         common.display_click('xpath,//span[.="入金"]')

# import pymysql
# import pandas as pd
# conn=pymysql.connect(host='atfx2-dev.cey5cywit5mk.ap-east-1.rds.amazonaws.com',port=3306,user='atfx2-dev',password='W22b3yA3-ae9jTrerpb',db='')

# import pymongo
# import ssl

# ssl._create_default_https_context=ssl._create_unverified_context()

# ssl._create_default_https_context=ssl._create_unverified_context()



# client=pymongo.MongoClient('mongodb+srv://atfx-dev-admin:m578A3MGrcR3pRXVU2pA@atfx2-dev-loa0g.azure.mongodb.net'
# '/atfx_test?authSource=admin&replicaSet=atfx2-dev-shard-0&'
# 'readPreference=primary&appname=MongoDB%20Compass%20Community&retryWrites=true&ssl=true')

# db=client['atfxgm-uat']

# mydb=db['atfx_ib_links']
# data=mydb.find({'mtName':'mt4'}).limit(5)
# for i in data:
#     print(i['link'])

# print(type(data))
# for i in data:
#     print(data['link'])
# def A():
#     lis=[]
#     for i in 'hel':
#         dic={}
#         dic['point']=i
#         dic['key']=i
#         lis.append(dic)
#     return lis
# print(A())


# test={
#     "accountNumber": 1000000593,
#     "accountIbLink": "A03",
#     "mtPlatform": "mt4",
#     "currency": "USD",
#     "markup": "0",
#     "commission": 30,
#     "leverage": 200,
#     "mtGroup": "demoforex200",
#     "spreadType": "Edge",
#     "riskVideo": "Y",
#     "link": "+Gdea2zEybngAKqr+Jz7TgFKwooZcyQj5Sf6SnXvdqsOHcnNDE5ImIxftKiZ7QHOoP1PE6PKEPz952y/Epv1Sg==1583223302873",
#     "createBy": "admin",
#     "updateBy": "admin",
#     "isDeleted": 1,
#     "deleteDate": {
#       "$date": "2020-03-03T08:15:02.873Z"
#     },
#     "createDate": {
#       "$date": "2020-02-27T06:43:14.086Z"
#     },
#     "lastUpdateDate": {
#       "$date": "2020-02-27T06:43:14.086Z"
#     },
#     "__v": 0
# },
# {
#     "accountNumber": 1000000593,
#     "accountIbLink": "A03",
#     "mtPlatform": "mt4",
#     "currency": "USD",
#     "markup": "0",
#     "commission": 30,
#     "leverage": 100,
#     "mtGroup": "demoforex200",
#     "spreadType": "Edge",
#     "riskVideo": "Y",
#     "link": "+Gdea2zEybngAKqr+Jz7TgFKwooZcyQj5Sf6SnXvdqsQfEW5wN3JYjsVL09qzf2XoP1PE6PKEPz952y/Epv1Sg==1583223305961",
#     "createBy": "admin",
#     "updateBy": "admin",
#     "isDeleted": 1,
#     "deleteDate": {
#       "$date": "2020-03-03T08:15:05.961Z"
#     },
#     "createDate": {
#       "$date": "2020-02-27T06:43:33.613Z"
#     },
#     "lastUpdateDate": {
#       "$date": "2020-02-27T06:43:33.613Z"
#     },
#     "__v": 0
# }

# tset_list=[]
# for i in test:
#     test_dict={}
#     test_dict['link']=i['link']
#     test_dict['mtGroup']=i['mtGroup']
#     tset_list.append(test_dict)
# print(tset_list)

# dic={'currency': 'USD', 'markup': '0', 'leverage': 200, 'mtGroup': 'demoforex200', 'link': '+Gdea2zEybngAKqr+Jz7TgFKwooZcyQj5Sf6SnXvdqsOHcnNDE5ImIxftKiZ7QHOoP1PE6PKEPz952y/Epv1Sg==1583223302873'}

# print(len(dic))

# def A(d=1,a=None,b=None):
#     print(a and b != None)

# A(1)
# a=None
# b=None
# print(a and b ==None)
# print(a is None)

# import pytest
# import os
# import sys
# path_public=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\public'

# class Testduanyan():

#     def testa(self):
#       assert 'a' in 'llou'

#     def testb(self):
#       assert 1==1

# if __name__=='__main__':
#   pytest.main(['-v','-s',r'{}\test_debug.py'.format(path_public)])

# def A():
#   for i in range(1,89):
#     print(i)
#     if i==55:
#       return i
#       break

# print(A())

# from browser_actions import Commonweb
# from common_method import Commonmethod
# import time
# import os

# common=Commonweb()
# dr=common.open_browser()
# commethed=Commonmethod(dr)

# common.open_web('https://www.baidu.com')
# # commethed.choose_bos_lang('CN')
# # commethed.loginbos('tyler.tang', 'Tl123456')

# # common.display_click('xpath,//div[@class="scroll-content"]//span[.="资金管理"]')
# # time.sleep(1)
# # # common.display_input('css,#kw', 'python')
# # # common.keyboard_operation('css,#kw', 'a')
# # common.display_click('xpath,//li[@class="ivu-menu-submenu ivu-menu-opened"]//span[.="汇率调整"]')
# # common.right_click_link('xpath,//li[@class="ivu-menu-submenu ivu-menu-opened"]//span[.="汇率调整"]')
# common.right_click_link('xpath,//a[.="新闻"]')

# def removeab():
#     list_a=['aabbabc','baabaaadc']
#     list_b=[]
#     for i in list_a:
#         list_b.append(i.replace('ab', ''))
#     return list_b

# # print(removeab())
# def num_0(a,b,c,*args,city='beijing',name,**kwnum):
#     print(a,b,c,name,city,args,kwnum)  # 输出的时候直接用*或者** 的变量名
# num_0(1,2,3,4,5,6,7,city='hangzhou',name='jack',age=18,country='haidian')


# def foo(**t):
#     print(t)
# foo(a=1,b=2)

# def demo1(*canshu):
#     print(canshu)
#     for i in canshu:
#         print(i)

# def demo2(**canshu):
#     print(canshu)
#     for i in canshu:
#         print(i)
        
# def demo3(*args,**kwargs):
#     for i in args:
#         print(i)
#     for i in kwargs:
#         print(i)


# demo1('l','a','b')
# demo2(a=1,b=2,c=3)
# demo3('hello','tyler',a='hello',b='tyler')

# def serach(**kwargs):
#     for i in kwargs.keys():
#         print(i)
#     for i in kwargs.values():
#         print(i)
#     for key,value in kwargs.items():
#         print('字段{}保存在{}列'.format(key,value))

# serach(zubie='A',diancha='B')
# print(111)

# # a=['name', 'host', 'proxy', 'password', 'pool']
# # print(a[2])


# class A():

#     def __init__(self,file=None):

#         if file:
#             self.configpath=file
#         else:
#             self.configpath='我是一个路径'

#     def a(self,b):
#         print(self.configpath)
# #         print(b)

# # c=A()
# # c.a('我是第二个路径')

# # def test_kwargs(**kwargs):
# #     print(kwargs)
# #     print(type(kwargs))
# #     for key, value in kwargs.items():
# #         print("{} = {}".format(key, value))

# # test_kwargs(a=122,b=888)

# import allure
# import pytest
# import os 
# import sys
# import subprocess
# from handlelog import MyLog

# path_public=os.path.dirname(os.path.abspath(__file__))
# sys.path.append(path_public)

# @allure.feature("智能质检系统")
# class TestCheck():

#     @allure.story("智能质检系统-接口用例")
#     def test_case_check(self):
#         with allure.step('我是一个步骤'):
#             print(55555)

# if __name__ == "__main__":
#     pytest.main(['-s','-v',r'{}\test_debug.py'.format(path_public),
#     r'--alluredir={}\report\report_data'.format(path_public),'--disable-pytest-warnings'])
#     subprocess.call(r'allure generate {}\report\report_data -o {}\report\new_report --clean'.format(path_public,path_public),shell=True)
#     subprocess.call(r'allure serve {}\report\report_data'.format(path_public),shell=True)
# with open(r'D:\code\tylerhub\demo\registration_process\register_actions_bin\picture\test11.png','rb') as f:
#     comtent=f.read()

# def A(a:int)->int:
#     print(type(a))

# from browser_actions import Commonweb
# from common_method import Commonmethod
# import time

# common=Commonweb()
# comthod=Commonmethod(common.open_browser())

# common.open_web('https://at-bos-frontend-sit.atfxdev.com/login')
# time.sleep(1)
# comthod.choose_bos_lang('CN')
# comthod.loginbos('tyler.tang', 'Tl123456')
# common.display_click('css,.ivu-badge >span',3)

# print(common.get_attributes('xpath,//*[@id="app"]/div/div/div[1]/div[1]/div[1]/div/ul/li[2]/ul', 'style')=='')
# common.display_click('css,.ivu-badge >span',3)
# print(common.get_attributes('xpath,//*[@id="app"]/div/div/div[1]/div[1]/div[1]/div/ul/li[2]/ul', 'style'))

# import pymongo
# import ssl



# ssl._create_default_https_context = ssl._create_unverified_context()
# ssl._create_default_https_context = ssl._create_unverified_context

# uri='mongodb+srv://tylertest:Tl123456@test.6wmyw.mongodb.net/test?authSource=admin&replicaSet=atlas-8x0ltw-shard-0&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true'

# client=pymongo.MongoClient(uri)
# db=client['sample_analytics']
# colletion=db['accounts']
# list_data=[]

# data=colletion.find().limit(3)
# for i in data:
#     list_data.append(i)
# print(list_data)

# from read_dataconfig import ReadConfig
# from about_data import Aboutdata

# conFig=ReadConfig()
# abDate=Aboutdata()

# old_uri=abDate.str_insert(conFig.get_value('mongodb_test', 'uri'), 14, conFig.get_value('mongodb_test', 'username'))
# uri=abDate.str_insert(old_uri, 24, conFig.get_value('mongodb_test', 'psword'))
# print(uri)

import pymongo
import ssl


# ssl._create_default_https_context = ssl._create_unverified_context()
# ssl._create_default_https_context = ssl._create_unverified_context

# uri='mongodb+srv://tylertest:Tl123456@test.6wmyw.mongodb.net/test?authSource=admin&replicaSet=atlas-8x0ltw-shard-0&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true'

# client=pymongo.MongoClient(uri)
# db=client['sample_geospatial']
# colletion=db['shipwrecks']
# list_data=[]

# search={"watlev":"always dry"}
# data=colletion.find(search).limit(2).sort([('_id',-1)])
# for i in data:
#     list_data.append(i)
# print(list_data)

# def A(b=5,**kwargs):
#     print(b)
#     print(str(kwargs.keys()))
#     for key,value in kwargs.items():
#         print(key)



# def demo1(*args):
#     print(args)
#     for i in args:
#         print(i)

# def demo2(**canshu):
#     list_a=[]
#     list_b=[]
#     for key,value in canshu.items():
#         list_a.append(key)
#         list_b.append(value)
#     # str_a=tuple(list_a)
#     demo1(*list_a)
#     print(list_b)

# demo2(a='A')


# list_a=['a','b']
# print(list_a[0])
# h=tuple(item for item in list_a)
# # h=tuple(list_a)
# print(h[0])
# print(h)

# def demo2(**canshu):
#     for i in canshu.keys():
#         print(i)

# demo2(a=2,c='ddd')

# for i in range(0,2):
#     print(i)
# a=['c','d','f']
# b=[1,2,4]
# for x,y,z in a,b:
#     print(x)

# def demo1(*args):
#     print(args)
#     for i in args:
#         print(i)

# def demo2(**kwargs):
#     print(kwargs)
#     for i in kwargs:
#         print(i)

# demo1(*['a','b',5])
# demo2(**{'a':1,'b':'jdk','c':'ello'})
# demo2(a=1,b='jdk',c='ello')
# list=[['a','b',5],[1,3,5]]
# print(*list)

# import random
# print(random.randint(0, 5))

# a=44444
# b="//a[.='{}']".format(a)
# print(b)
# import allure

# import os
# import sys


# print(os.environ['path'])


# import allure
# import os

# os.system(r'allure generate {}\report\result -o {}\report\allure_report --clean'.format(path_process,path_process))
# import pytest
# import os

# @pytest.mark.flaky(reruns=2, reruns_delay=2)
# def test_01():
#     print('执行1')
#     assert 0 == 1

# def test_02():
#     print('执行2')
#     assert 0 == 0

# if __name__=='__main__':
#     pytest.main(['-s','-v',os.path.abspath(__file__),'--reruns=2','--reruns-delay=2'])
#     pytest.main(['-s','-v',os.path.abspath(__file__)])

# a=2
# for i in range(0,3-a):
#     print(i)

# import collections
# list=['nlpay','cashu','cashu','cashu','nlpay','sticpay']

# result=collections.Counter(list)
# a=''
# for key,values in result.items():
#     if values>=3:
#         a=key
#         b=values
#         break
#     else:
#         a=list[0]
#         times=result[a]
        

# print(a)
# print(b)

# list1=['4stgYLRT5@qq.com', 'AWzB0iRgH@qq.com', 'P3mD8ZQqg@qq.com']
# list2=['5345645464@q.com', '1564564545@qq.com', '1564654466@qq.com', '54346575', '456456464@qq.com', 'yLopt0nHv@gmail.com', 'mPZG69XfH@qq.com', 'nr6pcNkSx@163.com', 'wT41opAuL@gmail.com', 
# 'pAqVXmZGf@qq.com', 'uT0MX1gmZ@qq.com', 'O4msn7b3v@gmail.com', 'AtBNRmklP@qq.com', 'wFm8J7zyL@qq.com', 'NwQbDXW0h@163.com', '15345644646@qq.com', 'P3mD8ZQqg@qq.com', 'uYpLrISnl@gmail.com', 'tvGgU5q7a@gmail.com', 'HhbKOdg9J@gmail.com', 'FbYdWO0hV@gmail.com', 'uYpLrISnl@gmail.com', 'AWzB0iRgH@qq.com', 'gFlA7mSNH@gmail.com', '4stgYLRT5@qq.com']


# a='/'.join(list1)
# b='/'.join(list2)
# print(a in b)

# import keyword

# print(keyword.kwlist)

# import random
# a=random.random()


# print(a)

# a='''你是一个憨憨 
# 天天不吃早餐
# 爱情与你无关 
# 整天郁郁寡欢'''
# print(a)

# print("xpath,//div[@class='bankinfo-page']/div[1]//div[@class='bank-row']/div[{}]//div/span[@class='del-btn c-float']",end='')
# print(111)
import requests

# import requests
# import json

# # host = "http://httpbin.org/"
# # endpoint = "get"

# # url = ''.join([host,endpoint])
# # print(url)
# # r = requests.get(url)
# # #response = r.json()

# # print (type(r.text))
# # print (eval(r.text))



# import requests
# import json

# # host = "http://httpbin.org/"
# # endpoint = "post"

# # url = ''.join([host,endpoint])
# # headers = {"User-Agent":"test request headers"}
# # data = {
# #     "sites": [
# #                 { "name":"test" , "url":"www.test.com" },
# #                 { "name":"google" , "url":"www.google.com" },
# #                 { "name":"weibo" , "url":"www.weibo.com" }
# #     ]
# # }

# # r = requests.post(url,headers=headers,json=data)
# # # r = requests.post(url,data=json.dumps(data))
# # response = (r.text)
# # print(response)

# from api import Api
# from read_dataconfig import ReadConfig


# host='https://at-client-portal-api-sit.atfxdev.com/'
# endpoint='login'
# url=''.join([host,endpoint])

# headers={
#     'accept':'application/json, text/plain, */*',
#     'accept-encoding':'gzip, deflate, br',
#     'accept-language':'zh,zh-CN;q=0.9,en;q=0.8',
#     'content-type':'application/json;charset=UTF-8',
#     'sec-ch-ua':'"Google Chrome";v="93","Not;A Brand";v="99", "Chromium";v="93"',
#     'sec-fetch-dest':'empty',
#     'sec-fetch-mode':'cors',
#     'sec-fetch-site':'same-site',
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
# }

# data={
#     "entity": "GM",
#     "email": "tyler.tang@test.com",
#     "password": "CzOMlg2xtgC0UmkRPdpi+Q==",
#     "loginType": "email",
#     "accountNumber":1000005349
# }

# re=Api()
# conFig=ReadConfig()
# tesda=re.api_post(host,path=endpoint,headers=headers,json=data)
# print(tesda.json()['data']['storageValue']['id_token'])
# conFig.modify('login_cpToken', 'x-token', tesda.json()['data']['storageValue']['id_token'])


# # r=requests.post(url,headers=headers,json=data)
# # retdata=r.json()
# # # print(retdata)
# # print(retdata['data']['storageValue']['id_token'])



# a=10
# b=10*0.05
# print(b)

# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser()
# common.open_web('https://www.baidu.com/')

# common.right_click_link("css,[href='http://tieba.baidu.com']")


# for i in range(0,7):
#     print(i)
#     if i==4:
#         print('到头了')
#         break
    



# from api import Api
# from read_dataconfig import ReadConfig

# host='https://at-bos-api-sit.atfxdev.com'
# endpoint='/v1/privilege/login'
# url=''.join([host,endpoint])

# headers_login={
#     'accept':'application/json, text/plain, */*',
#     'accept-encoding':'gzip, deflate, br',
#     'accept-language':'zh,zh-CN;q=0.9,en;q=0.8',
#     'content-type':'application/json;charset=UTF-8',
#     'sec-ch-ua':'"Google Chrome";v="93","Not;A Brand";v="99", "Chromium";v="93"',
#     'sec-fetch-dest':'empty',
#     'sec-fetch-mode':'cors',
#     'sec-fetch-site':'same-site',
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
#     }

# data_login={
# 	"account": "tyler.tang", 
# 	"passwd": "a12e16f04b1794c327b5d70f8954ff2f"
#     }

# re=Api()
# conFig=ReadConfig()
# deel=re.api_post(conFig.get_value('api_login_bos', 'host'),conFig.get_value('api_login_bos', 'path'),headers=headers_login,json=data_login)

# print(deel.json()['data']['token'])


# from browser_actions import Commonweb

# common1=Commonweb()
# common2=Commonweb()
# driver1=common1.open_browser()

# driver2=common2.open_browser()

# common1.open_web('https://at-bos-frontend-sit.atfxdev.com/login')
# common2.open_web('https://at-bos-frontend-sit.atfxdev.com/login')
# print(50001*4.1783)
# print(round(50001*4.1783))


# str=input('请输入：')
# print(str)

# import datetime
# from dateutil import parser

# from handle_database import Database_operate
# from read_dataconfig import ReadConfig


# now=datetime.datetime.now()
# print(now)

# yes=(datetime.datetime.now()-datetime.timedelta(days=2)).strftime('%Y-%m-%d')
# print(yes)

# yes2=(datetime.datetime.now() - datetime.timedelta(days=now.weekday()+1)).strftime('%Y-%m-%d')
# print(yes2)
# last_week_start = now - datetime.timedelta(days=now.weekday()+8)
# print(last_week_start)
# last_week_end = now - datetime.timedelta(days=now.weekday()+2)
# print(last_week_end)
# this_month_start = datetime.datetime(now.year, now.month, 1)
# # print(yes)
# print(this_month_start)
# print(last_week_start)
# print(last_week_end)

# print(last_week_start.strftime('%Y-%m-%d'))

# last_month_end = this_month_start - datetime.timedelta(days=1)
# print(last_month_end)
# last_month_start = (datetime.datetime(last_month_end.year, last_month_end.month, 1)).strftime('%Y-%m-%d')
# print(last_month_start)
# print(b)


# dataBase=Database_operate()
# conFig=ReadConfig()
# dateStr1 = '2021-09-06T00:00:00Z'
# dateStr2 = '2021-09-16T23:59:59Z'
# myDatetime1 = parser.parse(dateStr1)
# myDatetime2 = parser.parse(dateStr2)
# print(myDatetime1)
# print(myDatetime2)
# # times=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 
# # 'atfxgm-sit', 'atfx_deposit',{"$and": [{"createDate_mt": {"$gte": myDatetime1,"$lte": myDatetime2}}, 
# # {"accountNumber": 1200008143}]},'createDate_mt',N=0)
# # print(times)
# print(datetime.datetime(2021, 9, 10, 6, 1, 35, 831000))



# from handle_database import Database_operate
# from read_dataconfig import ReadConfig
# from dateutil import parser
# import datetime


# dataBase=Database_operate()
# conFig=ReadConfig()
# dateStr1 = '2021-09-01T00:00:00Z'
# dateStr2 = '2021-09-30T23:59:59Z'
# myDatetime1 = parser.parse(dateStr1)

# myDatetime2 = parser.parse(dateStr2)


# times=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 
# 'atfxgm-sit', 'atfx_deposit',{"$and": [{"createDate_mt": {"$gte": myDatetime1,"$lte": myDatetime2}},{"$or":[{"currStatus":'S'},{"currStatus":'U'}]}, 
# {"accountNumber": 1000005349}]},'createDate_mt','fromAmt','rate','mt4Amt','channel','currStatus',N=0)
# print(times[0]['createDate_mt'])

# print(times[0]['createDate_mt']+datetime.timedelta(hours=3))

# times2=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'), 
# 'atfxgm-sit', 'atfx_withdrawal',{"$and": [{"createDate_mt": {"$gte": myDatetime1,"$lte": myDatetime2}}, 
# {"accountNumber": 1000005349}]},'createDate_mt','settleAmt','realRate','mtAmt','channel','currStatus',N=0)
# print(times2)


# times3=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_fund_transfer',
# {"$and": [{"createDate_mt": {"$gte": myDatetime1,"$lte": myDatetime2}},{"currStatus":"S"},
# {"$or":[{"fromAccountNumber":1000005349},{"toAccountNumber":1000005349}]}]},'createDate_mt','toMtAmt','rate','currStatus',N=0)
# print(times3)


# import pytest
# import os
# import pytest_check

# class Testca():

#     def test01(self):
#         print('aaaa')

#     def test02(self):
#         for i in range(0,4):
#             pytest_check.equal(i,2,i)




# if __name__=='__main__':
#     pytest.main(['-s','-v',os.path.abspath(__file__)])
# from handle_database import Database_operate
# from read_dataconfig import ReadConfig

# dataBase=Database_operate()
# conFig=ReadConfig()
# data=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order where login ="{}" and Close_Time="1970-01-01 00:00:00"'.format(66200125),
# conFig.get_value('mysql_AWS', 'host'),conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'))

# print(data[6])

# import datetime

# timestr='16/09/2021 09:15:05'

# print((datetime.datetime.strptime(timestr,'%d/%m/%Y %H:%M:%S'))==data[6])



# import locale

# locale.setlocale(locale.LC_NUMERIC, "us")
# price = '-59,083.79'
# print(locale.atof(price))


# a=((536752,672003923,'2021-01-20 12:06:07'),(535449,65200841,'2020-10-30 05:24:46'),(533749,632000032,'2020-07-14 13:02:46'))
# b=[{'Ticket':535449,'account':65200841,'time':'2020-10-30 05:24:46'},{'Ticket':536752,'account':672003923,'time':'2021-01-20 12:06:07'}]

# for i in b:
#     for y in range(0,len(a)):
#         if i['Ticket']==a[y][0]:
#             print(i,y)
#             print(i['account']==a[y][1])
#             print(i['time']==a[y][2])
#             print('----------------')
#             break
#         else:
#             print(i,y)
#             print('没对上')

# import pytest
# import os
# import pytest_check

# class Testca():

#     def test01(self):
#         print('aaaa')

#     def test02(self):
#         print(pytest_check.equal(2,2,'断言失败'))




# if __name__=='__main__':
#     pytest.main(['-s','-v',os.path.abspath(__file__)])


# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser()

# common.open_web('https:///www.baidu.com')

# a='Open_Trade_List_2021-10-29.xlsx'

# import re

# b=re.findall('Open_Trade_List_...........xlsx',a)
# print(''.join(b))

# import os

# for i,x,y in os.walk(r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data'):
#     print(i,x,y)
# import re
# if re.findall('Close_Trade_List_...........xlsx', 'Close_Trade_List_2021-10-27.xlsx')!= None:
#     print(55555)
# print(re.findall('Trade_List_.........xlsx', 'Close_Trade_List_2021-10-27.xlsx'))
# openOrder_excel=''.join(re.findall('Close_Trade_List_...........xlsx', 'Close_Trade_List_2021-10-27.xlsx'))
# print(openOrder_excel)

import pyperclip



# pyperclip.copy('Hello World!')



# from about_data import Aboutdata
# dealData=Aboutdata()
# # workbook = openpyxl.load_workbook(r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\test.xlsx')
# pyperclip.copy(data)
# sheet=workbook.active



# workbook.save(r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\test.xlsx')
# print(pyperclip.paste())
# import openpyxl
# data=pyperclip.paste()
# li=[]
# for i in data:
#     li.append(i.strip('\n'))

# print(li)

# with open(r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\test.txt', 'w+') as f:
#     f.write(''.join(li))




# dealData.openexcel(r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\copy_openOrder.xlsx','copy_openOrder')
# a=dealData.dict_data()
# print(a)     

# import dbf


# dbf.Table(r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\copy_openOrder.xlsx').export(filename=r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\copy_openOrder2.xlsx')




import xlwt                     #需要的模块
def txt_xls(filename,xlsname):   
    """    :文本转换成xls的函数   
    :param filename txt文本文件名称、  
    :param xlsname 表示转换后的excel文件名  
    """   
    try:      
        f = open(filename,'r')
        print(f.read())
        f.seek(0,0)
        xls=xlwt.Workbook()        
        #生成excel的方法，声明excel        
        sheet = xls.add_sheet('sheet1',cell_overwrite_ok=True)        
        x = 0        
        while True:            
            #按行循环，读取文本文件           
            line = f.readline()
            print(line)            
            if not line:               
                break  #如果没有内容，则退出循环            
            for i in range(len(line.split('\t'))):               


                item=line.split('\t')[i]               
                sheet.write(x,i,item)
                #x单元格经度，i 单元格纬度           
            x += 1 #excel另起一行      
        f.close()        
        xls.save(xlsname)
        #保存xls文件   
    except:        
        raise

# if __name__ == "__main__" :   
#     filename =r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\test.txt'
#     xlsname  =r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\copy_openOrder1.xlsx'
#     txt_xls(filename,xlsname)

# filename =r'C:\Users\tyler.tang\Desktop\code\tylerhub\demo\order_list\test_data\test.txt'
# with open(filename,'r') as f:
#     data=f.read()
#     print(data)
#     f.seek(0.0)
#     line=f.readline()
#     print(line)
# print(len(line.split('\t'))-1)
# print(line)
# for i in range(len(line.split('\t'))-1):
#     item=line.split('\t')[i]
#     print(item) 

# import datetime

# str1='16/09/2021 09:35:30'
# time1=(datetime.datetime.strptime(str1,'%d/%m/%Y %H:%M:%S')).strftime('%Y-%m-%d %H:%M:%S')

# print(type(time1))
# print(time1)
# time2='2021-09-16 09:35:30'

# print(time1==time2)

# import random
# for i in range(10):
#     print(random.randint(31, 40))
# if  (not 1==3) and (7>9 and 9>8):
#     print(111)
# else:
#     print(222)

# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser(browsername='opera')

# common.open_web('https://www.baidu.com/')

# from selenium import webdriver

# dr=webdriver.Opera()

# dr.get('https://www.baidu.com/')


# import sys

# import re

# # path1=sys.path
# pattern = r'[Pp]ython\d*\S?\d{1,}$'

# # list1=['D:\Python\Python38-32\DLLs', 'D:\Python\Python38-32\lib', 'D:\Python\Python3-32']

# # for i in list1:
# #     result=re.findall(pattern, i)
# #     print(result)

# for i in sys.path:
#     if (''.join(re.findall(pattern, i))) !='':
#         print(i)
#         print(type(i))


# a=100
# b=100
# print(a is b)

# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser(browsername='chrome')

# common.open_web('https://www.baidu.com/')


# from selenium import webdriver
# options = webdriver.ChromeOptions()
# options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; JER-TN10 Build/HUAWEIJER-TN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/12.4 SP-engine/2.25.0 baiduboxapp/12.4.0.11 (Baidu; P1 10) NABar/1.0')
# # options.add_argument('--headless')  # 浏览器不提供可视化页面
# # options.add_argument('--user-agent=iphone8')
# driver=webdriver.Chrome(options=options)
# driver.get('https://at-client-portal-sit.atfxdev.com/login')


# chrome的user-agent配置
# firefox的安装路径
# 其他浏览器的驱动验证
# safari浏览器驱动下载
# 其他浏览器的无痕模式


# import win32con,win32api
# def get_Reg_key(path,key_):
#     # coding:utf-8
#     reg_root = win32con.HKEY_LOCAL_MACHINE
#     #reg_root = win32con.HKEY_CLASSES_ROOT
#     reg_path = r'%s' % path
#     reg_flags = win32con.KEY_READ | win32con.KEY_WOW64_64KEY
#     # 读取键值
#     key = win32api.RegOpenKey(reg_root, reg_path, 0, reg_flags)
#     value, key_type = win32api.RegQueryValueEx(key, key_)
    
#     #关闭键
#     win32api.RegCloseKey(key)
#     return {"value":value}


# import winreg
	
# reg_path=r"Software\\ThunderCloudToolboxs" #不要填入HKEY_CURRENT_USER，在openkey的时候填
# key=winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,reg_path)
# data=winreg.QueryValueEx(key,None) # 获取默认值 传递 None
# #data=winreg.QueryValueEx(key,'DisplayIcon') #默认值传递None
# print(data[0])#获取数据

# from selenium import webdriver
# dr=webdriver.Edge(r'D:\Python\Python38-32\msedgedriver.exe')

# import os
# from read_dataconfig import ReadConfig
# options = webdriver.ChromeOptions()
# # options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 8.1.0; OPPO R11t Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045410 Mobile Safari/537.36 V1_AND_SQ_7.7.0_884_YYB_D QQ/7.7.0.3645 NetType/WIFI WebP/0.3.0 Pixel/1080')
# # options.add_argument('--user-agent=Iphone X')

# import sys
# path=sys.executable.replace('python.exe', 'chromedriver.exe')

# from selenium import webdriver
# options=webdriver.ChromeOptions()
# options.add_argument('--start-maximized')
# dr=webdriver.Chrome(options=options,executable_path=path)
# filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'config\Chrome_userAgnet.ini')
# conFig_agnet=ReadConfig(filepath=filepath)
# conFig=ReadConfig()
# options.add_argument('--user-agent={}'.format(conFig_agnet.get_value('user_agnet','Ipad_Mini')))
# dr=webdriver.Chrome(options=options)
# # dr.maximize_window()
# dr.get(conFig.get_value('cp_login', 'sit'))


# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser(browsername='Edge')

# common.open_web('https://www.baidu.com/')

# from selenium import webdriver


# driver = webdriver.Safari()
# driver.get("https://baidu.com/")


# def is_chinese(string):
#     for ch in string.decode('utf-8'):
#         if u'/u4e00' <= ch <= u'/u9fa5':
#             print('这东西是中文')
#         else:
#             print('不知道是啥')

# is_chinese('中文')
# import langid
# print(langid.classify('Tiếng Việt')[0])

# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser(browsername='chrome')

# common.open_web('https://www.baidu.com/')

# print(common.check_language("css,[href='http://image.baidu.com/']"))

# from handle_database import Database_operate
# from read_dataconfig import ReadConfig

# dataBase=Database_operate()
# conFig=ReadConfig()

# dataBase.search_in_mongodb(conFig.get_value('mongodb','uri'),'atfxgm-sit','atfx_account_info',{"accountNumber":1000005349},'lang',N=1)

# from browser_actions import Commonweb


# common=Commonweb()

# # common.open_browser(browsername='firefox')

# a=str(common.open_browser(browsername='firefox'))

# if 'Message' in a:
#     print(666)
    
# a='Message: session not created: This version of ChromeDriver only supports Chrome version 93 Current browser version is 98.0.4758.82 with binary path C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# import re

# pattern=r'Current browser version is \S*'

# b=''.join(re.findall(pattern,a))
# # print(re.sub(r'\D','',b))
# pattern2=r'[\d*.]'
# c=re.findall(pattern2,b)
# print(''.join(c))

# from selenium import webdriver

# import time

# profile=webdriver.FirefoxProfile()
# profile.set_preference('browser.download.dir',r'D:\Python\Python38-32')

# profile.set_preference('browser.download.folderList',2)
# profile.set_preference('browser.helperApps.alwaysAsk.force',False)
# profile.set_preference('browser.download.manager.showwhenStarting',False)
# profile.set_preference('browser.download.manager.focusWhenStarting',False)
# profile.set_preference('browser.download.manager.alertOnEXEOpen',False)
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/zip,application/octet-stream')
# profile.set_preference('browser.download.manager.showAlertOnComplete',False)

# driver=webdriver.Firefox(firefox_profile=profile)

# driver.get('http://chromedriver.storage.googleapis.com/index.html')
# time.sleep(2)

# driver.find_element_by_xpath("//a[.='70.0.3538.16']").click()
# time.sleep(2)
# driver.find_element_by_xpath("//a[.='chromedriver_win32.zip']").click()


# from browser_actions import Commonweb

# common=Commonweb()

# common.open_browser(download_path=r'D:\Python\Python38-32',browsername='Firefox')

# common.open_web('http://chromedriver.storage.googleapis.com/index.html?path=70.0.3538.16/')

# common.display_click("xpath,//a[.='chromedriver_win32.zip']")


# import zipfile

# zip=zipfile.ZipFile(r'D:\code\chromedriver_win32.zip')

# zip_list = zip.namelist()

# for f in zip_list:
#     zip.extract(f, r'D:\code')

# zip.close()


# import os

# os.remove(r'D:\code\chromedriver.exe')


# print(3)

# print(2)               
# from selenium import webdriver
# import time

# dr=webdriver.Chrome()
# dr.maximize_window()
# dr.get('https://at-client-portal-sit.atfxdev.com/login')
# time.sleep(2)

# dr.find_element_by_css_selector("[placeholder='Please fill in your Email']").send_keys('tyler.tang@test.com')
# dr.find_element_by_css_selector("[placeholder='Please fill in your password']").send_keys('Tl123456')
# dr.find_element_by_css_selector('.login-btn').click()
# time.sleep(5)

# js='document.getElementsByClassName("el-scrollbar__thumb")[1].scrollTop=0'
# dr.execute_script(js)
# time.sleep(5)
# dr.find_element_by_xpath("//span[.='Deposit Withdrawal List']").click()

# from handle_database import Database_operate
# from read_dataconfig import ReadConfig


# dataBase=Database_operate()
# ConFig=ReadConfig()


# dataBase.search_in_mysql(sql, ConFig.get_value('mysql_datawarehouse_two', 'user'), ConFig.get_value('mysql_datawarehouse_two', 'host'), ConFig.get_value('mysql_datawarehouse_two', 'password'))

a=['', '1000005375', '1000005378', '1000005379', '1000005389']

print(list(filter(None, a)))






























    










































































































































































