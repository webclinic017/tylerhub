'''
Author: tyler
Date: 2022-04-28 16:17:30
LastEditTime: 2022-06-09 15:53:42
LastEditors: Tyler Tang tyler.tang@6317.io
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \tylerhub\demo\Position_Summary\Location\Location_of_position_summary.py
'''
import os
import sys
import time
import random
import datetime
import re
import pyperclip
import locale
from dateutil import parser

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


class Location_position_summary(object):

    global common,dataBase,log,conFig,dealData
    locale.setlocale(locale.LC_NUMERIC, "us")

    common=Commonweb()
    dataBase=Database_operate()
    log=MyLog()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver,设置下载文件路径
    def broswertype(self,download_path=os.path.join(path_project,'test_data'),browsername=conFig.get_value('browser', 'default')):
        self.driver=common.open_browser(download_path=download_path,browsername=browsername)
        self.comMethod=Commonmethod()

    
    #登录页
    def get_url(self,environment,username,password,lang='CN'):
        try:
            common.open_web(conFig.get_value('bos_login', '{}'.format(environment)))
            #选择bos页面语言,默认简中
            time.sleep(1)
            self.comMethod.choose_bos_lang(common,lang)
            #登录bos
            self.comMethod.loginbos(common,username, password)
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


    def logincp(self,account:int):
        if str(account)[0:2]=='10':
            #登录账号
            common.switch_windows(0)
            common.web_clear('css,[placeholder]')
            time.sleep(1)
            common.display_input('css,[placeholder]', account)
            time.sleep(0.5)
            #登录
            common.display_click('css,.ivu-btn > span',-1)
            time.sleep(3)
            #下级未平仓记录页面
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
            time.sleep(1)
            common.display_click("xpath,//span[.='仓位总结']")
            time.sleep(2)
            #格式化查询时间
            self.format_time()
            #筛选时间
            common.display_click('css,.el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            time.sleep(0.5)
            #每页条数
            common.display_click('css,.el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li",-1)
            return False
        else:
            return True


    #筛选时间查询
    def format_time(self):
        try:
            #随机选择时间random.randint(0, 6)
            self.index=random.randint(0, 6)
            #今天
            self.nowTime=datetime.datetime.now()
            #本月第一天
            self.monStart=datetime.datetime(self.nowTime.year, self.nowTime.month, 1)
            #上个月最后一天
            self.lastmonEnd=self.monStart-datetime.timedelta(days=1)
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
            elif self.index==6:
                #上月
                self.dateStart=(datetime.datetime(self.lastmonEnd.year, self.lastmonEnd.month, 1)).strftime('%Y-%m-%d')
                self.dateEnd=self.lastmonEnd.strftime('%Y-%m-%d')
            else:
                #全部
                self.dateStart='1990-01-01'
                self.dateEnd='2055-12-31'              
            
            #转换mongodb数据库查询时间格式
            self.dateGte=parser.parse('{}T00:00:00Z'.format(self.dateStart))
            self.dateLte=parser.parse('{}T23:59:59Z'.format(self.dateEnd))
        except Exception as msg:
            log.my_logger('!!--!!format_time').error(msg)


    def search_mongodb_deposit(self,tradeaccount:int):
        try:
            #查询数据库
            #入金表
            self.mongodbDeposit=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            'atfxgm-sit', 'atfx_deposit',{"$and": [{"createDate": {"$gte": self.dateGte,"$lte": self.dateLte}},
            {'currStatus':'S'},{"tradeAccount": "{}".format(tradeaccount)}]},'mtRefNo','mt4Amt',N=0)

            self.totalDeposit=0
            for i in self.mongodbDeposit:
                self.totalDeposit+=i['mt4Amt']
            
            # #资金调整表
            # self.mongodbDeposit_Adj=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            # 'atfxgm-sit', 'atfx_fund_adjust',{"$and": [{"createDate": {"$gte": self.dateGte,"$lte": self.dateLte}},
            # {'status':1},{"tradeAccount": tradeaccount},{"remark":re.compile('Deposit')}]},'mtOrderNo','amount',N=0)            


            # self.totalDeposit_Adj=0
            # for i in self.mongodbDeposit_Adj:
            #     self.totalDeposit_Adj+=i['amount']

            print('账号{}数据库总入金：{}'.format(tradeaccount,'%.2f'%(self.totalDeposit)))

            return self.totalDeposit
        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_deposit').error(msg)


    def search_mongodb_withdrawal(self,tradeaccount:int):
        try:
            #出金表
            self.mongodbWithdrawal=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            'atfxgm-sit', 'atfx_withdrawal',{"$and": [{"createDate": {"$gte": self.dateGte,"$lte": self.dateLte}},
            {'currStatus':'S'},{"tradeAccount": "{}".format(tradeaccount)}]},'mtRefNo','mtAmt',N=0)
            
            self.totalWithdrawal=0
            for i in self.mongodbWithdrawal:
                self.totalWithdrawal+=i['mtAmt']

             #资金调整表
            self.mongodbWithdrawal_Adj=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            'atfxgm-sit', 'atfx_fund_adjust',{"$and": [{"createDate": {"$gte": self.dateGte,"$lte": self.dateLte}},
            {'status':1},{"tradeAccount": tradeaccount},{"remark":re.compile('Withdrawal')}]},'mtOrderNo','amount',N=0)

            self.totalWithdrawal_Adj=0
            for i in self.mongodbWithdrawal_Adj:
                self.totalWithdrawal_Adj+=i['amount']


            print('账号{}数据库总出金：{}'.format(tradeaccount,'%.2f'%(-self.totalWithdrawal)))
            return self.totalWithdrawal
        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_withdrawal').error(msg)


    def search_mongodb_transfer(self,tradeaccount:int):
        try:
            self.mongodbTransfer=dataBase.search_in_mongodb(conFig.get_value('mongodb', 'uri'),
            'atfxgm-sit', 'atfx_fund_transfer',{"$and": [{"createDate": {"$gte": self.dateGte,"$lte": self.dateLte}},
            {'currStatus':'S'},{"toTradeAccount": "{}".format(tradeaccount)}]},'toMtRefNo','toMtAmt',N=0)
            
            self.totalTransfer=0
            for i in self.mongodbTransfer:
                self.totalTransfer+=i['toMtAmt']

            print('账号{}数据库总转账：{}'.format(tradeaccount,'%.2f'%self.totalTransfer))
            return self.totalTransfer
        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_transfer').error(msg)
   
    
    def search_mysql_order(self,tradeaccount:int):
        try:
            self.mysqlOrder=dataBase.search_mysql_dict('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="{}" and '
            ' Open_Time between "{} 00:00:00" and "{} 23:59:59"'.
            format(tradeaccount,self.dateStart,self.dateEnd), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')


            self.mysqlVolume=0 #交易量
            self.mysqlCommission=0 #佣金
            self.mysqlSwaps=0 #隔夜利息
            self.mysqlProfit=0 #盈亏
            #统计数据库数据
            for i in self.mysqlOrder:
                self.mysqlVolume+=i['Volume']/100
                self.mysqlCommission+=i['Commission']
                self.mysqlSwaps+=i['Swaps']
                self.mysqlProfit+=i['Profit']

            print('账号{}数据库总交易量：{}；总佣金：{}；总隔夜利息：{}；总盈亏：{}'.
            format(tradeaccount,self.mysqlVolume,self.mysqlCommission,self.mysqlSwaps,self.mysqlProfit))

        except Exception as msg:
            log.my_logger('!!--!!search_mongodb_transfer').error(msg)


    def count_pageData(self):
        try:                                                                                                                                                                    
            #获取页面总入金，净入金
            self.pattren=r'[^A-Z]'

            #统计总入金
            self.totalPage_deposit=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',1))).replace(',',''))
            #统计总出金
            self.totalPage_withdrawal=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',3))).replace(',',''))
            #统计净入金
            self.netPage_deposit=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',5))).replace(',',''))
            #统计资金转入
            self.totalPage_transfer=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',7))).replace(',',''))
            #统计交易量
            self.totalPage_volume=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',9))).replace(',',''))
            #统计总隔夜利息
            self.totalPage_swaps=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',11))).replace(',',''))
            #统计总盈亏
            self.totalPage_profit=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',13))).replace(',',''))
            #统计总佣金
            self.totalPage_commission=float(''.join(re.findall(self.pattren,common.display_get_text('css,.summary-cell > div > p',17))).replace(',',''))
            
        except Exception as msg:
            log.my_logger('!!--!!count_pageData').error(msg)


    def serch_basetraccount(self,tradeaccount):
        try:
            #根据交易账号筛选时间查询页面数据
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']", tradeaccount)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            #统计页面数据
            self.count_pageData()
            #查询数据库
            #查询入金
            self.search_mongodb_deposit(tradeaccount)
            #查询出金
            self.search_mongodb_withdrawal(tradeaccount)
            #查询转账
            self.search_mongodb_transfer(tradeaccount)
            #查询交易
            self.search_mysql_order(tradeaccount)
        except Exception as msg:
            log.my_logger('!!--!!serch_basetraccount').error(msg)


    #查询挡墙时间段下所有交易账号仓位总结数据
    def search_allTradeaccount(self):
        try:
            common.general_refresh_()
            time.sleep(2)
            #时间
            common.display_click('css,.el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            time.sleep(0.5)
            #每页条数
            common.display_click('css,.el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li",-1)
            time.sleep(2)
            self.tradeaccountLen=common.get_lenofelement('css,tbody > tr > .el-table_1_column_1 .account-txt')
            self.tdaccountList=[]

            for i in range(0,self.tradeaccountLen):
                self.tdaccountList.append(common.display_get_text('css,tbody > tr > .el-table_1_column_1 .account-txt',i))
            
            #去除空字符
            self.tdaccountList2=[y for y in self.tdaccountList if y!='']
            #while '' in self.tdaccountList:
                # self.tdaccountList.remove('')
            
            print('需要查询的交易账号：{}'.format(self.tdaccountList2))

            #统计页面数据
            self.count_pageData()

            #查询数据库
            self.allDeposit=0
            self.allWithdrawal=0
            self.allTrransfer=0
            self.allVolume=0
            self.allCommission=0
            self.allSwaps=0
            self.allProfit=0
            for i in self.tdaccountList2:
                self.allDeposit+=self.search_mongodb_deposit(int(i)) #所有交易账号数据库总入金
                self.allWithdrawal+=self.search_mongodb_withdrawal(int(i))#所有交易账号数据库总出金
                self.allTrransfer+=self.search_mongodb_transfer(int(i)) #所有交易账号数据库总转账
                #统计所有交易账号总交易数据
                self.search_mysql_order(int(i))
                self.allVolume+=self.mysqlVolume
                self.allCommission+=self.mysqlCommission
                self.allSwaps+=self.mysqlSwaps
                self.allProfit+=self.mysqlProfit

            print(self.allDeposit,self.allWithdrawal,self.allTrransfer,self.allVolume,self.allProfit)
        except Exception as msg:
            log.my_logger('!!--!!search_allTradeaccount').error(msg)


    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()
