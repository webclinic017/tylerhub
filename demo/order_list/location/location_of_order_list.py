'''
Author: tyler
Date: 2021-10-20 10:29:51
LastEditTime: 2021-11-18 18:28:17
LastEditors: Please set LastEditors
Description: Page operation
FilePath: \tylerhub\demo\order_list\location\location_of_order_list.py
'''
import os
import sys
import time
import random
import datetime
from dateutil import parser
import locale
import os
import re
import pyperclip

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

class Location_of_order_list(object):
    """
    已平仓未平仓订单页面定位操作
    """

    global common,dataBase,log,randomData,conFig,dealData
    locale.setlocale(locale.LC_NUMERIC, "us")
    common=Commonweb()
    dataBase=Dadabase_operate()
    log=MyLog()
    randomData=Random_data()
    conFig=ReadConfig()
    dealData=Aboutdata()

    #赋值对象driver
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

    
    #查询交易账号所有已平仓未平仓订单
    def search_order_len(self,trandaccount):
        try:
            common.switch_windows(1)
            time.sleep(3)
            common.display_click("xpath,//span[.='未平仓订单']")
            time.sleep(1)
            common.general_refresh_()
            time.sleep(2)
            #筛选每页显示为全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(1)
            #根据交易账号来搜索全部未平仓订单
            common.web_clear('css,[placeholder="搜索"]')
            time.sleep(0.5)
            common.display_input('css,[placeholder="搜索"]', trandaccount)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            #按订单号码排序
            common.display_click('css,th .ascending')
            time.sleep(2)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('当前交易账号{}不存在未平仓订单'.format(trandaccount))
                self.open_order_len=0
            else:
                #统计该交易账号的未平仓订单
                self.open_order_len=common.get_lenofelement("xpath,//tr//span[.='{}']".format(trandaccount))
                time.sleep(0.5)
                print('交易账号 {} 未平仓订单共有{}条'.format(trandaccount,self.open_order_len))
                #处理页面数据
                print('处理页面数据中.......')
                self.open_orderList=[]
                for i in range(0,self.open_order_len):
                    self.open_orderDict={}
                    self.open_orderDict['订单号码']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.open_orderDict['交易账户']=int(common.get_text('css,tbody > tr > .el-table_1_column_2 div span',i))
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i) 
                    self.open_orderDict['开仓时间']=(datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M:%S')).strftime('%Y-%m-%d %H:%M:%S') #开仓时间
                    self.open_orderDict['类型']=common.get_text('css,tbody > tr > .el-table_1_column_4 div',i)#类型
                    self.open_orderDict['交易量']=float(common.get_text('css,tbody > tr > .el-table_1_column_5 div span',i))
                    self.open_orderDict['商品代码']=common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i) #商品代码
                    self.open_orderDict['开仓价']=float(common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i)) #开仓价
                    self.open_orderDict['S/L']=float(common.get_text('css,tbody > tr > .el-table_1_column_8 div span',i))
                    self.open_orderDict['T/P']=float(common.get_text('css,tbody > tr > .el-table_1_column_9 div span',i))
                    self.open_orderDict['佣金']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_10 div span',i)) #佣金
                    self.open_orderDict['隔夜利息']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_11 div span',i)) #隔夜利息
                    self.open_orderDict['盈亏']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i)) #盈亏 
                    self.open_orderList.append(self.open_orderDict)
                     
            #核对导出数据是否与页面一致
            common.display_click('css,.la-share-square') #导出
            time.sleep(1)
            #获取下载文件名
            for root,dirname,filename in os.walk(os.path.join(path_project,'test_data')):
                for i in filename:
                    if re.findall('Open_Trade_List_...........xlsx', i)!=[]:
                        self.openOrder_excel=''.join(re.findall('Open_Trade_List_...........xlsx', i)) #正则匹配下载文件名
                        break
                    else:
                        pass
                    
            #读取下载文件
            dealData.openexcel(os.path.join(os.path.join(path_project,'test_data'),self.openOrder_excel), 'Sheet1')
            self.openOrderexcel_data=dealData.dict_data()
            time.sleep(1)
            
            #点击复制按钮，获取剪切板内容
            common.display_click('css,.lar')
            time.sleep(1)
            self.copyData=pyperclip.paste()
            #处理复制数据
            self.copy_openList=[]
            for i in self.copyData:
                self.copy_openList.append(i.strip('\n')) #去除换行键
            time.sleep(1)

            #写进txt文本
            with open(os.path.join(os.path.join(path_project,'test_data'),'copy_openOrder.txt'), 'w') as f:
                f.write(''.join(self.copy_openList))
            
            time.sleep(1)
            #txt转换成excel
            self.filename=os.path.join(os.path.join(path_project,'test_data'),'copy_openOrder.txt')
            self.xlsxname=os.path.join(os.path.join(path_project,'test_data'),'copy_openOrder.xlsx')
            dealData.txt_xlsx(self.filename, self.xlsxname)

            #读取复制数据
            dealData.openexcel(self.xlsxname,'sheet1')
            self.openOrder_data=dealData.dict_data()
            # print(self.openOrder_data)


            #查询已平仓订单
            common.display_click("xpath,//span[.='已平仓订单']")
            time.sleep(1)
            #刷新页面
            common.general_refresh_()
            time.sleep(2)
            #每页显示全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            #根据交易账号搜索
            time.sleep(1)
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']", trandaccount)
            time.sleep(0.5)
            #筛选时间
            common.display_click('css,.tradeList div > .el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            #按订单号码排序
            common.display_click('css,th .ascending')
            time.sleep(2)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('当前交易账号{}不存在平仓订单'.format(trandaccount))
                self.close_order_len=0
            else:
                self.close_order_len=common.get_lenofelement("xpath,//tr//span[.='{}']".format(trandaccount))
                time.sleep(0.5)
                print('交易账号 {} 已平仓订单共有{}条'.format(trandaccount,self.close_order_len))
                #处理页面数据
                print('处理页面数据中.......')
                self.close_orderList=[]
                for i in range(0,self.close_order_len):
                    self.close_orderDict={}
                    self.close_orderDict['订单号码']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.close_orderDict['交易账户']=int(common.get_text('css,tbody > tr > .el-table_1_column_2 div span',i))
                    self.timestr1=common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)
                    self.close_orderDict['开仓时间']=(datetime.datetime.strptime(self.timestr1,'%d/%m/%Y %H:%M:%S')).strftime('%Y-%m-%d %H:%M:%S') #开仓时间
                    self.timestr2=common.get_text('css,tbody > tr > .el-table_1_column_4 div span',i)
                    self.close_orderDict['平仓时间']=(datetime.datetime.strptime(self.timestr2,'%d/%m/%Y %H:%M:%S')).strftime('%Y-%m-%d %H:%M:%S')
                    self.close_orderDict['类型']=common.get_text('css,tbody > tr > .el-table_1_column_5 div',i)
                    self.close_orderDict['交易量']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i))
                    self.close_orderDict['商品代码']=common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i) #商品代码
                    self.close_orderDict['开仓价']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_8 div span',i)) #开仓价
                    self.close_orderDict['平仓价格']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_9 div span',i)) #平仓价
                    self.close_orderDict['S/L']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_10 div span',i))
                    self.close_orderDict['T/P']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_11 div span',i))
                    self.close_orderDict['佣金']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i)) #佣金
                    self.close_orderDict['隔夜利息']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_13 div span',i)) #隔夜利息
                    self.close_orderDict['盈亏']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_14 div span',i)) #盈亏
                    self.close_orderList.append(self.close_orderDict)
            time.sleep(1)
        
            #核对导出数据是否与页面一致
            common.display_click('css,.la-share-square') #导出
            time.sleep(1)
            #获取下载文件名
            for root,dirname,filename in os.walk(os.path.join(path_project,'test_data')):
                for i in filename:
                    if re.findall('Close_Trade_List_...........xlsx',i)!=[]:
                        self.closeOrder_excel=''.join(re.findall('Close_Trade_List_...........xlsx',i)) #正则匹配下载文件名
                        break
                    else:
                        pass
            
            #读取下载文件
            dealData.openexcel(os.path.join(os.path.join(path_project,'test_data'),self.closeOrder_excel), 'Sheet1')
            self.closeOrderexcel_data=dealData.dict_data()
            time.sleep(1)

            #点击复制按钮，获取剪切板内容
            common.display_click('css,.lar')
            time.sleep(1)
            self.copyData=pyperclip.paste()
            #处理复制数据
            self.copy_closeList=[]
            for i in self.copyData:
                self.copy_closeList.append(i.strip('\n')) #去除换行键
            time.sleep(1)

            #写进txt文本
            with open(os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.txt'), 'w') as f:
                f.write(''.join(self.copy_closeList))
            
            time.sleep(1)
            #txt转换成excel
            self.filename=os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.txt')
            self.xlsxname=os.path.join(os.path.join(path_project,'test_data'),'copy_closeOrder.xlsx')
            dealData.txt_xlsx(self.filename, self.xlsxname)

            #读取复制数据
            dealData.openexcel(self.xlsxname,'sheet1')
            self.closeOrder_data=dealData.dict_data()
            # print(self.closeOrder_data)

        except Exception as msg:
            log.my_logger('!!--!!search_order_len').error(msg)

    
    #格式化查询时间
    def fromat_datetime(self):
        #随机选择时间random.randint(1, 6)
        self.index=random.randint(1, 6)
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

    #查询某个时间段内的未平仓订单        
    def search_period_openOrder(self,trandaccount):
        try:
            self.fromat_datetime()
            #查询数据库
            self.mysql_openOrder=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="{}" and Close_Time="1970-01-01 00:00:00" and'
            ' Open_Time between "{} 00:00:00" and "{} 23:59:59" order by Open_Time desc'.
            format(trandaccount,self.dateStart,self.dateEnd), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            print('数据库查询返回{}条数据'.format(len(self.mysql_openOrder)))

            #查询页面时间段未平仓订单
            common.display_click("xpath,//span[.='未平仓订单']")
            time.sleep(1)
            common.general_refresh_()
            time.sleep(2)
            #每页显示全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(0.5)
            common.display_click('css,.tradeList div > .el-select .el-select__caret',1)
            time.sleep(0.5)
            #随机选择时间段查询
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            time.sleep(1)
            #根据交易账号来搜索全部未平仓订单
            common.web_clear('css,[placeholder="搜索"]')
            time.sleep(0.5)
            common.display_input('css,[placeholder="搜索"]', trandaccount)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            #按订单号码降序排序
            common.display_click('css,th .descending')
            time.sleep(1)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('当前交易账号{} 在{}至{} 时间段内不存在未平仓订单'.format(trandaccount,self.dateStart,self.dateEnd))
                self.open_order_len=0
                return False
            else:
                self.open_orderList=[]
                self.open_order_len=common.get_lenofelement("xpath,//tr//span[.='{}']".format(trandaccount))
                print('当前交易账号{} 在{} 00:00:00 至{} 23:59:59 时间段内存在{}条未平仓订单'.format(trandaccount,self.dateStart,self.dateEnd,self.open_order_len))
                #处理页面数据
                print('处理页面数据中........')
                for i in range(0,self.open_order_len):
                    self.open_orderDict={}
                    self.open_orderDict['Ticket']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)
                    self.open_orderDict['Open_Time']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M:%S') #开仓时间
                    self.open_orderDict['Volume']=float(common.get_text('css,tbody > tr > .el-table_1_column_5 div span',i)) #交易量
                    self.open_orderDict['Symbol']=common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i) #商品代码
                    self.open_orderDict['Open_Price']=float(common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i)) #开仓价
                    self.open_orderDict['Commission']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_10 div span',i)) #佣金
                    self.open_orderDict['Swaps']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_11 div span',i)) #隔夜利息
                    self.open_orderDict['Profit']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i))
                    self.open_orderList.append(self.open_orderDict)
                return True
        except Exception as msg:
            log.my_logger('!!--!!search_period_openOrder').error(msg)


    #查询某个时间段内的已平仓订单
    def search_period_closeOrder(self,trandaccount):
        try:
            self.fromat_datetime()
            #查询数据库
            self.mysql_closeOrder=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Login="{}" and'
            ' Close_Time between "{} 00:00:00" and "{} 23:59:59" order by Ticket desc'.
            format(trandaccount,self.dateStart,self.dateEnd), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            print('数据库查询返回{}条数据'.format(len(self.mysql_closeOrder)))
            
            common.display_click("xpath,//span[.='已平仓订单']")
            time.sleep(1)
            common.general_refresh_()
            time.sleep(2)
            #每页显示全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(0.5)
            common.display_click('css,.tradeList div > .el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li",self.index)
            #根据交易账号来搜索全部平仓订单
            common.web_clear('css,[placeholder="搜索"]')
            time.sleep(0.5)
            common.display_input('css,[placeholder="搜索"]', trandaccount)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            #根据订单号码降序排序
            common.display_click('css,th .descending')
            time.sleep(1)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('当前交易账号{} 在{}至{} 时间段内不存在已平仓订单'.format(trandaccount,self.dateStart,self.dateEnd))
                self.close_order_len=0
                return False
            else:
                self.close_orderList=[]
                self.close_order_len=common.get_lenofelement("xpath,//tr//span[.='{}']".format(trandaccount))
                print('当前交易账号{} 在{} 00:00:00 至{} 23:59:59 时间段内存在{}条已平仓订单'.format(trandaccount,self.dateStart,self.dateEnd,self.close_order_len))
                #处理页面数据
                print('处理页面数据中.........')
                for i in range(0,self.close_order_len):
                    self.close_orderDict={}
                    self.close_orderDict['Ticket']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.timestr1=common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)
                    self.close_orderDict['Open_Time']=datetime.datetime.strptime(self.timestr1,'%d/%m/%Y %H:%M:%S') #开仓时间
                    self.timestr2=common.get_text('css,tbody > tr > .el-table_1_column_4 div span',i)
                    self.close_orderDict['Close_Time']=datetime.datetime.strptime(self.timestr2,'%d/%m/%Y %H:%M:%S') #平仓时间
                    self.close_orderDict['Volume']=float(common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i)) #交易量
                    self.close_orderDict['Symbol']=common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i) #商品代码
                    self.close_orderDict['Open_Price']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_8 div span',i)) #开仓价
                    self.close_orderDict['Close_Price']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_9 div span',i)) #平仓价
                    self.close_orderDict['Commission']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i)) #佣金
                    self.close_orderDict['Swaps']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_13 div span',i)) #隔夜利息
                    self.close_orderDict['Profit']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_14 div span',i)) #盈亏
                    self.close_orderList.append(self.close_orderDict)
                return True
        except Exception as msg:
            log.my_logger('!!--!!search_period_closeOrder').error(msg)

    
    #根据商品代码核对未平仓订单数据
    def search_symbol_openOrder(self,symbol):
        try:
            #根据商品代码查询数据库
            self.mysql_symbol_openOrder=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Symbol="{}" and Close_Time="1970-01-01 00:00:00"'.
            format(symbol), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            print('数据库查询返回{}条数据'.format(len(self.mysql_symbol_openOrder)))

            #未平仓订单
            common.display_click("xpath,//span[.='未平仓订单']")
            time.sleep(1)
            common.general_refresh_()
            time.sleep(2)
            #每页显示全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(0.5)
            #选择商品代码查询
            common.display_click('css,.tradeList div > .el-select .el-select__caret')
            time.sleep(0.5)
            common.display_click('css,[x-placement="bottom-start"] li > span',2)
            time.sleep(1)
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']", symbol)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('商品代码{}不存在未平仓订单'.format(symbol))
                self.symbol_openLen=0
                return False
            else:
                print('处理页面数据中.......')
                self.symbol_openLen=common.get_lenofelement("xpath,//span[.='{}']".format(symbol))
                #处理页面数据
                self.symbol_openLsit=[]
                for i in range(0,self.symbol_openLen):
                    self.symbol_openDict={}
                    self.symbol_openDict['Ticket']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.symbol_openDict['Login']=int(common.get_text('css,tbody > tr > .el-table_1_column_2 div span',i))
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)
                    self.symbol_openDict['Open_time']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M:%S') #开仓时间
                    self.symbol_openDict['Volume']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_5 div span',i)) #交易量
                    self.symbol_openDict['Symbol']=common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i) #商品代码
                    self.symbol_openDict['Open_price']=float(common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i)) #开仓价
                    self.symbol_openDict['Commission']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_10 div span',i)) #佣金
                    self.symbol_openDict['Swaps']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_11 div span',i)) #隔夜利息
                    self.symbol_openDict['Profit']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i)) #盈亏
                    self.symbol_openLsit.append(self.symbol_openDict)
                return True
        except Exception as msg:
            log.my_logger('!!--!!search_period_closeOrder').error(msg)

    
    #根据商品代码核对已平仓订单
    def search_symbol_closeOrder(self,symbol):
        try:
            #根据商品代码查询数据库
            self.mysql_symbol_closeOrder=dataBase.search_in_mysql('SELECT * FROM report_atfx2_test.mt4_sync_order WHERE Symbol="{}" and Close_Time!="1970-01-01 00:00:00"'.
            format(symbol), conFig.get_value('mysql_AWS', 'host'), conFig.get_value('mysql_AWS','user'),conFig.get_value('mysql_AWS','password'),type='all')
            print('数据库查询返回{}条数据'.format(len(self.mysql_symbol_closeOrder)))

            #已平仓订单
            common.display_click("xpath,//span[.='已平仓订单']")
            time.sleep(1)
            common.general_refresh_()
            time.sleep(2)
            #每页显示全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',-1)
            time.sleep(0.5)
            common.display_click("xpath,//span[.='全部']",-1)
            time.sleep(0.5)
            #时间选择全部
            common.display_click('css,.tradeList div > .el-select .el-select__caret',1)
            time.sleep(0.5)
            common.display_click("css,[x-placement='bottom-start'] li")
            time.sleep(1)
            #选择商品代码查询
            common.display_click('css,.tradeList div > .el-select .el-select__caret')
            time.sleep(0.5)
            common.display_click('css,[x-placement="bottom-start"] li > span',2)
            time.sleep(1)
            common.web_clear("css,[placeholder='搜索']")
            time.sleep(0.5)
            common.display_input("css,[placeholder='搜索']", symbol)
            time.sleep(0.5)
            #搜索
            common.display_click('css,.el-icon-search')
            time.sleep(2)
            if common.ele_is_displayed('css,.el-table__empty-text', 1):
                print('商品代码{}不存在未平仓订单'.format(symbol))
                self.symbol_closeLen=0
                return False
            else:
                print('处理页面数据中.......')
                self.symbol_closeLen=common.get_lenofelement("xpath,//span[.='{}']".format(symbol))
                #处理页面数据
                self.symbol_closeLsit=[]
                for i in range(0,self.symbol_closeLen):
                    self.symbol_closeDict={}
                    self.symbol_closeDict['Ticket']=int(common.get_text('css,tbody > tr > .el-table_1_column_1 div span',i)) #订单号码
                    self.symbol_closeDict['Login']=int(common.get_text('css,tbody > tr > .el-table_1_column_2 div span',i))
                    self.timestr=common.get_text('css,tbody > tr > .el-table_1_column_3 div span',i)
                    self.symbol_closeDict['Open_time']=datetime.datetime.strptime(self.timestr,'%d/%m/%Y %H:%M:%S') #开仓时间
                    self.timestr2=common.get_text('css,tbody > tr > .el-table_1_column_4 div span',i)
                    self.symbol_closeDict['Close_time']=datetime.datetime.strptime(self.timestr2,'%d/%m/%Y %H:%M:%S') #平仓时间
                    self.symbol_closeDict['Volume']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_6 div span',i)) #交易量
                    self.symbol_closeDict['Symbol']=common.get_text('css,tbody > tr > .el-table_1_column_7 div span',i) #商品代码
                    self.symbol_closeDict['Open_price']=float(common.get_text('css,tbody > tr > .el-table_1_column_8 div span',i)) #开仓价
                    self.symbol_closeDict['Close_price']=float(common.get_text('css,tbody > tr > .el-table_1_column_9 div span',i)) #平仓价
                    self.symbol_closeDict['Commission']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_12 div span',i)) #佣金
                    self.symbol_closeDict['Swaps']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_13 div span',i)) #隔夜利息
                    self.symbol_closeDict['Profit']=locale.atof(common.get_text('css,tbody > tr > .el-table_1_column_14 div span',i)) #盈亏
                    self.symbol_closeLsit.append(self.symbol_closeDict)
                return True
        except Exception as msg:
            log.my_logger('!!--!!search_symbol_closeOrder').error(msg)


    def closebrowser(self):
        common.close_browser()

    def quitbrowser(self):
        common.quit_browser()