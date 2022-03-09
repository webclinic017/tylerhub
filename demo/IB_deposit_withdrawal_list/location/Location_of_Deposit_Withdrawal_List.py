'''
Author: your name
Date: 2022-02-21 17:22:03
LastEditTime: 2022-03-09 16:04:27
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_deposit_withdrawal_list\location\Location_of_Deposit_Withdrawal_List.py
'''
'''
Author: your name
Date: 2022-02-21 17:22:37
LastEditTime: 2022-02-21 17:40:55
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\IB_deposit_withdrawal_list\actions\Test_IB_Deposit_Withdrawal.py
'''
import os
import sys
import time
import random
import datetime
from dateutil import parser
import re

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Database_operate
from handlelog import MyLog
from randomdata import Random_data
from read_dataconfig import ReadConfig
from about_data import Aboutdata


class Location_of_deposit_withdrawal(object):
    """
    页面定位等操作
    """

    global common,dataBase,log,randomData,conFig,dealData

    common=Commonweb()
    dataBase=Database_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver
    def broswertype(self,browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(browsername)
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


    #查询mysql数据库，找到该IB下所有下级账号
    def search_ib_lower(self,account):
        try:
            self.IB_base=dataBase.search_in_mysql('SELECT path FROM client_relationship2_sit.relationship where path like "%{}%"'.format(account), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            self.pattern=r'(1000005349/[10|12]\d*)'
            self.pattern2=r'[10|12]\d*$'
            serach_list=[]

            for i in self.IB_base:
                serach_list.append(''.join(re.findall(self.pattern2,''.join(re.findall(self.pattern,''.join(list(i)))))))

            print(serach_list)
            #去除空字符
            serach_list2=list(filter(None,serach_list))
            #去重
            serach_list3=set(serach_list2)
            print(len(serach_list3))
        except Exception as msg:
            log.my_logger('!!--!!get_url').error(msg)
 

    def logincp(self,account):
        #登录账号
        common.switch_windows(0)
        common.web_clear('css,[placeholder]')
        time.sleep(1)
        common.display_input('css,[placeholder]', account)
        time.sleep(0.5)
        #登录
        common.display_click('css,.ivu-btn > span',-1)
        time.sleep(2)
        #出入金记录页面
        common.switch_windows(1)
        #判断页面是否加载完成
        while True:
            if common.ele_is_displayed("css,[src='/static/img/loading.webm']", 1):
                continue
            else:
                break
        time.sleep(1)
        while True:
            self.loading_attributes=common.get_attributes('css,.el-loading-mask', 'style')
            if 'none' in self.loading_attributes:
                break
            else:
                continue
        time.sleep(1)
        common.display_click('css,ul .el-submenu__icon-arrow',1)
        time.sleep(0.5)
        common.display_click('css,ul .el-submenu__icon-arrow',2)
        time.sleep(0.5)
        common.display_click('css,ul .el-submenu__icon-arrow',3)
        time.sleep(0.5)
        common.display_click("xpath,//span[.='下级出入金记录']")
        time.sleep(2)
        #每页条数-全部
        common.display_click('css,.el-select .el-select__caret',-1)
        time.sleep(0.5)
        common.display_click("xpath,//div[@class='formAndList']//span[.='全部']",-1)
        time.sleep(2)









