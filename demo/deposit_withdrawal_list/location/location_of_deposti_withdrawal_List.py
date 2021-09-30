'''
Author: tyler
Date: 2021-09-17 15:00:40
LastEditTime: 2021-09-30 17:27:51
LastEditors: Please set LastEditors
Description: Page operation
FilePath: \tylerhub\demo\walaopay_withdrawal\location\location_of_walaopay_withdrawal.py
'''
import os
import sys
import time
import random
import datetime
from dateutil import parser

path_demo=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_public=os.path.join(path_demo,'public')
sys.path.append(path_public)
path_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from browser_actions import Commonweb
from common_method import Commonmethod
from handle_database import Dadabase_operate
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
    dataBase=Dadabase_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver
    def broswertype(self,broswername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(broswername)
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

    def logincp(self,account):
        #登录账号
        common.display_input('css,[placeholder]', account)
        time.sleep(0.5)
        #登录
        common.display_click('css,.ivu-btn > span',-1)
        time.sleep(3)
        #出入金记录页面
        common.switch_windows(1)
        time.sleep(1)
        common.display_click("xpath,//span[.='出入金记录']")


    #筛选时间查询
    def serch_list(self,account):
        try:
            #每页条数
            common.display_click('css,.el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//div[@class='formAndList']//span[.='全部']",-1)
            time.sleep(1)
            common.display_click('css,.el-select .el-select__caret',1)
            #随机选择时间random.randint(1, 6)
            self.index=random.randint(1, 6)
            #今天
            self.nowTime=datetime.datetime.now()
            #本月第一天
            self.monStart=datetime.datetime(self.nowTime.year, self.nowTime.month, 1)
            #上个月最后一天
            self.lastmonEnd=self.monStart-datetime.timedelta(days=1)
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            time.sleep(2)
            if self.index==1:
                #今天
                self.dateStart=self.nowTime.strftime('%Y-%m-%d')
                self.dateEnd=self.nowTime.strftime('%Y-%m-%d')
            elif self.index==2:
                #最近三天
                self.dateStart=(self.nowTime-datetime.timedelta(days=2)).strftime('%Y-%m-%d')
                self.dateEnd=self.nowTime.strftime('%Y-%m-%d')
            elif self.index==3:
                #本周
                self.dateStart=(self.nowTime - datetime.timedelta(days=self.nowTime.weekday()+1)).strftime('%Y-%m-%d')
                self.dateEnd=self.nowTime.strftime('%Y-%m-%d')
            elif self.index==4:
                #上周
                self.dateStart=(self.nowTime - datetime.timedelta(days=self.nowTime.weekday()+8)).strftime('%Y-%m-%d')
                self.dateEnd=(self.nowTime - datetime.timedelta(days=self.nowTime.weekday()+2)).strftime('%Y-%m-%d')
            elif self.index==5:
                #本月
                self.dateStart=self.monStart.strftime('%Y-%m-%d')
                self.dateEnd=self.nowTime.strftime('%Y-%m-%d')
            else:
                #上月
                self.dateStart=(datetime.datetime(self.lastmonEnd.year, self.lastmonEnd.month, 1)).strftime('%Y-%m-%d')
                self.dateEnd=self.lastmonEnd.strftime('%Y-%m-%d')
            #获取当前时间段内出入金条数
            if common.ele_is_displayed('css,.el-table__empty-text', 2):
                self.list_len=0
                print('当前时间段 {} 至 {} 出入金记录为{}条'.format(self.dateStart,self.dateEnd,self.list_len))
            else:
                self.list_len=common.get_lenofelement('css,tbody > tr')
                #查询数据库,默认查询状态为成功的订单
                self.dateGte=parser.parse('{}T00:00:00Z'.format(self.dateStart))
                self.dateLte=parser.parse('{}T23:59:59Z'.format(self.dateEnd))
                #出金记录
                if common.ele_is_displayed("xpath,//tbody//span[.='出金']",2):
                    self.withdrawal_len=common.get_lenofelement("xpath,//tbody//span[.='出金']")
                    #查询数据库
                    print(dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
                    'atfxgm-sit', 'atfx_withdrawal',{"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}}, 
                    {"accountNumber": account},{"currStatus":"S"}]},'createDate_mt',N=0))
                else:
                    print('当前查询时间段不存在出金记录')
                #入金记录
                if common.ele_is_displayed("xpath,//tbody//span[.='入金']",2):
                    self.deposit_len=common.get_lenofelement("xpath,//tbody//span[.='入金']")
                    #查询数据库
                    print(dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
                    'atfxgm-sit', 'atfx_deposit',{"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}}, 
                    {"accountNumber": account},{"currStatus":"S"}]},'createDate_mt',N=0))
                else:
                    print('当前查询时间段不存在入金记录')
                if common.ele_is_displayed("xpath,//tbody//span[.='转账']",2):
                    self.transfer_len=common.get_lenofelement("xpath,//tbody//span[.='入金']")
                    #查询数据库
                    print(dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_fund_transfer',
                    {"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},{"currStatus":"S"},
                    {"$or":[{"fromAccountNumber":account},{"toAccountNumber":account}]}]},'createDate_mt',N=0))
                else:
                    print('当前查询时间段不存在转账记录')
                print('当前时间段 {} 至 {} 出入金记录为{}条：出金{}条，入金{}条，转账{}条'.format(
                    self.dateStart,self.dateEnd,self.list_len,self.withdrawal_len,self.deposit_len,self.transfer_len))

        except Exception as msg:
            log.my_logger('!!--!!serch_list').error(msg)          


    