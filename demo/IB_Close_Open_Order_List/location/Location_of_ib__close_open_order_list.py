'''
Author: your name
Date: 2022-03-29 17:15:17
LastEditTime: 2022-03-29 17:21:09
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_Close_Open_Order_List\location\Location_of_ib__close_open_order_list.py
'''
import os
import sys
import time
import random
import datetime
import re
import pyperclip

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Database_operate
from handlelog import MyLog
from read_dataconfig import ReadConfig
from about_data import Aboutdata


class Location_of_IB_CloseOpen_OrderList(object):

    global common,dataBase,log,conFig,dealData

    common=Commonweb()
    dataBase=Database_operate()
    log=MyLog()
    conFig=ReadConfig()
    dealData=Aboutdata()


    #赋值对象driver,设置下载文件路径
    def broswertype(self,download_path=os.path.join(path_project,'test_data'),browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(download_path=download_path,browsername=browsername)
        self.commeThod=Commonmethod(self.driver)

    #登录页
    def get_url(self,environment,username,password,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            #选择bos页面语言,默认简中
            time.sleep(1)
            self.commeThod.choose_bos_lang(lang)
            #登录bos
            self.commeThod.loginbos(username, password)
            time.sleep(1)
            common.display_click('css,[width="200"] li .ivu-icon-ios-arrow-down')
            time.sleep(0.5)
            common.display_click("xpath,//span[.='登录会员中心']")
            time.sleep(1)
            #选择登录会员中心页面语言
            common.display_click('css,.ivu-form div i',-1)
            time.sleep(0.5)
            
            common.display_click("xpath,//li[.='简体中文']",-1)
            time.sleep(0.5)
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)