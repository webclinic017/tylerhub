'''
Author: your name
Date: 2022-03-29 17:15:17
LastEditTime: 2022-04-07 18:10:34
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
import locale

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
    locale.setlocale(locale.LC_NUMERIC, "us")

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

    
    #查询mysql数据库，找到该IB下所有下级账号
    def search_ib_lower(self,account:int):
        try:
            self.IB_base=dataBase.search_in_mysql('SELECT path FROM client_relationship2_sit.relationship where path like "%{}%"'.format(account), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            self.pattern=r'[10|12]\d{9}'
            
            self.serach_list=[]

            for i in self.IB_base:
                self.serach_list.append(re.findall(self.pattern,''.join(list(i))))

            self.serach_list2=[]

            for y in self.serach_list:
                for x in y:
                    self.serach_list2.append(x)
            #去重
            self.serach_list3=list(set(self.serach_list2))

            #删除主账号
            self.serach_list3.remove('{}'.format(account))

            print('当前IB账号{}存在{}个直属/非直属下级'.format(account,len(self.serach_list3)))
            return self.serach_list3
        except Exception as msg:
            log.my_logger('!!--!!search_ib_lower').error(msg)


    def logincp(self,account:int):
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


    #筛选存在未平仓订单的下级账号
    def filter_lower_openOrder(self):
        try:
            #下级未平仓订单
            common.display_click("xpath,//span[.='下级未平仓订单']")
            time.sleep(0.5)
            common.display_click('css,.el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(0.5)
            common.display_click('css,.el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']")
            time.sleep(2)
            #所有下级出入金记录条数
            self.lenForOpenOrder=common.get_lenofelement('css,tbody > tr > .el-table_1_column_2 .account-txt')
            print('当前账号存在{}条下级出入金记录'.format(self.lenForOpenOrder))
            #遍历IB下级列表，找出存在未平仓记录的账号
            self.lower_list=[]
            print('筛选下级出入金账号中，loading......')

            for y in range(0,self.lenForOpenOrder):
                if common.display_get_text('css,tbody > tr > .el-table_1_column_2 .account-txt',y) in self.serach_list3:
                    self.lower_list.append(common.display_get_text('css,tbody > tr > .el-table_1_column_2 .account-txt',y))
            
            if len(self.lower_list)==0:
                return False
            else:
                #去重下级出入金账号列表
                self.deduplication_lower_list=list(set(self.lower_list))
                print('存在未平仓的下级账号：{}'.format(self.deduplication_lower_list))
                #查询某个下级会员账号的未平仓记录
                common.display_click('css,.el-select .el-select__caret')
                time.sleep(0.5)
                common.display_click("xpath,//span[.='会员账号']",-1)
                time.sleep(0.5)
                common.web_clear("css,[placeholder='搜索']")
                time.sleep(0.5)
                self.randomIndex=random.randint(0, len(self.deduplication_lower_list)-1)
                common.display_input("css,[placeholder='搜索']", int(self.deduplication_lower_list[self.randomIndex]))
                time.sleep(0.5)
                common.display_click('css,.el-icon-search')
                time.sleep(2)
                self.tradeAccount_list=[]
                self.tradelen=common.get_lenofelement("xpath,//tbody[1]//a[.='{}']".format(self.deduplication_lower_list[self.randomIndex]))
                for i in range(0,self.tradelen):
                    self.tradeAccount_list.append(common.display_get_text('css,tbody > tr > .el-table_1_column_3 .account-txt',i))
                #去重交易列表账号
                self.tradeAccount_list2=list(set(self.tradeAccount_list))
    
                common.display_click('css,.el-select .el-select__caret')
                time.sleep(0.5)
                common.display_click("xpath,//span[.='交易账号']",-1)
                time.sleep(0.5)
                print('查询下级会员账号{}名下交易账号{}未平仓订单数据'.format(self.deduplication_lower_list[self.randomIndex],self.tradeAccount_list2))
                return True
        except Exception as msg:
            log.my_logger('!!--!!lower_openOrder_list').error(msg)

    
    #格式化时间
    def fromat_datetime(self):
        #随机选择时间random.randint(1, 6)
        self.index=4
        #今天
        self.nowTime=datetime.datetime.now()
        #本月第一天
        self.monStart=datetime.datetime(self.nowTime.year, self.nowTime.month, 1)
        #上个月最后一天
        self.lastmonEnd=self.monStart-datetime.timedelta(days=1)
        time.sleep(1)
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


    #查询下级交易账号某个时间段内的未平仓订单        
    def search_period_openOrder(self,tradeAccount):
        try:
            #查询某个下级会员账号的未平仓记录

            self.fromat_datetime()
            #查询数据库
            self.mysql_openOrder=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="{}" and Close_Time="1970-01-01 00:00:00" and'
            ' Open_Time between "{} 00:00:00" and "{} 23:59:59" order by Open_Time desc'.
            format(tradeAccount,self.dateStart,self.dateEnd), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            print('数据库查询返回{}条数据'.format(len(self.mysql_openOrder)))

            #筛选时间
            common.display_click('css,.el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            time.sleep(1)
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']", tradeAccount)
            time.sleep(0.5)
            common.display_click('css,.el-icon-search')
            time.sleep(1)
            #按订单号码降序排序
            common.display_click('css,th .descending')
            time.sleep(1)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('当前交易账号{} 在{}至{} 时间段内不存在未平仓订单'.format(tradeAccount,self.dateStart,self.dateEnd))
                self.open_order_len=0
                return False
            else:
                self.open_orderList=[]
                self.open_order_len=common.get_lenofelement("xpath,//tbody[1]//a[.='{}']".format(tradeAccount))
                print('当前交易账号{} 在{} 00:00:00 至{} 23:59:59 时间段内存在{}条未平仓订单'.format(tradeAccount,self.dateStart,self.dateEnd,self.open_order_len))
                #处理页面数据
                print('处理页面数据中........')
                for i in range(0,self.open_order_len):
                    self.open_orderDict={}
                    self.open_orderDict['Ticket']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.open_orderDict['Login']=int(common.get_text('css,tbody > tr > .el-table_1_column_3 .account-txt',i)) #交易账号
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_8 div span',i)
                    self.open_orderDict['Open_Time']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M:%S') #开仓时间
                    self.open_orderDict['Volume']=float(common.get_text('css,tbody > tr > .el-table_1_column_10 div span',i)) #交易量
                    self.open_orderDict['Symbol']=common.get_text('css,tbody > tr > .el-table_1_column_11 div span',i) #商品代码
                    self.open_orderDict['Open_Price']=float(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i)) #开仓价
                    self.open_orderDict['Commission']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_15 div span',i)) #佣金
                    self.open_orderDict['Swaps']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_16 div span',i)) #隔夜利息
                    self.open_orderDict['Profit']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_17 div span',i)) #盈亏
                    self.open_orderList.append(self.open_orderDict)

                #计算页面总盈亏，总交易量，总隔夜利息，总佣金
                self.total_Volume=0
                self.total_Commission=0
                self.total_Swaps=0
                self.total_Profit=0
                for i in range(0,self.open_order_len):
                    self.total_Volume += float(common.get_text('css,tbody > tr > .el-table_1_column_10 div span',i))
                    self.total_Commission += locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_15 div span',i))
                    self.total_Swaps += locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_16 div span',i))
                    self.total_Profit += locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_17 div span',i))

                #计算数据库总盈亏，总交易量，总隔夜利息，总佣金
                self.dataBase_total_Volume=0
                self.dataBase_total_Commission=0
                self.dataBase_total_Swaps=0
                self.dataBase_total_Profit=0
                for y in self.mysql_openOrder:
                    self.dataBase_total_Volume += y[5]/100
                    self.dataBase_total_Commission += y[11]
                    self.dataBase_total_Swaps += y[13]
                    self.dataBase_total_Profit += y[15]

                print(self.total_Volume,self.total_Commission,self.total_Swaps,self.total_Profit)
                print(self.dataBase_total_Volume,self.dataBase_total_Commission,self.dataBase_total_Swaps,self.dataBase_total_Profit)
                return True
        except Exception as msg:
            log.my_logger('!!--!!search_period_openOrder').error(msg)


#隔夜利息保留2位小数处理，断言具体数据






































