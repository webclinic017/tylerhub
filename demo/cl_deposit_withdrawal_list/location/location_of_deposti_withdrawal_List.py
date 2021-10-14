'''
Author: tyler
Date: 2021-09-17 15:00:40
LastEditTime: 2021-10-13 19:15:15
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
        common.switch_windows(0)
        common.web_clear('css,[placeholder]')
        time.sleep(1)
        common.display_input('css,[placeholder]', account)
        time.sleep(0.5)
        #登录
        common.display_click('css,.ivu-btn > span',-1)
        time.sleep(3)
        #出入金记录页面
        common.switch_windows(1)
        time.sleep(1)
        common.display_click("xpath,//span[.='出入金记录']")
        time.sleep(2)
        #每页条数-全部
        common.display_click('css,.el-select .el-select__caret',-1)
        time.sleep(0.5)
        common.display_click("xpath,//div[@class='formAndList']//span[.='全部']",-1)
        time.sleep(2)


    #筛选时间查询
    def serch_list(self,account):
        try:
            time.sleep(1)
            common.display_click('css,.el-select .el-select__caret',1)
            time.sleep(1)
            #随机选择时间random.randint(1, 6)
            self.index=random.randint(1, 6)
            #今天
            self.nowTime=datetime.datetime.now()
            #本月第一天
            self.monStart=datetime.datetime(self.nowTime.year, self.nowTime.month, 1)
            #上个月最后一天
            self.lastmonEnd=self.monStart-datetime.timedelta(days=1)
            time.sleep(1)
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            time.sleep(3)
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
            #转换mongodb数据库查询时间格式
            self.dateGte=parser.parse('{}T00:00:00Z'.format(self.dateStart))
            self.dateLte=parser.parse('{}T23:59:59Z'.format(self.dateEnd))
        
            #判断当前时间段内页面出入金记录是否为空
            if common.ele_is_displayed('css,.el-table__empty-text', 2):
                self.list_len=0
                print('当前时间段 {} 至 {} 出入金记录为{}条'.format(self.dateStart,self.dateEnd,self.list_len))
                #出金表
                self.mongodbWithdrawal=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
                'atfxgm-sit', 'atfx_withdrawal',{"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},
                {"$or":[{"currStatus":'S'},{"currStatus":'U'}]},{"accountNumber": account}]},N=0)
                #入金表
                self.mongodbDeposit=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
                'atfxgm-sit', 'atfx_deposit',{"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},
                {"$or":[{"currStatus":'S'},{"currStatus":'U'}]},{"accountNumber": account}]},N=0)
                #转账表
                self.mongodbTransfer=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_fund_transfer',
                {"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},{"$or":[{"currStatus":'S'},{"currStatus":'U'}]},
                {"$or":[{"fromAccountNumber":account},{"toAccountNumber":account}]}]},N=0)
                return False
            else:
                self.list_len=common.get_lenofelement('css,tbody > tr')
                return True
        except Exception as msg:
            log.my_logger('!!--!!serch_list').error(msg)

    
    #时间段，交易金额，汇率，MT金额，时间，类型，管道，状态和Mongo数据进行核对。
    def search_withdrawal(self,account):
        #查询数据库,默认查询状态为成功的订单
        #出金记录
        if common.ele_is_displayed("xpath,//tbody//span[.='出金']",2):
            self.withdrawal_len=common.get_lenofelement("xpath,//tbody//span[.='出金']")
            print('页面出金记录{}条'.format(self.withdrawal_len))
            #查询数据库
            self.mongodbWithdrawal=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_withdrawal',
            {"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},{"$or":[{"currStatus":'S'},{"currStatus":'U'}]},{"accountNumber": account}]},
            'createDate_mt','settleAmt','realRate','mtAmt','currStatus','channel',N=0)


            #处理页面数据
            self.withdrawal_list=[]
            for i in range(0,self.list_len):
                if common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i)=='出金':
                    self.withdrawal_dict={}

                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i)

                    self.withdrawal_dict['createDate_mt']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M')
                    self.withdrawal_dict['settleAmt']=float(randomData.extract_numbers
                    (common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)))/100
                    self.withdrawal_dict['realRate']=float(common.get_text('css,tbody > tr > .el-table_1_column_4 div span',i))
                    self.withdrawal_dict['mtAmt']=float(randomData.extract_numbers
                    (common.get_text('css,tbody > tr > .el-table_1_column_5 div span',i)))/100
                    self.withdrawal_dict['currStatus']=common.get_text('css,tbody > tr > .el-table_1_column_9 div span:nth-of-type(2)',i)
                    self.withdrawal_list.append(self.withdrawal_dict)
                else:
                    pass
            return True
        else:
            self.withdrawal_len=0
            print('页面出金记录{}条'.format(self.withdrawal_len))
            #查询数据库
            self.mongodbWithdrawal=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            'atfxgm-sit', 'atfx_withdrawal',{"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},
            {"$or":[{"currStatus":'S'},{"currStatus":'U'}]},{"accountNumber": account}]},N=0)
            return False
    
    def search_deposit(self,account):
        #入金记录
        if common.ele_is_displayed("xpath,//tbody//span[.='入金']",2):
            self.deposit_len=common.get_lenofelement("xpath,//tbody//span[.='入金']")
            print('页面入金记录{}条'.format(self.deposit_len))
            #查询数据库
            self.mongodbDeposit=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_deposit',
            {"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},{"$or":[{"currStatus":'S'},{"currStatus":'U'}]},{"accountNumber": account}]},
            'createDate_mt','fromAmt','rate','mt4Amt','currStatus','channel',N=0)

            #处理页面数据
            self.deposti_list=[]
            for i in range(0,self.list_len):
                if common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i)=='入金':
                    self.deposit_dict={}
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i)
                    self.deposit_dict['createDate_mt']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M')
                    self.deposit_dict['fromAmt']=int(randomData.extract_numbers
                    (common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)))/100
                    self.deposit_dict['rate']=float(common.get_text('css,tbody > tr > .el-table_1_column_4 div span',i))
                    self.deposit_dict['mt4Amt']=float(randomData.extract_numbers
                    (common.get_text('css,tbody > tr > .el-table_1_column_5 div span',i)))/100
                    self.deposit_dict['currStatus']=common.get_text('css,tbody > tr > .el-table_1_column_9 div span:nth-of-type(2)',i)
                    self.deposti_list.append(self.deposit_dict)  
                else:
                    pass
            return True
        else:
            #查询数据库
            self.deposit_len=0
            print('页面入金记录{}条'.format(self.deposit_len))
            self.mongodbDeposit=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            'atfxgm-sit', 'atfx_deposit',{"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},
            {"$or":[{"currStatus":'S'},{"currStatus":'U'}]},{"accountNumber": account}]},N=0)
            return False

    
    def search_transfer(self,account):
        #转账记录
        if common.ele_is_displayed("xpath,//tbody//span[.='转账']",2):
            self.transfer_len=common.get_lenofelement("xpath,//tbody//span[.='转账']")
            print('页面转账记录{}条'.format(self.transfer_len))
            #查询数据库
            self.mongodbTransfer=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_fund_transfer',
            {"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},{"$or":[{"currStatus":'S'},{"currStatus":'U'}]},
            {"$or":[{"fromAccountNumber":account},{"toAccountNumber":account}]}]},'createDate_mt','toMtAmt','currStatus',N=0)

            #处理页面数据
            self.transfer_list=[]
            for i in range(0,self.list_len):
                if common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i)=='转账':
                    self.transfer_dict={}
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i)
                    self.transfer_dict['createDate_mt']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M')
                    self.transfer_dict['toMtAmt']=float(randomData.extract_numbers
                    (common.get_text('css,tbody > tr > .el-table_1_column_5 div span',i)))/100
                    self.transfer_dict['currStatus']=common.get_text('css,tbody > tr > .el-table_1_column_9 div span:nth-of-type(2)',i)
                    self.transfer_list.append(self.transfer_dict)
                else:
                    pass
            print('当前时间段 {} 至 {} 出入金记录为{}条：出金{}条，入金{}条，转账{}条'.format(
            self.dateStart,self.dateEnd,self.list_len,self.withdrawal_len,self.deposit_len,self.transfer_len))
            return True
        else:
            self.transfer_len=0
            print('页面转账记录{}条'.format(self.transfer_len))
            #查询数据库
            self.mongodbTransfer=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),'atfxgm-sit', 'atfx_fund_transfer',
            {"$and": [{"createDate_mt": {"$gte": self.dateGte,"$lte": self.dateLte}},{"$or":[{"currStatus":'S'},{"currStatus":'U'}]},
            {"$or":[{"fromAccountNumber":account},{"toAccountNumber":account}]}]},N=0)
            print('当前时间段 {} 至 {} 出入金记录为{}条：出金{}条，入金{}条，转账{}条'.format(
            self.dateStart,self.dateEnd,self.list_len,self.withdrawal_len,self.deposit_len,self.transfer_len))
            return False   


    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()