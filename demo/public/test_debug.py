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

import random
print(random.randint(0, 5))












